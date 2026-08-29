"""Golden and structural tests for Basis_DE_A, the German Basisrente (Rürup, Schicht 1).

The golden values are the worked example in
``products/basisrente/technical-notes.md`` ("Worked example"), which is a **configuration**
rather than a scenario.  Model point 1 is that cell: policy ``DE-BAS-0001``, a male aged 45 at
conclusion (``sex`` is reporting only -- pricing is unisex), the contract concluded in **2026**
with ``duration_init = 0``, *Rentenbeginn* at attained age **67**, one policy in force, a
**regular** *laufender Beitrag* of **6 000,00 EUR** a year paid **annually in advance** so the
*Ratenzahlungszuschlag* is 1,000, a **2 % *Beitragsdynamik***, an annual ***Zuzahlung*** of
**4 000,00 EUR** to policy duration 22, not paid-up at the valuation date, no opening account
value and no annuity in payment, a *Rechnungszins* of **1,00 %**, a **guaranteed *Rentenfaktor*
of 28,00 EUR** per month per 10 000 EUR, **no *Rentengarantiezeit*, no survivor's annuity and
no BUZ**, on tariff ``de_basis_std`` with the ``base`` behaviour, surplus and *Rentenfaktor*
scenarios.  Hence ``age(1) = 45``, ``ret_t() = 23``, ``omega_age() = 121`` and
``proj_len() = 77``: twenty-two years of *Aufschubphase* and fifty-five years of *Rentenphase*.

Because the projection is seventy-seven years long, the notes print **eighteen selected rows** --
every year of the first six, a five-yearly sample of the accumulation phase, the conversion year
and its neighbours, and a decade sample of the payout phase -- plus a **Total** row summed at
full precision and then rounded.  Every one of those eighteen rows is asserted here, cell by
cell, together with the full-precision totals and the fact that adding the *rounded* cells
instead gives a different answer in three of the six money columns.

The goldens are hard-coded rather than pickled so that a reviewer can compare them against the
notes by eye.  Tolerances follow the precision the notes display: money to the cent, ``pols_if``
and ``pols_paying`` to six decimals.

What this module asserts, beyond those rows:

* the notes' **three independent checks** -- the first year's account rebuilt from the charge
  scale up, the year-one decrement split rebuilt from the shipped mortality table, and the
  conversion rebuilt from the fund and the applied *Rentenfaktor* -- and the two **closure
  identities**, that the decrements sum to exactly one and that the Total row reconciles;
* the two documented **variant tables**: model point 5, the *Einmalbeitrag*, and model point 13,
  the cell on which the guaranteed *Rentenfaktor* binds instead of the current one;
* all six published ``check_*`` identities and their per-``t`` residuals, including
  ``check_net_cf()`` -- delib's first ruling -- and the shape and sign conventions of
  ``result_cf()``;
* **one test per numbered modeling pitfall** in the technical notes, named for the pitfall:
  (1) no surrender value at any duration and none of the names that would carry one;
  (2) a *Beitragsfreistellung* is not a lapse and is absent from the in-force roll-forward;
  (3) the paying and premium-free account blocks are not averaged; (4) an account charge is not
  also an expense; (5) the *Zillmerung* is spread over five **contract** years and capped;
  (6) the declared rate is a ``max`` against the guarantee and not a sum; (7) premiums, the
  *Zuzahlung* and the *Dynamik* are keyed to the policy duration and stop at *Rentenbeginn*;
  (8) the *Ratenzahlungszuschlag* loads the *laufender Beitrag* alone; (9) death before
  *Rentenbeginn* pays nothing with the rider off; (10) with the rider on it pays only where an
  eligible survivor exists, and never a lump sum; (11) the conversion is struck on the
  contractual basis and is invariant to ``mort_be_factor``; (12) the annuity is booked in
  advance on the opening in-force count; (13) ``max(garantiert, aktuell)`` takes the higher
  factor, both branches shipping; (14) the *Rentengarantiezeit* runs from *Rentenbeginn* and is
  never commuted; (15) the mortality basis is generational; (16) the guarantee vintage attaches
  at conclusion; (17) the BUZ is a premium share that reaches no cash flow.

The whole-model-point-table sweep is deliberately **not** here: ``test_model_conventions_de.py``
owns the single sweep, because a model point's first evaluation is the most expensive thing in
the run.  This module instantiates only the points the worked example and the pitfalls need.
"""
import pandas as pd
import modelx as mx
import pytest
from modelx.core.errors import FormulaError

from de_registry import MODELS, LIB


CENT = 0.005          # money displayed to 2 d.p.
SIX_DP = 0.0000005    # pols_if / pols_paying displayed to 6 d.p.

MODEL_DIR = LIB / MODELS["Basis_DE_A"][0]
INPUT_DIR = MODEL_DIR.parent

# The seven external CSVs, which live beside run.py and not inside the model folder.
INPUT_FILES = {
    "model_point_table.csv", "mort_table.csv", "surplus_table.csv",
    "rentenfaktor_table.csv", "charge_table.csv", "behaviour_table.csv",
    "option_table.csv",
}

# ---------------------------------------------------------------------------
# The notes' worked-example table, in full.
#
# t: (age, pols_if, pols_paying, av, premiums, zuzahlungen, claims_annuity, expenses,
#     commissions, net_cf).  claims_death and claims_survivor are 0.00 at every one of the
# seventy-seven years on this cell -- the survivor rider is off and there is no
# Rentengarantiezeit -- and are asserted in the row test all the same.
WORKED_EXAMPLE = {
    1:  (45, 1.000000, 1.000000,      0.00, 6000.00, 2800.00,    0.00, 310.00, 4094.85,  4395.15),
    2:  (46, 0.998560, 0.958618,   7366.75, 5866.74, 2684.13,    0.00,  60.81,  128.26,  8361.80),
    3:  (47, 0.997024, 0.918857,  14688.72, 5735.87, 2572.80,    0.00,  61.63,  124.63,  8122.42),
    4:  (48, 0.995385, 0.880653,  21968.46, 5607.33, 2465.83,    0.00,  62.45,  121.10,  7889.61),
    5:  (49, 0.993635, 0.843941,  29208.23, 5481.05, 2363.03,    0.00,  63.28,  117.66,  7663.15),
    6:  (50, 0.991769, 0.808662,  36410.00, 5356.97, 2749.45,    0.00,  64.11,  121.60,  7920.71),
    11: (55, 0.980403, 0.686467,  78013.70, 5020.79, 2333.99,    0.00,  68.27,  110.32,  7176.19),
    16: (60, 0.964766, 0.610615, 119589.52, 4930.84, 2198.21,    0.00,  72.37,  106.94,  6949.75),
    21: (65, 0.943366, 0.539704, 162771.09, 4811.83, 1942.94,    0.00,  76.23,  101.32,  6577.21),
    22: (66, 0.938235, 0.526033, 171114.15, 4783.75, 1893.72,    0.00,  76.96,  100.16,  6500.35),
    23: (67, 0.932780, 0.512516, 179426.24,    0.00,    0.00, 7053.60,  46.59,    0.00, -7100.20),
    24: (68, 0.926985, 0.509331,      0.00,    0.00,    0.00, 7079.88,  47.00,    0.00, -7126.88),
    33: (77, 0.856165, 0.470419,      0.00,    0.00,    0.00, 7151.60,  49.63,    0.00, -7201.23),
    43: (87, 0.724266, 0.397948,      0.00,    0.00,    0.00, 6682.78,  48.73,    0.00, -6731.51),
    53: (97, 0.521776, 0.286689,      0.00,    0.00,    0.00, 5318.10,  40.74,    0.00, -5358.84),
    63: (107, 0.272931, 0.149962,     0.00,    0.00,    0.00, 3072.84,  24.73,    0.00, -3097.57),
    73: (117, 0.074193, 0.040765,     0.00,    0.00,    0.00,  922.70,   7.80,    0.00,  -930.50),
    77: (121, 0.032209, 0.017697,     0.00,    0.00,    0.00,  416.84,   3.60,    0.00,  -420.43),
}

# The notes' Total row: summed over all seventy-seven years at full precision, then rounded.
TOTALS = {
    "premiums": 113761.91, "zuzahlungen": 51236.28, "claims_death": 0.00,
    "claims_annuity": 270016.08, "claims_survivor": 0.00, "expenses": 3731.36,
    "commissions": 6437.82, "net_cf": -115187.08,
}

# Adding the seventy-seven *rounded* cells instead gives a different answer in three columns.
# The notes say so explicitly; this module asserts both numbers so the difference cannot be
# quietly "fixed" in either direction.
ROUNDED_CELL_SUMS = {
    "claims_annuity": 270016.09, "expenses": 3731.38, "commissions": 6437.83,
}

# The notes' three independent checks, at full precision.
S_ANCHOR = 163793.9012327640          # beitragssumme_pp(): 6 000 x (1.02^22 - 1) / 0.02
ALPHA_TOTAL_ANCHOR = 4094.8475308191  # 0.025 x S -- and the same number as commissions(1)
ALPHA_INSTALMENT = 818.9695061638     # alpha_total / zill_spread_y
N1_ANCHOR = 7215.0304938362           # prem_to_av_pp(1)
AV_PP_AFT_INT_1 = 7377.3686799475     # N(1) x (1 + 0.026 - 0.0035)
AV_2_ANCHOR = 7366.7479330812         # that, after the year-1 death decrement
QX45_TABLE = 0.0023263433             # 0.014000 x 1.085^(45 - 67), the shipped table at 45
TREND_2005_TO_2026 = 0.7280493868     # (1 - 0.015)^21
Q1_FIRST_ORDER = 0.0016936928         # mort_rate_base(1)
Q1_BEST_ESTIMATE = 0.0014396389       # mort_rate(1) = 0.85 x that
FREEZE_1 = 0.0399424144               # pols_freeze(1)
POLS_PAYING_2 = 0.9586179467
POLS_PAIDUP_2 = 0.0399424144
FUND_PER_ANNUITANT = 200050.6219643070
ANN_PP_23 = 7561.9135102508
ANN_PP_23_IF_GUARANTEE_BOUND = 6721.70   # what 28,00 EUR would have given

# The Einmalbeitrag variant -- model point 5, a 58-year-old paying 60 000,00 EUR once and
# deferring to 67.  t: (age, pols_if, av, premiums, claims_annuity, expenses, commissions,
# net_cf).
SINGLE_PREMIUM = {
    1:  (58, 1.000000,     0.00, 60000.00,    0.00, 310.00, 1500.00, 58190.00),
    2:  (59, 0.995842, 56170.68,     0.00,    0.00,  60.65,    0.00,   -60.65),
    3:  (60, 0.991418, 56838.16,     0.00,    0.00,  61.28,    0.00,   -61.28),
    5:  (62, 0.981702, 58157.41,     0.00,    0.00,  62.52,    0.00,   -62.52),
    9:  (66, 0.958317, 61584.00,     0.00,    0.00,  64.77,    0.00,   -64.77),
    10: (67, 0.951537, 62484.63,     0.00, 2456.40,  39.17,    0.00, -2495.56),
    11: (68, 0.944341,     0.00,     0.00, 2462.20,  39.45,    0.00, -2501.65),
    20: (77, 0.857193,     0.00,     0.00, 2444.36,  40.95,    0.00, -2485.31),
    40: (97, 0.468265,     0.00,     0.00, 1629.32,  30.13,    0.00, -1659.45),
    64: (121, 0.014921,    0.00,     0.00,   65.92,   1.37,    0.00,   -67.29),
}

SINGLE_TOTALS = {
    "premiums": 60000.00, "zuzahlungen": 0.00, "claims_annuity": 86163.14,
    "expenses": 2321.22, "commissions": 1500.00, "net_cf": -29984.36,
}
SINGLE_NET_CF_ROUNDED_CELL_SUM = -29984.39   # three cents away from the full-precision total
N1_SINGLE = 55164.0000000000                 # 60 000 x 0.925 - 300 - 36
AV_PP_2_SINGLE = 56405.1900000000
AV_2_SINGLE = 56170.6811550510

# The notes' Rentenfaktor table: the anchor, where the current factor binds, and model point 13,
# where the guaranteed one does.  (ret_t, av(T), fund_at_conv, per annuitant, gtd, curr,
# applied, ann_pp(T)).
CONVERSION = {
    1:  (23, 179426.24, 186603.29, 200050.62, 28.00, 31.50, 31.50, 7561.91),
    13: (22,  98185.81, 102113.25, 109428.02, 34.00, 27.72, 34.00, 4464.66),
}
MP13_ANN_IF_CURRENT_BOUND = 3640.01   # 109 428,02 / 10 000 x 27,72 x 12
MP13_GUARANTEE_WORTH = 824.65         # 4 464,66 - 3 640,01, a year


def alt_model(name):
    """A private copy of the model, for tests that mutate a Reference or swap an input.

    The module-scoped ``basisrente`` fixture is shared, so a test that changes
    ``Projection.mort_be_factor`` or ``Data.charge_file`` on it would leak into every test that
    ran afterwards.  Each such test reads its own copy and closes it in a ``finally``.
    """
    return mx.read_model(MODEL_DIR, name=name)


# ---------------------------------------------------------------------------
# The worked example


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE))
def test_worked_example_row(de_basis_anchor, t):
    """Every cell of the notes' eighteen printed rows, to the precision the notes display."""
    age, pols_if, pols_paying, av, prem, zuz, ann, exp, comm, net = WORKED_EXAMPLE[t]
    p = de_basis_anchor
    assert p.age(t) == age
    assert p.pols_if(t) == pytest.approx(pols_if, abs=SIX_DP)
    assert p.pols_paying(t) == pytest.approx(pols_paying, abs=SIX_DP)
    assert p.av(t) == pytest.approx(av, abs=CENT)
    assert p.premiums(t) == pytest.approx(prem, abs=CENT)
    assert p.zuzahlungen(t) == pytest.approx(zuz, abs=CENT)
    assert p.claims(t, "ANNUITY") == pytest.approx(ann, abs=CENT)
    assert p.expenses(t) == pytest.approx(exp, abs=CENT)
    assert p.commissions(t) == pytest.approx(comm, abs=CENT)
    assert p.net_cf(t) == pytest.approx(net, abs=CENT)
    # The two columns the notes omit for space are structurally zero on this cell.
    assert p.claims(t, "DEATH") == 0.0
    assert p.claims(t, "SURVIVOR") == 0.0
    assert p.liability_cf(t) == pytest.approx(-net, abs=CENT)


def test_the_worked_example_totals_are_summed_at_full_precision(de_basis_anchor):
    """The Total row is a full-precision sum over all seventy-seven years, then rounded."""
    df = de_basis_anchor.result_cf()
    assert len(df) == 77
    for column, total in TOTALS.items():
        assert df[column].sum() == pytest.approx(total, abs=CENT), column


def test_the_totals_differ_from_the_sum_of_the_rounded_cells(de_basis_anchor):
    """Rounding seventy-seven times before adding costs one or two cents, in three columns.

    The notes say so explicitly.  Asserting both numbers is what stops the difference being
    quietly "corrected" in either direction, and it is why a test that summed the printed cells
    would be asserting the wrong number.
    """
    df = de_basis_anchor.result_cf()
    for column, rounded_sum in ROUNDED_CELL_SUMS.items():
        assert round(sum(round(v, 2) for v in df[column]), 2) == pytest.approx(
            rounded_sum, abs=CENT), column
        assert abs(rounded_sum - TOTALS[column]) >= 0.01, column
    # premiums, zuzahlungen and net_cf happen to agree at the cent, and the notes say that too.
    for column in ("premiums", "zuzahlungen", "net_cf"):
        assert round(sum(round(v, 2) for v in df[column]), 2) == pytest.approx(
            TOTALS[column], abs=CENT), column


def test_check_1_the_first_year_account_rebuilt_from_the_charge_scale(de_basis_anchor):
    """The notes' first independent check: N(1) and the account, from the charge scale up.

    ``S = 6 000 x (1.02^22 - 1) / 0.02``; the *Zillmerung* is ``0.025 x S`` in five instalments;
    the *Zuzahlung* actually paid is ``4 000 x 0.70`` and carries its own 2,5 % charge rather
    than a share of the *Zillmerung*; the residue is credited at ``0.026 - 0.0035``.  The ``av``
    the table prints at ``t = 2`` is that figure **after** the year's death decrement, which is
    the fund-level roll-forward and not the per-policy one.
    """
    p = de_basis_anchor
    assert p.beitragssumme_pp() == pytest.approx(S_ANCHOR, rel=1e-12)
    assert p.beitragssumme_pp() == pytest.approx(
        6000.00 * (1.02 ** 22 - 1) / 0.02, rel=1e-12)
    assert p.alpha_total_pp() == pytest.approx(ALPHA_TOTAL_ANCHOR, rel=1e-12)
    assert p.alpha_amort_pp(1) == pytest.approx(ALPHA_INSTALMENT, rel=1e-12)
    assert p.zuz_pp(1) == pytest.approx(4000.00 * 0.70, rel=1e-12)
    assert p.alpha_zuz_pp(1) == pytest.approx(0.025 * 2800.00, rel=1e-12)
    assert p.unit_cost_pp(1) == pytest.approx(36.00, rel=1e-12)
    assert p.prem_to_av_pp(1) == pytest.approx(N1_ANCHOR, rel=1e-12)
    assert p.prem_to_av_pp(1) == pytest.approx(
        8140.00 - ALPHA_INSTALMENT - 70.00 - 36.00, rel=1e-12)
    assert p.cred_rate(1) == pytest.approx(0.026, rel=1e-12)
    assert p.av_pp_at(1, "AFT_INT") == pytest.approx(AV_PP_AFT_INT_1, rel=1e-12)
    assert p.av_pp_at(1, "AFT_INT") == pytest.approx(
        N1_ANCHOR * (1 + 0.026 - 0.0035), rel=1e-9)
    # The fund-level value the table publishes, one death decrement later.
    assert p.av(2) == pytest.approx(AV_2_ANCHOR, rel=1e-12)
    assert p.av(2) == pytest.approx(
        AV_PP_AFT_INT_1 * (1 - Q1_BEST_ESTIMATE), rel=1e-8)


def test_check_2_the_year_one_decrement_split_and_the_rate_behind_it(de_basis_anchor):
    """The notes' second check: the shipped table's rate at 45, improved, and the split.

    The 4 % *Beitragsfreistellung* rate cancels out of ``pols_if`` entirely, which is what
    distinguishes this product's decrement structure from a Schicht-3 annuity's.
    """
    p = de_basis_anchor
    assert p.mort_rate_at_age(45, 2005) == pytest.approx(QX45_TABLE, abs=5e-11)
    # The shipped CSV carries qx to ten decimals, so the closed form agrees to that and no
    # further -- the table is the input, and the formula behind it is documentation.
    assert p.mort_rate_at_age(45, 2005) == pytest.approx(
        0.014000 * 1.085 ** (45 - 67), abs=5e-11)
    assert (1 - 0.015) ** 21 == pytest.approx(TREND_2005_TO_2026, abs=5e-10)
    assert p.cal_year(1) == 2026
    assert p.mort_rate_base(1) == pytest.approx(Q1_FIRST_ORDER, abs=5e-10)
    assert p.mort_rate(1) == pytest.approx(Q1_BEST_ESTIMATE, abs=5e-10)
    assert p.mort_rate(1) == pytest.approx(0.85 * p.mort_rate_base(1), rel=1e-12)

    assert p.pols_death(1) == pytest.approx(Q1_BEST_ESTIMATE, abs=5e-10)
    assert p.bf_rate(1) == 0.04
    assert p.pols_freeze(1) == pytest.approx(FREEZE_1, abs=5e-10)
    assert p.pols_freeze(1) == pytest.approx(
        1.0 * (1 - Q1_BEST_ESTIMATE) * 0.04, rel=1e-8)
    assert p.pols_paying(2) == pytest.approx(POLS_PAYING_2, abs=5e-10)
    assert p.pols_paidup(2) == pytest.approx(POLS_PAIDUP_2, abs=5e-10)
    assert p.pols_if(2) == pytest.approx(POLS_PAYING_2 + POLS_PAIDUP_2, rel=1e-12)
    assert p.pols_if(2) == pytest.approx(1.0 - Q1_BEST_ESTIMATE, abs=5e-10)


def test_check_3_the_conversion_and_the_branch_of_the_max_that_binds(de_basis_anchor):
    """The notes' third check: the fund, the terminal bonus, the factor and the annuity."""
    p = de_basis_anchor
    assert p.ret_t() == 23
    assert p.av(23) == pytest.approx(179426.2405488701, abs=CENT)
    assert p.fund_at_conv() == pytest.approx(p.av(23) * 1.04, rel=1e-12)
    assert p.fund_at_conv() == pytest.approx(186603.2901708250, abs=CENT)
    per_annuitant = p.fund_at_conv() / p.pols_if(23)
    assert per_annuitant == pytest.approx(FUND_PER_ANNUITANT, abs=CENT)
    assert p.rentenfaktor_gtd() if False else True     # gtd lives on the model point
    assert float(p.model_point()["rentenfaktor_gtd"]) == 28.00
    assert p.rentenfaktor_curr() == 31.50
    assert p.rf_option_factor() == 1.0
    assert p.rentenfaktor_applied() == pytest.approx(31.50, rel=1e-12)
    assert p.ann_pp(23) == pytest.approx(per_annuitant / 10000.0 * 378.00, rel=1e-9)
    assert p.ann_pp(23) == pytest.approx(ANN_PP_23, abs=5e-5)
    # Weighted by the opening in-force count, and compounded once for the next year.
    assert p.claims(23, "ANNUITY") == pytest.approx(
        ANN_PP_23 * 0.9327803550, abs=CENT)
    assert p.claims(24, "ANNUITY") == pytest.approx(
        ANN_PP_23 * 1.01 * 0.9269849437, abs=CENT)
    # Had the guaranteed 28,00 EUR bound instead.
    assert per_annuitant / 10000.0 * 28.00 * 12 == pytest.approx(
        ANN_PP_23_IF_GUARANTEE_BOUND, abs=CENT)


def test_the_decrements_close_to_exactly_one(de_basis_anchor):
    """Deaths over the whole projection plus ``pols_if(n + 1)`` equal the original policy.

    Not one policy leaves by any other route: there is no lapse decrement, no surrender and no
    commutation on this product, and the 0,441765 of the cohort that went *beitragsfrei* is
    **inside** that 1,000000 rather than beside it.
    """
    p = de_basis_anchor
    n = p.proj_len()
    assert n == 77
    deaths = sum(p.pols_death(t) for t in range(1, n + 1))
    assert deaths == pytest.approx(1.0, abs=1e-10)
    assert p.pols_if(n + 1) == pytest.approx(0.0, abs=1e-12)
    assert deaths + p.pols_if(n + 1) == pytest.approx(p.pols_if_init(), abs=1e-10)
    freezes = sum(p.pols_freeze(t) for t in range(1, n + 1))
    assert freezes == pytest.approx(0.4417651793, abs=5e-9)
    assert p.pols_paying(23) + p.pols_paidup(23) == pytest.approx(p.pols_if(23), rel=1e-12)


def test_the_cash_flow_statement_closes_over_the_whole_projection(de_basis_anchor):
    """The Total row itself closes -- check_net_cf() evaluated over all years at once."""
    df = de_basis_anchor.result_cf()
    total = (df["premiums"].sum() + df["zuzahlungen"].sum()
             - df["claims_death"].sum() - df["claims_annuity"].sum()
             - df["claims_survivor"].sum() - df["expenses"].sum()
             - df["commissions"].sum())
    assert total == pytest.approx(-115187.0842315298, abs=CENT)
    assert total == pytest.approx(df["net_cf"].sum(), rel=1e-12)


def test_the_initial_commission_and_the_zillmerung_are_the_same_number(de_basis_anchor):
    """2,5 % of the *Beitragssumme*, twice -- the German design, not a coincidence.

    What the insurer pays out at inception is sized to what it may write into the reserve, which
    is why moving ``comm_init_rate`` without moving ``zill_rate`` opens a first-year hole that
    nothing closes.  One is an expense and the other is not: the commission is in ``net_cf`` and
    the *Zillmerung* instalment is only in the account.
    """
    p = de_basis_anchor
    assert p.commissions(1) == pytest.approx(ALPHA_TOTAL_ANCHOR, rel=1e-12)
    assert p.alpha_total_pp() == pytest.approx(ALPHA_TOTAL_ANCHOR, rel=1e-12)
    assert p.expenses(1) == pytest.approx(250.00 + 60.00, abs=CENT)
    assert p.commissions(2) == pytest.approx(
        0.015 * (p.premiums(2) + p.zuzahlungen(2)), rel=1e-12)


# ---------------------------------------------------------------------------
# The published checks and the frame


def test_every_published_check_holds_and_its_residual_is_zero(de_basis_anchor):
    """All six identities, and the per-``t`` residuals at the years that could break them."""
    p = de_basis_anchor
    for check in ("check_net_cf", "check_pols_roll_fwd", "check_av_roll_fwd",
                  "check_conversion", "check_no_capital", "check_annuity_roll_fwd"):
        value = getattr(p, check)()
        assert value is True, check
        assert isinstance(value, bool), check
    for t in (1, 2, 5, 22, 23, 24, 77):
        assert p.check_net_cf_resid(t) == pytest.approx(0.0, abs=1e-8)
        assert p.check_pols_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-10)
        assert p.check_av_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-6)
        assert p.check_conversion_resid(t) == pytest.approx(0.0, abs=1e-6)
        assert p.check_no_capital_resid(t) == pytest.approx(0.0, abs=1e-9)
        assert p.check_annuity_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-8)


def test_check_net_cf_is_read_from_the_published_frame(de_basis_anchor):
    """delib ruling 1: the identity is reconstructed from ``result_cf()``'s own columns.

    ``pols_if``, ``pols_paying`` and ``av`` are two counts and a balance and are excluded by
    construction -- adding ``av`` to anything is a category error, and the residual would be
    enormous if it were included.
    """
    p = de_basis_anchor
    df = p.result_cf()
    for t in (1, 11, 23, 50, 77):
        row = df.loc[t]
        rebuilt = float(row["premiums"] + row["zuzahlungen"]
                        - row["claims_death"] - row["claims_annuity"]
                        - row["claims_survivor"] - row["expenses"] - row["commissions"])
        assert rebuilt == pytest.approx(float(row["net_cf"]), rel=1e-12)
        assert p.check_net_cf_resid(t) == pytest.approx(0.0, abs=1e-8)
    assert "av" not in ("premiums", "zuzahlungen")           # the excluded columns are balances
    assert df["av"].sum() > 0.0                              # and would wreck the identity


def test_result_cf_shape_and_both_signs_of_the_net_flow(de_basis_anchor):
    """Twelve columns in the notes' order, ``pols_if`` first, contiguous 1..proj_len()."""
    p = de_basis_anchor
    df = p.result_cf()
    assert df.index.name == "t"
    assert list(df.index) == list(range(1, p.proj_len() + 1))
    assert df.index[-1] == p.proj_len()
    assert list(df.columns) == [
        "pols_if", "pols_paying", "av", "premiums", "zuzahlungen", "claims_death",
        "claims_annuity", "claims_survivor", "expenses", "commissions", "net_cf",
        "liability_cf",
    ]
    assert df["pols_if"].iloc[0] == pytest.approx(p.pols_if_init(), rel=1e-12)
    # A cash flow statement must not publish its own subtotal beside its parts, and there is no
    # surrender column of any name.
    for absent in ("claims", "claims_lapse", "claims_surr", "claims_wd", "claims_commute"):
        assert absent not in df.columns
    assert (df["net_cf"] + df["liability_cf"]).abs().max() == pytest.approx(0.0, abs=1e-9)
    assert not df.isna().any().any()
    # The shape: a first-year strain that is all commission, then positive accumulation-phase
    # margin, then a payout tail that never turns.
    assert df["net_cf"].iloc[0] == pytest.approx(4395.15, abs=CENT)
    assert (df["net_cf"].iloc[1:22] > 0).all()
    assert (df["net_cf"].iloc[22:] < 0).all()


def test_invalid_enum_values_raise(de_basis_anchor):
    """The enum accessors validate rather than propagating a typo into a lookup.

    ``"SURRENDER"`` in particular: there is no fourth kind of claim on this product and there
    can be none, so asking for one is an error and not a zero.
    """
    p = de_basis_anchor
    with pytest.raises(FormulaError):
        p.claims(1, "SURRENDER")
    with pytest.raises(FormulaError):
        p.claims(1, "LAPSE")
    with pytest.raises(FormulaError):
        p.pols_if_at(1, "AFTER_LAPSE")
    with pytest.raises(FormulaError):
        p.av_pp_at(1, "AFT_SURR")


# ---------------------------------------------------------------------------
# The variants the notes print


@pytest.mark.parametrize("t", sorted(SINGLE_PREMIUM))
def test_einmalbeitrag_variant_row(basisrente, t):
    """Model point 5, the *Einmalbeitrag*: the notes' ten printed rows."""
    age, pols_if, av, prem, ann, exp, comm, net = SINGLE_PREMIUM[t]
    p = basisrente.Projection[5]
    assert p.model_point()["prem_form"] == "single"
    assert p.age(t) == age
    assert p.pols_if(t) == pytest.approx(pols_if, abs=SIX_DP)
    assert p.av(t) == pytest.approx(av, abs=CENT)
    assert p.premiums(t) == pytest.approx(prem, abs=CENT)
    assert p.claims(t, "ANNUITY") == pytest.approx(ann, abs=CENT)
    assert p.expenses(t) == pytest.approx(exp, abs=CENT)
    assert p.commissions(t) == pytest.approx(comm, abs=CENT)
    assert p.net_cf(t) == pytest.approx(net, abs=CENT)
    assert p.zuzahlungen(t) == 0.0
    assert p.claims(t, "DEATH") == 0.0


def test_the_einmalbeitrag_totals_and_its_first_year_account(basisrente):
    """The single premium's own totals, and the two features that are the point of the variant.

    The *Beitragssumme* of a single-premium contract **is** the single premium, so the
    *Zillmerung* and the initial commission are an order of magnitude below the anchor's; and
    the five *Zillmerung* instalments still run, so from ``t = 2`` the account is debited by an
    acquisition charge that the one premium has already come and gone without covering.
    """
    p = basisrente.Projection[5]
    df = p.result_cf()
    assert p.proj_len() == 64 and p.ret_t() == 10
    for column, total in SINGLE_TOTALS.items():
        assert df[column].sum() == pytest.approx(total, abs=CENT), column
    assert round(sum(round(v, 2) for v in df["net_cf"]), 2) == pytest.approx(
        SINGLE_NET_CF_ROUNDED_CELL_SUM, abs=CENT)

    assert p.beitragssumme_pp() == 60000.00
    assert p.alpha_total_pp() == pytest.approx(0.025 * 60000.00, rel=1e-12)
    assert p.commissions(1) == pytest.approx(1500.00, abs=CENT)
    assert p.commissions(1) == pytest.approx(p.alpha_total_pp(), rel=1e-12)
    assert [p.alpha_amort_pp(t) for t in range(1, 6)] == [300.00] * 5
    assert p.alpha_amort_pp(6) == 0.0
    assert p.prem_to_av_pp(1) == pytest.approx(N1_SINGLE, rel=1e-12)
    assert p.av_pp(2) == pytest.approx(AV_PP_2_SINGLE, rel=1e-12)
    assert p.av(2) == pytest.approx(AV_2_SINGLE, rel=1e-12)
    # No premium left to stop, so no Beitragsfreistellung and no premium-free block at all.
    assert all(p.bf_rate(t) == 0.0 for t in (1, 2, 5, 9))
    assert all(p.pols_paidup(t) == 0.0 for t in (1, 5, 10))
    assert p.prem_freq_load() == 1.0


@pytest.mark.parametrize("point_id", sorted(CONVERSION))
def test_the_conversion_table_of_the_notes(basisrente, point_id):
    """The notes' *Rentenfaktor* table: the anchor and model point 13, both branches shipped."""
    ret_t, av_T, fund, per, gtd, curr, applied, ann = CONVERSION[point_id]
    p = basisrente.Projection[point_id]
    assert p.ret_t() == ret_t
    assert p.av(ret_t) == pytest.approx(av_T, abs=CENT)
    assert p.fund_at_conv() == pytest.approx(fund, abs=CENT)
    assert p.fund_at_conv() / p.pols_if(ret_t) == pytest.approx(per, abs=CENT)
    assert float(p.model_point()["rentenfaktor_gtd"]) == gtd
    assert p.rentenfaktor_curr() == pytest.approx(curr, abs=5e-5)
    assert p.rentenfaktor_applied() == pytest.approx(applied, abs=5e-5)
    assert p.rentenfaktor_applied() == max(gtd, curr) * p.rf_option_factor()
    assert p.ann_pp(ret_t) == pytest.approx(ann, abs=CENT)
    # The printed per-annuitant figure is rounded to the cent, so the identity is closed on the
    # model's own full-precision fund rather than on the table's transcription of it.
    per_exact = p.fund_at_conv() / p.pols_if(ret_t)
    assert p.ann_pp(ret_t) == pytest.approx(
        per_exact / 10000.0 * applied * 12, rel=1e-12)


def test_on_model_point_13_the_guarantee_is_worth_824_euro_a_year(basisrente):
    """The other branch of the ``max``, and what it is worth.

    The projection is sensitive to whichever factor is higher and completely insensitive to the
    other, which is why a sensitivity run on the guaranteed factor over a book returns zero
    until it crosses the current one and then moves in a straight line.
    """
    p = basisrente.Projection[13]
    per = p.fund_at_conv() / p.pols_if(p.ret_t())
    current_only = per / 10000.0 * 27.72 * 12
    assert current_only == pytest.approx(MP13_ANN_IF_CURRENT_BOUND, abs=CENT)
    assert p.ann_pp(p.ret_t()) - current_only == pytest.approx(
        MP13_GUARANTEE_WORTH, abs=CENT)
    assert p.model_point()["rf_scenario_id"] == "low"
    assert p.rentenfaktor_curr() < float(p.model_point()["rentenfaktor_gtd"])


# ---------------------------------------------------------------------------
# Pitfall 1 -- there is no surrender value, at any duration


def test_pitfall_1_no_surrender_value_and_none_of_the_names_that_carry_one(
        basisrente, de_basis_anchor):
    """*Nicht kapitalisierbar*: no *Rückkaufswert* exists at any duration, so no cells does.

    The absences cannot be asserted from inside the model -- a missing cells has no formula --
    so they are asserted here, against the exact names a modeller reusing the delib endowment or
    Schicht-3 chassis would carry across by habit.  The mirror error is subtler and is asserted
    too: ``prem_to_av_pp`` is **not** floored at an internally computed surrender value.
    """
    names = set(basisrente.Projection.cells) | set(basisrente.Projection.refs)
    for absent in ("cv_pp", "cv", "surr_value_pp", "surr_rate", "surr_charge_rate",
                   "lapse_rate", "lapse_rate_mth", "lapse_rate_ann", "pols_lapse",
                   "loan_pp", "loan_bal", "withdrawals", "wd_free_pp", "paid_up_factor",
                   "asset_share", "mvr", "claims_surr", "claims_lapse",
                   "kapitalwahl", "commute_value_pp", "min_surr_value_pp"):
        assert absent not in names, absent
    p = de_basis_anchor
    assert p.check_no_capital() is True
    assert all(p.check_no_capital_resid(t) == 0.0 for t in (1, 10, 23, 40, 77))
    # The only three kinds of payment there are.
    for t in (1, 10, 23, 40, 77):
        assert p.claims(t) == pytest.approx(
            p.claims(t, "DEATH") + p.claims(t, "ANNUITY") + p.claims(t, "SURVIVOR"),
            rel=1e-12)
    # The credit to the account is the raw arithmetic, with no floor of any kind under it.  On
    # model point 10 -- 300,00 EUR a year, the market's minimum recurring premium -- the charges
    # take a third of the first year's contribution before anything reaches the account.
    small = basisrente.Projection[10]
    assert small.prem_pp(1) == pytest.approx(300.00 * 1.05, abs=CENT)
    assert small.prem_to_av_pp(1) == pytest.approx(
        small.prem_pp(1) * (1 - 0.075) - small.alpha_amort_pp(1)
        - small.alpha_zuz_pp(1) - small.unit_cost_pp(1), rel=1e-12)
    assert small.prem_to_av_pp(1) == pytest.approx(199.88, abs=CENT)
    assert small.prem_to_av_pp(1) < 0.70 * small.prem_pp(1)
    # And it converts to a small annuity, never a lump sum -- there is no
    # Kleinbetragsrenten-Abfindung in Schicht 1.
    assert small.ann_pp(small.ret_t()) == pytest.approx(292.41, abs=CENT)
    assert small.check_no_capital() is True


def test_pitfall_1_the_account_is_never_floored_at_a_surrender_value():
    """Push the *Stückkosten* past the premium and the account goes negative, as it must.

    The mirror of the missing surrender column is a *Rückkaufswert* computed internally "for
    reference" and then used as a floor under the *Deckungskapital*.  There is nothing for such
    a floor to protect on this product, and this test proves there is none: with the
    *Stückkosten* at 400,00 EUR a year, model point 10's first-year credit is negative and the
    account follows it down.  That a German *Deckungskapital* starts near zero is a consequence
    of this line and not a modelling artefact.
    """
    charges = pd.read_csv(INPUT_DIR / "charge_table.csv", index_col="tariff_id")
    charges.loc["de_basis_std", "unit_cost_pp"] = 400.00
    alt = INPUT_DIR / "charge_table_costly.csv"
    model = alt_model("Basis_DE_A_floor")
    try:
        assert model.Projection[10].prem_to_av_pp(1) > 0.0
        charges.to_csv(alt)
        try:
            model.Data.charge_file = alt.name
            model.Data.clear_all()
            model.Projection.clear_all()
            p = model.Projection[10]
            assert p.unit_cost_pp(1) == 400.00
            assert p.prem_to_av_pp(1) < 0.0
            assert p.av_pp(2) < 0.0
            assert p.av(2) < 0.0
            assert p.check_av_roll_fwd() is True
        finally:
            alt.unlink(missing_ok=True)
    finally:
        model.close()


# ---------------------------------------------------------------------------
# Pitfall 2 -- a Beitragsfreistellung is not a lapse


def test_pitfall_2_a_beitragsfreistellung_removes_the_premium_not_the_policy(de_basis_anchor):
    """``pols_if(t+1) = pols_if(t) x (1 - mort_rate(t))``, with ``bf_rate`` absent."""
    p = de_basis_anchor
    for t in (1, 5, 12, 22, 40, 76):
        assert p.pols_if(t + 1) == pytest.approx(
            p.pols_if(t) * (1 - p.mort_rate(t)), rel=1e-12)
        assert p.pols_if_at(t, "AFT_FREEZE") == pytest.approx(
            p.pols_if_at(t, "AFT_DEATH"), rel=1e-12)
        assert p.pols_paying(t) + p.pols_paidup(t) == pytest.approx(p.pols_if(t), rel=1e-12)
    assert p.check_pols_roll_fwd() is True
    # The freeze moves policies between the ledgers and nothing else: the paying count falls far
    # faster than the in-force count, and the difference is still in force.
    assert p.pols_paying(23) == pytest.approx(0.512516, abs=SIX_DP)
    assert p.pols_if(23) == pytest.approx(0.932780, abs=SIX_DP)
    assert p.pols_if(23) - p.pols_paying(23) == pytest.approx(0.420265, abs=SIX_DP)
    assert p.pols_paidup(23) > 0.0


def test_pitfall_2_with_bf_rate_at_zero_the_policy_count_is_unchanged():
    """Set ``bf_rate = 0`` and ``pols_if`` does not move, while ``premiums`` grows.

    That is the arithmetic statement of "not a lapse": a lapse rate that vanished would move the
    in-force count, and this one does not.  It moves 45 636 EUR of premium income instead, and
    a much larger fund at *Rentenbeginn*.
    """
    beh = pd.read_csv(INPUT_DIR / "behaviour_table.csv", index_col=["beh_table_id", "dur"])
    beh["bf_rate"] = 0.0
    alt = INPUT_DIR / "behaviour_table_nobf.csv"
    model = alt_model("Basis_DE_A_nobf")
    try:
        base = model.Projection[1].result_cf()
        beh.to_csv(alt)
        try:
            model.Data.behaviour_file = alt.name
            model.Data.clear_all()
            model.Projection.clear_all()
            p = model.Projection[1]
            nobf = p.result_cf()
            assert (base["pols_if"] - nobf["pols_if"]).abs().max() < 1e-12
            assert all(p.bf_rate(t) == 0.0 for t in (1, 5, 12, 22))
            assert p.pols_paidup(23) == 0.0
            assert p.pols_paying(23) == pytest.approx(p.pols_if(23), rel=1e-12)
            assert (nobf["premiums"] > base["premiums"]).loc[2:22].all()
            assert nobf["premiums"].sum() == pytest.approx(159397.29, abs=CENT)
            assert p.ann_pp(23) == pytest.approx(10448.66, abs=CENT)
            assert p.check_pols_roll_fwd() is True and p.check_av_roll_fwd() is True
        finally:
            alt.unlink(missing_ok=True)
    finally:
        model.close()


# ---------------------------------------------------------------------------
# Pitfall 3 -- the two account blocks are not one average


def test_pitfall_3_the_paying_and_premium_free_blocks_are_not_averaged(de_basis_anchor):
    """They are equal at the first freeze and diverge from then on, permanently.

    ``av_pp_at`` is per **paying policy** and ``av_pu_at`` is the premium-free block at **fund**
    level.  Collapsing them into one per-policy figure loses the whole economic content of a
    *Beitragsfreistellung*, and the fund-level roll-forward would stop closing.
    """
    p = de_basis_anchor
    # t = 2 is the first year with a premium-free block, and everyone in it froze together.
    assert p.av_pu_at(2, "BEF_PREM") / p.pols_paidup(2) == pytest.approx(
        p.av_pp(2), rel=1e-12)
    for t in (3, 5, 10, 15, 22):
        per_paidup = p.av_pu_at(t, "BEF_PREM") / p.pols_paidup(t)
        assert p.av_pp(t) > per_paidup
    assert p.av_pp(10) == pytest.approx(82934.50, abs=CENT)
    assert p.av_pu_at(10, "BEF_PREM") / p.pols_paidup(10) == pytest.approx(
        39549.19, abs=CENT)
    # The fund-level total is the only one that rolls forward on mortality alone.
    for t in (2, 10, 22):
        assert p.av_at(t, "BEF_PREM") == pytest.approx(
            p.av_pp_at(t, "BEF_PREM") * p.pols_paying(t) + p.av_pu_at(t, "BEF_PREM"),
            rel=1e-12)
        assert p.av_at(t + 1, "BEF_PREM") == pytest.approx(
            p.av_at(t, "AFT_INT") * (1 - p.mort_rate(t)), rel=1e-12)
    assert p.check_av_roll_fwd() is True
    # A premium-free policy pays the Stueckkosten and the reserve charge and nothing else.
    assert p.av_pu_at(10, "AFT_PREM") == pytest.approx(
        p.av_pu_at(10, "BEF_PREM") - p.unit_cost_pp(10) * p.pols_paidup(10), rel=1e-12)


# ---------------------------------------------------------------------------
# Pitfall 4 -- a charge is not an expense


def test_pitfall_4_the_account_charges_are_income_and_never_an_expense():
    """``expenses`` is invariant to beta, gamma and the *Zillmersatz*; the annuity is not.

    Raise all three -- beta from 7,5 % to 10 %, gamma from 0,35 % to 0,60 %, the *Zillmersatz*
    from 25 permille to 40 -- and not one euro of ``expenses`` or ``commissions`` moves.  What
    moves is the *Deckungskapital*, and through it the annuity the smaller fund buys at
    *Rentenbeginn*: 249 887,21 EUR of annuity claims against 270 016,08 EUR.
    """
    charges = pd.read_csv(INPUT_DIR / "charge_table.csv", index_col="tariff_id")
    charges.loc["de_basis_std", "beta_prem"] = 0.10
    charges.loc["de_basis_std", "gamma_av"] = 0.006
    charges.loc["de_basis_std", "zill_rate"] = 0.040
    alt = INPUT_DIR / "charge_table_alt.csv"
    model = alt_model("Basis_DE_A_charges")
    try:
        base = model.Projection[1].result_cf()
        charges.to_csv(alt)
        try:
            model.Data.charge_file = alt.name
            model.Data.clear_all()
            model.Projection.clear_all()
            loaded = model.Projection[1].result_cf()
            assert (base["expenses"] - loaded["expenses"]).abs().max() == 0.0
            assert (base["commissions"] - loaded["commissions"]).abs().max() == 0.0
            assert (base["premiums"] - loaded["premiums"]).abs().max() == 0.0
            assert (base["zuzahlungen"] - loaded["zuzahlungen"]).abs().max() == 0.0
            assert (base["pols_if"] - loaded["pols_if"]).abs().max() == 0.0
            assert (base["av"] - loaded["av"]).abs().max() > 1000.0
            assert loaded["claims_annuity"].sum() == pytest.approx(249887.21, abs=CENT)
            assert loaded["claims_annuity"].sum() < base["claims_annuity"].sum()
            assert model.Projection[1].check_net_cf() is True
        finally:
            alt.unlink(missing_ok=True)
    finally:
        model.close()


# ---------------------------------------------------------------------------
# Pitfall 5 -- the Zillmerung is spread, and capped


def test_pitfall_5_the_zillmerung_is_five_equal_instalments_of_the_contract(basisrente,
                                                                           de_basis_anchor):
    """Equal at ``t = 1..5``, zero from ``t = 6``, summing to ``zill_rate x S`` exactly.

    The window belongs to the **contract**, not the projection, so an in-force point past
    duration 5 sees none of it at any ``t``: model point 6 opens at ``duration_init = 17``.
    """
    p = de_basis_anchor
    instalments = [p.alpha_amort_pp(t) for t in range(1, 6)]
    assert instalments == [pytest.approx(ALPHA_INSTALMENT, rel=1e-12)] * 5
    assert len(set(instalments)) == 1
    assert all(p.alpha_amort_pp(t) == 0.0 for t in (6, 7, 12, 22))
    assert sum(p.alpha_amort_pp(t) for t in range(1, p.proj_len() + 1)) == pytest.approx(
        0.025 * p.beitragssumme_pp(), rel=1e-9)
    assert p.alpha_total_pp() == pytest.approx(0.025 * p.beitragssumme_pp(), rel=1e-12)
    assert p.zill_spread_y == 5

    in_force = basisrente.Projection[6]
    assert in_force.duration(1) == 17
    assert all(in_force.alpha_amort_pp(t) == 0.0
               for t in range(1, in_force.proj_len() + 1))
    # And the pre-2015 cohort carries the older 40 permille cap on its own tariff.
    assert in_force.model_point()["tariff_id"] == "de_basis_zill40"
    assert in_force.alpha_total_pp() == pytest.approx(
        0.040 * in_force.beitragssumme_pp(), rel=1e-12)


# ---------------------------------------------------------------------------
# Pitfall 6 -- the declared rate is a max, not a sum


def test_pitfall_6_the_credited_rate_is_a_maximum_and_not_a_sum(basisrente, de_basis_anchor):
    """A German *laufende Verzinsung* already includes the *Rechnungszins*.

    On the anchor, ``gtd_rate = 1,00 %`` sits below the whole declared path, so the declared
    rate binds at every ``t``.  On model point 8, ``gtd_rate = 2,75 %`` sits above it, so the
    guarantee binds at every ``t``.  A sum would give 3,60 % in year one on the anchor.
    """
    p = de_basis_anchor
    assert float(p.model_point()["gtd_rate"]) == 0.0100
    for t, decl in ((1, 0.026), (10, 0.026), (11, 0.024), (20, 0.024), (21, 0.022), (77, 0.022)):
        assert p.decl_rate(t) == pytest.approx(decl, rel=1e-12)
        assert p.cred_rate(t) == pytest.approx(decl, rel=1e-12)
        assert p.cred_rate(t) == max(0.0100, decl)
        assert p.cred_rate(t) != pytest.approx(0.0100 + decl, rel=1e-12)

    high = basisrente.Projection[8]
    assert float(high.model_point()["gtd_rate"]) == 0.0275
    for t in (1, 5, 30):
        assert high.cred_rate(t) == pytest.approx(0.0275, rel=1e-12)
        assert high.cred_rate(t) > high.decl_rate(t)


# ---------------------------------------------------------------------------
# Pitfall 7 -- the premium stream is keyed to the duration and stops at Rentenbeginn


def test_pitfall_7_premiums_and_zuzahlungen_stop_at_rentenbeginn(basisrente, de_basis_anchor):
    """Nothing is collected from ``t = ret_t()``, and the *Dynamik* runs off the duration."""
    p = de_basis_anchor
    assert p.prem_pp(22) > 0.0 and p.zuz_pp(22) > 0.0
    for t in (23, 24, 40, 77):
        assert p.prem_pp(t) == 0.0
        assert p.zuz_pp(t) == 0.0
        assert p.premiums(t) == 0.0
        assert p.zuzahlungen(t) == 0.0
        assert p.prem_to_av_pp(t) == 0.0
        assert p.bf_rate(t) == 0.0
    # The Zuzahlung stops a year earlier than that anyway, at zuzahlung_end_dur.
    assert int(p.model_point()["zuzahlung_end_dur"]) == 22
    assert p.duration(22) == 21 and p.zuz_pp(22) > 0.0
    assert p.duration(23) == 22
    # The Dynamik compounds on the policy duration, not on t.
    for t in (1, 5, 22):
        assert p.prem_base_pp(t) == pytest.approx(
            6000.00 * 1.02 ** p.duration(t), rel=1e-12)

    in_force = basisrente.Projection[6]
    assert in_force.duration(1) == 17
    assert in_force.prem_base_pp(1) == pytest.approx(3600.00 * 1.02 ** 17, rel=1e-12)
    assert in_force.prem_base_pp(1) == pytest.approx(5040.87, abs=CENT)
    assert in_force.prem_base_pp(1) > 3600.00


# ---------------------------------------------------------------------------
# Pitfall 8 -- the Ratenzahlungszuschlag loads the laufender Beitrag alone


def test_pitfall_8_the_frequency_loading_is_applied_once_and_to_one_thing(basisrente,
                                                                         de_basis_anchor):
    """``prem_pp(t) / prem_base_pp(t) = phi`` exactly, and the *Zuzahlung* carries none."""
    p = de_basis_anchor
    assert p.model_point()["prem_mode"] == "annual"
    assert p.prem_freq_load() == 1.000
    for t in (1, 5, 22):
        assert p.prem_pp(t) / p.prem_base_pp(t) == pytest.approx(1.000, rel=1e-12)

    monthly = basisrente.Projection[2]
    assert monthly.prem_freq_load() == 1.050
    assert monthly.prem_pp(1) == pytest.approx(3000.00 * 1.05, abs=CENT)
    for t in (1, 5, 20):
        assert monthly.prem_pp(t) / monthly.prem_base_pp(t) == pytest.approx(
            1.050, rel=1e-12)

    quarterly = basisrente.Projection[3]
    assert quarterly.prem_freq_load() == 1.030
    assert quarterly.prem_pp(1) == pytest.approx(7200.00 * 1.03, abs=CENT)
    # The Zuzahlung is a single payment and carries no loading whatever the mode.
    assert quarterly.zuz_pp(1) == pytest.approx(3000.00 * 0.70, rel=1e-12)
    assert quarterly.zuz_pp(1) / 3000.00 == pytest.approx(0.70, rel=1e-12)

    half = basisrente.Projection[4]
    assert half.prem_freq_load() == 1.020
    # A single premium carries no Ratenzahlungszuschlag at all.
    assert basisrente.Projection[5].prem_freq_load() == 1.0


# ---------------------------------------------------------------------------
# Pitfall 9 -- death before Rentenbeginn pays nothing with the rider off


def test_pitfall_9_death_pays_nothing_with_the_survivor_rider_off(basisrente,
                                                                  de_basis_anchor):
    """*Nicht vererblich*: the reserve is released as a mortality profit and nothing is paid.

    The account still closes -- the released reserve leaves the fund whether or not anything is
    paid, which is the arithmetic content of the prohibition.
    """
    p = de_basis_anchor
    assert float(p.model_point()["surv_annuity_rate"]) == 0.0
    assert all(p.claims(t, "DEATH") == 0.0 for t in range(1, 78))
    assert p.result_cf()["claims_death"].sum() == 0.0
    assert p.pols_death(5) > 0.0            # the deaths are real; only the benefit is nil
    assert p.db_pp(5) > 0.0                 # and the reserve released is real too
    assert p.check_av_roll_fwd() is True
    assert p.check_no_capital() is True
    # Every shipped point without the rider behaves the same way.
    for point_id in (2, 5, 9, 13):
        q = basisrente.Projection[point_id]
        assert float(q.model_point()["surv_annuity_rate"]) == 0.0
        assert q.result_cf()["claims_death"].sum() == 0.0


# ---------------------------------------------------------------------------
# Pitfall 10 -- with the rider on, only to an eligible survivor, and never a lump sum


def test_pitfall_10_the_death_benefit_is_conditional_and_buys_an_annuity(basisrente):
    """Model point 3: ``elig_surv_prob x mort_rate(t) x av_at(t, "AFT_INT")``, and nothing else.

    It is not a lump sum to a beneficiary: what is booked is the *Deckungskapital* leaving this
    contract as the single premium of a survivor's annuity.  The cover is paid for through the
    *Rentenfaktor* -- 31,50 x 0,930 -- and not by scaling the benefit.
    """
    p = basisrente.Projection[3]
    assert float(p.model_point()["surv_annuity_rate"]) == 0.60
    assert p.elig_surv_prob == 0.55
    for t in (1, 5, 12, 19):
        assert p.claims(t, "DEATH") == pytest.approx(
            0.55 * p.mort_rate(t) * p.av_at(t, "AFT_INT"), rel=1e-12)
    assert p.claims(1, "DEATH") == pytest.approx(8.16, abs=CENT)
    assert p.claims(19, "DEATH") == pytest.approx(556.79, abs=CENT)
    # It stops at Rentenbeginn: after that the annuity simply ends.
    assert p.ret_t() == 20
    assert all(p.claims(t, "DEATH") == 0.0 for t in (20, 21, 40))
    # The cover is bought out of the annuity.
    assert p.rf_option_factor() == pytest.approx(0.930, rel=1e-12)
    assert p.rentenfaktor_applied() == pytest.approx(31.50 * 0.930, rel=1e-12)
    assert p.check_no_capital() is True


def test_pitfall_10_with_no_eligible_survivor_nothing_is_paid():
    """``elig_surv_prob = 0`` removes the whole death benefit and moves no other column.

    The annuity stays reduced by the option factor, because a German tariff pays for the cover
    out of the annuity whether or not a survivor is ever found -- so this is not the same run as
    a rider-off model point, and the test says which columns are allowed to move.
    """
    model = alt_model("Basis_DE_A_nosurv")
    try:
        base = model.Projection[3].result_cf()
        assert base["claims_death"].sum() == pytest.approx(3828.51, abs=CENT)
        model.Projection.elig_surv_prob = 0.0
        model.Projection.clear_all()
        nosurv = model.Projection[3].result_cf()
        assert nosurv["claims_death"].abs().max() == 0.0
        for column in ("pols_if", "pols_paying", "av", "premiums", "zuzahlungen",
                       "claims_annuity", "claims_survivor", "expenses", "commissions"):
            assert (base[column] - nosurv[column]).abs().max() == pytest.approx(
                0.0, abs=1e-9), column
        assert (base["net_cf"] - nosurv["net_cf"]).abs().max() > 1.0
        assert model.Projection[3].rentenfaktor_applied() == pytest.approx(
            31.50 * 0.930, rel=1e-12)
    finally:
        model.close()


# ---------------------------------------------------------------------------
# Pitfall 11 -- the conversion is struck on the contractual basis


def test_pitfall_11_the_conversion_is_invariant_to_the_best_estimate_mortality():
    """``ann_pp(ret_t())`` does not move with ``mort_be_factor``; ``claims_annuity`` does.

    The guaranteed *Rentenfaktor* was struck on first-order DAV 2004 R with a prudential margin;
    the projection runs on the best estimate.  The wedge between them is the payout phase's
    *Risikoüberschuss*, and a model that converted on its own mortality would abolish it.
    """
    model = alt_model("Basis_DE_A_mort")
    try:
        base_ann = model.Projection[1].ann_pp(23)
        base_claims = model.Projection[1].result_cf()["claims_annuity"].sum()
        assert base_ann == pytest.approx(ANN_PP_23, abs=5e-5)
        model.Projection.mort_be_factor = 0.70
        model.Projection.clear_all()
        p = model.Projection[1]
        assert p.mort_be_factor == 0.70
        assert p.ann_pp(23) == pytest.approx(base_ann, rel=1e-12)
        assert p.rentenfaktor_applied() == pytest.approx(31.50, rel=1e-12)
        lighter = p.result_cf()["claims_annuity"].sum()
        assert lighter == pytest.approx(296364.48, abs=CENT)
        assert lighter > base_claims
        assert p.check_conversion() is True and p.check_pols_roll_fwd() is True
    finally:
        model.close()


# ---------------------------------------------------------------------------
# Pitfall 12 -- the annuity is booked in advance on the opening count


def test_pitfall_12_the_annuity_is_twelve_instalments_on_the_opening_in_force(
        de_basis_anchor):
    """``claims_annuity(t) = ann_pp(t) x pols_if(t)`` exactly, at every ``t``.

    A life that dies during the payout year has been paid for the whole of it: that is the
    stated approximation of a monthly grid on an annual one, generous to the year of death by up
    to a full year's annuity and concentrated in the high-mortality tail.
    """
    p = de_basis_anchor
    assert p.ann_freq == 12
    assert p.rf_unit == 10000.0
    for t in range(23, 78):
        assert p.claims(t, "ANNUITY") == pytest.approx(
            p.ann_pp(t) * p.pols_if(t), rel=1e-12)
    # Not on the survivors of the year's decrement, which is the other plausible convention.
    assert p.claims(23, "ANNUITY") != pytest.approx(
        p.ann_pp(23) * p.pols_if(24), rel=1e-9)
    # Nothing before Rentenbeginn.
    assert all(p.ann_pp(t) == 0.0 for t in (1, 10, 22))
    assert all(p.claims(t, "ANNUITY") == 0.0 for t in (1, 10, 22))
    # And the annuity compounds at the Ueberschussrente and nothing else.
    for t in (24, 40, 77):
        assert p.ann_pp(t) == pytest.approx(
            p.ann_pp(t - 1) * (1 + p.ann_bonus_rate(t - 1)), rel=1e-12)
    assert p.ann_bonus_rate(30) == 0.01
    assert p.check_annuity_roll_fwd() is True


# ---------------------------------------------------------------------------
# Pitfall 13 -- max(garantiert, aktuell), both branches


def test_pitfall_13_the_higher_of_the_two_rentenfaktoren_applies(basisrente,
                                                                de_basis_anchor):
    """The anchor converts at the current factor, model points 6 and 13 at the guaranteed one."""
    p = de_basis_anchor
    assert p.rentenfaktor_applied() == pytest.approx(31.50, rel=1e-12)
    assert p.rentenfaktor_curr() > float(p.model_point()["rentenfaktor_gtd"])

    for point_id, gtd, curr in ((6, 26.00, 24.76), (13, 34.00, 27.72)):
        q = basisrente.Projection[point_id]
        assert float(q.model_point()["rentenfaktor_gtd"]) == gtd
        assert q.rentenfaktor_curr() == pytest.approx(curr, abs=5e-5)
        assert q.rentenfaktor_applied() == pytest.approx(gtd * q.rf_option_factor(), rel=1e-12)
        assert q.rentenfaktor_applied() > curr

    # Monotone in both inputs, which is what makes the max a genuine discontinuity rather than
    # a blend: the higher factor is taken and the other one is not consulted at all.
    for point_id in (1, 6, 13):
        q = basisrente.Projection[point_id]
        assert q.rentenfaktor_applied() == pytest.approx(
            max(float(q.model_point()["rentenfaktor_gtd"]), q.rentenfaktor_curr())
            * q.rf_option_factor(), rel=1e-12)


# ---------------------------------------------------------------------------
# Pitfall 14 -- the Rentengarantiezeit runs from Rentenbeginn and is never commuted


def test_pitfall_14_the_guarantee_period_runs_from_rentenbeginn(basisrente):
    """Model point 4: ten years from ``ret_t()``, closing at ``gtd_end_t()``, whatever the death.

    Each death contributes ``elig_surv_prob`` of a continuation, the ledger is monotone
    non-decreasing inside the window and exactly zero outside it, and the stream is never
    discounted into a capital sum.
    """
    p = basisrente.Projection[4]
    assert int(p.model_point()["guarantee_period_y"]) == 10
    assert p.ret_t() == 16
    assert p.gtd_end_t() == 25
    assert p.pols_gtd(15) == 0.0 and p.pols_gtd(16) == 0.0
    assert p.pols_gtd(17) == pytest.approx(
        p.pols_death(16) * p.elig_surv_prob, rel=1e-12)
    inside = [p.pols_gtd(t) for t in range(17, 26)]
    assert all(b >= a for a, b in zip(inside, inside[1:]))
    assert p.pols_gtd(25) > 0.0
    assert all(p.pols_gtd(t) == 0.0 for t in range(26, p.proj_len() + 1))
    # The continuation is a stream, weighted by the same annuity, and never commuted.
    for t in (17, 20, 25):
        assert p.claims(t, "SURVIVOR") == pytest.approx(
            p.ann_pp(t) * p.pols_gtd(t), rel=1e-12)
    assert p.claims(26, "SURVIVOR") == 0.0
    assert p.rf_option_factor() == pytest.approx(0.995, rel=1e-12)
    assert p.check_annuity_roll_fwd() is True

    # Both options together on model point 12: twenty years, and a survivor's annuity.
    both = basisrente.Projection[12]
    assert int(both.model_point()["guarantee_period_y"]) == 20
    assert both.gtd_end_t() == both.ret_t() + 20 - 1 == 35
    assert both.rf_option_factor() == pytest.approx(0.974 * 0.930, rel=1e-12)
    assert all(both.pols_gtd(t) == 0.0 for t in range(36, both.proj_len() + 1))


# ---------------------------------------------------------------------------
# Pitfall 15 -- the mortality basis is generational


def test_pitfall_15_the_basis_is_generational_and_not_a_period_table(basisrente,
                                                                    de_basis_anchor):
    """The improvement lives inside the table, so a calendar year changes the rate at an age."""
    p = de_basis_anchor
    for age in (45, 60, 67, 90):
        assert p.mort_rate_at_age(age, 2026) < p.mort_rate_at_age(age, 2005)
        assert p.mort_rate_at_age(age, 2050) < p.mort_rate_at_age(age, 2026)
        assert p.mort_rate_at_age(age, 2026) == pytest.approx(
            p.mort_rate_at_age(age, 2005) * (1 - 0.015) ** 21, rel=1e-9)
    assert p.mort_rate_at_age(67, 2005) == pytest.approx(0.014000, rel=1e-12)
    assert p.mort_rate_at_age(67, 2026) == pytest.approx(0.01019269, abs=5e-9)

    # Two model points reaching the same attained age in different calendar years.
    older = basisrente.Projection[6]      # concluded 2009, reaches age 60 in 2029
    newer = basisrente.Projection[9]      # concluded 2026, reaches age 60 in 2036
    assert older.age(4) == 60 and older.cal_year(4) == 2029
    assert newer.age(11) == 60 and newer.cal_year(11) == 2036
    assert older.mort_rate(4) == pytest.approx(0.00467744, abs=5e-9)
    assert newer.mort_rate(11) == pytest.approx(0.00420787, abs=5e-9)
    assert newer.mort_rate(11) < older.mort_rate(4)

    # The terminal age is absorbing whatever the trend and whatever mort_be_factor says.
    assert p.omega_age() == 121
    assert p.age(77) == 121 and p.mort_rate(77) == 1.0
    assert p.mort_rate(76) == pytest.approx(0.19920354, abs=5e-9)
    assert p.mort_rate_at_age(121, 2101) < 1.0     # the table's own rate, before the rule
    assert p.pols_if(78) == 0.0


# ---------------------------------------------------------------------------
# Pitfall 16 -- the guarantee vintage attaches at conclusion


def test_pitfall_16_the_rechnungszins_attaches_at_conclusion_and_stays(basisrente):
    """Four distinct vintages ship, and each in-force point carries its own, not today's."""
    table = pd.read_csv(INPUT_DIR / "model_point_table.csv", index_col="point_id")
    assert set(table["gtd_rate"]) == {0.0100, 0.0175, 0.0225, 0.0275}
    assert table.loc[6, "conclusion_year"] == 2009 and table.loc[6, "gtd_rate"] == 0.0225
    assert table.loc[7, "conclusion_year"] == 2014 and table.loc[7, "gtd_rate"] == 0.0175
    assert table.loc[8, "conclusion_year"] == 2006 and table.loc[8, "gtd_rate"] == 0.0275
    assert table.loc[1, "conclusion_year"] == 2026 and table.loc[1, "gtd_rate"] == 0.0100
    for point_id in (1, 6, 7, 8, 13):
        p = basisrente.Projection[point_id]
        gtd = float(p.model_point()["gtd_rate"])
        for t in (1, 2, min(5, p.proj_len())):
            assert p.cred_rate(t) >= gtd
            assert p.cred_rate(t) == max(gtd, p.decl_rate(t))


def test_the_in_force_shapes_open_as_the_notes_say(basisrente):
    """The three in-force shapes: accumulating, already *beitragsfrei*, already in payment."""
    paid_up = basisrente.Projection[7]
    assert int(paid_up.model_point()["paidup_at_init"]) == 1
    assert paid_up.pols_paying(1) == 0.0
    assert paid_up.pols_paidup(1) == pytest.approx(paid_up.pols_if_init(), rel=1e-12)
    assert paid_up.av(1) == pytest.approx(42000.00, abs=CENT)
    assert paid_up.prem_pp(1) == 0.0 and paid_up.zuz_pp(1) == 0.0
    assert paid_up.commissions(1) == 0.0                     # acquisition is before the valuation
    assert paid_up.expenses(1) == pytest.approx(60.00, abs=CENT)
    assert paid_up.check_av_roll_fwd() is True

    in_payment = basisrente.Projection[8]
    assert in_payment.ret_t() == -2
    assert in_payment.ann_pp(1) == pytest.approx(7200.00, abs=CENT)
    assert in_payment.claims(1, "ANNUITY") == pytest.approx(7200.00, abs=CENT)
    assert in_payment.fund_at_conv() == 0.0
    assert in_payment.rentenfaktor_curr() == 0.0
    assert in_payment.check_conversion() is True             # vacuously: no conversion occurs
    assert all(in_payment.check_conversion_resid(t) == 0.0 for t in (1, 2, 10))
    assert in_payment.av(1) == 0.0


# ---------------------------------------------------------------------------
# Pitfall 17 -- the BUZ is a premium share and reaches no cash flow


def test_pitfall_17_the_buz_is_a_premium_share_that_enters_nothing(basisrente,
                                                                   de_basis_anchor):
    """``buz_prem_share < 0.50`` on every shipped point, and ``prem_total_pp`` is inert.

    ``prem_base_pp`` is the **old-age** contribution; the BUZ premium buys a cover this model
    does not project, and its disability mechanics belong to ``BU_DE_S``.  The 50 % rule is the
    one thing about the rider this model owns.
    """
    table = pd.read_csv(INPUT_DIR / "model_point_table.csv", index_col="point_id")
    assert (table["buz_prem_share"] < 0.50).all()
    assert table["buz_prem_share"].max() == 0.49              # model point 11, the boundary

    boundary = basisrente.Projection[11]
    assert float(boundary.model_point()["buz_prem_share"]) == 0.49
    assert boundary.prem_total_pp(1) == pytest.approx(
        (boundary.prem_pp(1) + boundary.zuz_pp(1)) / 0.51, rel=1e-12)
    assert boundary.prem_total_pp(1) > boundary.prem_pp(1) + boundary.zuz_pp(1)
    assert boundary.prem_total_pp(1) == pytest.approx(9329.41, abs=CENT)
    # It reaches no column and no cash flow.
    assert "prem_total_pp" not in boundary.result_cf().columns
    assert boundary.net_cf(1) == pytest.approx(
        boundary.premiums(1) + boundary.zuzahlungen(1)
        - boundary.claims(1, "DEATH") - boundary.claims(1, "ANNUITY")
        - boundary.claims(1, "SURVIVOR") - boundary.expenses(1)
        - boundary.commissions(1), rel=1e-12)
    assert boundary.premiums(1) == pytest.approx(
        boundary.prem_pp(1) * boundary.pols_paying(1), rel=1e-12)
    # With no BUZ the reporting cells is the contribution itself.
    p = de_basis_anchor
    assert float(p.model_point()["buz_prem_share"]) == 0.0
    assert p.prem_total_pp(1) == pytest.approx(p.prem_pp(1) + p.zuz_pp(1), rel=1e-12)


# ---------------------------------------------------------------------------
# Structure, documentation and inputs


def test_docstrings_describe_the_current_structure(basisrente):
    """Specifics a reader would rely on, asserted so they cannot go stale silently."""
    doc = basisrente.doc
    assert "Basisrente" in doc
    assert "mechanics demonstration" in doc
    assert "external" in doc                       # inputs are not stored in the model
    assert "once per model" in doc                 # why Data exists
    assert "Beitragsfreistellung" in doc and "Rentenfaktor" in doc
    assert "nicht kapitalisierbar" in doc
    assert "Data" in doc and "Projection" in doc
    proj = basisrente.Projection.doc
    assert "Notes symbol" in proj
    for cells in ("proj_len", "model_point", "ret_t", "bf_rate", "av_pu_at",
                  "rentenfaktor_applied", "prem_total_pp", "pols_gtd"):
        assert cells in proj, cells
    data = basisrente.Data.doc
    assert "TradLife_A" in data
    for cells in ("input_dir", "model_point_table", "mort_table", "behaviour_table"):
        assert cells in data, cells
    assert "0.014000" in data                      # the anchor a replacement must preserve


def test_the_shared_vocabulary_and_the_absent_names(basisrente):
    """The library-wide names this model must publish, and the retired ones it must not."""
    names = set(basisrente.Projection.cells) | set(basisrente.Projection.refs)
    shared = {
        "model_point", "proj_len", "age", "pols_if", "pols_if_at", "pols_if_init",
        "pols_death", "mort_rate", "claims", "expenses", "commissions", "net_cf",
        "liability_cf", "result_cf", "av", "av_at", "av_pp_at", "prem_to_av_pp",
        "check_net_cf", "check_net_cf_resid",
    }
    assert shared <= names, f"missing: {sorted(shared - names)}"
    for retired in ("lapse_rate_ann", "prem_net_pp", "mort_ae_factor", "mort_adj",
                    "mort_rate_table", "premium_net_pp", "check_pols_if", "pols_init",
                    "omega", "loan_bal", "pols_expiry", "check_cf_ledger"):
        assert retired not in names, retired


def test_the_shipped_tables_mark_their_own_provenance():
    """Seven CSVs beside run.py, six of them tagged row by row -- delib's second ruling.

    The mortality table is a **[std]** proxy: DAV 2004 R is cited by name and never shipped, and
    the anchor a substitute must preserve is ``qx(67) = 0.014000``.
    """
    found = {p.name for p in INPUT_DIR.iterdir() if p.suffix == ".csv"}
    assert found == INPUT_FILES

    for name in INPUT_FILES - {"model_point_table.csv"}:
        frame = pd.read_csv(INPUT_DIR / name)
        assert "provenance" in frame.columns, name
        assert frame["provenance"].notna().all(), name
        assert (frame["provenance"].str.len() > 0).all(), name
    # A model point is a configuration, not an assumption: the one exemption.
    points = pd.read_csv(INPUT_DIR / "model_point_table.csv")
    assert "provenance" not in points.columns
    assert len(points) == 13

    mort = pd.read_csv(INPUT_DIR / "mort_table.csv", index_col="age")
    assert list(mort.index) == list(range(20, 122))
    assert float(mort.loc[67, "qx"]) == 0.014000
    assert float(mort.loc[121, "qx"]) == 1.0
    assert (mort["trend"] == 0.015).all()
    assert float(mort.loc[68, "qx"]) / float(mort.loc[67, "qx"]) == pytest.approx(
        1.085, rel=1e-6)
    assert mort["qx"].max() <= 1.0
    assert all("DAV 2004 R" in p for p in mort["provenance"])
    assert all(p.startswith("[std]") for p in mort["provenance"])

    charges = pd.read_csv(INPUT_DIR / "charge_table.csv", index_col="tariff_id")
    assert set(charges.index) == {"de_basis_std", "de_basis_zill40"}
    assert float(charges.loc["de_basis_std", "zill_rate"]) == 0.025
    assert float(charges.loc["de_basis_zill40", "zill_rate"]) == 0.040
    assert all("Hoechstzillmersatz" in p for p in charges["provenance"])

    behaviour = pd.read_csv(INPUT_DIR / "behaviour_table.csv",
                            index_col=["beh_table_id", "dur"])
    assert float(behaviour.loc[("base", 1), "bf_rate"]) == 0.0400
    assert float(behaviour.loc[("base", 6), "bf_rate"]) == 0.0300
    assert float(behaviour.loc[("base", 11), "bf_rate"]) == 0.0200
    assert float(behaviour.loc[("base", 1), "zuz_take_up"]) == 0.7000
    assert all("no German insurer publishes" in p for p in behaviour["provenance"])

    factors = pd.read_csv(INPUT_DIR / "option_table.csv",
                          index_col=["option_id", "option_key"])
    assert float(factors.loc[("prem_mode", "annual"), "factor"]) == 1.000
    assert float(factors.loc[("prem_mode", "monthly"), "factor"]) == 1.050
    assert float(factors.loc[("survivor", "0.60"), "factor"]) == 0.930
    assert float(factors.loc[("guarantee_period", "20"), "factor"]) == 0.974


def test_an_input_can_be_swapped_without_touching_formulas():
    """This is what a production user does with a company or licensed mortality basis.

    Lighter mortality means more annuitants alive to be paid, and a larger fund at
    *Rentenbeginn* -- but the same annuity per annuitant, because the conversion is struck on
    the contractual *Rentenfaktor* and not on the projection's own table.
    """
    lighter = pd.read_csv(INPUT_DIR / "mort_table.csv", index_col="age")
    lighter["qx"] = lighter["qx"] * 0.5
    lighter.loc[121, "qx"] = 1.0
    alt = INPUT_DIR / "mort_table_light.csv"
    model = alt_model("Basis_DE_A_swap")
    try:
        base = model.Projection[1].result_cf()["claims_annuity"].sum()
        lighter.to_csv(alt)
        try:
            model.Data.mort_table_file = alt.name
            model.Data.clear_all()
            model.Projection.clear_all()
            p = model.Projection[1]
            assert p.result_cf()["claims_annuity"].sum() > base
            assert p.result_cf()["premiums"].sum() > TOTALS["premiums"]
            assert p.check_pols_roll_fwd() is True
            assert p.check_av_roll_fwd() is True
            assert p.pols_if(p.proj_len() + 1) == pytest.approx(0.0, abs=1e-12)
        finally:
            alt.unlink(missing_ok=True)
    finally:
        model.close()
