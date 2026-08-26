"""Golden and structural tests for Euro_FR_A.

The golden values are the worked example in
products/assurance_vie_euro/technical-notes.md ("Worked example"): an in-force
euro-support cell with EUR 100,000 of `epargne acquise` at duration 5, male aged 60,
EUR 2,400 a year of `versements` and EUR 3,000 a year of `rachats partiels` from projection
year 6, a 0.60% management charge, a nil TMG, a 2.30% target `taux servi`, a 17.2% social
levy, and an opening PPB of EUR 4,000 in eight equal vintages falling due in projection
years 1 to 8.  Model point 1 is that cell.  They are hard-coded here rather than pickled so
that a reviewer can compare them against the notes by eye, to the precision the notes
display: money to the cent, rates to the fourth decimal of a percentage.

Beyond the worked example this module asserts the product facts the notes list as modelling
pitfalls, one test each and each named for the failure it catches, because every one of
them is a way an implementation can look right and be wrong.
"""
import modelx as mx
import pytest
from modelx.core.errors import FormulaError

from fr_registry import LIB, MODELS


def model_files(folder):
    """The model's own file names, ignoring ``__pycache__``.

    Those caches appear as soon as anything imports the model - which building the
    autodoc API pages does - and are not part of it.
    """
    return {p.name for p in folder.rglob("*")
            if p.is_file() and "__pycache__" not in p.parts}


CENT = 0.01           # money, to the precision the notes display
RATE = 1e-6           # rates, displayed as a percentage to four decimals

MODEL_DIR = LIB / MODELS["Euro_FR_A"][0]

CHECKS = ("check_av_roll_fwd", "check_ppb_roll_fwd", "check_ppb_clock",
          "check_pols_roll_fwd", "check_pb_allocation", "check_cliquet",
          "check_guar_floor")

# Table 1 -- the taux servi and the PPB.
# t: (r_fin, pm_avg_pp, 0.85 x fin_acct_pp, policyholder technical share, pb_min_pp,
#     ts_stat, PPB release less dotation, ppb_pp(t+1), ts_net)
TABLE_1 = {
    1: (0.0330, 101200.00, 2950.86, 121.00, 3071.86, 0.024354, 362.94, 3637.06, 0.027941),
    2: (0.0325, 105941.25, 3027.10, 132.49, 3159.59, 0.023824, 412.70, 3224.36, 0.027720),
    3: (0.0320, 110772.80, 3100.72, 144.21, 3244.93, 0.023294, 467.48, 2756.88, 0.027514),
    4: (0.0310, 115696.36, 3121.24, 156.14, 3277.39, 0.022327, 500.00, 2256.88, 0.026649),
    5: (0.0295, 120649.25, 3081.87, 168.15, 3250.02, 0.020938, 500.00, 1756.88, 0.025082),
    6: (0.0280, 124054.88, 2994.32, 176.28, 3170.60, 0.019558, 500.00, 1256.88, 0.023589),
    7: (0.0265, 125877.84, 2863.71, 180.45, 3044.16, 0.018183, 606.30, 650.58, 0.023000),
    8: (0.0255, 127675.06, 2781.46, 184.55, 2966.01, 0.017231, 650.58, 0.00, 0.022327),
    9: (0.0245, 129435.30, 2695.49, 188.55, 2884.04, 0.016282, 0.00, 0.00, 0.016282),
    10: (0.0240, 130580.26, 2663.84, 191.01, 2854.85, 0.015863, 0.00, 0.00, 0.015863),
    11: (0.0235, 131695.35, 2630.61, 193.39, 2824.00, 0.015443, 0.00, 0.00, 0.015443),
    12: (0.0230, 132779.35, 2595.84, 195.68, 2791.51, 0.015024, 0.00, 0.00, 0.015024),
}

# Table 2 -- the epargne acquise roll-forward.
# t: (av_pp(t), prem_to_av_pp, withdrawals_pp, int_credited_pp, soc_levy_pp, av_pp(t+1))
TABLE_2 = {
    1: (100000.00, 2400.00, 0.00, 2827.60, 486.35, 104741.25),
    2: (104741.25, 2400.00, 0.00, 2936.65, 505.10, 109572.80),
    3: (109572.80, 2400.00, 0.00, 3047.77, 524.22, 114496.36),
    4: (114496.36, 2400.00, 0.00, 3083.21, 530.31, 119449.25),
    5: (119449.25, 2400.00, 0.00, 3026.13, 520.49, 124354.88),
    6: (124354.88, 2400.00, 3000.00, 2926.27, 503.32, 126177.84),
    7: (126177.84, 2400.00, 3000.00, 2895.19, 497.97, 127975.06),
    8: (127975.06, 2400.00, 3000.00, 2850.54, 490.29, 129735.30),
    9: (129735.30, 2400.00, 3000.00, 2107.43, 362.48, 130880.26),
    10: (130880.26, 2400.00, 3000.00, 2071.36, 356.27, 131995.35),
    11: (131995.35, 2400.00, 3000.00, 2033.83, 349.82, 133079.35),
    12: (133079.35, 2400.00, 3000.00, 1994.84, 343.11, 134131.08),
}

# The decrement and cash-flow extract.
# t: (lapse_rate, pols_if, claims_death, claims_lapse, expenses, liability_cf)
DECREMENTS = {
    1: (0.040000, 1.000000, 628.45, 4164.51, 378.20, 2771.16),
    3: (0.080000, 0.910080, 743.00, 8276.62, 375.34, 7210.78),
    6: (0.050000, 0.738099, 862.56, 4613.46, 339.56, 6258.43),
    9: (0.062873, 0.613775, 968.78, 4989.75, 294.65, 6621.44),
}


# ---------------------------------------------------------------------------
# The worked example


@pytest.mark.parametrize("t", sorted(TABLE_1))
def test_the_worked_example_row(fr_euro_anchor, t):
    """Every cell of the notes' Tables 1 and 2 for year t, to the displayed precision.

    Table 2's recursion is then restated on the notes' own printed numbers, so that a row
    which reproduces the model still has to reproduce the next row's opening balance.
    """
    r_fin, pm, fin85, ph_tech, pb_min, ts_stat, ppb_flow, ppb_next, ts_net = TABLE_1[t]
    p = fr_euro_anchor
    assert p.r_fin(t) == pytest.approx(r_fin, abs=RATE)
    assert p.pm_avg_pp(t) == pytest.approx(pm, abs=CENT)
    assert 0.85 * p.fin_acct_pp(t) == pytest.approx(fin85, abs=CENT)
    assert p.tech_acct_pp(t) - p.insurer_tech_share_pp(t) == pytest.approx(
        ph_tech, abs=CENT)
    assert p.pb_min_pp(t) == pytest.approx(pb_min, abs=CENT)
    assert p.ts_stat(t) == pytest.approx(ts_stat, abs=RATE)
    assert p.ppb_release_pp(t) - p.ppb_dotation_pp(t) == pytest.approx(
        ppb_flow, abs=CENT)
    assert p.ppb_pp(t + 1) == pytest.approx(ppb_next, abs=CENT)
    assert p.ts_net(t) == pytest.approx(ts_net, abs=RATE)

    av, prem, wd, interest, levy, av_next = TABLE_2[t]
    assert p.av_pp(t) == pytest.approx(av, abs=CENT)
    assert p.prem_to_av_pp(t) == pytest.approx(prem, abs=CENT)
    assert p.withdrawals_pp(t) == pytest.approx(wd, abs=CENT)
    assert p.int_credited_pp(t) == pytest.approx(interest, abs=CENT)
    assert p.soc_levy_pp(t) == pytest.approx(levy, abs=CENT)
    assert p.av_pp(t + 1) == pytest.approx(av_next, abs=CENT)
    assert p.av_pp(t + 1) == pytest.approx(
        av + prem - wd + interest - levy, abs=2 * CENT)


@pytest.mark.parametrize("t", sorted(DECREMENTS))
def test_the_decrement_and_cash_flow_extract(fr_euro_anchor, t):
    """The notes' decrement extract, including the duration-8 surrender step at t = 3."""
    lapse, pols, death, lapse_cl, exp, liab = DECREMENTS[t]
    p = fr_euro_anchor
    assert p.lapse_rate(t) == pytest.approx(lapse, abs=RATE)
    assert p.pols_if(t) == pytest.approx(pols, abs=1e-6)
    assert p.claims(t, "DEATH") == pytest.approx(death, abs=CENT)
    assert p.claims(t, "LAPSE") == pytest.approx(lapse_cl, abs=CENT)
    assert p.expenses(t) == pytest.approx(exp, abs=CENT)
    assert p.liability_cf(t) == pytest.approx(liab, abs=CENT)
    assert p.net_cf(t) == pytest.approx(-liab, abs=CENT)


def test_the_year_six_trace_at_full_precision(fr_euro_anchor):
    """Year 6 is the year in which every lever is active at once.

    The discretionary release the target wants is EUR 426.99, the vintage falling due is
    EUR 500.00, and the forced release wins - so the rate lands *above* target.
    """
    p = fr_euro_anchor
    assert p.pm_avg_pp(6) == pytest.approx(124054.884701, abs=1e-6)
    assert p.fee_pp(6) == pytest.approx(744.329308, abs=1e-6)
    assert p.expenses_pp(6) == pytest.approx(460.046913, abs=1e-6)
    assert p.fin_acct_pp(6) == pytest.approx(3522.729293, abs=1e-6)
    assert 0.85 * p.fin_acct_pp(6) == pytest.approx(2994.319899, abs=1e-6)
    assert p.tech_acct_pp(6) == pytest.approx(284.282396, abs=1e-6)
    assert p.insurer_tech_share_pp(6) == pytest.approx(108.000000, abs=1e-6)
    assert p.pb_acct_pp(6) == pytest.approx(3170.602295, abs=1e-6)
    assert p.pb_min_pp(6) == pytest.approx(p.pb_acct_pp(6), abs=1e-9)
    assert p.ts_stat(6) == pytest.approx(0.01955806, abs=1e-8)
    assert p.pb_target_pp(6) == pytest.approx(3597.591656, abs=1e-6)
    assert p.ppb_discr_rel_pp(6) == pytest.approx(426.989361, abs=1e-6)
    assert p.ppb_forced_pp(6) == pytest.approx(500.000000, abs=1e-6)
    assert p.ppb_release_pp(6) == pytest.approx(500.000000, abs=1e-6)
    assert p.pb_credited_pp(6) == pytest.approx(3670.602295, abs=1e-6)
    assert p.ts_net(6) == pytest.approx(0.02358853, abs=1e-8)
    assert p.int_credited_pp(6) == pytest.approx(2926.272987, abs=1e-6)
    assert p.soc_levy_pp(6) == pytest.approx(503.318954, abs=1e-6)
    assert p.av_pp(7) == pytest.approx(126177.838734, abs=1e-6)
    # And the same rate from a different direction: 0.85 x financial + technical share
    # - the charge + the PPB flow, all over the base.  Year 9 has the PPB exhausted.
    for t, expected in ((6, 0.02358853), (9, 0.01628173)):
        base = p.pm_avg_pp(t)
        built = (0.85 * p.fin_acct_pp(t) / base
                 + (p.tech_acct_pp(t) - p.insurer_tech_share_pp(t)) / base
                 - p.fee_rate()
                 + (p.ppb_release_pp(t) - p.ppb_dotation_pp(t)) / base)
        assert built == pytest.approx(expected, abs=1e-8)
        assert built == pytest.approx(p.ts_net(t), abs=1e-12)


def test_the_twelve_year_identities_close(fr_euro_anchor):
    """Interest EUR 31,800.82 and levies EUR 5,469.74, reaching EUR 134,131.08.

    The same total the other way: PB credited gross of the charge is EUR 40,538.97 less
    `frais de gestion` of EUR 8,738.15.  Then year 1 at fund level:
    100,000 + 2,400 + 2,827.60 - 486.35 - 628.45 - 4,164.51 = 99,948.29.
    """
    p = fr_euro_anchor
    interest = sum(p.int_credited_pp(t) for t in range(1, 13))
    levies = sum(p.soc_levy_pp(t) for t in range(1, 13))
    credited = sum(p.pb_credited_pp(t) for t in range(1, 13))
    fees = sum(p.fee_pp(t) for t in range(1, 13))
    assert interest == pytest.approx(31800.82, abs=CENT)
    assert levies == pytest.approx(5469.74, abs=CENT)
    assert levies / interest == pytest.approx(0.172000, abs=1e-9)
    assert credited == pytest.approx(40538.97, abs=CENT)
    assert fees == pytest.approx(8738.15, abs=CENT)
    assert credited - fees == pytest.approx(interest, abs=1e-9)
    assert 100000.00 + 28800.00 - 21000.00 + interest - levies == pytest.approx(
        134131.08, abs=CENT)
    assert p.av_pp(13) == pytest.approx(134131.08, abs=CENT)
    assert p.pols_if(2) == pytest.approx(0.954240, abs=1e-6)
    assert p.av(2) == pytest.approx(99948.29, abs=CENT)
    assert p.check_av_roll_fwd() is True


def test_the_guarantee_floor_never_binds_on_this_path(fr_euro_anchor):
    """G(13) = 100,000 + 28,800 - 21,000 - 8,738.15 = 99,061.85 against 139,600.82.

    Compared to the account **before** cumulative social levies, because the published
    minimum surrender-value tables are stated before social and tax levies.
    """
    p = fr_euro_anchor
    assert p.guarantee_form() == "net"
    assert p.guar_floor_pp(13) == pytest.approx(99061.85, abs=CENT)
    assert p.av_pp(13) + p.soc_levy_cum_pp(13) == pytest.approx(139600.82, abs=CENT)
    assert p.check_guar_floor() is True
    assert all(p.check_guar_floor_resid(t) == 0.0 for t in range(1, 13))


# ---------------------------------------------------------------------------
# Pitfalls 1 and 2: the charge and the crediting base


def test_the_management_charge_is_not_deducted_twice(fr_euro_anchor):
    """`ts_net` is already net of the charge; `av x (1 + ts_net) x (1 - c)` takes it twice."""
    p = fr_euro_anchor
    for t in (1, 6, 9, 12):
        assert p.pb_credited_pp(t) - p.fee_pp(t) == pytest.approx(
            p.int_credited_pp(t), abs=1e-9)
        assert p.av_pp_at(t, "AFT_INT") == pytest.approx(
            p.av_pp_at(t, "AFT_WD") + p.int_credited_pp(t), abs=1e-9)
        # What the double deduction would cost: 0.60% of the closing balance, every year.
        doubled = p.av_pp_at(t, "AFT_INT") * (1.0 - p.fee_rate())
        assert p.av_pp_at(t, "AFT_INT") - doubled == pytest.approx(
            p.fee_rate() * p.av_pp_at(t, "AFT_INT"), rel=1e-12)
        assert p.av_pp_at(t, "AFT_INT") - doubled > 600.0


def test_the_crediting_base_is_pro_rata_temporis(assurance_vie_euro, fr_euro_anchor):
    """B(t) = AV(t) + 0.5 P(t) - 0.5 W(t), not the closing balance.

    The two differ by exactly ``0.5 ts_net(t) (P(t) - W(t))`` - a full year's interest on
    a December payment - and coincide where nothing moves, which is the paid-up cell.
    """
    p = fr_euro_anchor
    for t in (1, 6, 12):
        closing = p.av_pp(t) + p.prem_to_av_pp(t) - p.withdrawals_pp(t)
        assert closing - p.pm_avg_pp(t) == pytest.approx(
            0.5 * (p.prem_to_av_pp(t) - p.withdrawals_pp(t)), abs=1e-9)
        assert p.ts_net(t) * closing - p.int_credited_pp(t) == pytest.approx(
            0.5 * p.ts_net(t) * (p.prem_to_av_pp(t) - p.withdrawals_pp(t)), abs=1e-9)
    paid_up = assurance_vie_euro.Projection[4]
    assert paid_up.prem_gross_pp(3) == 0.0 and paid_up.withdrawals_pp(3) == 0.0
    assert paid_up.pm_avg_pp(3) == pytest.approx(paid_up.av_pp(3), rel=1e-15)


# ---------------------------------------------------------------------------
# Pitfalls 3 and 4: the statutory split


def test_the_eighty_five_percent_attaches_to_the_financial_account(fr_euro_anchor):
    """Not "90% of the financial account and 85% of the technical result".

    The popular form gives EUR 3,319.09 in year 1 against the correct EUR 3,071.86.
    """
    p = fr_euro_anchor
    for t in (1, 6, 12):
        ph_tech = p.tech_acct_pp(t) - p.insurer_tech_share_pp(t)
        assert p.pb_acct_pp(t) - ph_tech == pytest.approx(
            0.85 * p.fin_acct_pp(t), abs=1e-9)
    assert 0.90 * p.fin_acct_pp(1) + 0.85 * p.tech_acct_pp(1) == pytest.approx(
        3319.09, abs=CENT)
    assert p.pb_acct_pp(1) == pytest.approx(3071.86, abs=CENT)


def test_the_four_and_a_half_percent_of_premiums_limb_binds(
        assurance_vie_euro, fr_euro_anchor):
    """EUR 108.00 against EUR 28.43 for the 10% limb in year 6; nil on a paid-up cell.

    Two cells identical but for their premium stream credit different rates, which is the
    article working as written.
    """
    p = fr_euro_anchor
    assert p.insurer_tech_share_pp(6) == pytest.approx(108.00, abs=CENT)
    assert 0.10 * p.tech_acct_pp(6) == pytest.approx(28.43, abs=CENT)
    assert p.insurer_tech_share_pp(6) == pytest.approx(
        0.045 * p.prem_gross_pp(6), abs=1e-9)
    paid_up = assurance_vie_euro.Projection[4]
    assert paid_up.prem_gross_pp(3) == 0.0
    assert paid_up.insurer_tech_share_pp(3) == pytest.approx(
        0.10 * paid_up.tech_acct_pp(3), abs=1e-12)
    assert paid_up.ts_stat(1) > p.ts_stat(1)


# ---------------------------------------------------------------------------
# Pitfalls 5, 6 and 7: the PPB


def test_the_ppb_is_inside_the_financial_base_and_does_not_accrete(fr_euro_anchor):
    """Struck on ``pm_avg_pp + ppb_pp``; omitting it costs EUR 41.81 in year 6.

    The mirror error is accreting the vintages, which pays the PPB's own return twice.
    """
    p = fr_euro_anchor
    assert p.fin_acct_pp(6) == pytest.approx(
        p.r_fin(6) * (p.pm_avg_pp(6) + p.ppb_pp(6)), abs=1e-9)
    assert 0.85 * p.r_fin(6) * p.ppb_pp(6) == pytest.approx(41.81, abs=CENT)
    for t in range(1, 12):
        for v in range(p.ppb_vintage_first(), t):
            assert p.ppb_vintage_pp(t + 1, v) == pytest.approx(
                p.ppb_vintage_pp(t, v) - p.ppb_vintage_release_pp(t, v), abs=1e-9)


def test_the_ppb_is_released_fifo_oldest_vintage_first(fr_euro_anchor):
    """The year-7 release of EUR 606.30 clears the last EUR 500 vintage first.

    It then takes EUR 106.30 from the year-0 vintage, leaving EUR 393.70 to be forced out
    in year 8 - which the year-8 discretionary need of EUR 650.58 more than covers, so the
    PPB reaches zero exactly at the clock's last date.
    """
    p = fr_euro_anchor
    assert p.ppb_release_pp(7) == pytest.approx(606.30, abs=CENT)
    assert p.ppb_vintage_release_pp(7, -1) == pytest.approx(500.00, abs=CENT)
    assert p.ppb_vintage_release_pp(7, 0) == pytest.approx(106.30, abs=CENT)
    assert p.ppb_vintage_release_pp(7, 1) == 0.0
    assert p.ppb_vintage_pp(8, -1) == pytest.approx(0.0, abs=1e-9)
    assert p.ppb_vintage_pp(8, 0) == pytest.approx(393.70, abs=CENT)
    assert p.ppb_forced_pp(8) == pytest.approx(393.70, abs=CENT)
    assert p.ppb_release_pp(8) == pytest.approx(650.58, abs=CENT)
    assert p.ppb_pp(9) == pytest.approx(0.0, abs=CENT)


def test_the_vintage_ledger_table_in_model_md(fr_euro_anchor):
    """model.md's PPB ledger table, every cell of it.

    The table has an uncapped-want column and a capped-discretionary column because the
    two separate twice and for different reasons - a negative want in years 1 to 3, which
    is what a dotation year is, and a binding balance from year 8 - and a release column
    because neither want column is the release wherever the clock outranks the target.
    Nothing else in this module asserts the years 9 onward row, which is how a figure the
    model does not produce once stood in it.
    """
    p = fr_euro_anchor
    # t: (forced, want uncapped, discretionary, released)
    ledger = {
        1: (500.00, -137.06, 0.00, 500.00),
        2: (500.00, -87.30, 0.00, 500.00),
        3: (500.00, -32.52, 0.00, 500.00),
        4: (500.00, 77.81, 77.81, 500.00),
        5: (500.00, 248.81, 248.81, 500.00),
        6: (500.00, 426.99, 426.99, 500.00),
        7: (500.00, 606.30, 606.30, 606.30),
        8: (393.70, 736.57, 650.58, 650.58),
        9: (0.00, 869.58, 0.00, 0.00),
        10: (0.00, 931.98, 0.00, 0.00),
        11: (0.00, 995.17, 0.00, 0.00),
        12: (0.00, 1059.09, 0.00, 0.00),
    }
    for t, (forced, want, discr, released) in ledger.items():
        assert p.ppb_forced_pp(t) == pytest.approx(forced, abs=CENT), t
        assert p.pb_target_pp(t) - p.pb_min_pp(t) == pytest.approx(want, abs=CENT), t
        assert p.ppb_discr_rel_pp(t) == pytest.approx(discr, abs=CENT), t
        assert p.ppb_release_pp(t) == pytest.approx(released, abs=CENT), t
    # The want column is the dotation's mirror image while it is negative.
    for t in (1, 2, 3):
        assert p.ppb_dotation_pp(t) == pytest.approx(
            p.pb_min_pp(t) - p.pb_target_pp(t), abs=1e-9)
    # From year 9 the balance is nil, so the want rises and nothing is released.
    assert p.ppb_pp(9) == pytest.approx(0.0, abs=CENT)


def test_no_ppb_vintage_outlives_its_eight_year_clock(assurance_vie_euro):
    """Nothing survives the year after its deadline, and the ledger ties to the balance.

    A LIFO release satisfies the aggregate recursion exactly and breaches the clock
    invisibly, which is why the per-vintage ledger exists at all.
    """
    for point_id in assurance_vie_euro.Data.model_point_table().index:
        p = assurance_vie_euro.Projection[point_id]
        assert p.check_ppb_clock() is True, point_id
        assert p.check_ppb_roll_fwd() is True, point_id
        for t in range(1, p.proj_len() + 1):
            assert p.ppb_pp(t) >= -1e-9
            assert p.ppb_ledger_pp(t) == pytest.approx(p.ppb_pp(t), abs=1e-8)
            for v in range(p.ppb_vintage_first(), t - 8):
                assert p.ppb_vintage_pp(t, v) == pytest.approx(0.0, abs=1e-8)


def test_the_clock_reaches_dotation_vintages_and_a_young_profile_defers_it(
        assurance_vie_euro):
    """Point 8 credits a dotation every year and each comes back out at v + 8.

    Point 6 carries the same EUR 4,000 in four vintages rather than eight, due in years 5
    to 8, so nothing is forced out before year 5 - which is why the vintage split is a
    **[std]** worth naming.
    """
    high = assurance_vie_euro.Projection[8]
    assert high.scenario_id() == "high"
    assert all(high.ppb_dotation_pp(t) > 0.0 for t in range(1, 13))
    for t in range(9, 15):
        assert high.ppb_forced_pp(t) == pytest.approx(
            high.ppb_dotation_pp(t - 8), abs=CENT)
    assert high.ppb_pp(41) > 0.0     # a growing PPB, and still no vintage overdue
    young = assurance_vie_euro.Projection[6]
    assert young.ppb_vintages_init() == 4 and young.ppb_vintage_first() == -3
    assert young.ppb_vintage_pp(1, -3) == pytest.approx(1000.00, abs=CENT)
    assert all(young.ppb_forced_pp(t) == 0.0 for t in range(1, 5))
    assert young.ppb_forced_pp(5) > 0.0
    assert young.ts_net(1) == pytest.approx(young.ts_target(), abs=1e-12)


def test_the_statutory_minimum_is_allocated_in_full_not_credited_in_full(
        assurance_vie_euro, fr_euro_anchor):
    """A dotation year credits *less* than ts_stat, and that is legal.

    The balance goes to the PPB, not to the insurer, so the invariant is an allocation
    identity rather than a rate inequality.  Model point 5 opens with no PPB and credits
    below the statutory floor rate in year 1; the anchor cell never does, only because its
    forced release always exceeds its dotation.
    """
    p = fr_euro_anchor
    assert p.check_pb_allocation() is True
    for t in (1, 6, 9):
        assert p.check_pb_allocation_resid(t) == pytest.approx(0.0, abs=1e-7)
        assert p.int_credited_pp(t) + p.fee_pp(t) + p.ppb_dotation_pp(t) == pytest.approx(
            p.pb_min_pp(t) + p.ppb_release_pp(t) + p.insurer_topup_pp(t), abs=1e-7)
    no_ppb = assurance_vie_euro.Projection[5]
    assert no_ppb.ppb_pp(1) == 0.0 and no_ppb.ppb_dotation_pp(1) > 0.0
    assert no_ppb.ts_net(1) < no_ppb.ts_stat(1)
    assert no_ppb.ts_net(1) == pytest.approx(no_ppb.ts_target(), abs=1e-12)
    assert no_ppb.check_pb_allocation() is True


# ---------------------------------------------------------------------------
# Pitfalls 8 and 9: the prelevements sociaux


def test_the_social_levy_is_annual_not_deferred_to_surrender(fr_euro_anchor):
    """17.2% every year on euro-denominated rights, inside the account and outside net_cf.

    Deferring it to `denouement` is right for the UC compartment and wrong here, and it
    overstates the account and every benefit measured on it.
    """
    p = fr_euro_anchor
    for t in range(1, 13):
        assert p.soc_levy_pp(t) > 0.0
        assert p.soc_levy_pp(t) == pytest.approx(
            p.soc_levy_rate() * max(p.int_credited_pp(t), 0.0), abs=1e-12)
    total_levy = sum(p.soc_levy_pp(t) for t in range(1, 13))
    total_int = sum(p.int_credited_pp(t) for t in range(1, 13))
    assert total_levy == pytest.approx(0.172 * total_int, abs=1e-9)
    assert p.av_pp(2) == pytest.approx(
        p.av_pp_at(1, "AFT_INT") - p.soc_levy_pp(1), abs=1e-12)
    df = p.result_cf()
    outgo = df[["claims_death", "claims_lapse", "withdrawals", "expenses"]].sum(axis=1)
    assert (outgo - df["premiums"] - df["liability_cf"]).abs().max() == pytest.approx(
        0.0, abs=1e-9)
    assert df["soc_levy"].sum() > 0.0


def test_the_social_levy_base_is_the_years_interest_not_the_account(fr_euro_anchor):
    """17.2% of EUR 100,000 is EUR 17,200; of year 1's EUR 2,827.60 it is EUR 486.35."""
    p = fr_euro_anchor
    assert 0.172 * p.av_pp(1) == pytest.approx(17200.00, abs=CENT)
    assert p.soc_levy_pp(1) == pytest.approx(486.35, abs=CENT)
    assert p.int_credited_pp(1) == pytest.approx(2827.60, abs=CENT)
    assert p.soc_levy_cum_pp(1) == 0.0
    assert p.soc_levy_cum_pp(13) == pytest.approx(5469.74, abs=CENT)


# ---------------------------------------------------------------------------
# Pitfalls 10, 11 and 12: the cliquet, the death benefit and mid-year exits


def test_the_cliquet_ratchets_credited_pb_not_the_account_balance(
        assurance_vie_euro, fr_euro_anchor):
    """Credited PB is definitively acquired; the balance is not.

    Model point 10, a drawdown cell, falls every year from year 4 while its ratchet holds
    throughout.  Testing the cliquet as "``av_pp`` never falls" is the pitfall.
    """
    p = fr_euro_anchor
    assert p.check_cliquet() is True and p.pb_cum_pp(1) == 0.0
    for t in range(1, 13):
        assert p.int_credited_pp(t) >= 0.0
        assert p.ts_net(t) >= p.tmg_rate()
        assert p.pb_cum_pp(t + 1) == pytest.approx(
            p.pb_cum_pp(t) + p.pb_credited_pp(t), abs=1e-9)
    drawdown = assurance_vie_euro.Projection[10]
    assert drawdown.av_pp(5) < drawdown.av_pp(4)
    assert drawdown.check_cliquet() is True
    assert drawdown.pb_cum_pp(20) > drawdown.pb_cum_pp(10)


def test_the_death_benefit_is_the_account_value_with_no_uplift(fr_euro_anchor):
    """DB = CV = av_pp(t+1), no uplift and no surrender penalty; and no maturity kind."""
    p = fr_euro_anchor
    for t in (1, 6, 12, 30):
        assert p.db_pp(t) == pytest.approx(p.av_pp(t + 1), rel=1e-15)
        assert p.cv_pp(t) == pytest.approx(p.av_pp(t + 1), rel=1e-15)
        assert p.claim_pp(t, "DEATH") == pytest.approx(p.claim_pp(t, "LAPSE"), rel=1e-15)
    with pytest.raises(FormulaError):
        p.claim_pp(1, "MATURITY")
    assert "claims_maturity" not in p.result_cf().columns


def test_mid_year_exits_take_the_full_years_taux_servi(fr_euro_anchor):
    """The base model does exactly that, and says so.

    Decrements act at 31 December after crediting.  The contractual rule is the announced
    floor rate `pro rata temporis`, which at a nil TMG is no in-year interest at all; the
    difference is one year's revalorisation net of the levy.
    """
    p = fr_euro_anchor
    for t in (1, 6, 12):
        strict = p.av_pp_at(t, "AFT_WD")          # the pro rata rule at a nil TMG
        assert p.claim_pp(t, "LAPSE") - strict == pytest.approx(
            p.int_credited_pp(t) - p.soc_levy_pp(t), abs=1e-9)
        assert p.claim_pp(t, "LAPSE") > strict
    assert p.tmg_rate() == 0.0
    assert p.pols_if_at(6, "AFT_DECR") == pytest.approx(
        p.pols_if(6) * (1 - p.mort_rate(6)) * (1 - p.lapse_rate(6)), abs=1e-12)


# ---------------------------------------------------------------------------
# Behaviour


def test_the_duration_eight_surrender_step_is_the_tax_threshold(fr_euro_anchor):
    """Keyed to the **contract's** eighth anniversary, not to projection year 8.

    The anchor cell is five years in, so duration 8 falls at t = 3.  A model indexing the
    lapse table by t would put the step five years late.
    """
    p = fr_euro_anchor
    assert p.duration_init() == 5
    assert [p.duration(t) for t in (1, 3, 6)] == [6, 8, 11]
    assert p.lapse_rate_base(3) == pytest.approx(0.08, abs=1e-12)
    assert p.lapse_rate_base(2) == pytest.approx(0.04, abs=1e-12)
    assert p.lapse_rate_base(4) == pytest.approx(0.05, abs=1e-12)
    assert p.ref_rate(1) == pytest.approx(0.0220, abs=1e-12)


def test_the_dynamic_surrender_term_is_one_sided(assurance_vie_euro, fr_euro_anchor):
    """Additive in the gap, and nil while the `taux servi` beats the reference rate."""
    p = fr_euro_anchor
    for t in range(1, 9):
        assert p.ts_net(t) > p.ref_rate(t)
        assert p.lapse_dyn_add(t) == 0.0
        assert p.lapse_rate(t) == pytest.approx(p.lapse_rate_base(t), abs=1e-12)
    assert p.lapse_dyn_add(9) == pytest.approx(
        4.0 * (p.ref_rate(9) - p.ts_net(9) - 0.0025), abs=1e-12)
    assert p.lapse_rate(9) == pytest.approx(0.062873, abs=RATE)
    # A 0.73% taux servi against a 2.20% Livret A adds 4.88 points to a 5% base rate.
    low = assurance_vie_euro.Projection[7]
    assert low.scenario_id() == "low" and low.ts_net(20) < low.ref_rate(20)
    assert low.lapse_dyn_add(20) == pytest.approx(0.048755, abs=RATE)
    assert low.lapse_rate(20) == pytest.approx(0.098755, abs=RATE)


def test_the_dynamic_surrender_cap_binds_when_the_gap_is_wide():
    """The cap has no public calibration and never binds on the shipped scenarios.

    Raising the coefficient on a throwaway instance is the only way to see it, and seeing
    it is the point: a mass-lapse run here is a pre-management-action number in any case.
    """
    model = mx.read_model(MODEL_DIR, name="Euro_FR_A_cap")
    try:
        assert model.Projection.lapse_cap == 0.3
        model.Projection.lapse_dyn_a = 60.0
        model.Projection.clear_all()
        p = model.Projection[7]
        assert p.lapse_dyn_add(20) > 0.3
        assert p.lapse_rate(20) == pytest.approx(0.3, abs=1e-12)
    finally:
        model.close()


# ---------------------------------------------------------------------------
# The variants the shipped model points carry


def test_the_shipped_variants_behave_as_their_columns_say(assurance_vie_euro):
    """Points 2, 3, 9 and 11 against the anchor cell.

    The `garantie brute` (2) leaves the account path untouched and lifts only the floor, by
    the cumulative charge.  A 2.90% target (3) drains the PPB by year 7 and then credits the
    statutory floor rate.  The small new-business cell (9) carries a 0.50% entry charge and
    a 0.80% management charge, and the fixed part of its expense loading dominates its
    `compte technique`.  The grouped cell (11) scales every flow by 250 and no state at all.
    """
    anchor = assurance_vie_euro.Projection[1]

    gross = assurance_vie_euro.Projection[2]
    assert gross.guarantee_form() == "gross" and anchor.guarantee_form() == "net"
    assert gross.av_pp(13) == pytest.approx(anchor.av_pp(13), rel=1e-15)
    assert gross.guar_floor_pp(13) == pytest.approx(
        anchor.guar_floor_pp(13) + 8738.15, abs=CENT)
    assert gross.guar_floor_pp(13) == pytest.approx(107800.00, abs=CENT)

    eager = assurance_vie_euro.Projection[3]
    assert eager.ts_target() == pytest.approx(0.0290, abs=1e-12)
    assert eager.ppb_pp(5) < anchor.ppb_pp(5)
    assert eager.ppb_pp(7) == pytest.approx(0.0, abs=CENT)
    assert eager.ts_net(10) == pytest.approx(eager.ts_stat(10), abs=1e-12)

    small = assurance_vie_euro.Projection[9]
    assert small.prem_charge_rate() == pytest.approx(0.005, abs=1e-12)
    assert small.prem_to_av_pp(1) == pytest.approx(1200.0 * 0.995, abs=1e-9)
    assert small.duration_init() == 0 and small.age(1) == 45
    assert small.lapse_rate_base(8) == pytest.approx(0.08, abs=1e-12)
    assert small.ts_stat(1) < anchor.ts_stat(1)

    grouped = assurance_vie_euro.Projection[11]
    assert grouped.pols_if_init() == 250.0
    for t in (1, 9, 20):
        assert grouped.av_pp(t) == pytest.approx(anchor.av_pp(t), rel=1e-15)
        assert grouped.ts_net(t) == pytest.approx(anchor.ts_net(t), rel=1e-15)
        assert grouped.net_cf(t) == pytest.approx(250.0 * anchor.net_cf(t), rel=1e-9)


def test_no_model_point_elects_an_avance_or_carries_a_positive_tmg(assurance_vie_euro):
    """Both are unpublished in the source set, so both are validated rather than guessed.

    At ``tmg_rate() = 0`` the two things the notes call the TMG coincide: the art. A132-12
    subtraction of interest already credited, which belongs to a `taux technique` fixed at
    subscription, and the floor on the year's total revalorisation.  Above zero they are
    different quantities and a cell would have to choose, so none is shipped.
    """
    table = assurance_vie_euro.Data.model_point_table()
    assert (table["avance_on"] == 0).all() and (table["tmg_rate"] == 0.0).all()
    assert assurance_vie_euro.Projection[1].avance_on() is False
    for point_id in table.index:
        p = assurance_vie_euro.Projection[point_id]
        assert p.pb_min_pp(3) == pytest.approx(max(0.0, p.pb_acct_pp(3)), abs=1e-12)
        assert all(p.insurer_topup_pp(t) == 0.0 for t in (1, 10, 30))
        assert all(p.ts_net(t) == p.ts_raw(t) for t in (1, 10, 30))


# ---------------------------------------------------------------------------
# Structure, documentation and inputs


def test_result_cf_shape_and_both_signs_of_the_net_flow(fr_euro_anchor):
    """liability_cf is the notes' outgo-positive CF(t); net_cf is the library's sign.

    ``int_credited`` and ``soc_levy`` are published beside the flows and in neither: a
    state movement and a policyholder tax.  No subtotal is published beside its parts, and
    the enum accessors validate rather than propagating a typo into a lookup.
    """
    df = fr_euro_anchor.result_cf()
    assert list(df.index) == list(range(1, 41)) and df.index.name == "t"
    assert list(df.columns) == [
        "pols_if", "premiums", "withdrawals", "claims_death", "claims_lapse",
        "expenses", "int_credited", "soc_levy", "liability_cf", "net_cf",
    ]
    for absent in ("claims", "claims_surr", "claims_wd", "claims_maturity"):
        assert absent not in df.columns
    assert (df["net_cf"] + df["liability_cf"]).abs().max() == pytest.approx(0.0, abs=1e-9)
    with pytest.raises(FormulaError):
        fr_euro_anchor.av_pp_at(1, "AFT_LEVY")
    with pytest.raises(FormulaError):
        fr_euro_anchor.pols_if_at(1, "AFT_SURR")


def test_every_model_point_projects_and_every_check_holds(assurance_vie_euro):
    """The whole shipped table, and all seven invariants on each of its eleven rows."""
    ids = list(assurance_vie_euro.Data.model_point_table().index)
    assert len(ids) == 11
    columns = None
    for point_id in ids:
        p = assurance_vie_euro.Projection[point_id]
        df = p.result_cf()
        assert len(df) == 40 and df.notna().all().all(), point_id
        if columns is None:
            columns = list(df.columns)
        else:
            assert list(df.columns) == columns, point_id
        for name in CHECKS:
            assert getattr(p, name)() is True, (point_id, name)


def test_docstrings_carry_their_reference_material(assurance_vie_euro):
    """Specifics a reader would rely on, asserted so they cannot go stale silently."""
    doc = assurance_vie_euro.doc
    for phrase in ("mechanics demonstration", "external", "once per model",
                   "eight-year clock", "effet cliquet", "Prélèvements sociaux"):
        assert phrase in doc
    proj = assurance_vie_euro.Projection.doc
    assert "Notes symbol" in proj
    for cells in ("proj_len", "model_point", "av_pp_at", "ppb_vintage_pp",
                  "pm_avg_pp", "ts_net", "insurer_topup_pp", "lapse_dyn_add"):
        assert cells in proj
    data = assurance_vie_euro.Data.doc
    assert "TradLife_A" in data
    for cells in ("input_dir", "model_point_table", "fin_rate_table"):
        assert cells in data


def test_the_inputs_live_beside_the_model_and_mark_their_own_provenance():
    """Four external CSVs, none inside the model folder, each saying what it is.

    The statutory tables annexed to the arrêté du 1er août 2006 are cited in the documents
    and not redistributed here, so the shipped mortality table is INSEE-shaped and anchored
    so that ``mort_be_factor`` reproduces the notes' ``q = 0.0060`` at male age 60.
    """
    import pandas as pd

    assert {"model_point_table.csv", "mort_table.csv", "lapse_table.csv",
            "fin_rate_table.csv"} == {p.name for p in MODEL_DIR.parent.iterdir()
                                      if p.suffix == ".csv"}
    assert not list(MODEL_DIR.rglob("*.csv"))
    assert {p.name for p in MODEL_DIR.iterdir() if p.is_file()} == {
        "__init__.py", "_system.json"}
    mort = pd.read_csv(MODEL_DIR.parent / "mort_table.csv")
    assert set(mort["provenance"]) == {"[std] INSEE-shaped French population proxy"}
    assert mort["mort_rate"].max() <= 1.0
    q60 = mort[(mort["sex"] == "M") & (mort["age"] == 60)]["mort_rate"].iloc[0]
    assert q60 == pytest.approx(0.0075, rel=1e-12)
    assert 0.80 * q60 == pytest.approx(0.0060, rel=1e-12)
    assert mort[(mort["sex"] == "F") & (mort["age"] == 120)]["mort_rate"].iloc[0] == 1.0
    lapse = pd.read_csv(MODEL_DIR.parent / "lapse_table.csv")
    assert all(v.startswith("[std]") for v in lapse["provenance"])
    assert lapse[lapse["policy_duration"] == 8]["lapse_rate_base"].iloc[0] == 0.08
    fin = pd.read_csv(MODEL_DIR.parent / "fin_rate_table.csv")
    assert all(v.startswith("[std]") for v in fin["provenance"])
    assert set(fin["scenario_id"]) == {"base", "low", "high"}
    assert (fin["ref_rate"] == 0.0220).all()


def test_an_input_can_be_swapped_without_touching_formulas():
    """This is what a production user does with a permitted TGH05/TGF05 basis."""
    import pandas as pd

    lighter = pd.read_csv(MODEL_DIR.parent / "mort_table.csv", index_col=["sex", "age"])
    lighter["mort_rate"] = lighter["mort_rate"] * 0.5
    model = mx.read_model(MODEL_DIR, name="Euro_FR_A_swap")
    try:
        alt_name = "mort_table_light.csv"
        lighter.to_csv(model.Data.input_dir() / alt_name)
        try:
            base = model.Projection[1].result_cf()["claims_death"].sum()
            model.Data.mort_table_file = alt_name
            model.Data.clear_all()
            model.Projection.clear_all()
            # Lighter mortality means fewer deaths and later releases of the account.
            assert model.Projection[1].result_cf()["claims_death"].sum() < base
        finally:
            (model.Data.input_dir() / alt_name).unlink(missing_ok=True)
    finally:
        model.close()


def test_round_trip_is_stable(tmp_path):
    """read -> write -> re-read reproduces the goldens and the same file set."""
    import shutil

    model = mx.read_model(MODEL_DIR, name="Euro_FR_A_rt_src")
    try:
        dest = tmp_path / MODEL_DIR.name
        mx.write_model(model, str(dest), backup=False)
    finally:
        model.close()

    for csv in MODEL_DIR.parent.glob("*.csv"):
        shutil.copy(csv, tmp_path / csv.name)

    reread = mx.read_model(dest, name="Euro_FR_A_rt")
    try:
        p = reread.Projection[1]
        for t, row in TABLE_2.items():
            assert p.av_pp(t) == pytest.approx(row[0], abs=CENT)
            assert p.int_credited_pp(t) == pytest.approx(row[3], abs=CENT)
            assert p.soc_levy_pp(t) == pytest.approx(row[4], abs=CENT)
        assert p.ppb_pp(9) == pytest.approx(0.0, abs=CENT)
        assert "Notes symbol" in reread.Projection.doc
    finally:
        reread.close()

    assert model_files(dest) == model_files(MODEL_DIR)
