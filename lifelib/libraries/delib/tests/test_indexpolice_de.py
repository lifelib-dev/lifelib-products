"""Golden and structural tests for Index_DE_A, the German *Indexpolice*.

The golden values are the worked example in
``products/indexpolice/technical-notes.md`` ("Worked example"), which is a
**configuration** and not a scenario: model point 1, ``policy_id = "DE-IDX-0001"``, a male
aged 40 last birthday writing an *indexgebundene Rentenversicherung* to *Rentenbeginn* at
67, so ``proj_len() = 67 - 40 = 27``.  It is new business -- ``dur_init = 0``, hence
``t_start() = 1``, ``pols_if_init = 1.0``, ``av_pp_init = guar_locked_init =
prem_paid_init = 0`` -- which makes the notes' twenty-seven-row table the **entire**
projection rather than a slice of one, so every row of it is asserted here.

The cell in full: a level *Beitrag* of 2 400,00 EUR a year (the research file's 200,00 EUR
a month taken annually) payable for all 27 years, ``prem_freq = annual`` so
``freq_load() = 1.000`` and the premium collected equals the premium due, giving a
*Beitragssumme* of ``27 x 2 400,00 = 64 800,00 EUR``; ``guar_level = 0.90``, a
*Beitragsgarantie* of 58 320,00 EUR at *Rentenbeginn* plus every locked-in credit;
``guar_rate = 0.0100``, the *Hoechstrechnungszins* for 2025-2026; ``payoff_form = "cap"``,
the monthly-Cap design; ``index_id = "eqidx_vol17"``, a broad equity price index at a
3,00 % monthly Cap whose *Indexjahre* at ``t = 9`` and ``t = 10`` are the research file's
constructed Example A and Example B; ``elect_id = "always_index"``, so ``w(t) = 1.00`` in
every one of the 27 years and the *sichere Verzinsung* arm is never used;
``death_min_rate = 0.50``, a *Mindesttodesfallschutz* floor of 32 400,00 EUR;
``ann_option = "annuity"``; and ``surr_charge_on = 1``.

Goldens are hard-coded rather than pickled so a reviewer can compare them against the
notes by eye.  Tolerances follow the precision the notes display: money to the cent,
``pols_if`` to six decimals, and the totals at **full precision** -- 3 780,63 EUR of death
claims that way against 3 780,62 EUR if the twenty-seven rounded cells are added, and the
same one-cent split on ``expenses`` and on ``net_cf``.

What this module asserts: every row of the notes' table and the Total row at full
precision; the notes' six independent checks (policy year 1 rebuilt end to end, the
*Indexjahr* of year 9 rebuilt on its own terms, the three-way decrement closure, the
fund-level account roll-forward at ``t = 9``, the cash flow statement closing on the Total
row, and the guarantee at *Rentenbeginn*); the *Partizipationsquote* variant on the
identical index path, with its printed rows, its totals and the four designs at
*Rentenbeginn*; **one test per numbered modeling pitfall**, each named for its pitfall and
each asserting the specific way an implementation of *this* product looks right and is
wrong; the product's own invariants and each of the six ``check_*()`` identities with its
per-``t`` residual, ``check_net_cf()`` among them, which is delib's first ruling; and the
frame's shape, the enum accessors, the docstrings, the shared vocabulary, the shipped
tables' own provenance, an input swapped without touching a formula, and a round trip.

There is deliberately **no sweep of the whole model point table** here: the conventions
suite owns the single sweep, a model point's first evaluation being the most expensive
thing in the run.
"""
import modelx as mx
import pytest
from modelx.core.errors import FormulaError

from de_registry import MODELS, LIB


def model_files(folder):
    """The model's own file names, ignoring the ``__pycache__`` an import leaves behind:
    those caches are not part of the model and must not fail a round-trip comparison."""
    return {p.name for p in folder.rglob("*")
            if p.is_file() and "__pycache__" not in p.parts}


CENT = 0.005          # money displayed to 2 d.p.
SIX_DP = 0.0000005    # pols_if displayed to 6 d.p.

MODEL_DIR = LIB / MODELS["Index_DE_A"][0]

# The eight external CSVs the model reads, all in the model folder's parent.
INPUT_CSVS = {
    "model_point_table.csv", "index_return_table.csv", "index_param_table.csv",
    "surplus_rate_table.csv", "election_table.csv", "mort_table.csv",
    "lapse_table.csv", "freq_load_table.csv",
}

# The notes' worked-example table, in full.
# t: (x(t), pols_if, premiums, claims_death, claims_lapse, claims_maturity,
#     expenses, guar_int, index_credit, av, net_cf)
# surplus_credit is 0.00 at every t on this cell and liability_cf is exactly -net_cf; both
# are omitted from the notes' printed table for width and are asserted in the row test.
WORKED_EXAMPLE = {
    1:  (40, 1.000000, 2400.00,  38.88,   98.81,     0.00, 1656.00,  19.99,    0.00,     0.00,    606.31),
    2:  (41, 0.948860, 2277.26,  40.40,  188.20,     0.00,   34.67,  38.08,   81.79,  1915.73,   2014.00),
    3:  (42, 0.900233, 2160.56,  41.97,  163.70,     0.00,   33.39,  55.21,  186.81,  3730.48,   1921.51),
    4:  (43, 0.871969, 2092.73,  44.51,  216.92,     0.00,   32.82,  73.17, 1204.06,  5587.67,   1798.47),
    5:  (44, 0.844477, 2026.75,  47.20,  297.26,     0.00,   32.27, 100.28,    0.00,  8360.99,   1650.01),
    6:  (45, 0.817730, 1962.55,  50.05,  346.23,     0.00,   31.71, 116.82,   41.78,  9807.67,   1534.56),
    7:  (46, 0.791700, 1900.08,  53.06,  393.37,     0.00,   31.16, 132.75,    0.00, 11465.08,   1422.49),
    8:  (47, 0.766360, 1839.26,  56.24,  436.27,     0.00,   30.62, 147.26,    0.00, 12978.50,   1316.13),
    9:  (48, 0.741686, 1780.05,  59.60,  476.31,     0.00,   30.08, 160.80, 1239.56, 14394.07,   1214.06),
    10: (49, 0.717651, 1722.36,  63.15,  550.17,     0.00,   29.54, 185.79,    0.00, 16954.47,   1079.50),
    11: (50, 0.694231, 1666.15,  66.89,  583.79,     0.00,   29.00, 197.19,    0.00, 18152.02,    986.47),
    12: (51, 0.671401, 1611.36,  70.84, 1229.59,     0.00,   28.47, 207.72,    0.00, 19261.02,    282.46),
    13: (52, 0.629062, 1509.75,  75.88,  415.58,     0.00,   27.08, 210.68,  823.46, 19656.70,    991.21),
    14: (53, 0.614282, 1474.28,  90.60,  453.04,     0.00,   26.84, 229.75,    0.00, 21602.56,    903.80),
    15: (54, 0.599646, 1439.15, 103.58,  472.83,     0.00,   26.59, 239.88,    0.00, 22651.89,    836.15),
    16: (55, 0.585141, 1404.34, 117.93,  491.43,     0.00,   26.34, 249.41,    0.00, 23641.56,    768.64),
    17: (56, 0.570753, 1369.81, 133.76,  508.81,     0.00,   26.07, 258.35,    0.00, 24571.29,    701.16),
    18: (57, 0.556471, 1335.53, 151.20,  524.98,     0.00,   25.80, 266.69,    0.00, 25440.64,    633.55),
    19: (58, 0.542280, 1301.47, 170.37,  539.92,     0.00,   25.52, 274.43,    0.00, 26249.06,    565.67),
    20: (59, 0.528168, 1267.60, 191.39,  553.60,     0.00,   25.23, 281.55,    0.00, 26995.84,    497.38),
    21: (60, 0.514121, 1233.89, 214.41,  566.02,     0.00,   24.93, 288.05,    0.00, 27680.11,    428.53),
    22: (61, 0.500125, 1200.30, 239.56,  577.14,     0.00,   24.61, 293.91,    0.00, 28300.85,    358.99),
    23: (62, 0.486168, 1166.80, 266.98,  586.94,     0.00,   24.29, 299.14,    0.00, 28856.92,    288.59),
    24: (63, 0.472234, 1133.36, 296.81,  595.39,     0.00,   23.94, 303.70,    0.00, 29346.98,    217.22),
    25: (64, 0.458311, 1099.95, 329.17,  602.46,     0.00,   23.59, 307.59,    0.00, 29769.58,    144.73),
    26: (65, 0.444386, 1066.53, 364.19,  608.12,     0.00,   23.21, 310.80,    0.00, 30123.10,     71.00),
    27: (66, 0.430446, 1033.07, 402.00,    0.00, 31240.67,   22.82, 313.29,    0.00, 30405.82, -30632.42),
}

# The notes' Total row: summed at full precision and then rounded.  Three of the eight
# differ from the rounded-cell sum by one cent, and the test below asserts both.
TOTALS = {
    "premiums": 42474.94, "claims_death": 3780.63, "claims_lapse": 12476.88,
    "claims_maturity": 31240.67, "expenses": 2376.60, "guar_int": 5562.28,
    "surplus_credit": 0.00, "index_credit": 3577.46, "net_cf": -7399.84,
}

# The twelve monthly returns of the two Indexjahre the mechanic turns on, in per cent,
# straight from the research file: eqidx_vol17 rows t = 9 and t = 10.
EXAMPLE_A = (1.80, -2.40, 4.60, 0.90, -3.70, 2.20, 3.40, -1.10, 0.40, 5.20, -0.80, 2.60)
EXAMPLE_B = (6.50, -2.10, 5.80, -1.90, -2.40, 4.20, -3.10, 0.60, -2.80, 5.10, -1.70, -1.20)

# t: (index_sum S(t), index_return_year Y(t), index_credit_rate rho(t)) on the anchor --
# the years that credit something, plus the four that most sharply separate S from Y.
INDEXJAHR = {
    1:  (0.1204, 0.195591, 0.1204),
    2:  (0.0450, 0.126362, 0.0450),
    3:  (0.0517, 0.209523, 0.0517),
    4:  (0.2225, 0.592280, 0.2225),
    5:  (-0.0868, -0.031740, 0.0000),
    6:  (0.0044, 0.028913, 0.0044),
    9:  (0.0890, 0.134548, 0.0890),
    10: (-0.0260, 0.064402, 0.0000),
    11: (-0.0122, 0.080888, 0.0000),
    13: (0.0429, 0.064102, 0.0429),
    16: (-0.1114, 0.100909, 0.0000),
    27: (-0.2139, -0.168146, 0.0000),
}

# The Partizipationsquote variant -- model point 2, the anchor with payoff_form = "quote"
# and nothing else changed, so both designs run against the same twelve monthly returns.
# t: (pols_if, premiums, claims_death, claims_lapse, claims_maturity, expenses,
#     guar_int, index_credit, av, net_cf)
QUOTE_VARIANT = {
    1:  (1.000000, 2400.00,  38.88,  98.81,     0.00, 1656.00,  19.99,    0.00,     0.00,    606.31),
    4:  (0.871969, 2092.73,  44.51, 226.65,     0.00,   32.82,  76.45, 2036.27,  5916.59,   1788.74),
    9:  (0.741686, 1780.05,  59.60, 511.12,     0.00,   30.08, 172.56, 1216.40, 15572.35,   1179.24),
    10: (0.717651, 1722.36,  63.15, 583.42,     0.00,   29.54, 197.01,  675.83, 18079.93,   1046.25),
    13: (0.629062, 1509.75,  84.90, 465.03,     0.00,   27.08, 235.75,  832.65, 22169.87,    932.74),
    27: (0.430446, 1033.07, 538.84,   0.00, 41875.02,   22.82, 419.94,    0.00, 41097.09, -41403.61),
}

QUOTE_TOTALS = {
    "premiums": 42474.94, "claims_death": 4636.36, "claims_lapse": 14723.29,
    "claims_maturity": 41875.02, "expenses": 2376.60, "guar_int": 6712.41,
    "surplus_credit": 0.00, "index_credit": 16521.86, "net_cf": -21136.33,
}

# The notes' "four designs at Rentenbeginn" table.  Every column is per policy at
# t = n + 1, so the credit columns are the ledger credit_cum_pp(n+1) and are larger than
# the frame's fund-level totals, which carry the decrements.
# point_id: (index credits, safe-arm credits, account, guaranteed capital, benefit,
#            monthly Rente, index_budget_ratio)
DESIGNS = {
    1:  (4851.44,      0.00,  73511.39, 63171.44,  73511.39, 183.78, 0.2082),
    2:  (28216.23,     0.00,  98534.74, 86536.23,  98534.74, 246.34, 0.9782),
    3:  (46118.84,     0.00, 116178.75, 104438.84, 116178.75, 290.45, 1.6482),
    11: (0.00,     25967.50,  95425.52, 84287.50,  95425.52, 238.56, 0.0000),
}


# --- The worked example ----------------------------------------------------


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE))
def test_worked_example_row(de_index_anchor, t):
    """Every cell of the notes' twenty-seven-row table, to the displayed precision.

    ``surplus_credit`` and ``liability_cf`` are omitted from the notes' printed table for
    width and are asserted anyway: zero on a cell that elects the index arm every year, and
    the sign convention made verifiable in the frame.
    """
    (age, pols_if, prem, cd, cl, cm, exp, gi, ic, av, net) = WORKED_EXAMPLE[t]
    p = de_index_anchor
    assert p.age(t) == age
    assert p.pols_if(t) == pytest.approx(pols_if, abs=SIX_DP)
    assert p.premiums(t) == pytest.approx(prem, abs=CENT)
    assert p.claims(t, "DEATH") == pytest.approx(cd, abs=CENT)
    assert p.claims(t, "LAPSE") == pytest.approx(cl, abs=CENT)
    assert p.claims(t, "MATURITY") == pytest.approx(cm, abs=CENT)
    assert p.expenses(t) == pytest.approx(exp, abs=CENT)
    assert p.guar_int(t) == pytest.approx(gi, abs=CENT)
    assert p.index_credit(t) == pytest.approx(ic, abs=CENT)
    assert p.av(t) == pytest.approx(av, abs=CENT)
    assert p.net_cf(t) == pytest.approx(net, abs=CENT)
    assert p.surplus_credit(t) == 0.0
    assert p.liability_cf(t) == pytest.approx(-net, abs=CENT)
    # The same row, read off the published frame rather than off the cells.
    row = p.result_cf().loc[t]
    assert row["pols_if"] == pytest.approx(pols_if, abs=SIX_DP)
    assert row["claims_death"] == pytest.approx(cd, abs=CENT)
    assert row["net_cf"] == pytest.approx(net, abs=CENT)


def test_the_worked_example_totals_are_summed_at_full_precision(de_index_anchor):
    """The Total row is a full-precision sum, then rounded -- not a sum of rounded cells.

    Three of the eight differ from the rounded-cell sum by one cent; a test written against
    the rounded column fails on all three and looks like a modelling error, so both are
    asserted here and the difference is on the record.
    """
    df = de_index_anchor.result_cf()
    for column, total in TOTALS.items():
        assert df[column].sum() == pytest.approx(total, abs=CENT), column
    rounded = {c: sum(round(WORKED_EXAMPLE[t][i], 2) for t in WORKED_EXAMPLE)
               for c, i in (("claims_death", 3), ("expenses", 6), ("net_cf", 10))}
    assert rounded["claims_death"] == pytest.approx(3780.62, abs=CENT)
    assert rounded["expenses"] == pytest.approx(2376.59, abs=CENT)
    assert rounded["net_cf"] == pytest.approx(-7399.83, abs=CENT)
    # The av column is deliberately not totalled: it is a balance, and adding twenty-seven
    # opening balances together is not a quantity.
    assert df["av"].iloc[0] == 0.0
    assert df["av"].iloc[-1] == pytest.approx(30405.82, abs=CENT)


def test_check_one_policy_year_one_rebuilt_from_scratch(de_index_anchor):
    """The notes' first check: row 1 rebuilt end to end, nothing read from the frame."""
    p = de_index_anchor
    assert p.prem_sum() == 64800.0 and p.freq_load() == 1.0
    assert p.prem_gross_pp(1) == pytest.approx(2400.00, abs=CENT)
    assert p.prem_charge_acq_pp(1) == pytest.approx(0.025 * 64800.0 / 5, abs=CENT)
    assert p.prem_charge_acq_pp(1) == pytest.approx(324.00, abs=CENT)
    assert p.prem_charge_adm_pp(1) == pytest.approx(0.03 * 2400.00, abs=CENT)
    assert p.prem_to_av_pp(1) == pytest.approx(2400.00 - 324.00 - 72.00, abs=CENT)
    assert p.av_pp_at(1, "BEF_PREM") == 0.0
    assert p.av_pp_at(1, "AFT_PREM") == pytest.approx(2004.00, abs=CENT)
    assert p.av_charge_pp(1) == pytest.approx(0.0025 * 2004.00, abs=CENT)
    assert p.av_pp_at(1, "AFT_CHARGE") == pytest.approx(1998.99, abs=CENT)
    assert p.guar_int_pp(1) == pytest.approx(0.01 * 1998.99, rel=1e-12)
    assert p.guar_int(1) == pytest.approx(19.9899, abs=5e-5)
    assert p.av_pp_at(1, "AFT_GUAR") == pytest.approx(2018.9799, abs=5e-5)
    # Decrements: q_d(1) is the proxy's own anchor, then surrender on the survivors.
    assert p.mort_rate(1) == 0.001200 and p.lapse_rate(1) == 0.05
    assert p.pols_death(1) == pytest.approx(0.001200, rel=1e-12)
    assert p.pols_lapse(1) == pytest.approx(0.05 * (1 - 0.001200), rel=1e-12)
    assert p.pols_if(2) == pytest.approx(0.948860, abs=SIX_DP)
    # Benefits: the Mindesttodesfallschutz floor dominates the account in year 1.
    assert p.db_pp(1) == pytest.approx(0.50 * 64800.0, abs=CENT)
    assert p.claims(1, "DEATH") == pytest.approx(32400.00 * 0.001200, abs=CENT)
    assert p.cv_pp(1) == pytest.approx(2018.9799 * 0.98, abs=5e-4)
    assert p.claims(1, "LAPSE") == pytest.approx(1978.6003 * 0.049940, abs=5e-4)
    assert p.expenses(1) == pytest.approx(1620.00 + 36.00, abs=CENT)
    assert p.net_cf(1) == pytest.approx(2400.00 - 38.88 - 98.81 - 0.0 - 1656.00, abs=CENT)


def test_check_two_the_indexjahr_of_year_nine_rebuilt_on_its_own_terms(de_index_anchor):
    """The notes' second check: Example A, rebuilt from its twelve monthly returns.

    ``S(9) = +8,90 %`` is positive, so ``rho(9) = 8,90 %`` on the **opening** balance, to
    the survivors of both decrements.  Compounding the same twelve capped returns gives
    8,9599 %, and the raw year return is +13,4548 % against a raw sum of +13,10 %.
    """
    p = de_index_anchor
    monthly = [p.index_return(9, m) for m in range(1, 13)]
    capped = [p.index_return_capped(9, m) for m in range(1, 13)]
    assert monthly == pytest.approx([r / 100.0 for r in EXAMPLE_A], abs=1e-12)
    assert capped == pytest.approx([min(r / 100.0, 0.03) for r in EXAMPLE_A], abs=1e-12)
    assert sum(monthly) == pytest.approx(0.1310, abs=1e-12)
    assert p.index_sum(9) == pytest.approx(0.0890, abs=1e-12)
    assert p.index_credit_rate(9) == pytest.approx(0.0890, abs=1e-12)
    assert p.index_base_pp(9) == pytest.approx(19407.2450, abs=5e-5)
    assert p.index_credit_pp(9) == pytest.approx(0.0890 * 19407.2450, abs=5e-4)
    assert p.index_credit_pp(9) == pytest.approx(1727.2448, abs=5e-4)
    assert p.pols_if_at(9, "AFT_LAPSE") == pytest.approx(0.717651, abs=SIX_DP)
    assert p.index_credit(9) == pytest.approx(1727.2448 * 0.717651, abs=1e-3)
    assert p.index_credit(9) == pytest.approx(1239.56, abs=CENT)
    compounded_capped = 1.0
    for x in capped:
        compounded_capped *= (1.0 + x)
    assert compounded_capped - 1.0 == pytest.approx(0.089599, abs=5e-7)
    assert p.index_return_year(9) == pytest.approx(0.134548, abs=5e-7)
    # The cap bound in exactly three months and cost 4,20 points.
    assert sum(1 for m in range(1, 13) if p.index_return(9, m) > 0.03) == 3
    assert sum(monthly) - p.index_sum(9) == pytest.approx(0.0420, abs=1e-12)


def test_check_three_the_decrements_close_three_ways(de_index_anchor):
    """The notes' third check: deaths, surrenders and maturities sum to exactly one, by
    direct summation over the exit cells with no reference to the recursion that produced
    ``pols_if`` -- which is what catches a life that leaves twice or never leaves."""
    p = de_index_anchor
    n = p.proj_len()
    deaths = sum(p.pols_death(t) for t in range(1, n + 1))
    lapses = sum(p.pols_lapse(t) for t in range(1, n + 1))
    mats = sum(p.pols_maturity(t) for t in range(1, n + 1))
    assert deaths == pytest.approx(0.074584, abs=5e-7)
    assert lapses == pytest.approx(0.500439, abs=5e-7)
    assert mats == pytest.approx(0.424977, abs=5e-7)
    assert deaths + lapses + mats == pytest.approx(1.0, abs=1e-12)
    assert p.pols_if(n + 1) == 0.0
    assert p.pols_maturity(n) == pytest.approx(p.pols_if_at(n, "AFT_LAPSE"), rel=1e-12)
    assert all(p.pols_maturity(t) == 0.0 for t in range(1, n))
    assert p.check_pols_roll_fwd() is True


def test_check_four_the_account_rolls_forward_at_year_nine(de_index_anchor):
    """The notes' fourth check: the fund-level roll-forward at ``t = 9``, term by term.

    Every term is on a **different population** -- premium, charge and guaranteed interest
    on the opening in-force, the credit on the survivors, ``av_released`` on the exits at
    the balance they left with, which is what they take out and not what they are paid.
    """
    p = de_index_anchor
    assert p.av(9) == pytest.approx(14394.0730, abs=5e-4)
    assert p.prem_to_av_pp(9) == pytest.approx(2328.00, abs=CENT)
    assert p.prem_to_av(9) == pytest.approx(2328.00 * p.pols_if(9), rel=1e-12)
    assert p.prem_to_av(9) == pytest.approx(1726.6439, abs=5e-4)
    assert p.av_charge(9) == pytest.approx(40.3018, abs=5e-4)
    assert p.guar_int(9) == pytest.approx(160.8042, abs=5e-4)
    assert p.surplus_credit(9) == 0.0
    assert p.index_credit(9) == pytest.approx(1239.5583, abs=5e-4)
    assert p.av_pp_at(9, "AFT_GUAR") == pytest.approx(21897.7159, abs=5e-4)
    assert p.av_released(9) == pytest.approx(
        p.av_pp_at(9, "AFT_GUAR") * (p.pols_death(9) + p.pols_lapse(9)), rel=1e-12)
    assert p.av_released(9) == pytest.approx(526.3103, abs=5e-4)
    assert p.av(10) == pytest.approx(
        p.av(9) + p.prem_to_av(9) - p.av_charge(9) + p.guar_int(9)
        + p.surplus_credit(9) + p.index_credit(9) - p.av_released(9), abs=1e-9)
    assert p.av(10) == pytest.approx(16954.4673, abs=5e-4)
    assert p.check_av_roll_fwd() is True


def test_check_five_the_cash_flow_statement_closes_on_the_total_row(de_index_anchor):
    """The notes' fifth check: ``42 474,94 - 3 780,63 - 12 476,88 - 31 240,67 - 2 376,60
    = -7 399,84``, and adding the guaranteed interest and the index credits would move
    ``net_cf`` by 9 139,74 EUR."""
    p = de_index_anchor
    df = p.result_cf()
    outgo = (df["claims_death"] + df["claims_lapse"] + df["claims_maturity"]
             + df["expenses"])
    assert (df["premiums"] - outgo - df["net_cf"]).abs().max() == pytest.approx(
        0.0, abs=1e-9)
    assert df["net_cf"].sum() == pytest.approx(-7399.842410, abs=5e-5)
    assert df["premiums"].sum() - outgo.sum() == pytest.approx(-7399.842410, abs=5e-5)
    assert df["guar_int"].sum() + df["index_credit"].sum() == pytest.approx(
        9139.74, abs=CENT)
    assert p.check_net_cf() is True


def test_check_six_the_guarantee_at_rentenbeginn(de_index_anchor):
    """The notes' sixth check: the ledger, the *Beitragsgarantie* and what falls due.

    4 851,4383 EUR of credits plus a 58 320,00 EUR *Beitragsgarantie* gives a guaranteed
    capital of 63 171,4383 EUR; the account stands above it, so the floor does **not** bind
    and the maturity is the account.  The monthly *Rente* is reported, never paid.
    """
    p = de_index_anchor
    n = p.proj_len()
    assert p.credit_cum_pp(n + 1) == pytest.approx(4851.4383, abs=5e-4)
    assert p.credit_cum_pp(n + 1) == pytest.approx(
        sum(p.index_credit_pp(t) for t in range(1, n + 1)), rel=1e-12)
    assert p.prem_paid_pp(n + 1) == pytest.approx(64800.0, abs=CENT)
    assert p.guar_floor_pp(n + 1) == pytest.approx(0.90 * 64800.0, abs=CENT)
    assert p.guar_cap_pp(n + 1) == pytest.approx(63171.4383, abs=5e-4)
    assert p.av_pp(n + 1) == pytest.approx(73511.3936, abs=5e-4)
    assert p.av_pp(n + 1) > p.guar_cap_pp(n + 1)          # the floor does not bind here
    assert p.mat_pp(n) == pytest.approx(73511.39, abs=CENT)
    assert p.pols_maturity(n) == pytest.approx(0.424977, abs=SIX_DP)
    assert p.claims(n, "MATURITY") == pytest.approx(
        p.mat_pp(n) * p.pols_maturity(n), rel=1e-12)
    assert p.claims(n, "MATURITY") == pytest.approx(31240.67, abs=CENT)
    assert p.rentenfaktor() == 25.0
    assert p.ann_monthly_pp() == pytest.approx(73511.3936 / 10000.0 * 25.0, abs=5e-4)
    assert p.ann_monthly_pp() == pytest.approx(183.78, abs=CENT)


# --- The Partizipationsquote variant, and the four designs -----------------


@pytest.mark.parametrize("t", sorted(QUOTE_VARIANT))
def test_the_partizipationsquote_variant_row(indexpolice, t):
    """Model point 2 is the anchor with ``payoff_form = "quote"`` and nothing else changed,
    so both designs run against the **same** twelve monthly returns in every year."""
    (pols_if, prem, cd, cl, cm, exp, gi, ic, av, net) = QUOTE_VARIANT[t]
    p = indexpolice.Projection[2]
    assert p.payoff_form() == "quote" and p.index_id() == "eqidx_vol17"
    assert p.pols_if(t) == pytest.approx(pols_if, abs=SIX_DP)
    assert p.premiums(t) == pytest.approx(prem, abs=CENT)
    assert p.claims(t, "DEATH") == pytest.approx(cd, abs=CENT)
    assert p.claims(t, "LAPSE") == pytest.approx(cl, abs=CENT)
    assert p.claims(t, "MATURITY") == pytest.approx(cm, abs=CENT)
    assert p.expenses(t) == pytest.approx(exp, abs=CENT)
    assert p.guar_int(t) == pytest.approx(gi, abs=CENT)
    assert p.index_credit(t) == pytest.approx(ic, abs=CENT)
    assert p.av(t) == pytest.approx(av, abs=CENT)
    assert p.net_cf(t) == pytest.approx(net, abs=CENT)


def test_the_two_payoff_designs_are_not_interchangeable(indexpolice, de_index_anchor):
    """``t = 10`` is the most instructive row in the library: nothing against 675,83 EUR.

    The Cap design credits **zero** on a sum of ``-2,60 %``; the *Quote* design credits
    3,8641 % of ``G`` on the same twelve returns.  At ``t = 9`` the ranking reverses,
    Example A's give-up having been concentrated in three months.
    """
    cap, quote = de_index_anchor, indexpolice.Projection[2]
    assert cap.index_credit_rate(10) == 0.0 and cap.index_credit(10) == 0.0
    assert quote.index_credit_rate(10) == pytest.approx(0.0386412, abs=5e-7)
    assert quote.index_credit_rate(10) == pytest.approx(
        0.60 * quote.index_return_year(10), rel=1e-12)
    assert quote.index_credit(10) == pytest.approx(675.83, abs=CENT)
    assert cap.index_credit_rate(9) == pytest.approx(0.0890, abs=1e-12)
    assert quote.index_credit_rate(9) == pytest.approx(0.0807289, abs=5e-7)
    assert cap.index_credit_rate(9) > quote.index_credit_rate(9)
    df = quote.result_cf()
    for column, total in QUOTE_TOTALS.items():
        assert df[column].sum() == pytest.approx(total, abs=CENT), column
    # What does not move with the payoff design: the premium and the expenses.
    base = cap.result_cf()
    assert df["premiums"].sum() == pytest.approx(base["premiums"].sum(), rel=1e-12)
    assert df["expenses"].sum() == pytest.approx(base["expenses"].sum(), rel=1e-12)


@pytest.mark.parametrize("point_id", sorted(DESIGNS))
def test_the_four_designs_at_rentenbeginn(indexpolice, point_id):
    """The notes' comparison: the same 2,50 % of surplus, spent four different ways -- all
    four a 40-year-old paying 2 400,00 EUR a year to 67 under a 90 % *Beitragsgarantie* at
    ``i_g = 1,00 %``, differing only in what the declared surplus buys."""
    idx, safe, account, guar, benefit, rente, ratio = DESIGNS[point_id]
    p = indexpolice.Projection[point_id]
    n = p.proj_len()
    assert sum(p.index_credit_pp(t) for t in range(1, n + 1)) == pytest.approx(
        idx, abs=CENT)
    assert sum(p.surplus_credit_pp(t) for t in range(1, n + 1)) == pytest.approx(
        safe, abs=CENT)
    assert p.credit_cum_pp(n + 1) == pytest.approx(idx + safe, abs=CENT)
    assert p.av_pp(n + 1) == pytest.approx(account, abs=CENT)
    assert p.guar_cap_pp(n + 1) == pytest.approx(guar, abs=CENT)
    assert p.mat_pp(n) == pytest.approx(benefit, abs=CENT)
    assert p.ann_monthly_pp() == pytest.approx(rente, abs=CENT)
    assert p.index_budget_ratio() == pytest.approx(ratio, abs=5e-5)


def test_the_safe_arm_beats_the_cap_design_on_this_path(indexpolice, de_index_anchor):
    """21 914,12 EUR of terminal capital, and it is not an argument against the product.

    The notes print 21 914,13 EUR, differencing the two *displayed* figures; both are
    asserted, the one-cent split being the artefact a reader would read as an error.
    """
    safe = indexpolice.Projection[11]
    assert safe.elect_id() == "always_safe"
    assert safe.av_pp(28) - de_index_anchor.av_pp(28) == pytest.approx(21914.12, abs=CENT)
    assert round(safe.av_pp(28), 2) - round(de_index_anchor.av_pp(28), 2) == (
        pytest.approx(21914.13, abs=CENT))


# --- One test per numbered modeling pitfall --------------------------------


def test_pitfall_01_treating_the_contract_as_unit_linked(indexpolice, de_index_anchor):
    """No *Anlagestock*, no unit price, no fund value: the capital is a general-account
    reserve and a bad *Indexjahr* credits zero rather than taking anything away.  The absent
    names are asserted too -- they are what a unit-linked reading would add."""
    p = de_index_anchor
    n = p.proj_len()
    for t in range(1, n + 1):
        assert p.av_pp_at(t, "AFT_CREDIT") >= p.av_pp_at(t, "AFT_GUAR")
    assert any(p.index_sum(t) < 0.0 for t in range(1, n + 1))
    assert all(p.index_credit_pp(t) >= 0.0 for t in range(1, n + 1))
    # The surrender value derives from the account, not from a unit price.
    for t in (1, 9, 13, 26):
        assert p.cv_pp(t) == pytest.approx(
            max(p.av_pp_at(t, "AFT_GUAR"), p.min_surr_pp(t)) - p.surr_charge_pp(t),
            rel=1e-12)
    names = set(indexpolice.Projection.cells) | set(indexpolice.Projection.refs)
    for absent in ("unit_price", "unit_value", "fund_value", "units", "unit_fund",
                   "anlagestock", "nav", "bid_offer_spread", "asset_share", "mvr",
                   "fund_return", "inv_return", "claims_surr", "claims_wd",
                   "withdrawals", "wd_free_pp"):
        assert absent not in names, absent


def test_pitfall_02_flooring_each_month_at_zero(de_index_anchor):
    """``x(m) = min(r, C)`` has **no lower bound**; the floor is on the year alone.

    On ``t = 10`` (Example B) the sum is ``-2,60 %`` and the credit is 0,00 EUR.  Flooring
    each capped month gives ``S = +12,60 %``, the corrected figure the notes record, 9,60
    points being what the cap *gave away* rather than what flooring produces.
    """
    p = de_index_anchor
    monthly = [p.index_return(10, m) for m in range(1, 13)]
    capped = [p.index_return_capped(10, m) for m in range(1, 13)]
    assert monthly == pytest.approx([r / 100.0 for r in EXAMPLE_B], abs=1e-12)
    assert min(capped) == pytest.approx(-0.031, abs=1e-12)   # not floored at zero
    assert p.index_sum(10) == pytest.approx(-0.0260, abs=1e-12)
    assert p.index_sum(10) < 0.0
    assert p.index_credit_rate(10) == 0.0
    assert p.index_credit_pp(10) == 0.0 and p.index_credit(10) == 0.0
    # What a month-floored implementation would produce, and what the cap gave away.
    assert sum(max(x, 0.0) for x in capped) == pytest.approx(0.1260, abs=1e-12)
    assert sum(monthly) - p.index_sum(10) == pytest.approx(0.0960, abs=1e-12)
    assert p.check_index_credit() is True


def test_pitfall_03_compounding_the_capped_returns(de_index_anchor):
    """The contractual formula is a **sum**: ``S(9) = +8,90 %`` exactly.  Compounding the
    same twelve capped returns gives 8,9599 % -- 0,0599 points, small enough to look like
    rounding and wrong at every duration; on the anchor's base, 11,62 EUR in year 9."""
    p = de_index_anchor
    capped = [p.index_return_capped(9, m) for m in range(1, 13)]
    assert p.index_sum(9) == pytest.approx(sum(capped), rel=1e-12)
    assert p.index_sum(9) == pytest.approx(0.0890, abs=1e-12)
    compounded = 1.0
    for x in capped:
        compounded *= (1.0 + x)
    assert compounded - 1.0 == pytest.approx(0.0895989, abs=5e-7)
    assert compounded - 1.0 - p.index_sum(9) == pytest.approx(0.000599, abs=5e-7)
    assert (compounded - 1.0 - p.index_sum(9)) * p.index_base_pp(9) == pytest.approx(
        11.62, abs=CENT)
    for t in (2, 3, 4, 13):
        assert p.index_sum(t) == pytest.approx(
            sum(p.index_return_capped(t, m) for m in range(1, 13)), rel=1e-12)


@pytest.mark.parametrize("t", sorted(INDEXJAHR))
def test_pitfall_04_applying_the_floor_to_the_compounded_raw_return(de_index_anchor, t):
    """``rho(t) = max(S(t), 0)`` -- never ``max(Y(t), 0)``, never ``max(q Y(t), 0)``.  At
    ``t = 10``, ``Y = +6,4402 %`` and the credit is **zero**; the two wrong readings would
    credit 6,44 % and 3,86 % on a Cap point."""
    s, y, rho = INDEXJAHR[t]
    p = de_index_anchor
    assert p.index_sum(t) == pytest.approx(s, abs=5e-7)
    assert p.index_return_year(t) == pytest.approx(y, abs=5e-7)
    assert p.index_credit_rate(t) == pytest.approx(rho, abs=5e-7)
    assert p.index_credit_rate(t) == pytest.approx(max(p.index_sum(t), 0.0), rel=1e-12)
    assert p.index_credit_rate(t) >= 0.0


def test_pitfall_04_the_index_rose_and_the_credit_was_nothing(de_index_anchor):
    """The row the whole product is criticised for, and not a one-off on this path."""
    p = de_index_anchor
    assert p.index_return_year(10) == pytest.approx(0.064402, abs=5e-7)
    assert p.index_return_year(10) > 0.0 and p.index_credit_rate(10) == 0.0
    assert 0.60 * p.index_return_year(10) == pytest.approx(0.038641, abs=5e-7)
    for t in (11, 16):
        assert p.index_return_year(t) > 0.0 and p.index_credit_rate(t) == 0.0


def test_pitfall_05_striking_the_participation_on_the_wrong_base(de_index_anchor):
    """``G(t) = av_pp(t)``, **before** the year's premium and before the year's charges.

    So a new-business point credits nothing in year 1 however well the index does, and
    striking the base after the premium instead credits a first-year amount that does not
    exist -- 243,09 EUR here.
    """
    p = de_index_anchor
    for t in range(1, p.proj_len() + 1):
        assert p.index_base_pp(t) == pytest.approx(p.av_pp(t), rel=1e-12)
        assert p.index_base_pp(t) == pytest.approx(p.av_pp_at(t, "BEF_PREM"), rel=1e-12)
    assert p.index_base_pp(1) == 0.0
    assert p.index_credit_rate(1) == pytest.approx(0.1204, abs=1e-12)
    assert p.index_credit_pp(1) == 0.0            # the base is zero, not the rate
    assert p.opt_budget_pp(1) == 0.0
    assert 0.1204 * p.av_pp_at(1, "AFT_GUAR") == pytest.approx(243.09, abs=CENT)
    assert p.index_base_pp(2) == pytest.approx(2018.9799, abs=5e-5)
    assert p.index_base_pp(2) < p.av_pp_at(2, "AFT_PREM")


def test_pitfall_06_crediting_the_index_and_the_declared_surplus(
        indexpolice, de_index_anchor):
    """They are alternative applications of **one** budget, never both and never neither;
    ``check_surplus_alloc()`` is that identity.  Point 1 elects the index arm every year,
    point 11 the safe arm every year, and point 12 splits the budget exactly in half."""
    p = de_index_anchor
    n = p.proj_len()
    assert p.check_surplus_alloc() is True
    for t in (1, 2, 9, 10, 27):
        assert p.check_surplus_alloc_resid(t) == pytest.approx(0.0, abs=1e-9)
        assert p.opt_budget_pp(t) + p.surplus_credit_pp(t) == pytest.approx(
            p.surplus_rate(t) * p.index_base_pp(t), rel=1e-12)
    assert all(p.elect_index(t) == 1.0 for t in range(1, n + 1))
    assert all(p.surplus_credit_pp(t) == 0.0 for t in range(1, n + 1))
    assert all(p.opt_budget_pp(t) == pytest.approx(0.025 * p.av_pp(t), rel=1e-12)
               for t in range(1, n + 1))
    safe = indexpolice.Projection[11]
    assert safe.check_surplus_alloc() is True
    assert all(safe.elect_index(t) == 0.0 for t in range(1, safe.proj_len() + 1))
    assert all(safe.index_credit_pp(t) == 0.0 for t in range(1, safe.proj_len() + 1))
    assert all(safe.opt_budget_pp(t) == 0.0 for t in range(1, safe.proj_len() + 1))
    half = indexpolice.Projection[12]
    assert half.elect_id() == "half_half" and half.check_surplus_alloc() is True
    for t in (1, 5, 20, 37):
        assert half.elect_index(t) == 0.5
        assert half.opt_budget_pp(t) == pytest.approx(half.surplus_credit_pp(t), rel=1e-12)


def test_pitfall_07_adding_the_declared_rate_on_top_of_the_guaranteed_rate(indexpolice):
    """In the index arm the surplus is **not** credited at all; it is spent.

    Point 9 runs ``zero_path`` at ``w = 1``, so the account grows at exactly
    ``(1 - gamma)(1 + i_g)`` and by nothing more; point 11 runs ``w = 0``, so it grows by
    that **plus** ``b G(t)`` and by nothing more either.
    """
    flat = indexpolice.Projection[9]
    assert flat.index_id() == "zero_path" and flat.elect_id() == "always_index"
    for t in range(1, flat.proj_len() + 1):
        assert flat.index_credit_rate(t) == 0.0
        assert flat.index_credit_pp(t) == 0.0
        assert flat.surplus_credit_pp(t) == 0.0
        assert flat.av_pp_at(t, "AFT_CREDIT") == pytest.approx(
            flat.av_pp_at(t, "AFT_PREM") * (1.0 - 0.0025) * (1.0 + 0.01), rel=1e-12)
    safe = indexpolice.Projection[11]
    for t in (2, 9, 15, 27):
        assert safe.av_pp_at(t, "AFT_CREDIT") == pytest.approx(
            safe.av_pp_at(t, "AFT_PREM") * (1.0 - 0.0025) * (1.0 + 0.01)
            + 0.025 * safe.av_pp(t), rel=1e-12)
        assert safe.surplus_credit_pp(t) == pytest.approx(
            0.025 * safe.av_pp(t), rel=1e-12)


def test_pitfall_08_crediting_the_indexjahr_to_the_lives_that_left(de_index_anchor):
    """Credits go to ``pols_if_at(t, "AFT_LAPSE")``, not to ``pols_if(t)``; give the
    *Indexjahr* to the opening in-force and the roll-forward residual is exactly the credit
    the leavers should not have had."""
    p = de_index_anchor
    n = p.proj_len()
    assert p.check_av_roll_fwd() is True
    for t in range(1, n + 1):
        assert p.check_av_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-6)
        assert p.index_credit(t) == pytest.approx(
            p.index_credit_pp(t) * p.pols_if_at(t, "AFT_LAPSE"), rel=1e-12)
        assert p.surplus_credit(t) == pytest.approx(
            p.surplus_credit_pp(t) * p.pols_if_at(t, "AFT_LAPSE"), rel=1e-12)
    # While the premium, the charge and the guaranteed interest are on the opening count.
    for t in (1, 9, 20):
        assert p.prem_to_av(t) == pytest.approx(
            p.prem_to_av_pp(t) * p.pols_if(t), rel=1e-12)
        assert p.av_charge(t) == pytest.approx(p.av_charge_pp(t) * p.pols_if(t), rel=1e-12)
        assert p.guar_int(t) == pytest.approx(p.guar_int_pp(t) * p.pols_if(t), rel=1e-12)
    wrong = p.index_credit_pp(9) * (p.pols_if(9) - p.pols_if_at(9, "AFT_LAPSE"))
    assert wrong == pytest.approx(41.50, abs=1.0) and wrong > 0.0


def test_pitfall_09_paying_a_pro_rata_index_credit_on_a_mid_year_exit(de_index_anchor):
    """A death or a surrender is struck on the balance **before** the year's credits.

    The assertion carrying the meaning is on ``av_pp_at(t, "AFT_GUAR")`` and **not** on
    ``db_pp``: the *Mindesttodesfallschutz* floor of 32 400,00 EUR exceeds the account
    until year 13, so the benefit is larger than the account at any timing there.  That is
    the correction the notes record.
    """
    p = de_index_anchor
    n = p.proj_len()
    floor = 0.50 * p.prem_sum()
    assert floor == 32400.0
    for t in range(1, n + 1):
        assert p.db_pp(t) == pytest.approx(
            max(p.av_pp_at(t, "AFT_GUAR"), floor), rel=1e-12)
        assert p.cv_pp(t) <= max(p.av_pp_at(t, "AFT_GUAR"), p.min_surr_pp(t))
    credited = [t for t in range(1, n + 1) if p.index_credit_pp(t) > 0.0]
    assert credited == [2, 3, 4, 6, 9, 13]
    for t in credited:
        assert p.av_pp_at(t, "AFT_GUAR") < p.av_pp(t + 1)
        assert p.av_pp(t + 1) - p.av_pp_at(t, "AFT_GUAR") == pytest.approx(
            p.index_credit_pp(t), rel=1e-12)
    # The floor binds to year 12 and stops binding at year 13, exactly as the notes say.
    assert all(p.db_pp(t) == floor for t in range(1, 13))
    assert p.db_pp(13) == pytest.approx(p.av_pp_at(13, "AFT_GUAR"), rel=1e-12)
    assert p.db_pp(13) > floor
    # The maturity is the one benefit that does include the year's credits.
    assert p.mat_pp(n) == pytest.approx(
        max(p.av_pp(n + 1), p.guar_cap_pp(n + 1)), rel=1e-12)


def test_pitfall_10_testing_the_lock_in_as_the_account_never_falls(
        indexpolice, de_index_anchor):
    """It is the **credits** that ratchet, not the balance.  On point 13 the
    *Rechnungszins* equals the reserve charge and premiums stop at year 12, so the account
    falls from year 14 while ``guar_cap_pp`` is still monotone; a lock-in check written on
    ``av_pp`` would fail a correct implementation and pass a wrong one."""
    p = de_index_anchor
    assert p.check_lock_in() is True
    for t in (1, 9, 13, 27):
        assert p.check_lock_in_resid(t) == pytest.approx(0.0, abs=1e-9)
    falling = indexpolice.Projection[13]
    n = falling.proj_len()
    assert falling.guar_rate() == 0.0025 == falling.exp_av_rate
    assert falling.prem_term_y() == 12 and falling.t_start() == 5 and n == 22
    assert falling.check_lock_in() is True
    assert any(falling.av_pp(t + 1) < falling.av_pp(t)
               for t in range(falling.t_start(), n + 1))
    assert falling.av_pp(23) < falling.av_pp(14)
    assert all(falling.guar_cap_pp(t + 1) >= falling.guar_cap_pp(t)
               for t in range(falling.t_start(), n + 1))
    assert all(falling.credit_cum_pp(t + 1) >= falling.credit_cum_pp(t)
               for t in range(falling.t_start(), n + 1))
    assert all(p.guar_cap_pp(t) == pytest.approx(
        p.guar_floor_pp(t) + p.credit_cum_pp(t), rel=1e-12) for t in (1, 9, 27, 28))


def test_pitfall_11_running_the_guarantee_as_an_annual_rate_on_the_reserve(
        de_index_anchor):
    """*Neue Klassik*: the guarantee is owed at *Rentenbeginn* and at no other date.

    ``guar_cap_pp(t)`` enters one benefit and no other, and ``av_pp(t) < guar_cap_pp(t)``
    at intermediate ``t`` is permitted and ordinary -- it holds at ``t = 2 ... 7`` here,
    while the *Zillmer* charge is being recovered -- with no check failing there.
    """
    p = de_index_anchor
    n = p.proj_len()
    assert [t for t in range(1, n + 2) if p.av_pp(t) < p.guar_cap_pp(t)] == [
        2, 3, 4, 5, 6, 7]
    assert p.check_lock_in() is True and p.check_av_roll_fwd() is True
    # No death benefit and no surrender value anywhere sees the guaranteed capital: their
    # forms are asserted for every t by the tests for pitfalls 9 and 13.
    for t in (2, 5, 7):
        assert p.db_pp(t) < p.guar_cap_pp(t) and p.cv_pp(t) < p.guar_cap_pp(t)
    assert p.claims(n, "MATURITY") == pytest.approx(
        max(p.av_pp(n + 1), p.guar_cap_pp(n + 1)) * p.pols_maturity(n), rel=1e-12)
    assert all(p.mat_pp(t) == 0.0 for t in range(1, n))


def test_pitfall_12_forgetting_the_beitragsgarantie_floor_at_rentenbeginn(
        indexpolice, de_index_anchor):
    """A model with no floor and one with a floor that never binds look identical.  Point 9
    exists so that it binds: a 100 % *Beitragsgarantie* against the flat ``zero_path``,
    where the charges take more than the 1,00 % *Rechnungszins* returns."""
    binding = indexpolice.Projection[9]
    n = binding.proj_len()
    assert binding.guar_level() == 1.0 and binding.index_id() == "zero_path"
    assert binding.credit_cum_pp(n + 1) == 0.0
    assert binding.guar_cap_pp(n + 1) == pytest.approx(28800.00, abs=CENT)
    assert binding.av_pp(n + 1) == pytest.approx(28555.54, abs=CENT)
    assert binding.guar_cap_pp(n + 1) > binding.av_pp(n + 1)
    assert binding.mat_pp(n) == pytest.approx(binding.guar_cap_pp(n + 1), rel=1e-12)
    assert binding.mat_pp(n) == pytest.approx(28800.00, abs=CENT)
    # And it does not bind on the anchor, which is why one point is not enough.
    p = de_index_anchor
    assert p.mat_pp(27) == pytest.approx(p.av_pp(28), rel=1e-12)
    assert p.av_pp(28) > p.guar_cap_pp(28)


def test_pitfall_13_confusing_the_minimum_surrender_value_with_the_zillmer_cap(
        indexpolice, de_index_anchor):
    """Two rules with two functions: what may be **reserved** against what must be **paid**.

    With ``zill_years = 5`` the tariff and shadow accounts coincide at every ``t``, so the
    floor is a no-op -- delib's charge profile already sits at the statutory floor -- while
    the 2 % *Stornoabzug* still bites.
    """
    p = de_index_anchor
    n = p.proj_len()
    assert p.zill_years == 5 and p.acq_cost_rate == 0.025 and p.zill_cap_rate == 0.025
    for t in range(1, n + 2):
        assert p.av_min_pp(t) == pytest.approx(p.av_pp(t), abs=1e-6)
    for t in range(1, n + 1):
        assert p.prem_charge_acq_min_pp(t) == pytest.approx(
            p.prem_charge_acq_pp(t), rel=1e-12)
        assert p.min_surr_pp(t) == pytest.approx(p.av_pp_at(t, "AFT_GUAR"), abs=1e-6)
        assert p.cv_pp(t) < p.av_pp_at(t, "AFT_GUAR")
        assert p.surr_charge_pp(t) == pytest.approx(
            0.02 * max(p.av_pp_at(t, "AFT_GUAR"), p.min_surr_pp(t)), rel=1e-12)
    # A tariff without the clause is a real configuration and not a special case.
    no_charge = indexpolice.Projection[13]
    assert no_charge.surr_charge_on() == 0
    for t in (5, 12, 22):
        assert no_charge.surr_charge_pp(t) == 0.0
        assert no_charge.cv_pp(t) == pytest.approx(
            max(no_charge.av_pp_at(t, "AFT_GUAR"), no_charge.min_surr_pp(t)), rel=1e-12)


def test_pitfall_14_double_charging_or_mis_basing_the_ratenzahlungszuschlag(indexpolice):
    """``phi`` multiplies the premium **collected** and does not enter the *Beitragssumme*.

    Point 4 pays monthly: 2 520,00 EUR a year collected against a ``prem_sum()`` of
    76 800,00 EUR.  A frequency surcharge is the price of paying in instalments, so it may
    not inflate the acquisition charge or the death floor.
    """
    p = indexpolice.Projection[4]
    assert p.prem_freq() == "monthly" and p.freq_load() == 1.05
    assert p.prem_base_pp(1) == pytest.approx(2400.00, abs=CENT)
    assert p.prem_gross_pp(1) == pytest.approx(2400.00 * 1.05, abs=CENT)
    assert p.prem_gross_pp(1) == pytest.approx(2520.00, abs=CENT)
    assert p.prem_sum() == pytest.approx(2400.00 * 32, abs=CENT)
    assert p.prem_sum() == pytest.approx(76800.00, abs=CENT)
    assert p.prem_charge_acq_pp(1) == pytest.approx(0.025 * 76800.00 / 5, abs=CENT)
    assert p.prem_charge_acq_pp(1) == pytest.approx(384.00, abs=CENT)
    assert p.db_pp(1) == pytest.approx(0.50 * 76800.00, abs=CENT)
    # The premium administration charge is on what is collected, so it does move.
    assert p.prem_charge_adm_pp(1) == pytest.approx(0.03 * 2520.00, abs=CENT)
    assert indexpolice.Projection[5].freq_load() == 1.03
    assert indexpolice.Projection[6].freq_load() == 1.02
    assert indexpolice.Projection[1].freq_load() == 1.0
    assert indexpolice.Projection[1].prem_gross_pp(1) == pytest.approx(
        indexpolice.Projection[1].prem_base_pp(1), rel=1e-12)


def test_pitfall_15_letting_the_cap_and_the_option_budget_be_independent(
        indexpolice, de_index_anchor):
    """The Cap is the level at which the option strip costs the budget, so the two are not
    free parameters, and ``index_budget_ratio()`` reports the discrepancy.

    On the anchor it is **0,2082** on amounts, for timing rather than pricing reasons: the
    path credits in years 1-4, 6, 9 and 13 and never after, while ``G(t)`` runs to
    70 637,97 EUR.  On rates it credits 2,1330 % against a 2,50 % budget, a ratio of 0,853.
    """
    p = de_index_anchor
    n = p.proj_len()
    credits = sum(p.index_credit_pp(t) for t in range(1, n + 1))
    budget = sum(p.opt_budget_pp(t) for t in range(1, n + 1))
    assert credits == pytest.approx(4851.44, abs=CENT)
    assert budget == pytest.approx(23298.38, abs=CENT)
    assert p.index_budget_ratio() == pytest.approx(credits / budget, rel=1e-12)
    assert p.index_budget_ratio() == pytest.approx(0.2082, abs=5e-5)
    mean_rate = sum(p.index_credit_rate(t) for t in range(1, n + 1)) / n
    assert mean_rate == pytest.approx(0.021330, abs=5e-7)
    assert mean_rate / 0.025 == pytest.approx(0.853, abs=5e-4)
    assert p.index_base_pp(1) == 0.0
    assert p.index_base_pp(27) == pytest.approx(70637.97, abs=CENT)
    # The other two designs sit either side of 1, which is the point of reporting it.
    assert indexpolice.Projection[2].index_budget_ratio() == pytest.approx(
        0.9782, abs=5e-5)
    assert indexpolice.Projection[3].index_budget_ratio() == pytest.approx(
        1.6482, abs=5e-5)
    assert indexpolice.Projection[11].index_budget_ratio() == 0.0


def test_pitfall_16_assuming_the_wahlrecht_is_exercised_optimally(indexpolice):
    """The election is a **behavioural** assumption whose path is read, never derived.

    Point 11 reproduces a *klassische Rentenversicherung* exactly -- every index cells
    evaluates and none reaches the account -- and point 10 switches arms at 15, never
    crediting both in one year.
    """
    safe = indexpolice.Projection[11]
    n = safe.proj_len()
    assert safe.elect_id() == "always_safe" and safe.payoff_form() == "cap"
    assert safe.index_credit_rate(4) == pytest.approx(0.2225, abs=1e-12)   # it evaluates
    assert safe.index_sum(10) == pytest.approx(-0.0260, abs=1e-12)
    assert all(safe.index_credit_pp(t) == 0.0 for t in range(1, n + 1))
    assert safe.result_cf()["index_credit"].sum() == 0.0
    assert safe.result_cf()["surplus_credit"].sum() == pytest.approx(13770.05, abs=CENT)
    switch = indexpolice.Projection[10]
    assert switch.elect_id() == "switch_at_15"
    assert all(switch.elect_index(t) == 1.0 for t in range(1, 16))
    assert all(switch.elect_index(t) == 0.0 for t in range(16, 28))
    assert all(switch.surplus_credit_pp(t) == 0.0 for t in range(1, 16))
    assert all(switch.index_credit_pp(t) == 0.0 for t in range(16, 28))
    assert switch.check_surplus_alloc() is True
    df = switch.result_cf()
    assert df["index_credit"].sum() > 0.0 and df["surplus_credit"].sum() > 0.0


def test_pitfall_17_a_lapse_assumption_flat_in_duration(de_index_anchor):
    """The duration-12 tax threshold is the strongest single driver of German surrender.

    ``lapse_rate(12) = 6 %`` against 3 % the year before, and the worked example's year-12
    spike -- 1 229,59 EUR against 583,79 EUR -- is that step and nothing else.  In the final
    year the applied rate is zero while the table still says 2 %.
    """
    p = de_index_anchor
    n = p.proj_len()
    assert p.lapse_rate(1) == 0.05 and p.lapse_rate(2) == 0.05
    assert p.lapse_rate(11) == 0.03 and p.lapse_rate(12) == 0.06
    assert p.lapse_rate(12) > p.lapse_rate(11)
    assert p.lapse_rate(13) == 0.02
    assert p.lapse_rate(n) == 0.0 and p.lapse_rate_base(n) == 0.02
    assert p.pols_lapse(n) == 0.0 and p.claims(n, "LAPSE") == 0.0
    assert len({p.lapse_rate(t) for t in range(1, n + 1)}) == 5
    assert p.claims(12, "LAPSE") == pytest.approx(1229.59, abs=CENT)
    assert p.claims(11, "LAPSE") == pytest.approx(583.79, abs=CENT)
    assert p.claims(12, "LAPSE") > 2.0 * p.claims(11, "LAPSE")


def test_pitfall_18_reporting_the_credits_inside_net_cf(de_index_anchor):
    """``guar_int``, ``surplus_credit`` and ``index_credit`` are state movements: they
    reach the insurer's cash flow only later, through a benefit.  ``net_cf`` is unchanged
    when the three columns are dropped, and adding them would move the total by
    9 139,74 EUR."""
    p = de_index_anchor
    df = p.result_cf()
    statement = df.drop(columns=["guar_int", "surplus_credit", "index_credit", "av"])
    rebuilt = (statement["premiums"] - statement["claims_death"]
               - statement["claims_lapse"] - statement["claims_maturity"]
               - statement["expenses"])
    assert (rebuilt - statement["net_cf"]).abs().max() == pytest.approx(0.0, abs=1e-9)
    assert p.check_net_cf() is True
    for t in range(1, p.proj_len() + 1):
        assert p.check_net_cf_resid(t) == pytest.approx(0.0, abs=1e-9)
    moved = df["guar_int"].sum() + df["surplus_credit"].sum() + df["index_credit"].sum()
    assert moved == pytest.approx(9139.74, abs=CENT)
    assert df["net_cf"].sum() + moved == pytest.approx(1739.89, abs=CENT)


# --- The published identities, and delib's first ruling --------------------


def test_every_check_returns_a_bool_and_its_residual_is_zero(de_index_anchor):
    """Six ``check_*()`` cells, each no-argument and each returning a real ``bool``.

    delib's first ruling is that ``check_net_cf()`` is mandatory: the identity that rebuilds
    ``net_cf(t)`` from the statement's own published parts, so no model's headline number is
    reconciled only in prose.  It takes the kind-less ``claims(t)`` while ``net_cf`` names
    the kinds one by one, so the two agree only if both carry the same list of kinds.
    """
    p = de_index_anchor
    checks = ("check_net_cf", "check_av_roll_fwd", "check_pols_roll_fwd",
              "check_surplus_alloc", "check_lock_in", "check_index_credit")
    for name in checks:
        value = getattr(p, name)()
        assert value is True, name
        assert isinstance(value, bool), name
        resid = getattr(p, name + "_resid")
        for t in (1, 2, 9, 10, 13, 27):
            assert abs(resid(t)) < 1e-6, (name, t)
    for t in (1, 9, 12, 27):
        assert p.claims(t) == pytest.approx(
            p.claims(t, "DEATH") + p.claims(t, "LAPSE") + p.claims(t, "MATURITY"),
            rel=1e-12)
        assert p.check_net_cf_resid(t) == pytest.approx(
            p.net_cf(t) - (p.premiums(t) - p.claims(t) - p.expenses(t)), abs=1e-12)


def test_the_index_credit_bounds_hold_in_both_payoff_designs(indexpolice, de_index_anchor):
    """``0 <= rho <= 12 C`` in the Cap form, ``0 <= rho <= q max(Y, 0)`` in the *Quote*."""
    cap, quote = de_index_anchor, indexpolice.Projection[2]
    assert cap.check_index_credit() is True and quote.check_index_credit() is True
    for t in range(1, cap.proj_len() + 1):
        assert 0.0 <= cap.index_credit_rate(t) <= 12.0 * cap.index_cap(t)
        assert 0.0 <= quote.index_credit_rate(t) <= (
            quote.index_quote(t) * max(quote.index_return_year(t), 0.0) + 1e-12)
    assert cap.index_cap(1) == 0.03 and cap.index_quote(1) == 0.60
    house = indexpolice.Projection[3]
    assert house.index_cap(1) == 0.06 and house.index_quote(1) == 1.00


def test_the_in_force_cell_reproduces_both_indexjahre_on_a_50000_euro_base(indexpolice):
    """Model point 8 starts at ``dur_init = 8`` with 50 000,00 EUR, the research file's ``G``,
    so its first projected *Indexjahr* is ``t = 9`` on exactly that base: Example A credits
    4 450,00 EUR against a safe arm of 1 250,00 EUR, and Example B credits nothing."""
    p = indexpolice.Projection[8]
    assert p.dur_init() == 8 and p.t_start() == 9 and p.proj_len() == 27
    assert len(p.result_cf()) == 19
    assert p.result_cf().index[-1] == p.proj_len() == 27
    assert p.av_pp_init() == 50000.0 and p.index_base_pp(9) == 50000.0
    assert p.index_credit_pp(9) == pytest.approx(0.0890 * 50000.0, abs=CENT)
    assert p.index_credit_pp(9) == pytest.approx(4450.00, abs=CENT)
    assert p.index_credit_pp(9) / (0.025 * 50000.0) == pytest.approx(3.56, abs=5e-3)
    assert p.index_base_pp(10) == pytest.approx(60631.57, abs=CENT)
    assert p.index_credit_pp(10) == 0.0
    assert 0.025 * p.index_base_pp(10) == pytest.approx(1515.79, abs=CENT)
    assert p.guar_locked_init() == 4300.0 and p.credit_cum_pp(9) == 4300.0
    assert p.check_av_roll_fwd() is True and p.check_lock_in() is True


# --- Structure, documentation and inputs -----------------------------------


def test_result_cf_shape_and_both_signs_of_the_net_flow(de_index_anchor):
    """The frame's twelve columns, in order, with ``pols_if`` first and ``net_cf`` in it."""
    p = de_index_anchor
    df = p.result_cf()
    assert list(df.columns) == [
        "pols_if", "premiums", "claims_death", "claims_lapse", "claims_maturity",
        "expenses", "guar_int", "surplus_credit", "index_credit", "av",
        "liability_cf", "net_cf",
    ]
    assert list(df.index) == list(range(1, 28))
    assert df.index.name == "t"
    assert df.index[-1] == p.proj_len() == 27
    assert df["pols_if"].iloc[0] == p.pols_if_init() == 1.0
    assert "claims" not in df.columns          # never the subtotal beside its parts
    assert (df["net_cf"] + df["liability_cf"]).abs().max() == pytest.approx(0.0, abs=1e-9)
    assert (df["pols_if"] >= 0.0).all()
    assert df.notna().all().all()
    # A Zillmer-financed savings contract: a thin first year, then thin positive years,
    # then one very large negative year when the whole cohort's capital falls due.
    assert df["net_cf"].iloc[0] == pytest.approx(606.31, abs=CENT)
    assert (df["net_cf"].iloc[:-1] > 0).all()
    assert df["net_cf"].iloc[-1] < -30000.0


def test_invalid_enum_values_raise(de_index_anchor):
    """The enum accessors validate rather than propagating a typo into a lookup."""
    with pytest.raises(FormulaError):
        de_index_anchor.claims(1, "SURRENDER")
    with pytest.raises(FormulaError):
        de_index_anchor.pols_if_at(1, "AFTER_LAPSE")
    with pytest.raises(FormulaError):
        de_index_anchor.av_pp_at(1, "AFTER_CREDIT")


def test_docstrings_describe_the_current_structure(indexpolice):
    """Specifics a reader would rely on, asserted so they cannot go stale silently."""
    doc = indexpolice.doc
    assert "Indexpolice" in doc
    assert "mechanics demonstration" in doc
    assert "external" in doc                    # inputs are not stored in the model
    assert "once per model" in doc              # why Data exists
    assert "Sicherungsvermögen" in doc and "Anlagestock" in doc
    assert "Data" in doc and "Projection" in doc
    proj = indexpolice.Projection.doc
    assert "Notes symbol" in proj
    for cells in ("proj_len", "model_point", "index_sum", "index_credit_rate",
                  "index_base_pp", "opt_budget_pp", "credit_cum_pp", "guar_cap_pp",
                  "av_pp_at", "elect_index"):
        assert cells in proj, cells
    data = indexpolice.Data.doc
    assert "TradLife_A" in data
    assert "input_dir" in data and "model_point_table" in data
    assert "0.001200" in data                   # the mortality proxy's stated anchor
    for cells in ("index_return_table", "index_param_table", "surplus_rate_table",
                  "election_table", "mort_table", "lapse_table", "freq_load_table"):
        assert cells in data, cells


def test_the_shared_library_vocabulary_is_present(indexpolice):
    """The names every delib model publishes must mean the same thing on all ten."""
    shared = {
        "model_point", "proj_len", "age", "pols_if", "pols_if_at", "pols_if_init",
        "pols_death", "pols_lapse", "pols_maturity", "mort_rate", "lapse_rate",
        "lapse_rate_base", "premiums", "claims", "expenses", "net_cf", "liability_cf",
        "result_cf", "av", "av_at", "av_pp", "av_pp_at", "prem_to_av_pp",
        "check_net_cf", "check_net_cf_resid",
    }
    names = set(indexpolice.Projection.cells) | set(indexpolice.Projection.refs)
    assert shared <= names, f"missing: {sorted(shared - names)}"
    for retired in ("lapse_rate_ann", "prem_net_pp", "mort_ae_factor", "mort_adj",
                    "mort_rate_table", "premium_net_pp", "check_pols_if", "pols_init",
                    "omega", "loan_bal", "pols_expiry", "check_cf_ledger"):
        assert retired not in names, retired
    assert indexpolice.Projection.parameters == ("point_id",)
    assert set(indexpolice.spaces) == {"Data", "Projection"}


def test_the_shipped_tables_mark_their_own_provenance():
    """Eight CSVs beside run.py, and each says what it is -- especially what it is not.

    delib's second ruling: every assumption file carries a populated ``provenance`` column,
    ``model_point_table.csv`` being the only exemption.  The mortality table is a **[std]**
    Gompertz proxy anchored at ``qx(M, 40) = 0.001200``; DAV 2008 T and DAV 2004 R are cited
    by name and never shipped.
    """
    import pandas as pd

    parent = MODEL_DIR.parent
    assert INPUT_CSVS == {p.name for p in parent.iterdir() if p.suffix == ".csv"}
    for name in sorted(INPUT_CSVS - {"model_point_table.csv"}):
        frame = pd.read_csv(parent / name)
        assert "provenance" in frame.columns, name
        assert frame["provenance"].notna().all(), name
        assert (frame["provenance"].astype(str).str.strip() != "").all(), name
    points = pd.read_csv(parent / "model_point_table.csv", index_col="point_id")
    assert "provenance" not in points.columns
    assert len(points) == 13 and points.loc[1, "policy_id"] == "DE-IDX-0001"

    mort = pd.read_csv(parent / "mort_table.csv", index_col=["sex", "age"])
    assert float(mort.loc[("M", 40), "qx"]) == pytest.approx(0.001200, rel=1e-9)
    assert float(mort.loc[("M", 41), "qx"]) == pytest.approx(0.001200 * 1.095, rel=1e-9)
    assert float(mort.loc[("F", 40), "qx"]) == pytest.approx(0.65 * 0.001200, rel=1e-9)
    assert mort["qx"].max() <= 1.0
    assert all("[std]" in p and "DAV" in p for p in mort["provenance"])

    months = ["m%02d" % m for m in range(1, 13)]
    returns = pd.read_csv(parent / "index_return_table.csv", index_col=["index_id", "t"])
    assert set(returns.index.get_level_values("index_id")) == {
        "eqidx_vol17", "houseidx_vol5", "zero_path"}
    assert [c for c in returns.columns if c != "provenance"] == months
    # The two anchor rows a replacement path must preserve.
    assert returns.loc[("eqidx_vol17", 9), months].astype(float).tolist() == (
        pytest.approx([r / 100.0 for r in EXAMPLE_A], abs=1e-12))
    assert returns.loc[("eqidx_vol17", 10), months].astype(float).tolist() == (
        pytest.approx([r / 100.0 for r in EXAMPLE_B], abs=1e-12))
    assert (returns.loc["zero_path", months].astype(float) == 0.0).all().all()

    params = pd.read_csv(parent / "index_param_table.csv", index_col=["index_id", "t"])
    assert float(params.loc[("eqidx_vol17", 1), "cap"]) == 0.03
    assert float(params.loc[("eqidx_vol17", 1), "quote"]) == 0.60
    assert float(params.loc[("houseidx_vol5", 1), "cap"]) == 0.06
    assert float(params.loc[("houseidx_vol5", 1), "quote"]) == 1.00

    surplus = pd.read_csv(parent / "surplus_rate_table.csv", index_col="t")
    assert set(surplus["surplus_rate"]) == {0.025}
    election = pd.read_csv(parent / "election_table.csv", index_col=["elect_id", "t"])
    assert set(election.index.get_level_values("elect_id")) == {
        "always_index", "always_safe", "half_half", "switch_at_15"}
    assert float(election.loc[("half_half", 1), "w"]) == 0.5
    lapse = pd.read_csv(parent / "lapse_table.csv", index_col="t")
    assert [float(lapse.loc[t, "lapse_rate"]) for t in (1, 3, 12, 13)] == [
        0.05, 0.03, 0.06, 0.02]
    freq = pd.read_csv(parent / "freq_load_table.csv", index_col="prem_freq")
    assert [float(freq.loc[f, "freq_load"]) for f in
            ("annual", "half_yearly", "quarterly", "monthly")] == [1.0, 1.02, 1.03, 1.05]


def test_an_input_can_be_swapped_without_touching_formulas():
    """This is what a production user does with a company index path: swapping the return
    table for one whose *Indexjahre* all sum below zero leaves a projection that credits
    nothing -- the mechanic following the data, with no formula change anywhere."""
    import pandas as pd

    months = ["m%02d" % m for m in range(1, 13)]
    bleak = pd.read_csv(MODEL_DIR.parent / "index_return_table.csv",
                        index_col=["index_id", "t"])
    bleak[months] = -0.01

    model = mx.read_model(MODEL_DIR, name="Index_DE_A_swap")
    try:
        alt_name = "index_return_table_bleak.csv"
        bleak.to_csv(model.Data.input_dir() / alt_name)
        try:
            base = model.Projection[1].result_cf()["index_credit"].sum()
            assert base == pytest.approx(3577.46, abs=CENT)
            model.Data.index_return_file = alt_name
            model.Data.clear_all()
            model.Projection.clear_all()
            p = model.Projection[1]
            assert p.index_sum(9) == pytest.approx(-0.12, abs=1e-12)
            assert p.result_cf()["index_credit"].sum() == 0.0
            assert p.check_index_credit() is True and p.check_lock_in() is True
            # The account still grows: the guaranteed rate is untouched by the index.
            assert p.av_pp(28) > 0.0 and p.result_cf()["guar_int"].sum() > 0.0
        finally:
            (model.Data.input_dir() / alt_name).unlink(missing_ok=True)
    finally:
        model.close()


def test_round_trip_is_stable(tmp_path):
    """read -> write -> re-read reproduces the goldens and the same file set."""
    import shutil

    model = mx.read_model(MODEL_DIR, name="Index_DE_A_rt_src")
    try:
        dest = tmp_path / MODEL_DIR.name
        mx.write_model(model, str(dest), backup=False)
    finally:
        model.close()

    for csv in MODEL_DIR.parent.glob("*.csv"):
        shutil.copy(csv, tmp_path / csv.name)

    reread = mx.read_model(dest, name="Index_DE_A_rt")
    try:
        p = reread.Projection[1]
        for t, row in WORKED_EXAMPLE.items():
            assert p.premiums(t) == pytest.approx(row[2], abs=CENT)
            assert p.claims(t, "DEATH") == pytest.approx(row[3], abs=CENT)
            assert p.index_credit(t) == pytest.approx(row[8], abs=CENT)
            assert p.net_cf(t) == pytest.approx(row[10], abs=CENT)
        assert "Notes symbol" in reread.Projection.doc
        assert p.check_net_cf() is True and p.check_av_roll_fwd() is True
        assert p.index_budget_ratio() == pytest.approx(0.2082, abs=5e-5)
    finally:
        reread.close()

    assert model_files(dest) == model_files(MODEL_DIR)
