"""Golden and structural tests for PER_FR_A.

The golden values are the worked example in
``products/per_assurance/technical-notes.md`` ("Worked example"): a male aged 52 with a
declared horizon of 64, two completed years since his first *versement*, compartment 1 on
the *équilibré horizon retraite* glide path, opening EUR 16,600 entirely in *unités de
compte* against a EUR 16,000 *garantie plancher* base, paying EUR 3,000 at the start of
each of the twelve plan years, and settling 70% as capital and 30% as a *rente viagère*
that turns out to be small enough to commute.  Model point 1 is that cell.  The numbers
are hard-coded here rather than pickled so that a reviewer can compare them against the
notes by eye.

Tolerances follow the precision the notes display: money to the cent, the in-force
probability to six decimals, shares to the basis point.

One naming point runs through the module.  The notes index the in force at the **end** of
the plan year and call it ``l(t)``; the library publishes the exposure at the **start** of
the period under the shared name ``pols_if``, because that is the weight the period's own
cash flows carry.  Both are here: ``pols_if(t)`` is ``l(t - 1)``, ``pols_if_at(t,
"AFT_DECR")`` is ``l(t)``, and ``result_state()`` prints the latter as ``pols_if_eoy``.
The last column of ``WORKED_EXAMPLE`` below is the notes' ``l(t)``.

Beyond the worked example this module asserts each of the twelve "Known modeling
pitfalls" the notes list, because each is a way an implementation of *this* product can
look right and be wrong, and every test below is named for the failure it catches: the
glide-path boundary belonging to the **tighter** band; a *versement* allocated at the
target mix and therefore not a switch; the arbitrage charge coming off the **source**
support, which on a de-risking switch is what keeps the euro share at or above the
regulatory minimum; that minimum binding at the **rebalancing date** rather than
continuously; the *garantie plancher* being a floor at *versements* net of loading and
net of charges and never at gross premiums; neither exit being a lapse, and an early
release paying the **whole** account value; the transfer indemnity window running from
the first *versement*; the three decrements not double-counting; the annuity conversion
factor being **undiscounted**, because a PER tariff is capped at a 0% technical rate;
commutation happening at the conversion basis against a **monthly** EUR 110 threshold;
per-policy and aggregate quantities not being multiplied together twice; and the
projection stopping at the declared horizon with tax outside it entirely.
"""
import modelx as mx
import pandas as pd
import pytest
from modelx.core.errors import FormulaError

from fr_registry import LIB, MODELS


CENT = 0.005          # money displayed to 2 d.p.
POLS = 5e-7           # the in-force probability displayed to 6 d.p.

MODEL_DIR = LIB / MODELS["PER_FR_A"][0]
PRODUCT_DIR = MODEL_DIR.parent

# t: (k, a(t), arb, av_euro_pp, av_uc_pp, av_pp, l(t))
# The notes' worked-example table, read straight off the page.  V_net is 2,925.00 in
# every row and is asserted separately.  The last column is the notes' l(t), the in force
# at the END of the year, which the model publishes as pols_if_at(t, "AFT_DECR").
WORKED_EXAMPLE = {
    1:  (12, 0.00,     0.00,     0.00, 20357.74, 20357.74, 0.969289),
    2:  (11, 0.00,     0.00,     0.00, 24275.75, 24275.75, 0.939522),
    3:  (10, 0.20,    14.57,  5584.66, 22673.50, 28258.16, 0.910668),
    4:  (9,  0.20,     0.20,  6402.30, 26010.29, 32412.59, 0.882701),
    5:  (8,  0.20,     0.24,  7255.25, 29475.54, 36730.79, 0.855592),
    6:  (7,  0.20,     0.27,  8141.84, 33077.41, 41219.24, 0.829316),
    7:  (6,  0.20,     0.31,  9063.37, 36821.28, 45884.65, 0.803847),
    8:  (5,  0.50,    41.64, 25053.10, 25402.28, 50455.38, 0.779161),
    9:  (4,  0.50,     0.52, 27399.17, 27827.98, 55227.15, 0.755232),
    10: (3,  0.50,     0.64, 29848.43, 30315.50, 60163.93, 0.732038),
    11: (2,  0.70,    36.80, 45335.35, 19695.53, 65030.89, 0.709557),
    12: (1,  0.70,     0.56, 48832.72, 21255.68, 70088.40, 0.687766),
}

# The notes' settlement table, per policy except where the label says otherwise.
SETTLEMENT = {
    "av_pp": 70088.40,
    "capital_leg_pp": 49061.88,
    "annuity_cap_pp": 21026.52,
    "rente_gross_pp": 955.75,
    "rente_net_pp": 941.41,
    "rente_net_mth": 78.45,
    "commuted_pp": 20711.12,
    "death_floor_pp": 47267.36,
}


def model_files(folder):
    """The model's own file names, ignoring interpreter caches."""
    return {p.name for p in folder.rglob("*")
            if p.is_file() and "__pycache__" not in p.parts}


def alt_model_point_file(model, rows, name):
    """Write a one-row model point table beside the model and point the model at it.

    The only way to assert that an invalid model point *raises* is to build one, and the
    shipped table cannot hold one — every row in it has to project.  The caller is
    responsible for deleting the file.
    """
    path = model.Data.input_dir() / name
    pd.DataFrame(rows).to_csv(path, index=False)
    model.Data.model_point_file = name
    model.Data.clear_all()
    model.Projection.clear_all()
    return path


def anchor_row(**overrides):
    """The anchor model point as a dict, with the named columns replaced."""
    table = pd.read_csv(PRODUCT_DIR / "model_point_table.csv")
    row = table[table["point_id"] == 1].iloc[0].to_dict()
    row.update(overrides)
    return row


# ---------------------------------------------------------------------------
# The worked example


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE))
def test_worked_example_row(fr_per_anchor, t):
    """Every cell of the notes' table, to the precision the notes display."""
    k, a, arb, euro, uc, av, l_t = WORKED_EXAMPLE[t]
    p = fr_per_anchor
    assert p.years_to_horizon(t) == k
    assert p.alloc_euro(t) == pytest.approx(a, abs=1e-4)
    assert p.prem_to_av_pp(t) == pytest.approx(2925.00, abs=CENT)
    assert p.arbitrage_charge_pp(t) == pytest.approx(arb, abs=CENT)
    assert p.av_euro_pp(t) == pytest.approx(euro, abs=CENT)
    assert p.av_uc_pp(t) == pytest.approx(uc, abs=CENT)
    assert p.av_pp(t) == pytest.approx(av, abs=CENT)
    assert p.pols_if_at(t, "AFT_DECR") == pytest.approx(l_t, abs=POLS)
    # The notes' l(t) is what result_state prints, under a name that cannot be confused
    # with the start-of-period exposure result_cf publishes.
    assert p.result_state().loc[t, "pols_if_eoy"] == pytest.approx(l_t, abs=POLS)


def test_the_worked_example_settlement(fr_per_anchor):
    """The notes' second table: capital leg, conversion, commutation test, lump sum."""
    p = fr_per_anchor
    s = p.result_settlement()
    for label, value in SETTLEMENT.items():
        assert s[label] == pytest.approx(value, abs=CENT), label
    assert p.annuity_share() == 0.30
    assert p.annuity_factor() == 22.0
    assert p.is_commuted() is True
    assert p.claim_pp(12, "MATURITY") == pytest.approx(69773.00, abs=CENT)
    assert p.claims(12, "MATURITY") == pytest.approx(47987.47, abs=CENT)
    # The whole maturity claim is the account value less the arrerage charge on the
    # converted part, and nothing else: there is no exit charge on a PER.
    assert p.claim_pp(12, "MATURITY") == pytest.approx(
        p.av_pp(12) - 0.015 * p.annuity_cap_pp(), abs=CENT)


def test_the_aggregate_benefits_over_the_twelve_years(fr_per_anchor):
    """claims_death 2,160.30, claims_early_release 6,878.40, claims_transfer 4,225.92."""
    df = fr_per_anchor.result_cf()
    assert df["claims_death"].sum() == pytest.approx(2160.30, abs=CENT)
    assert df["claims_early_release"].sum() == pytest.approx(6878.40, abs=CENT)
    assert df["claims_transfer"].sum() == pytest.approx(4225.92, abs=CENT)


def test_the_maintenance_expense_scale(fr_per_anchor):
    """E(t) = 30 x 1.018^(t-1), so E(12) = 36.50 and the twelve-year total is 397.87."""
    p = fr_per_anchor
    per_policy = [p.expenses(t) / p.pols_if(t) for t in range(1, 13)]
    assert per_policy[0] == pytest.approx(30.00, abs=CENT)
    assert per_policy[11] == pytest.approx(36.50, abs=CENT)
    assert sum(per_policy) == pytest.approx(397.87, abs=CENT)
    # The weight on the row is the in force at the START of the year, not the end - and
    # that is exactly the pols_if the same row of result_cf publishes.
    assert p.expenses(12) == pytest.approx(
        30.0 * 1.018 ** 11 * p.pols_if(12), rel=1e-12)
    assert p.pols_if(12) == pytest.approx(p.pols_if_at(11, "AFT_DECR"), rel=1e-14)
    assert p.expenses(12) == pytest.approx(
        30.0 * 1.018 ** 11 * p.result_cf().loc[12, "pols_if"], rel=1e-12)


# ---------------------------------------------------------------------------
# Pitfall 1 - the glide-path band edge


def test_the_band_boundary_belongs_to_the_tighter_band(fr_per_anchor):
    """k = 10 reads 20%, k = 5 reads 50%, k = 2 reads 70% - not the looser band.

    The looser reading understates the euro share for a full year at each of three
    transitions, which on the anchor cell is three years of a 5.00% UC return where the
    grid asks for a 3.38% euro one.
    """
    p = fr_per_anchor
    edges = {11: 0.00, 10: 0.20, 6: 0.20, 5: 0.50, 3: 0.50, 2: 0.70, 1: 0.70}
    for k, share in edges.items():
        t = p.proj_len() - k + 1
        assert p.years_to_horizon(t) == k
        assert p.alloc_euro(t) == pytest.approx(share, abs=1e-9), k


def test_the_four_profiles_are_read_from_the_file(per_assurance):
    """The grid is an input table: four ladders, and dynamique equals offensif."""
    grid = per_assurance.Data.allocation_grid()
    expected = {
        "prudent":   (0.30, 0.60, 0.80, 0.90),
        "equilibre": (0.00, 0.20, 0.50, 0.70),
        "dynamique": (0.00, 0.00, 0.30, 0.50),
        "offensif":  (0.00, 0.00, 0.30, 0.50),
    }
    for profile, (far, mid, near, close) in expected.items():
        for k, share in ((20, far), (10, mid), (5, near), (2, close)):
            assert grid.loc[(profile, k), "euro_share"] == pytest.approx(
                share, abs=1e-9), (profile, k)
    # The two shares close in every row, which is what check_glide_path_closes asserts
    # on the years a projection actually reads.
    assert (grid["euro_share"] + grid["uc_share"]).sub(1.0).abs().max() < 1e-12


def test_a_prudent_cell_holds_euro_from_the_first_year(per_assurance):
    """Moving the grid is the product's dominant lever, and it needs no code change."""
    p = per_assurance.Projection[3]
    assert p.allocation_profile() == "prudent"
    assert p.years_to_horizon(1) == 19
    assert p.alloc_euro(1) == pytest.approx(0.30, abs=1e-9)
    assert p.av_euro_pp(1) > 0.0
    # The anchor cell, on the equilibre grid at 12 years out, holds none at all.
    assert per_assurance.Projection[1].alloc_euro(1) == 0.0
    assert per_assurance.Projection[1].av_euro_pp(1) == 0.0


# ---------------------------------------------------------------------------
# Pitfalls 2, 3 and 4 - the rebalancing and the arbitrage charge


def test_a_versement_is_not_a_switch(fr_per_anchor):
    """No arbitrage charge in a year that opens on target, though 3,000 was paid.

    New money is allocated at the target mix directly.  Charging it as though it were a
    switch would take 0.30% of every contribution for the life of the plan.
    """
    p = fr_per_anchor
    for t in (1, 2):
        assert p.premium_pp(t) == 3000.00
        assert p.switch_pp(t) == 0.0
        assert p.arbitrage_charge_pp(t) == 0.0
    # And the versement still reaches the account in full, net of the entry loading only.
    assert p.av_pp(1) == pytest.approx(
        (16600.0 + 2925.0) * 1.05 * 0.993, abs=CENT)


def test_the_arbitrage_charge_comes_off_the_source_support(fr_per_anchor):
    """Year 8: the UC bucket pays 41.64 and the euro side receives the switch in full."""
    p = fr_per_anchor
    assert p.switch_pp(8) == pytest.approx(13878.95, abs=CENT)
    assert p.arbitrage_charge_pp(8) == pytest.approx(41.64, abs=CENT)
    # The euro destination gets the whole switch plus its share of the versement.
    assert p.av_euro_pp_at(8, "BOY") == pytest.approx(24404.82, abs=CENT)
    assert p.av_euro_pp_at(8, "BOY") == pytest.approx(
        p.av_euro_pp(7) + p.switch_pp(8) + 0.50 * 2925.0, abs=CENT)
    # The UC source pays for it.
    assert p.av_uc_pp_at(8, "BOY") == pytest.approx(
        p.av_uc_pp(7) - p.switch_pp(8) - p.arbitrage_charge_pp(8) + 0.50 * 2925.0,
        abs=CENT)


def test_the_post_rebalancing_euro_share_meets_the_minimum(fr_per_anchor):
    """50.04% against a 50% target at the year-8 crossing, and never under all year.

    Taking the charge from the destination instead puts the share below the regulatory
    minimum by (1 - a) x arb at every band crossing.
    """
    p = fr_per_anchor
    share = p.av_euro_pp_at(8, "BOY") / p.av_pp_at(8, "BOY")
    assert share == pytest.approx(0.500427, abs=1e-6)
    assert share >= p.alloc_euro(8)
    assert p.check_euro_share_min() is True
    for t in range(1, p.proj_len() + 1):
        assert p.euro_share_min_bound(t) == 0.0, t
        assert p.check_euro_share_min_resid(t) >= -1e-8, t


def test_a_reverse_switch_is_the_one_case_the_convention_cannot_cover(per_assurance):
    """Model point 2 arrives at 40% euro against a 20% minimum and sells euro down.

    The euro support is then the *source*, so charging the source takes the charge out of
    the very balance the minimum is measured on and leaves it (1 - a) x arb below the
    line.  The notes ask both for a symmetric formula and for a share at or above the
    minimum, and in this direction the two cannot both hold; the model implements the
    formula and states the bound.
    """
    p = per_assurance.Projection[2]
    assert p.switch_pp(1) == pytest.approx(-4000.00, abs=CENT)
    assert p.arbitrage_charge_pp(1) == pytest.approx(12.00, abs=CENT)
    assert p.check_euro_share_min_resid(1) == pytest.approx(-9.60, abs=CENT)
    assert p.euro_share_min_bound(1) == pytest.approx(-9.60, abs=CENT)
    assert p.check_euro_share_min() is True
    # It happens once and only at the arrival, because the euro support then grows more
    # slowly than the UC bucket and falls back below the minimum on its own.
    assert all(p.switch_pp(t) >= 0.0 for t in range(2, p.proj_len() + 1))


def test_the_minimum_binds_at_the_rebalancing_date_not_continuously(fr_per_anchor):
    """70.00% after the year-12 rebalancing, 69.67% at the year end - both correct."""
    p = fr_per_anchor
    assert p.alloc_euro(12) == pytest.approx(0.70, abs=1e-9)
    boy = p.av_euro_pp_at(12, "BOY") / p.av_pp_at(12, "BOY")
    eoy = p.av_euro_pp(12) / p.av_pp(12)
    assert boy == pytest.approx(0.700006, abs=1e-6)
    assert eoy == pytest.approx(0.696730, abs=1e-6)
    assert eoy < 0.70
    # Re-imposing the target at the year end would invent a rebalancing frequency the
    # annual grid does not have, so nothing in the model reads the year-end share.


# ---------------------------------------------------------------------------
# Pitfall 5 - the garantie plancher


def test_the_floor_is_not_a_floor_at_gross_premiums(fr_per_anchor):
    """A(t) - g(t) = [A(0) - g(0)] + cumulative gross investment return, exactly.

    A base accumulated at gross V rather than V_net, or one that forgets the arbitrage
    charge, or one charged something other than what the account was charged, breaks this
    in the first year in which it is wrong.
    """
    p = fr_per_anchor
    assert p.death_floor_pp(0) == 16000.00
    assert p.av_pp(0) == 16600.00
    gap = p.av_pp(12) - p.death_floor_pp(12)
    assert gap == pytest.approx(22821.04, abs=CENT)
    credited = sum(p.inv_income_pp(t) for t in range(1, 13))
    assert credited == pytest.approx(22221.04, abs=CENT)
    assert gap == pytest.approx(600.00 + credited, abs=CENT)
    assert p.check_floor_identity() is True
    # Year 1 alone: the base grows by V_net less the charge, not by the gross premium.
    charge1 = p.mgmt_charge_pp(1)
    assert p.death_floor_pp(1) == pytest.approx(16000.0 + 2925.0 - charge1, abs=CENT)
    assert p.death_floor_pp(1) < 16000.0 + 3000.0


def test_the_floor_bites_only_where_investment_return_is_negative(per_assurance):
    """Model point 10 is the anchor cell with a 19,000 opening base rather than 16,000.

    It opens 2,400 above the account value - a plan whose accumulated investment return
    to date is negative - so the floor bites until cumulative return overtakes it, and
    then stops.
    """
    p = per_assurance.Projection[10]
    assert p.death_floor_init() == 19000.00
    assert p.death_benefit_pp(1) == pytest.approx(p.death_floor_pp(1), abs=CENT)
    assert p.death_benefit_pp(1) > p.av_pp(1)
    assert p.death_benefit_pp(2) == pytest.approx(p.death_floor_pp(2), abs=CENT)
    assert p.death_benefit_pp(3) == pytest.approx(p.av_pp(3), abs=CENT)
    assert p.death_floor_pp(3) < p.av_pp(3)
    # It costs more than the anchor cell, and only through the death benefit.
    base = per_assurance.Projection[1].result_cf()
    assert (p.result_cf()["claims_death"].sum()
            > base["claims_death"].sum())


def test_the_cover_ceases_at_seventy_and_is_capped_across_contracts(per_assurance):
    """Model point 9 retires at 70, so the cover switches off in its final plan year."""
    assert per_assurance.Projection.floor_cease_age == 70
    assert per_assurance.Projection.death_floor_cap == 762245.0
    p = per_assurance.Projection[9]
    assert [p.age(t) for t in range(1, 5)] == [67, 68, 69, 70]
    assert [p.floor_in_force(t) for t in range(1, 5)] == [True, True, True, False]
    assert p.death_benefit_pp(4) == p.av_pp(4)
    # And a cell that never carried the cover is never floored at all.
    off = per_assurance.Projection[11]
    assert off.death_floor_flag() is False
    for t in range(1, off.proj_len() + 1):
        assert off.floor_in_force(t) is False
        assert off.death_benefit_pp(t) == off.av_pp(t)


# ---------------------------------------------------------------------------
# Pitfalls 6 and 7 - the two exits, neither of which is a lapse


def test_there_is_no_lapse_machinery_anywhere(per_assurance):
    """A cited product fact: the plan is blocked and carries no surrender right.

    Naming either exit a lapse attaches a surrender formula - a charge, a market value
    adjustment, a surrender value - to an event that has none of them.
    """
    names = set(per_assurance.Projection.cells) | set(per_assurance.Projection.refs)
    for absent in ("lapse_rate", "lapse_rate_ann", "lapse_rate_mth", "pols_lapse",
                   "surr_rate", "surr_charge_rate", "surr_value_pp", "cv_pp",
                   "mvr_pp", "dyn_lapse_factor", "withdrawals", "wd_pp"):
        assert absent not in names, absent
    columns = per_assurance.Projection[1].result_cf().columns
    for absent in ("claims_lapse", "claims_surr", "claims_wd", "withdrawals"):
        assert absent not in columns, absent


def test_an_early_release_pays_the_whole_account_value(fr_per_anchor):
    """No charge, no reduction: the seven statutory cases carry neither.

    A transfer out of the same cell in the same year pays 1% less, which is the whole
    difference between the two exits and the reason they are two decrements.
    """
    p = fr_per_anchor
    for t in (1, 6, 12):
        assert p.claim_pp(t, "EARLY_RELEASE") == p.av_pp(t)
        assert p.claims(t, "EARLY_RELEASE") == pytest.approx(
            p.pols_release(t) * p.av_pp(t), rel=1e-14)
    assert p.claim_pp(1, "TRANSFER") == pytest.approx(0.99 * p.av_pp(1), rel=1e-14)
    assert p.early_release_rate(1) == 0.016
    assert p.transfer_out_rate(1) == 0.010


def test_the_transfer_indemnity_window_runs_from_the_first_versement(fr_per_anchor):
    """duration_ifo = 2, so the window closes at the end of projected year 2.

    Measuring it from the projection start instead would charge the indemnity for five
    projected years on a plan that is already three years old.
    """
    p = fr_per_anchor
    assert p.duration_ifo() == 2
    assert [p.duration(t) for t in (1, 2, 3)] == [3, 4, 5]
    for t in (1, 2):
        assert p.transfer_indemnity_rate(t) == 0.01
        assert p.claims(t, "TRANSFER") / (p.pols_transfer(t) * p.av_pp(t)) == (
            pytest.approx(0.99, rel=1e-12))
    for t in (3, 8, 12):
        assert p.transfer_indemnity_rate(t) == 0.0
        assert p.claims(t, "TRANSFER") / (p.pols_transfer(t) * p.av_pp(t)) == (
            pytest.approx(1.00, rel=1e-12))


def test_a_new_plan_carries_the_indemnity_for_four_projected_years(per_assurance):
    """Model point 3 opens at duration 0, so its window closes at the end of year 4."""
    p = per_assurance.Projection[3]
    assert p.duration_ifo() == 0
    assert [p.transfer_indemnity_rate(t) for t in range(1, 7)] == [
        0.01, 0.01, 0.01, 0.01, 0.0, 0.0]


def test_compartment_three_carries_a_reduced_release_rate(per_assurance):
    """The main-residence case is the only discretionary limb, and c3 is excluded."""
    c1 = per_assurance.Projection[1]
    c3 = per_assurance.Projection[2]
    assert c3.compartment() == "c3"
    assert c3.early_release_rate(1) < c1.early_release_rate(1)
    # The transfer rate does not vary by compartment: a transfer moves the rights
    # without changing them.
    assert c3.transfer_out_rate(1) == c1.transfer_out_rate(1)


# ---------------------------------------------------------------------------
# Pitfall 8 - double-counting the exits


def test_the_three_decrements_do_not_double_count(per_assurance):
    """d_death + d_release + d_transfer + l(t) = l(t-1), exactly, in every year.

    Applying two decrements to the same start-of-year in force instead of in sequence
    removes more of the book than exists, and every downstream number stays plausible.
    """
    for point_id in per_assurance.Data.model_point_table().index:
        p = per_assurance.Projection[point_id]
        assert p.check_pols_roll_fwd() is True, point_id
        for t in range(1, p.proj_len() + 1):
            assert abs(p.check_pols_roll_fwd_resid(t)) < 1e-12, (point_id, t)


def test_the_decrement_order_is_death_then_release_then_transfer(fr_per_anchor):
    """An ordered dependent-decrement convention, exposed step by step."""
    p = fr_per_anchor
    q, we, wr = p.mort_rate(1), p.early_release_rate(1), p.transfer_out_rate(1)
    assert p.pols_if_at(1, "BEF_DECR") == 1.0
    assert p.pols_if_at(1, "BEF_RELEASE") == pytest.approx(1 - q, rel=1e-14)
    assert p.pols_if_at(1, "BEF_TRANSFER") == pytest.approx(
        (1 - q) * (1 - we), rel=1e-14)
    assert p.pols_if_at(1, "AFT_DECR") == pytest.approx(
        (1 - q) * (1 - we) * (1 - wr), rel=1e-14)
    assert p.pols_release(1) == pytest.approx((1 - q) * we, rel=1e-14)
    assert p.pols_transfer(1) == pytest.approx((1 - q) * (1 - we) * wr, rel=1e-14)


def test_the_account_value_roll_forward_closes(per_assurance):
    """A(t) = A(t-1) + V_net - arb + return credited - charge levied.

    A conservation statement: the switch does not appear in it, because it moves money
    between the supports rather than across the plan's boundary.
    """
    for point_id in per_assurance.Data.model_point_table().index:
        p = per_assurance.Projection[point_id]
        assert p.check_av_roll_fwd() is True, point_id


# ---------------------------------------------------------------------------
# Pitfalls 9 and 10 - the annuity conversion and its commutation


def test_the_conversion_factor_is_undiscounted(fr_per_anchor):
    """A PER tariff may not use a technical rate above 0%, so a_x counts instalments.

    Nothing in the model discounts it: rente_gross is a plain division, and multiplying
    the instalment back by the factor returns the converted capital exactly.  A 2% rate
    would shorten the factor from 22.0000 to 17.658 - a fall of 19.7% - and so inflate the
    annuity, which is annuity_cap divided by the factor, by 22 / 17.658 - 1 = 24.6%.  The
    two percentages are different numbers and quoting the first as the second is the slip
    this assertion pins down.
    """
    p = fr_per_anchor
    assert p.annuity_factor() == 22.0
    assert p.rente_gross_pp() * p.annuity_factor() == pytest.approx(
        p.annuity_cap_pp(), rel=1e-14)
    discounted = sum(1.02 ** -k for k in range(1, 23))
    assert discounted == pytest.approx(17.658, abs=0.001)
    # The factor falls by about a fifth ...
    assert 1.0 - discounted / p.annuity_factor() == pytest.approx(0.197, abs=0.001)
    # ... and the annuity therefore rises by about a quarter, which is not the same
    # number.  Both documents must quote the second one.
    assert p.annuity_cap_pp() / discounted / p.rente_gross_pp() == pytest.approx(
        1.246, abs=0.001)


def test_commutation_returns_the_capital_less_the_arrerage_charge(fr_per_anchor):
    """commuted = rente_net x a_x = annuity_cap x (1 - c_arr), to the cent.

    Commuting at a book value instead manufactures a gain out of nothing.
    """
    p = fr_per_anchor
    assert p.commuted_pp() == pytest.approx(
        p.rente_net_pp() * p.annuity_factor(), rel=1e-14)
    assert p.commuted_pp() == pytest.approx(
        p.annuity_cap_pp() * 0.985, rel=1e-14)
    assert p.commuted_pp() == pytest.approx(20711.12, abs=CENT)
    assert p.check_commutation_identity() is True


def test_the_commutation_threshold_is_monthly(per_assurance):
    """EUR 110 a month, scaled by the months in the payment period - so 1,320 a year.

    Testing an annual instalment against 110 would commute almost nothing, and testing a
    monthly one against 1,320 would commute almost everything.
    """
    assert per_assurance.Projection.commute_threshold_mth == 110.0
    assert per_assurance.Projection.payment_mths == 12
    p = per_assurance.Projection[1]
    assert p.rente_net_pp() == pytest.approx(941.41, abs=CENT)
    assert p.result_settlement()["rente_net_mth"] == pytest.approx(78.45, abs=CENT)
    # The annual instalment is well above 110 and the monthly one well below it, so the
    # two readings of the threshold give opposite answers on the same cell.
    assert 78.45 <= 110.0 < 941.41
    assert p.is_commuted() is True


def test_the_commutation_cliff(per_assurance):
    """Model point 6 is the anchor cell at a 50% annuity share, above the threshold.

    The cliff sits at 42.06% of the settlement balance; below it the annuity reverses at
    settlement into a lump sum, above it a rente is paid and the capital is handed to
    Rente_FR_S.
    """
    p1, p6 = per_assurance.Projection[1], per_assurance.Projection[6]
    assert p6.av_pp(12) == pytest.approx(p1.av_pp(12), rel=1e-14)
    assert p6.annuity_share() == 0.50
    assert p6.rente_net_pp() == pytest.approx(1569.02, abs=CENT)
    assert p6.result_settlement()["rente_net_mth"] == pytest.approx(130.75, abs=CENT)
    assert p6.is_commuted() is False
    assert p6.commuted_pp() == 0.0
    assert p6.annuity_conversion_pp() == pytest.approx(p6.annuity_cap_pp(), rel=1e-14)
    # The cliff itself: 110 x 12 / (1 - c_arr) x a_x / A(n).
    cliff = 110.0 * 12 / 0.985 * 22.0 / p1.av_pp(12)
    assert cliff == pytest.approx(0.4206, abs=1e-4)


def test_the_two_annuity_legs_are_mutually_exclusive(per_assurance):
    """Commuted money leaves as claims_maturity; a rente leaves as annuity_conversion."""
    for point_id in per_assurance.Data.model_point_table().index:
        p = per_assurance.Projection[point_id]
        assert min(p.commuted_pp(), p.annuity_conversion_pp()) == 0.0, point_id
        df = p.result_cf()
        n = p.proj_len()
        assert df["annuity_conversion"].sum() == pytest.approx(
            df.loc[n, "annuity_conversion"], rel=1e-14)


def test_a_capital_only_exit_has_no_annuity_at_all(per_assurance):
    """Model point 7 elects capital in one payment: theta = 0 and nothing to commute."""
    p = per_assurance.Projection[7]
    assert p.exit_form() == "capital_single"
    assert p.annuity_share() == 0.0
    assert p.annuity_cap_pp() == 0.0
    assert p.is_commuted() is False
    assert p.annuity_conversion_pp() == 0.0
    assert p.claim_pp(p.proj_len(), "MATURITY") == pytest.approx(
        p.av_pp(p.proj_len()), rel=1e-14)


def test_staged_capital_publishes_its_instalment_and_settles_at_the_horizon(
        per_assurance):
    """A documented simplification: the fractionne option changes when, not how much."""
    p = per_assurance.Projection[8]
    assert p.exit_form() == "capital_staged"
    assert p.capital_instalments() == 5
    assert p.capital_instalment_pp() == pytest.approx(
        p.capital_leg_pp() / 5, rel=1e-14)
    assert p.proj_len() == p.retirement_age() - p.age_init()
    assert p.claims(p.proj_len(), "MATURITY") == pytest.approx(
        p.capital_leg_pp() * p.pols_maturity(p.proj_len()), rel=1e-12)


def test_a_compartment_three_cell_must_elect_the_annuity(per_assurance):
    """Those rights may be delivered no other way, so the model refuses the alternative."""
    p = per_assurance.Projection[2]
    assert p.compartment() == "c3"
    assert p.exit_form() == "annuity"
    assert p.annuity_share() == 1.0
    assert p.capital_leg_pp() == 0.0


# ---------------------------------------------------------------------------
# Pitfall 11 - per policy against aggregate


def test_the_account_value_column_is_per_policy_and_the_claims_are_not(fr_per_anchor):
    """Multiplying a claims column by pols_if again squares the survival factor."""
    p = fr_per_anchor
    df = p.result_cf()
    assert df.loc[12, "av_pp"] == pytest.approx(70088.40, abs=CENT)
    assert df.loc[12, "av_pp"] > df.loc[12, "claims_maturity"]
    # av_at is the weighted quantity where one is wanted, and it is not in result_cf.
    # At EOY the weight is the END-of-year count, which is pols_if_at(t, "AFT_DECR").
    assert p.av_at(12, "EOY") == pytest.approx(
        p.av_pp(12) * p.pols_if_at(12, "AFT_DECR"), rel=1e-14)
    assert p.av_at(12, "BOY") == pytest.approx(
        p.av_pp_at(12, "BOY") * p.pols_if(12), rel=1e-14)
    assert "av_at" not in df.columns
    # Every claims column is already a decrement times a per-policy amount.
    assert df.loc[6, "claims_death"] == pytest.approx(
        p.pols_death(6) * p.death_benefit_pp(6), rel=1e-14)


# ---------------------------------------------------------------------------
# Pitfall 12 - the horizon, and tax


def test_the_projection_stops_at_the_declared_horizon(per_assurance):
    """No versement after settlement, k never negative, one maturity year."""
    for point_id in per_assurance.Data.model_point_table().index:
        p = per_assurance.Projection[point_id]
        n = p.proj_len()
        assert n == p.retirement_age() - p.age_init(), point_id
        assert list(p.result_cf().index) == list(range(1, n + 1)), point_id
        assert p.premium_pp(n) > 0.0 or p.premium_init() == 0.0
        assert p.premium_pp(n + 1) == 0.0
        assert p.years_to_horizon(n + 1) == 0
        assert p.check_horizon() is True, point_id


def test_the_deduction_election_is_carried_and_inert(per_assurance):
    """It changes what the holder keeps, never what the insurer pays.

    The anchor cell with the election flipped produces the identical cash flow table, to
    the last floating-point bit.  Tax appears in no recursion in this model: the
    deductibility of the *versements* moves the exit taxation between the pension regime
    and the *rente viagère à titre onéreux* fractions, and the insurer pays the same euro
    amount either way.
    """
    base = per_assurance.Projection[1].result_cf()
    assert per_assurance.Projection[1].deduction_elected() is True
    assert set(per_assurance.Data.model_point_table()["deduction_elected"]) == {
        True, False}

    model = mx.read_model(MODEL_DIR, name="PER_FR_A_ded")
    try:
        path = alt_model_point_file(
            model, [anchor_row(deduction_elected=False)],
            "model_point_table_ded.csv")
        try:
            p = model.Projection[1]
            assert p.deduction_elected() is False
            flipped = p.result_cf()
        finally:
            path.unlink(missing_ok=True)
    finally:
        model.close()

    assert (flipped - base).abs().max().max() == pytest.approx(0.0, abs=1e-12)


# ---------------------------------------------------------------------------
# Model points the shipped tables must refuse


def test_a_c3_cell_electing_capital_raises():
    """The compartment rule is enforced, not assumed - and the table cannot hold the row."""
    model = mx.read_model(MODEL_DIR, name="PER_FR_A_c3")
    try:
        path = alt_model_point_file(
            model, [anchor_row(compartment="c3", exit_form="mixed")],
            "model_point_table_c3.csv")
        try:
            with pytest.raises(FormulaError):
                model.Projection[1].exit_form()
        finally:
            path.unlink(missing_ok=True)
    finally:
        model.close()


def test_an_annuity_share_contradicting_the_exit_form_raises():
    """capital_single with a 30% annuity share is two statements, not one."""
    model = mx.read_model(MODEL_DIR, name="PER_FR_A_share")
    try:
        path = alt_model_point_file(
            model, [anchor_row(exit_form="capital_single", annuity_share=0.30)],
            "model_point_table_share.csv")
        try:
            with pytest.raises(FormulaError):
                model.Projection[1].annuity_share()
        finally:
            path.unlink(missing_ok=True)
    finally:
        model.close()


def test_invalid_enum_values_raise(fr_per_anchor):
    """The enum accessors validate rather than propagating a typo into a lookup."""
    with pytest.raises(FormulaError):
        fr_per_anchor.claim_pp(1, "SURRENDER")
    with pytest.raises(FormulaError):
        fr_per_anchor.claims(1, "LAPSE")
    with pytest.raises(FormulaError):
        fr_per_anchor.av_pp_at(1, "MID")
    with pytest.raises(FormulaError):
        fr_per_anchor.pols_if_at(1, "AFT_SURR")


# ---------------------------------------------------------------------------
# Mortality


def test_the_two_mortality_bases_agree_in_the_anchor_cell_first_year(per_assurance):
    """The table's level is anchored so that mort_be_factor x q(M, 52) is 0.00500."""
    flat = per_assurance.Projection[1]
    assert flat.mort_basis() == "flat"
    assert flat.mort_rate(1) == 0.005
    assert all(flat.mort_rate(t) == 0.005 for t in range(1, 13))
    table = per_assurance.Data.mort_table()
    anchored = float(table.loc[("M", 52), "mort_rate"]) * (
        per_assurance.Projection.mort_be_factor)
    assert anchored == pytest.approx(0.00500, rel=1e-12)
    # A table cell reads the age at the START of the plan year.
    tabled = per_assurance.Projection[3]
    assert tabled.mort_basis() == "table"
    assert tabled.mort_rate(1) == pytest.approx(
        float(table.loc[("M", tabled.age_init()), "mort_rate"]) * 0.85, rel=1e-12)
    assert tabled.mort_rate(2) > tabled.mort_rate(1)


def test_the_shipped_mortality_table_marks_its_own_provenance():
    """A population-shaped proxy with an anchored level, and the file says so."""
    table = pd.read_csv(PRODUCT_DIR / "mort_table.csv")
    assert len(set(table["provenance"])) == 1
    note = table["provenance"].iloc[0]
    assert note.startswith("[std]")
    assert "INSEE" in note
    assert table["mort_rate"].max() <= 1.0
    assert set(table["sex"]) == {"M", "F"}
    # Female mortality is lighter than male at every age in the table.
    wide = table.pivot(index="age", columns="sex", values="mort_rate")
    assert (wide["F"] <= wide["M"]).all()


def test_the_exit_table_marks_its_own_provenance_and_avoids_the_word_lapse():
    """The decrements are [std] and the file names them for what they are."""
    table = pd.read_csv(PRODUCT_DIR / "exit_table.csv")
    assert list(table.columns) == [
        "compartment", "duration", "early_release_rate", "transfer_out_rate",
        "provenance"]
    assert all(n.startswith("[std]") for n in set(table["provenance"]))
    assert "lapse" not in " ".join(table.columns).lower()
    assert set(table["compartment"]) == {"c1", "c2", "c3"}
    c1 = table[table["compartment"] == "c1"]
    c3 = table[table["compartment"] == "c3"]
    assert c1["early_release_rate"].max() == 0.016
    assert c3["early_release_rate"].max() < 0.016
    assert set(table["transfer_out_rate"]) == {0.01}


def test_the_annuity_factor_table_marks_itself_a_placeholder():
    """TGH05 / TGF05 are cited and not shipped, and the file says so."""
    table = pd.read_csv(PRODUCT_DIR / "annuity_factor.csv")
    assert all("[std]" in n and "TGH05" in n for n in set(table["provenance"]))
    male64 = table[(table["sex"] == "M") & (table["age"] == 64)]
    assert male64["annuity_factor"].iloc[0] == pytest.approx(22.0, rel=1e-12)
    assert (table["annuity_factor"] > 0).all()
    # The factor falls with age on both sexes: fewer instalments remain.
    for sex in ("M", "F"):
        column = table[table["sex"] == sex].sort_values("age")["annuity_factor"]
        assert column.is_monotonic_decreasing


# ---------------------------------------------------------------------------
# Structure, sign convention and inputs


def test_result_cf_shape(fr_per_anchor):
    df = fr_per_anchor.result_cf()
    assert df.index.name == "t"
    assert list(df.index) == list(range(1, 13))
    assert list(df.columns) == [
        "pols_if", "av_pp", "premiums", "claims_death", "claims_early_release",
        "claims_transfer", "claims_maturity", "annuity_conversion", "expenses",
        "liability_cf", "net_cf",
    ]


def test_both_signs_of_the_net_flow_are_published(fr_per_anchor):
    """liability_cf is the notes' outgo-positive CF(t); net_cf is the library's sign."""
    df = fr_per_anchor.result_cf()
    assert (df["net_cf"] + df["liability_cf"]).abs().max() == pytest.approx(
        0.0, abs=1e-9)
    outgo = df[["claims_death", "claims_early_release", "claims_transfer",
                "claims_maturity", "annuity_conversion", "expenses"]].sum(axis=1)
    assert (outgo - df["premiums"] - df["liability_cf"]).abs().max() == (
        pytest.approx(0.0, abs=1e-9))
    # A contributing plan is cash-positive in every year but the settlement one.
    assert (df.loc[1:11, "net_cf"] > 0).all()
    assert df.loc[12, "net_cf"] < 0


def test_pols_if_is_the_start_of_period_count(per_assurance):
    """pols_if(t) is the count row t OPENS with, and the weight that row's flows carry.

    The library's settled convention, asserted here because breaking it is silent.  This
    model was first written with the notes' end-of-year l(t) published under the name
    ``pols_if``: every cash flow on the row was still weighted correctly, but the exposure
    column beside them was the right series shifted one period, so a reader dividing a
    flow by that row's ``pols_if`` recovered a one-period-stale per-policy amount and
    nothing raised.  The end-of-year quantity now lives at ``pols_if_at(t, "AFT_DECR")``
    and in ``result_state()`` as ``pols_if_eoy``.

    The checkable consequence is the first row: no decrement has been applied when a
    period opens, so ``result_cf()`` must open at ``pols_if_init()`` exactly, on every
    model point.
    """
    for point_id in per_assurance.Data.model_point_table().index:
        p = per_assurance.Projection[point_id]
        df = p.result_cf()
        assert df["pols_if"].iloc[0] == pytest.approx(p.pols_if_init(), rel=1e-12), (
            point_id)
        for t in range(1, p.proj_len() + 1):
            assert df.loc[t, "pols_if"] == pytest.approx(p.pols_if(t), rel=1e-14)
            # ... and one period behind the notes' l(t).
            assert p.pols_if_at(t, "AFT_DECR") == pytest.approx(
                p.pols_if(t + 1), rel=1e-14), (point_id, t)

    p = per_assurance.Projection[1]
    assert p.pols_if(1) == 1.0
    assert p.pols_if_at(1, "BEF_DECR") == 1.0
    assert p.pols_if_at(1, "AFT_DECR") == pytest.approx(0.969289, abs=POLS)
    assert p.pols_if(2) == pytest.approx(0.969289, abs=POLS)
    # The flows on a row are weighted by that row's own pols_if.
    assert p.premiums(2) == pytest.approx(3000.0 * p.pols_if(2), rel=1e-14)
    assert p.result_state().loc[1, "pols_if_eoy"] == pytest.approx(
        p.result_cf().loc[2, "pols_if"], rel=1e-14)
    # The horizon settlement is the one flow taken at the END-of-year count, because the
    # survivors settle after the final year's own decrements.
    n = p.proj_len()
    assert p.pols_maturity(n) == pytest.approx(
        p.pols_if_at(n, "AFT_DECR"), rel=1e-14)
    assert p.pols_maturity(n) < p.result_cf().loc[n, "pols_if"]


def test_inputs_live_beside_the_model():
    """Five external CSVs, and the glide path is one of them."""
    expected = {"model_point_table.csv", "allocation_grid.csv", "mort_table.csv",
                "exit_table.csv", "annuity_factor.csv"}
    assert expected == {p.name for p in PRODUCT_DIR.iterdir() if p.suffix == ".csv"}
    assert model_files(MODEL_DIR) == {"__init__.py", "_system.json"}


def test_the_glide_path_can_be_swapped_without_touching_formulas():
    """This is what a user does with an insurer's own twenty-band ladder."""
    src = PRODUCT_DIR / "allocation_grid.csv"
    grid = pd.read_csv(src, index_col=["allocation_profile", "years_to_horizon"])
    # A ladder that de-risks harder: 10 points more euro everywhere, capped at 1.
    harder = grid.copy()
    harder["euro_share"] = (harder["euro_share"] + 0.10).clip(upper=1.0)
    harder["uc_share"] = 1.0 - harder["euro_share"]

    model = mx.read_model(MODEL_DIR, name="PER_FR_A_grid")
    try:
        alt = "allocation_grid_hard.csv"
        harder.to_csv(model.Data.input_dir() / alt)
        try:
            base = model.Projection[1].av_pp(12)
            model.Data.allocation_grid_file = alt
            model.Data.clear_all()
            model.Projection.clear_all()
            # More euro support means less of the 5.00% UC return, so a smaller balance.
            assert model.Projection[1].av_pp(12) < base
            assert model.Projection[1].check_euro_share_min() is True
        finally:
            (model.Data.input_dir() / alt).unlink(missing_ok=True)
    finally:
        model.close()


def test_model_docstring_describes_the_current_structure(per_assurance):
    """Specifics a reader would rely on, asserted so they cannot go stale silently."""
    doc = per_assurance.doc
    assert "mechanics demonstration" in doc
    assert "external" in doc                      # inputs are not stored in the model
    assert "once per model" in doc                # why Data exists
    assert "Rente_FR_S" in doc                    # where the annuity goes
    assert "lapse_rate" in doc                    # and why there is not one
    for space in ("Data", "Projection"):
        assert space in doc


def test_space_docstrings_carry_their_reference_material(per_assurance):
    """Projection holds the symbol mapping; Data explains the input arrangement."""
    proj = per_assurance.Projection.doc
    assert "Notes symbol" in proj
    for cells in ("proj_len", "model_point", "alloc_euro", "switch_pp",
                  "death_floor_pp", "early_release_rate", "transfer_out_rate",
                  "annuity_factor", "is_commuted"):
        assert cells in proj, cells
    data = per_assurance.Data.doc
    assert "TradLife_A" in data
    for cells in ("input_dir", "model_point_table", "allocation_grid", "exit_table"):
        assert cells in data, cells


def test_round_trip_is_stable(tmp_path):
    """read -> write -> re-read reproduces the goldens and the same file set."""
    import shutil

    model = mx.read_model(MODEL_DIR, name="PER_FR_A_rt_src")
    try:
        dest = tmp_path / MODEL_DIR.name
        mx.write_model(model, str(dest), backup=False)
    finally:
        model.close()

    for csv in PRODUCT_DIR.glob("*.csv"):
        shutil.copy(csv, tmp_path / csv.name)

    reread = mx.read_model(dest, name="PER_FR_A_rt")
    try:
        p = reread.Projection[1]
        for t, row in WORKED_EXAMPLE.items():
            assert p.av_pp(t) == pytest.approx(row[5], abs=CENT)
            assert p.pols_if_at(t, "AFT_DECR") == pytest.approx(row[6], abs=POLS)
        assert p.commuted_pp() == pytest.approx(20711.12, abs=CENT)
        assert "Notes symbol" in reread.Projection.doc
    finally:
        reread.close()

    assert model_files(dest) == model_files(MODEL_DIR)
