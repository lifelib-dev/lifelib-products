"""Golden and structural tests for TermLifeUS.

The golden values are the worked example in us/products/term-life/technical-notes.md
("Worked example"), which projects the specimen anchor cell M35 / StdNT / $100,000 /
10-year plan / annual mode.  They are hard-coded here rather than pickled so that a
reviewer can compare them against the notes by eye.

Tolerances follow the precision the notes display: money to the cent, in-force to six
decimals.
"""
import modelx as mx
import pytest

from conftest import MODELS, REPO

CENT = 0.005          # money displayed to 2 d.p.
INFORCE = 5e-7        # in-force displayed to 6 d.p.

# t: (l(t), G, DC, K, E, X, NetCF, l(t+1))
WORKED_EXAMPLE = {
    1:  (1.000000, 140.00,  80.00, 112.00, 330.00, 2.80, -384.80, 0.939248),
    2:  (0.939248, 131.49,  79.84,   6.57,  28.74, 2.63,   13.71, 0.891527),
    3:  (0.891527, 124.81,  80.24,   6.24,  27.83, 2.50,    8.01, 0.855096),
    4:  (0.855096, 119.71,  81.23,   5.99,  27.22, 2.39,    2.88, 0.820112),
    5:  (0.820112, 114.82,  82.01,   5.74,  26.63, 2.30,   -1.86, 0.786520),
    6:  (0.786520, 110.11,  86.52,   5.51,  26.05, 2.20,  -10.16, 0.754229),
    7:  (0.754229, 105.59,  90.51,   5.28,  25.48, 2.11,  -17.79, 0.723191),
    8:  (0.723191, 101.25,  94.01,   5.06,  24.92, 2.02,  -24.78, 0.693361),
    9:  (0.693361,  97.07, 100.54,   4.85,  24.37, 1.94,  -34.63, 0.650814),
    10: (0.650814,  91.11, 104.13,   4.56,  23.33, 1.82,  -42.73, 0.129955),
    11: (0.129955,  99.29,  81.87,   1.99,   4.75, 1.99,    8.69, 0.090395),
    12: (0.090395,  75.03,  60.56,   1.50,   3.37, 1.50,    8.09, 0.076321),
}


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE))
def test_worked_example_row(anchor, t):
    """Every cell of the notes' 12-row table, to the displayed precision."""
    l_t, g, dc, k, e, x, net, l_next = WORKED_EXAMPLE[t]
    assert anchor.l(t) == pytest.approx(l_t, abs=INFORCE)
    assert anchor.G(t) == pytest.approx(g, abs=CENT)
    assert anchor.DC(t) == pytest.approx(dc, abs=CENT)
    assert anchor.K(t) == pytest.approx(k, abs=CENT)
    assert anchor.E(t) == pytest.approx(e, abs=CENT)
    assert anchor.X_tax(t) == pytest.approx(x, abs=CENT)
    assert anchor.NetCF(t) == pytest.approx(net, abs=CENT)
    assert anchor.l(t + 1) == pytest.approx(l_next, abs=INFORCE)


def test_shock_lapse_collapse(anchor):
    """The notes' headline check: l(11) = l(10)(1-0.0016)(1-0.80) = 0.129955."""
    assert anchor.l(10) * (1 - 0.0016) * (1 - 0.80) == pytest.approx(0.129955, abs=INFORCE)
    assert anchor.l(11) == pytest.approx(0.129955, abs=INFORCE)
    assert anchor.shock_lapse() == 0.80
    assert anchor.w(10) == 0.80


def test_jump_ratio(anchor):
    """J = AP(11)/AP(10) = 764/140, fee included in both."""
    assert anchor.AP(10) == 140.0
    assert anchor.AP(11) == 764.0
    assert anchor.J() == pytest.approx(764.0 / 140.0, rel=1e-12)


def test_m1_formula_diverges_from_the_pinned_fixture(term_life):
    """Documented divergence: the rule gives 3.4514, the worked example pins 3.50.

    Point 1 carries m1_override = 3.50 so the golden table reproduces; point 2 is
    otherwise identical and leaves the override blank, taking the formula.  Neither is
    "correct" - both are standardizations, and the test exists so the gap cannot be
    closed silently in either direction.
    """
    p1, p2 = term_life.Projection[1], term_life.Projection[2]
    assert p1.M1_formula() == pytest.approx(3.4514, abs=5e-5)
    assert p1.M1() == 3.50                      # the pin the worked example uses
    assert p2.M1() == pytest.approx(3.4514, abs=5e-5)   # the formula path
    assert p1.M1() != pytest.approx(p2.M1(), abs=1e-3)


def test_plt_multiplier_grades_to_two(anchor):
    """M(d) = max(2.0, M(1) - 0.15(d-1)); reaches the 2.00 floor at d = 11."""
    assert anchor.M_plt(1) == 3.50
    assert anchor.M_plt(2) == pytest.approx(3.35)
    assert anchor.M_plt(11) == pytest.approx(2.00)
    assert anchor.M_plt(12) == 2.00             # level thereafter
    assert anchor.M_plt(30) == 2.00


def test_decrement_identity(anchor):
    """The roll-forward closes: l(t) - l(t+1) = deaths + lapses + conversions + expiry.

    `expiry` is non-zero only in the final policy year, where coverage ends at attained
    age 95.  That is not a decrement - the contract runs out - but without it in the
    identity the last year appears to lose lives with no cause.
    """
    for t in range(1, anchor.max_t() + 1):
        out = anchor.d_death(t) + anchor.x(t) + anchor.c(t) + anchor.expiry(t)
        assert anchor.l(t) - anchor.l(t + 1) == pytest.approx(out, abs=1e-12)


def test_expiry_is_confined_to_the_final_year(anchor):
    for t in range(1, anchor.max_t()):
        assert anchor.expiry(t) == 0.0
    assert anchor.expiry(anchor.max_t()) > 0.0


def test_inforce_is_a_decreasing_probability(anchor):
    for t in range(1, anchor.max_t() + 2):
        assert 0.0 <= anchor.l(t) <= 1.0
        assert anchor.l(t + 1) <= anchor.l(t) + 1e-15


def test_expiry_at_attained_age_95(anchor):
    """Policy year 60 is the last for issue age 35; nothing survives past it."""
    assert anchor.max_t() == 60
    assert anchor.attained_age(60) == 94        # age at the start of the final year
    assert anchor.l(60) > 0.0
    assert anchor.l(61) == 0.0
    assert anchor.phase(61) == "EXPIRED"


def test_phase_switches_at_the_level_period_end(anchor):
    assert anchor.phase(10) == "LEVEL"
    assert anchor.phase(11) == "PLT"


def test_conversion_is_off_in_the_base_run(anchor):
    """The worked example sets cv = 0; the eligibility window is still modelled."""
    assert anchor.cv(5) == 0.0
    assert all(anchor.CV(t) == 0.0 for t in range(1, 13))
    assert anchor.conv_elig(10) is True         # within level period, age 44 < 70
    assert anchor.conv_elig(11) is False        # level period over


def test_result_cf_shape(anchor):
    df = anchor.result_cf()
    assert list(df.index) == list(range(1, anchor.max_t() + 1))
    assert set(df.columns) == {
        "l", "premium_G", "claims_DC", "commission_K", "expense_E",
        "premium_tax_X", "conv_credit_CV", "net_cf",
    }
    assert df.loc[1, "net_cf"] == pytest.approx(-384.80, abs=CENT)


def test_no_pickled_inputs():
    """Inputs are CSV-only; _data/ may contain iospecs.py and nothing else."""
    folder = REPO / MODELS["TermLifeUS"][0]
    assert not list(folder.rglob("*.pickle"))
    assert sorted(p.name for p in (folder / "_data").iterdir()) == ["iospecs.py"]


def test_round_trip_is_stable(tmp_path):
    """read -> write -> re-read reproduces the goldens and the same file set."""
    src = REPO / MODELS["TermLifeUS"][0]
    model = mx.read_model(src)
    try:
        dest = tmp_path / "TermLifeUS"
        mx.write_model(model, str(dest))
    finally:
        model.close()

    reread = mx.read_model(dest, name="TermLifeUS_rt")
    try:
        anchor = reread.Projection[1]
        for t, row in WORKED_EXAMPLE.items():
            assert anchor.l(t) == pytest.approx(row[0], abs=INFORCE)
            assert anchor.NetCF(t) == pytest.approx(row[6], abs=CENT)
    finally:
        reread.close()

    written = {p.name for p in dest.rglob("*") if p.is_file()}
    committed = {p.name for p in src.rglob("*") if p.is_file()}
    assert written == committed
