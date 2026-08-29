"""Golden and structural tests for Riester_DE_A.

The golden values are the worked example in
products/riester_rente/technical-notes.md ("Worked example"), which is a
**configuration** rather than a scenario: an in-force *klassische
Riester-Rentenversicherung* -- a certified Altersvorsorgevertrag under the AltZertG,
Schicht 2 -- at the 1 January 2027 valuation date.  The saver is female (reporting only;
the tariff, the decrements and the *Rentenfaktor* are unisex), the contract was concluded
at attained age 47 on 1 January 2024 and has run three complete contract years, so
``age(1) = 50``, ``duration(1) = 4`` and ``calendar_year(1) = 2027``.  *Rentenbeginn* is
attained age 67, the *Rechnungszins* 0,25 %, the *Beitragssumme* 33 600,00 EUR, the
contribution form ``mindest`` at ``contrib_ratio = 1.00`` with no unsubsidised second
pool and no biometric rider, the earnings path ``grow2`` from 42 000,00 EUR, the
entitlement path ``k1_2010`` -- one child born in 2010 drawing *Kindergeld* to 2028, so
475,00 EUR of entitlement in contribution years 2027 and 2028 and 175,00 EUR after --
with 475,00 EUR credited in projection year 1 for the 2026 contribution year, annual
payment (``prem_freq_load = 1.0000``), no *Beitragsfreistellung*, opening balances
``dk_pp_init = 3 860,50``, ``surplus_pp_init = 150,48`` and ``guar_pp_init = 4 369,92``
so that the cell opens 358,94 EUR **under** its own guarantee, a 30 % elected
*Teilkapitalauszahlung*, a guaranteed *Rentenfaktor* of 29,00 EUR per 10 000 EUR per
month, a ten-year *Rentengarantiezeit* and the ``base`` declared-rate scenario at 2,30 %.
Hence ``t_conv() = 18`` (attained 67, calendar 2044) and ``proj_len() = 61``: accumulation
runs ``t = 1 ... 17`` and the lifelong annuity ``t = 18 ... 61``.  Model point 1 is that
cell.

The goldens are hard-coded rather than pickled so that a reviewer can compare them against
the notes by eye.  Tolerances follow the precision the notes display: money to the cent,
``pols_if`` and ``pols_annuity_pay`` to six decimals.  Because the projection is
sixty-one periods long, the notes print the eighteen accumulation-and-conversion rows in
full and a representative set of payout rows; both are asserted here, together with the
**full-precision** totals -- ``net_cf`` of -7 827,39 EUR that way against -7 827,43 EUR if
the sixty-one already-rounded cells are added.

Beyond the worked example this module asserts the notes' four independent rebuilds
(projection year 1 from the statute up, the conversion year, the aggregate account
roll-forward with the exit charge that closes it, and the four-way decrement closure to
1.00000000), the two variants (model point 11's binding *Garantielücke* of 518,28 EUR and
model point 5's *Kleinbetragsrenten-Abfindung*), the six ``check_*`` identities with their
residuals, and **one test per numbered modeling pitfall** -- the eighteen ways an
implementation of *this* product looks right and is wrong:

1.  the two subsidy lags are **different lags**, one calendar and one projection;
2.  the final contribution year's Zulage is credited **at** ``t_conv()``;
3.  the § 86 Kürzung is **proportional**, not a cliff edge;
4.  the Zulage is a **contribution**, published in its own positive column;
5.  the *Günstigerprüfung* top-up is not a contract cash flow and has no cells;
6.  the two *Kinderzulage* rates are a **birth-cohort** split and run together;
7.  the *Beitragsgarantie* is tested **once**, at *Rentenbeginn*, and floors no benefit;
8.  the biometric carve-out is capped at 20 % of total contributions;
9.  **unsubsidised** contributions are inside the guarantee;
10. the declared rate **includes** the *Rechnungszins* and is not added to it;
11. the *Ratenzuschlag* is a **charge** and never reaches the account;
12. the acquisition charge is spread over five contract years and survives *Beitragsfreistellung*;
13. an *Anbieterwechsel* is a **separate decrement** from a *Kündigung*;
14. *Beitragsfreistellung* is a **state change**, not a termination;
15. the two phases use **different mortality bases**, and the annuity basis is generational;
16. the *Kleinbetragsrente* is tested on the **post-lump-sum** annuity against a flat threshold;
17. the *Rentengarantiezeit* changes the **payment count**, never the payment;
18. every benefit is published **gross** of the *Rückzahlungsbetrag*.

The whole-model-point-table sweep is deliberately absent: it belongs to
tests/test_model_conventions_de.py, which owns the library's single sweep.
"""
import pathlib

import modelx as mx
import pytest
from modelx.core.errors import FormulaError

from de_registry import MODELS, LIB


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

MODEL_DIR = LIB / MODELS["Riester_DE_A"][0]
INPUT_DIR = MODEL_DIR.parent

# The notes' worked-example table, in full: the eighteen accumulation-and-conversion rows.
# t: (pols_if, premiums, zulagen, int_credited, claims_death, claims_lapse,
#     claims_transfer, claims_lumpsum, claims_annuity, expenses, commissions, net_cf)
# claims_commutation is 0.00 at every t on this cell -- the anchor's annuity clears the
# Kleinbetragsrente threshold -- and is asserted in the row test rather than tabulated.
WORKED_EXAMPLE = {
    1:  (1.000000, 1205.00, 475.00, 125.21,   6.68,  43.61,  65.62,      0.00,   0.00, 33.52, 25.20,  1505.37),
    2:  (0.978920, 1212.49, 464.99, 158.37,   9.30,  55.15,  83.16,      0.00,   0.00, 33.45, 25.16,  1471.25),
    3:  (0.958169, 1507.08, 455.13, 201.64,  13.02,  52.66,  79.69,      0.00,   0.00, 32.99, 29.43,  1754.41),
    4:  (0.942478, 1515.34, 164.93, 239.74,  17.03,  62.60,  94.82,      0.00,   0.00, 33.09, 25.20,  1447.53),
    5:  (0.926909, 1523.36, 162.21, 278.17,  21.74,  72.62, 110.07,      0.00,   0.00, 33.18, 25.28,  1422.67),
    6:  (0.911451, 1531.11, 159.50, 316.90,  27.24,  82.72, 125.44,      0.00,   0.00, 33.27, 25.36,  1396.58),
    7:  (0.896093, 1538.55, 156.82, 355.91,  33.65,  92.88, 140.92,      0.00,   0.00, 33.35, 25.43,  1369.13),
    8:  (0.880824, 1545.66, 154.14, 395.18,  41.10,  68.74, 104.53,      0.00,   0.00, 33.08, 25.50,  1426.86),
    9:  (0.869997, 1560.24, 152.25, 436.87,  49.98,  75.97, 115.56,      0.00,   0.00, 33.32, 25.69,  1411.96),
    10: (0.859103, 1574.53, 150.34, 479.17,  60.30,  83.31, 126.75,      0.00,   0.00, 33.56, 25.87,  1395.07),
    11: (0.848126, 1588.46, 148.42, 522.04,  72.27,  90.74, 138.08,      0.00,   0.00, 33.80, 26.05,  1375.95),
    12: (0.837051, 1602.01, 146.48, 565.45,  86.11,  98.25, 149.53,      0.00,   0.00, 34.03, 26.23,  1354.34),
    13: (0.825864, 1589.79, 144.53, 608.79, 101.98, 105.75, 160.96,      0.00,   0.00, 34.25, 26.01,  1305.36),
    14: (0.814546, 1568.00, 142.55, 651.80, 120.10, 113.17, 172.29,      0.00,   0.00, 34.46, 25.66,  1244.86),
    15: (0.803079, 1545.93, 140.54, 694.42, 140.75, 120.52, 183.50,      0.00,   0.00, 34.67, 25.30,  1181.73),
    16: (0.791444, 1523.53, 138.50, 736.58, 164.23, 127.78, 194.57,      0.00,   0.00, 34.86, 24.93,  1115.67),
    17: (0.779621, 1500.77, 136.43, 778.20, 190.86, 134.94, 205.48,      0.00,   0.00, 35.04, 24.56,  1046.34),
    18: (0.767588,    0.00, 134.33,   0.00,   0.00,   0.00,   0.00, 10536.61, 855.57, 18.81,  0.00, -11276.67),
}

# The notes' Total row: all sixty-one periods, summed at full precision and then rounded.
TOTALS = {
    "premiums": 25631.84, "zulagen": 3627.10, "int_credited": 7544.45,
    "claims_death": 1156.35, "claims_lapse": 1481.42, "claims_transfer": 2250.97,
    "claims_lumpsum": 10536.61, "claims_commutation": 0.00,
    "claims_annuity": 20154.82, "expenses": 1069.29, "commissions": 436.87,
    "net_cf": -7827.39,
}

# What the same columns come to if the sixty-one *rounded* cells are added instead.  Nine
# of the eleven differ, and net_cf differs by four cents; the notes say so and this module
# asserts the difference rather than papering over it.
ROUNDED_CELL_SUMS = {
    "premiums": 25631.85, "zulagen": 3627.09, "int_credited": 7544.44,
    "claims_death": 1156.34, "claims_lapse": 1481.41, "claims_transfer": 2250.97,
    "claims_lumpsum": 10536.61, "claims_annuity": 20154.83, "expenses": 1069.32,
    "commissions": 436.86, "net_cf": -7827.43,
}

# The notes' payout table: selected rows of t = 18 ... 61.
# t: (age, pols_if, pols_annuity_pay, claims_annuity, expenses, net_cf)
PAYOUT_ROWS = {
    18: (67, 0.767588, 0.767588, 855.57, 18.81, -11276.67),
    19: (68, 0.762677, 0.767588, 855.57, 18.85,   -874.43),
    27: (76, 0.701403, 0.767588, 855.57, 19.33,   -874.91),
    28: (77, 0.690013, 0.690013, 769.11, 17.56,   -786.67),
    29: (78, 0.677530, 0.677530, 755.19, 17.35,   -772.55),
    35: (84, 0.574463, 0.574463, 640.31, 15.60,   -655.91),
    45: (94, 0.273819, 0.273819, 305.21,  9.43,   -314.63),
    55: (104, 0.016013, 0.016013, 17.85,  0.94,    -18.79),
    61: (110, 0.000079, 0.000079,  0.09,  0.01,     -0.10),
}

# The notes' payout subtotal row, t = 19 ... 61, at full precision then rounded.
PAYOUT_SUBTOTAL = {
    "pols_if": 17.024474, "pols_annuity_pay": 17.314559,
    "claims_annuity": 19299.25, "expenses": 476.56, "net_cf": -19775.81,
}

# The anchor's conversion at t = 18, from the notes' second independent rebuild.
CONVERSION = {
    "dk_pp": 36172.815098, "surplus_acct_pp": 8224.490372, "prem_to_av_pp": 156.00,
    "raw_account": 44553.305470, "slueb_pp": 757.544616, "bewres_pp": 445.533055,
    "account_conv_pp": 45756.383140, "guar": 37877.2308, "capital_conv_pp": 45756.383140,
    "garantieluecke_conv_pp": 0.0, "ann_factor": 20.8722287915,
    "rentenfaktor_curr": 27.947822, "rentenfaktor_applied": 29.00,
    "teilkapital_pp": 13726.914942, "annuity_capital_pp": 32029.468198,
    "annuity_month_pp": 92.885458, "annuity_pp": 1114.625493,
    "pols_conv": 0.7675876849,
}

# The notes' four-way decrement closure over the whole sixty-one-year projection.
CLOSURE = {
    "deaths_accum": 0.04132833, "deaths_payout": 0.76758768,
    "lapses": 0.07668891, "transfers": 0.11439508,
}

# Variant 1 -- model point 11, the low declared-rate cell on which the guarantee binds.
# t: (pols_if, premiums, zulagen, int_credited, claims_death, claims_lapse,
#     claims_transfer, claims_lumpsum, claims_annuity, expenses, commissions, net_cf)
VARIANT_LOW = {
    1:  (1.000000, 1625.00, 475.00, 35.08, 21.95, 55.11,  83.09,      0.00,   0.00, 33.67, 31.50,  1874.68),
    2:  (0.977045, 1587.70, 464.10, 43.81, 30.15, 68.80, 103.89,      0.00,   0.00, 33.55, 30.78,  1784.63),
    3:  (0.954320, 1837.07, 453.30, 53.94, 40.83, 63.51,  96.21,      0.00,   0.00, 33.03, 34.36,  2022.42),
    4:  (0.936516, 1802.79, 163.89, 62.58, 52.11, 73.66, 111.65,      0.00,   0.00, 33.07, 29.50,  1666.69),
    5:  (0.918697, 1768.49, 160.77, 70.91, 64.95, 83.42, 126.51,      0.00,   0.00, 33.09, 28.94,  1592.36),
    6:  (0.900842, 1734.12, 157.65, 78.90, 79.50, 92.79, 140.77,      0.00,   0.00, 33.10, 28.38,  1517.25),
    7:  (0.882930, 1699.64, 154.51, 86.57, 95.94, 101.75, 154.41,     0.00,   0.00, 33.09, 27.81,  1441.15),
    8:  (0.864938,    0.00, 151.36,  0.00,  0.00,  0.00,   0.00, 5449.11, 442.47, 21.28,  0.00, -5761.50),
    9:  (0.858363,    0.00,   0.00,  0.00,  0.00,  0.00,   0.00,    0.00, 442.47, 21.33,  0.00,  -463.80),
    20: (0.731563,    0.00,   0.00,  0.00,  0.00,  0.00,   0.00,    0.00, 374.24, 19.04,  0.00,  -393.28),
    51: (0.000061,    0.00,   0.00,  0.00,  0.00,  0.00,   0.00,    0.00,   0.03,  0.01,  0.00,    -0.04),
}

VARIANT_LOW_TOTALS = {
    "premiums": 12054.81, "zulagen": 2180.59, "int_credited": 431.80,
    "claims_death": 385.43, "claims_lapse": 539.04, "claims_transfer": 816.52,
    "claims_lumpsum": 5449.11, "claims_commutation": 0.00,
    "claims_annuity": 10121.79, "expenses": 776.66, "commissions": 211.26,
    "net_cf": -4064.43,
}

VARIANT_LOW_CONVERSION = {
    "raw_account": 19863.088636, "slueb_pp": 420.00, "bewres_pp": 198.630886,
    "account_conv_pp": 20481.719523, "guar": 21000.00,
    "capital_conv_pp": 21000.00, "garantieluecke_conv_pp": 518.280477,
    "teilkapital_pp": 6300.00, "annuity_capital_pp": 14700.00,
    "annuity_month_pp": 42.63, "annuity_pp": 511.56, "pols_conv": 0.8649383502,
}

# Variant 2 -- model point 5, the *mittelbar* eligible spouse at the Sockelbeitrag, which
# commutes rather than annuitising.  claims_lumpsum and claims_annuity are 0.00 throughout
# and claims_commutation replaces them, so the column order below carries the commutation
# in place of the lump sum.
# t: (pols_if, premiums, zulagen, int_credited, claims_death, claims_lapse,
#     claims_transfer, claims_commutation, expenses, commissions, net_cf)
VARIANT_FIXED = {
    1:  (1.000000, 60.00, 175.00, 32.74,  3.10,  8.55, 12.55,    0.00, 35.15, 3.52,   172.13),
    2:  (0.982960, 58.98, 172.02, 37.75,  3.93,  9.85, 14.55,    0.00, 35.23, 3.46,   163.97),
    11: (0.856985, 51.42, 149.97, 81.96, 20.10, 14.21, 21.41,    0.00, 36.35, 3.02,   106.29),
    12: (0.843758,  0.00, 147.66,  0.00,  0.00,  0.00,  0.00, 3828.31,  0.00, 0.00, -3680.65),
    13: (0.000000,  0.00,   0.00,  0.00,  0.00,  0.00,  0.00,    0.00,  0.00, 0.00,     0.00),
    55: (0.000000,  0.00,   0.00,  0.00,  0.00,  0.00,  0.00,    0.00,  0.00, 0.00,     0.00),
}

VARIANT_FIXED_TOTALS = {
    "premiums": 609.80, "zulagen": 1926.26, "int_credited": 631.80,
    "claims_death": 108.72, "claims_lapse": 123.71, "claims_transfer": 184.87,
    "claims_lumpsum": 0.00, "claims_commutation": 3828.31, "claims_annuity": 0.00,
    "expenses": 391.21, "commissions": 35.83, "net_cf": -2136.59,
}

RESULT_CF_COLUMNS = [
    "pols_if", "pols_annuity_pay", "premiums", "zulagen", "int_credited",
    "claims_death", "claims_lapse", "claims_transfer", "claims_lumpsum",
    "claims_commutation", "claims_annuity", "expenses", "commissions",
    "net_cf", "liability_cf",
]

CLAIM_KINDS = ("DEATH", "LAPSE", "TRANSFER", "LUMPSUM", "COMMUTATION", "ANNUITY")


# ---------------------------------------------------------------------------
# The worked example


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE))
def test_worked_example_row(de_riester_anchor, t):
    """Every cell of the notes' eighteen accumulation-and-conversion rows.

    Money to the cent, ``pols_if`` to six decimals -- the precision the notes display.
    ``claims_commutation`` is zero on this cell at every t, because the anchor's annuity
    of 92,89 EUR a month clears the 39,55 EUR *Kleinbetragsrente* threshold comfortably.
    """
    (pols, prem, zul, intc, cd, cl, ct, clump, cann,
     exp, comm, net) = WORKED_EXAMPLE[t]
    p = de_riester_anchor
    assert p.pols_if(t) == pytest.approx(pols, abs=SIX_DP)
    assert p.premiums(t) == pytest.approx(prem, abs=CENT)
    assert p.zulagen(t) == pytest.approx(zul, abs=CENT)
    assert p.int_credited(t) == pytest.approx(intc, abs=CENT)
    assert p.claims(t, "DEATH") == pytest.approx(cd, abs=CENT)
    assert p.claims(t, "LAPSE") == pytest.approx(cl, abs=CENT)
    assert p.claims(t, "TRANSFER") == pytest.approx(ct, abs=CENT)
    assert p.claims(t, "LUMPSUM") == pytest.approx(clump, abs=CENT)
    assert p.claims(t, "ANNUITY") == pytest.approx(cann, abs=CENT)
    assert p.claims(t, "COMMUTATION") == 0.0
    assert p.expenses(t) == pytest.approx(exp, abs=CENT)
    assert p.commissions(t) == pytest.approx(comm, abs=CENT)
    assert p.net_cf(t) == pytest.approx(net, abs=CENT)
    assert p.liability_cf(t) == pytest.approx(-net, abs=CENT)


@pytest.mark.parametrize("t", sorted(PAYOUT_ROWS))
def test_the_payout_phase_rows(de_riester_anchor, t):
    """The notes' payout table, and the five columns that are zero from t = 18 onward.

    The account is extinguished at conversion, so there is no interest to credit and a
    death pays nothing outside the *Rentengarantiezeit*.  ``zulagen`` is the exception at
    t = 18: the final contribution year's subsidy lands in the conversion year.
    """
    age, pols, pay, ann, exp, net = PAYOUT_ROWS[t]
    p = de_riester_anchor
    assert p.age(t) == age
    assert p.pols_if(t) == pytest.approx(pols, abs=SIX_DP)
    assert p.pols_annuity_pay(t) == pytest.approx(pay, abs=SIX_DP)
    assert p.claims(t, "ANNUITY") == pytest.approx(ann, abs=CENT)
    assert p.expenses(t) == pytest.approx(exp, abs=CENT)
    assert p.net_cf(t) == pytest.approx(net, abs=CENT)
    assert p.premiums(t) == 0.0
    assert p.int_credited(t) == 0.0
    assert p.claims(t, "DEATH") == 0.0
    assert p.claims(t, "LAPSE") == 0.0
    assert p.claims(t, "TRANSFER") == 0.0
    assert p.zulagen(t) == (pytest.approx(134.33, abs=CENT) if t == 18 else 0.0)


def test_the_totals_are_summed_at_full_precision(de_riester_anchor):
    """The notes' Total row is a full-precision sum over all sixty-one periods.

    Nine of the eleven columns differ from the sum of the already-rounded cells, and
    ``net_cf`` differs by four cents accumulated over sixty-one rows.  Both are asserted:
    the full-precision figure is the one the notes print, and the rounded-cell figure is
    the one an implementation that rounds as it goes would produce.
    """
    df = de_riester_anchor.result_cf()
    for column, total in TOTALS.items():
        assert df[column].sum() == pytest.approx(total, abs=CENT), column
    for column, rounded in ROUNDED_CELL_SUMS.items():
        assert sum(round(v, 2) for v in df[column]) == pytest.approx(
            rounded, abs=CENT), column
    # The two agree on exactly two columns, and differ on the other nine.
    differing = [c for c in ROUNDED_CELL_SUMS
                 if abs(ROUNDED_CELL_SUMS[c] - TOTALS[c]) > 1e-9]
    assert sorted(differing) == sorted([
        "premiums", "zulagen", "int_credited", "claims_death", "claims_lapse",
        "claims_annuity", "expenses", "commissions", "net_cf"])
    assert TOTALS["net_cf"] - ROUNDED_CELL_SUMS["net_cf"] == pytest.approx(0.04, abs=CENT)


def test_the_payout_subtotals(de_riester_anchor):
    """The notes' t = 19 ... 61 subtotal row, including both count columns.

    17.314559 instalments are paid against 17.024474 policy-years in force: the whole of
    the difference is the *Rentengarantiezeit*.
    """
    df = de_riester_anchor.result_cf().loc[19:61]
    for column, total in PAYOUT_SUBTOTAL.items():
        tol = SIX_DP if column.startswith("pols") else CENT
        assert df[column].sum() == pytest.approx(total, abs=tol), column
    assert (df["pols_annuity_pay"].sum() - df["pols_if"].sum()) == pytest.approx(
        0.290085, abs=SIX_DP)


# ---------------------------------------------------------------------------
# The notes' independent checks


def test_projection_year_one_rebuilt_from_the_statute_up(de_riester_anchor):
    """The notes' first rebuild: year 1 reconstructed a different way, in one pass.

    ``Y(1) = 42 000``; ``Z*(1) = 175 + 300 = 475``;
    ``M(1) = max(60, min(0,04 x 42 000, 2 100) - 475) = 1 205``; ``E(1) = M(1)``;
    ``K_a = 0,025 x 33 600 / 5 = 168``; ``K_v = 0,04 x 1 680 + 12 = 79,20``;
    ``S(1) = 1 432,80``; interest ``0,023 x (3 860,50 + 1 432,80 + 150,48) = 125,206940``.
    """
    p = de_riester_anchor
    assert p.income_ref(1) == pytest.approx(42000.00, abs=CENT)
    assert p.zulage_entitlement_pp(1) == pytest.approx(175.00 + 300.00, abs=CENT)
    assert p.mindesteigenbeitrag_pp(1) == pytest.approx(
        max(60.0, min(0.04 * 42000.0, 2100.0) - 475.0), abs=CENT)
    assert p.mindesteigenbeitrag_pp(1) == pytest.approx(1205.00, abs=CENT)
    assert p.eigenbeitrag_pp(1) == pytest.approx(1205.00, abs=CENT)
    assert p.eigenbeitrag_paid_pp(1) == pytest.approx(1205.00, abs=CENT)
    assert p.zulage_pp(1) == pytest.approx(475.00, abs=CENT)
    assert p.contrib_total_pp(1) == pytest.approx(1680.00, abs=CENT)
    assert p.acq_charge_pp(1) == pytest.approx(0.025 * 33600.0 / 5, abs=CENT)
    assert p.acq_charge_pp(1) == pytest.approx(168.00, abs=CENT)
    assert p.admin_charge_pp(1) == pytest.approx(0.04 * 1680.0 + 12.0, abs=CENT)
    assert p.prem_to_av_pp(1) == pytest.approx(1680.00 - 168.00 - 79.20, abs=CENT)
    assert p.int_credited_pp(1) == pytest.approx(
        0.023 * (3860.50 + 1432.80 + 150.48), abs=CENT)
    assert p.int_credited_pp(1) == pytest.approx(125.206940, abs=CENT)
    assert p.av_pp(2) == pytest.approx(5568.986940, abs=CENT)
    # The decrements at attained age 50, contract duration 4, applied in the stated order.
    assert p.mort_rate(1) == pytest.approx(0.001500 * 0.80, rel=1e-12)
    assert p.lapse_rate(1) == 0.008
    assert p.transfer_rate(1) == 0.012
    assert p.pols_death(1) == pytest.approx(0.001200, rel=1e-12)
    assert p.pols_lapse(1) == pytest.approx(0.9988 * 0.008, rel=1e-12)
    assert p.pols_transfer(1) == pytest.approx(0.9988 * 0.992 * 0.012, rel=1e-12)
    # The benefits, struck on A(2).
    assert p.claims(1, "DEATH") == pytest.approx(5568.986940 * 0.001200, abs=CENT)
    assert p.claims(1, "LAPSE") == pytest.approx(
        0.98 * 5568.986940 * 0.0079904, abs=CENT)
    assert p.claims(1, "TRANSFER") == pytest.approx(
        (5568.986940 - 50.0) * 0.0118897152, abs=CENT)
    # The expenses, inflated on *contract* duration and not on projection year.
    assert p.expenses(1) == pytest.approx(
        30.0 * 1.02 ** 3 + 80.0 * (0.001200 + 0.0079904 + 0.0118897152), abs=CENT)
    assert p.commissions(1) == pytest.approx(0.015 * (1205.00 + 475.00), abs=CENT)
    assert p.net_cf(1) == pytest.approx(
        1680.00 - 6.682784 - 43.608465 - 65.619183 - 33.522649 - 25.20, abs=CENT)


def test_the_conversion_year_rebuilt_a_different_way(de_riester_anchor):
    """The notes' second rebuild: everything struck at t = 18, from its own parts.

    The raw account is ``D(18) + S(18) + U(18)``, the *Sparbeitrag* being the last Zulage
    net of its charge, ``175 - (0,04 x 175 + 12) = 156,00``.  The
    *Schlussüberschussanteil* is 2 % of the contributions credited over the life of the
    contract, which is exactly the guarantee accumulator, and the *Bewertungsreserven*
    share is 1 % of the raw account.
    """
    p = de_riester_anchor
    T = p.t_conv()
    assert T == 18
    assert p.dk_pp(T) == pytest.approx(CONVERSION["dk_pp"], abs=CENT)
    assert p.surplus_acct_pp(T) == pytest.approx(CONVERSION["surplus_acct_pp"], abs=CENT)
    assert p.prem_to_av_pp(T) == pytest.approx(175.0 - (0.04 * 175.0 + 12.0), abs=CENT)
    raw = p.dk_pp(T) + p.prem_to_av_pp(T) + p.surplus_acct_pp(T)
    assert raw == pytest.approx(CONVERSION["raw_account"], abs=CENT)
    assert p.slueb_pp() == pytest.approx(0.02 * p.guar_pp(T + 1), abs=CENT)
    assert p.slueb_pp() == pytest.approx(CONVERSION["slueb_pp"], abs=CENT)
    assert p.bewres_pp() == pytest.approx(0.01 * raw, abs=CENT)
    assert p.bewres_pp() == pytest.approx(CONVERSION["bewres_pp"], abs=CENT)
    assert p.account_conv_pp() == pytest.approx(CONVERSION["account_conv_pp"], abs=CENT)
    # The guarantee rebuilt without the recursion: the opening seed plus the subsidised
    # pool, the anchor carrying no unsubsidised contribution and no rider carve-out.
    assert p.guar_pp(T + 1) == pytest.approx(
        p.guar_pp_init() + p.pool_gefoerdert_pp(T), abs=CENT)
    assert p.guar_pp(T + 1) == pytest.approx(CONVERSION["guar"], abs=CENT)
    assert p.capital_conv_pp() == pytest.approx(CONVERSION["capital_conv_pp"], abs=CENT)
    assert p.garantieluecke_conv_pp() == 0.0
    assert p.account_conv_pp() - p.guar_pp(T + 1) == pytest.approx(7879.15, abs=CENT)
    # The annuity basis, and the two-Rentenfaktor comparison the guarantee wins.
    assert p.ann_factor() == pytest.approx(CONVERSION["ann_factor"], abs=5e-9)
    assert p.rentenfaktor_curr() == pytest.approx(
        0.70 * 10000.0 / (12.0 * p.ann_factor()), rel=1e-12)
    assert p.rentenfaktor_curr() == pytest.approx(
        CONVERSION["rentenfaktor_curr"], abs=5e-7)
    assert p.rentenfaktor_curr() < p.rentenfaktor_guar()
    assert p.rentenfaktor_applied() == pytest.approx(29.00, abs=1e-12)
    # The disposal of the capital.
    assert p.teilkapital_pp() == pytest.approx(
        0.30 * p.capital_conv_pp(), rel=1e-12)
    assert p.teilkapital_pp() == pytest.approx(CONVERSION["teilkapital_pp"], abs=CENT)
    assert p.annuity_capital_pp() == pytest.approx(
        CONVERSION["annuity_capital_pp"], abs=CENT)
    assert p.annuity_month_pp() == pytest.approx(
        CONVERSION["annuity_capital_pp"] / 10000.0 * 29.00, abs=CENT)
    assert p.annuity_month_pp() == pytest.approx(
        CONVERSION["annuity_month_pp"], abs=CENT)
    assert p.annuity_pp(T) == pytest.approx(12.0 * p.annuity_month_pp(), rel=1e-12)
    assert p.annuity_pp(T) == pytest.approx(CONVERSION["annuity_pp"], abs=CENT)
    # And the two conversion-year cash flows the notes read off row 18.
    assert p.pols_conv() == pytest.approx(CONVERSION["pols_conv"], abs=SIX_DP)
    assert p.claims(T, "LUMPSUM") == pytest.approx(
        p.teilkapital_pp() * p.pols_conv(), rel=1e-12)
    assert p.claims(T, "LUMPSUM") == pytest.approx(10536.61, abs=CENT)
    assert p.claims(T, "ANNUITY") == pytest.approx(855.57, abs=CENT)


def test_the_account_rolls_forward_and_the_exit_charge_closes_it(de_riester_anchor):
    """The notes' third rebuild: the aggregate account, and the residue that closes it.

    The account released by an exiting policy either leaves as a benefit or stays with the
    insurer as ``exit_charge_pp``.  Dropping the second -- a *Stornoabzug* and a transfer
    charge look like income rather than like account released -- leaves a residual of
    1,48 EUR in year 1, which is exactly the usual way this identity fails.
    """
    p = de_riester_anchor
    opening_next = p.av_at(2, "BEF_PREM")
    assert opening_next == pytest.approx(5451.592054, abs=CENT)
    exit_charge = p.exit_charge_pp(1)
    assert exit_charge == pytest.approx(
        0.02 * 5568.986940 * 0.0079904 + 50.0 * 0.0118897152, abs=CENT)
    assert exit_charge == pytest.approx(1.484454, abs=CENT)
    rebuilt = (p.av_at(1, "BEF_PREM") + p.prem_to_av_pp(1) * p.pols_if(1)
               + p.int_credited(1)
               - p.claims(1, "DEATH") - p.claims(1, "LAPSE") - p.claims(1, "TRANSFER")
               - exit_charge)
    assert rebuilt == pytest.approx(opening_next, abs=1e-9)
    assert p.check_av_roll_fwd_resid(1) == pytest.approx(0.0, abs=1e-9)
    # Without the exit charge the identity misses by exactly that amount.
    assert rebuilt + exit_charge - opening_next == pytest.approx(1.48, abs=CENT)
    # And from the conversion year on, the identity is the assertion that the account is
    # gone: av_pp(t) is zero for every t after t_conv().
    assert all(p.av_pp(t) == 0.0 for t in (19, 20, 40, 61))
    assert p.check_av_roll_fwd() is True


def test_the_decrements_close_four_ways(de_riester_anchor):
    """The notes' fourth rebuild: deaths in accumulation, deaths in payout, surrenders and
    transfers sum to exactly one, with nothing left in force.

    ``mort_rate`` is forced to 1 at ``omega_age = 110``, so ``pols_if(62)`` is exactly zero
    and the identity is exact rather than approximate.  The split is itself a product
    statement: 23,24 % of the cohort leaves before *Rentenbeginn*, and half again as many
    of those transfer out as surrender.
    """
    p = de_riester_anchor
    n, T = p.proj_len(), p.t_conv()
    deaths_accum = sum(p.pols_death(t) for t in range(1, T))
    deaths_payout = sum(p.pols_death(t) for t in range(T, n + 1))
    lapses = sum(p.pols_lapse(t) for t in range(1, n + 1))
    transfers = sum(p.pols_transfer(t) for t in range(1, n + 1))
    assert deaths_accum == pytest.approx(CLOSURE["deaths_accum"], abs=5e-9)
    assert deaths_payout == pytest.approx(CLOSURE["deaths_payout"], abs=5e-9)
    assert lapses == pytest.approx(CLOSURE["lapses"], abs=5e-9)
    assert transfers == pytest.approx(CLOSURE["transfers"], abs=5e-9)
    assert deaths_accum + deaths_payout + lapses + transfers == pytest.approx(
        1.0, abs=1e-12)
    assert p.pols_if(n + 1) == 0.0
    assert p.mort_rate(n) == 1.0
    # Pre-Rentenbeginn exits, and the transfer-to-surrender ratio the notes read off.
    before = deaths_accum + lapses + transfers
    assert before == pytest.approx(0.2324, abs=5e-5)
    assert transfers / before == pytest.approx(0.492, abs=5e-4)
    assert lapses / before == pytest.approx(0.330, abs=5e-4)
    assert p.check_pols_roll_fwd() is True


def test_the_statement_reconciles_on_the_totals(de_riester_anchor):
    """The notes' closure identity on the Total row -- check_net_cf() in aggregate.

    ``25 631,84 + 3 627,10 - 35 580,17 - 1 069,29 - 436,87 = -7 827,39``, where the middle
    term is the sum of all six ``claims_*`` columns.  ``int_credited`` of 7 544,45 EUR is
    **not** in it: adding it would report the cell's undiscounted deficit as 282,94 EUR.
    """
    df = de_riester_anchor.result_cf()
    claims = sum(df["claims_" + k.lower()].sum() for k in CLAIM_KINDS)
    assert claims == pytest.approx(35580.17, abs=CENT)
    assert (df["premiums"].sum() + df["zulagen"].sum() - claims
            - df["expenses"].sum() - df["commissions"].sum()) == pytest.approx(
                -7827.39, abs=CENT)
    wrong = df["net_cf"].sum() + df["int_credited"].sum()
    assert wrong == pytest.approx(-282.94, abs=CENT)


# ---------------------------------------------------------------------------
# Variant 1 -- the low declared rate, and a Garantielücke that binds (model point 11)


@pytest.mark.parametrize("t", sorted(VARIANT_LOW))
def test_variant_low_scenario_row(riester_rente, t):
    """The notes' Variant 1 table: model point 11 on the ``low`` scenario."""
    (pols, prem, zul, intc, cd, cl, ct, clump, cann,
     exp, comm, net) = VARIANT_LOW[t]
    p = riester_rente.Projection[11]
    assert p.scenario_id() == "low"
    assert p.pols_if(t) == pytest.approx(pols, abs=SIX_DP)
    assert p.premiums(t) == pytest.approx(prem, abs=CENT)
    assert p.zulagen(t) == pytest.approx(zul, abs=CENT)
    assert p.int_credited(t) == pytest.approx(intc, abs=CENT)
    assert p.claims(t, "DEATH") == pytest.approx(cd, abs=CENT)
    assert p.claims(t, "LAPSE") == pytest.approx(cl, abs=CENT)
    assert p.claims(t, "TRANSFER") == pytest.approx(ct, abs=CENT)
    assert p.claims(t, "LUMPSUM") == pytest.approx(clump, abs=CENT)
    assert p.claims(t, "ANNUITY") == pytest.approx(cann, abs=CENT)
    assert p.expenses(t) == pytest.approx(exp, abs=CENT)
    assert p.commissions(t) == pytest.approx(comm, abs=CENT)
    assert p.net_cf(t) == pytest.approx(net, abs=CENT)


def test_the_guarantee_binds_on_the_low_scenario(riester_rente):
    """The number the product exists to produce: garantieluecke_conv_pp() = 518,28 EUR.

    The 2 100 EUR ceiling binds in every contribution year on this cell, so the guarantee
    accumulator lands on a round 21 000,00 EUR, and the annuity is then struck on the
    **guaranteed** capital rather than on the account.  It is a declared-rate result, not a
    *Rechnungszins* result: the same cell on ``base`` reaches an account above the
    guarantee and the *Garantielücke* is zero.
    """
    p = riester_rente.Projection[11]
    T = p.t_conv()
    assert T == 8 and p.proj_len() == 51
    raw = p.dk_pp(T) + p.prem_to_av_pp(T) + p.surplus_acct_pp(T)
    assert raw == pytest.approx(VARIANT_LOW_CONVERSION["raw_account"], abs=CENT)
    assert p.slueb_pp() == pytest.approx(VARIANT_LOW_CONVERSION["slueb_pp"], abs=CENT)
    assert p.bewres_pp() == pytest.approx(VARIANT_LOW_CONVERSION["bewres_pp"], abs=CENT)
    assert p.account_conv_pp() == pytest.approx(
        VARIANT_LOW_CONVERSION["account_conv_pp"], abs=CENT)
    assert p.guar_pp(T + 1) == pytest.approx(21000.00, abs=CENT)
    assert p.capital_conv_pp() == pytest.approx(21000.00, abs=CENT)
    assert p.capital_conv_pp() > p.account_conv_pp()
    assert p.garantieluecke_conv_pp() == pytest.approx(518.280477, abs=CENT)
    assert p.garantieluecke_conv_pp() / p.capital_conv_pp() == pytest.approx(
        0.0247, abs=5e-4)
    # The annuity is struck on the guaranteed capital.
    assert p.teilkapital_pp() == pytest.approx(6300.00, abs=CENT)
    assert p.annuity_capital_pp() == pytest.approx(14700.00, abs=CENT)
    assert p.annuity_month_pp() == pytest.approx(14700.0 / 10000.0 * 29.00, abs=CENT)
    assert p.annuity_pp(T) == pytest.approx(511.56, abs=CENT)
    assert p.claims(T, "LUMPSUM") == pytest.approx(
        6300.0 * VARIANT_LOW_CONVERSION["pols_conv"], abs=CENT)
    assert p.check_conversion() is True


def test_variant_low_totals(riester_rente):
    """The Variant 1 Total row, again summed at full precision and then rounded."""
    df = riester_rente.Projection[11].result_cf()
    for column, total in VARIANT_LOW_TOTALS.items():
        assert df[column].sum() == pytest.approx(total, abs=CENT), column
    # The seven columns where the rounded-cell sum differs, per the notes.
    assert sum(round(v, 2) for v in df["zulagen"]) == pytest.approx(2180.58, abs=CENT)
    assert sum(round(v, 2) for v in df["claims_annuity"]) == pytest.approx(
        10121.82, abs=CENT)
    assert sum(round(v, 2) for v in df["net_cf"]) == pytest.approx(-4064.45, abs=CENT)


# ---------------------------------------------------------------------------
# Variant 2 -- the fixed contribution form, and a contract that commutes (model point 5)


@pytest.mark.parametrize("t", sorted(VARIANT_FIXED))
def test_variant_fixed_form_row(riester_rente, t):
    """The notes' Variant 2 table: the *mittelbar* spouse at the 60,00 EUR Sockelbeitrag.

    ``income_id = zero`` and ``contrib_form = fixed``, so ``M(t) = max(60, min(0, 2 100) -
    175) = 60,00`` and the floor binds by construction.  The frame carries zeros to t = 55
    rather than being truncated after the *Abfindung*.
    """
    (pols, prem, zul, intc, cd, cl, ct, ccom, exp, comm, net) = VARIANT_FIXED[t]
    p = riester_rente.Projection[5]
    assert p.contrib_form() == "fixed" and p.contrib_fixed_pp() == 60.0
    assert p.pols_if(t) == pytest.approx(pols, abs=SIX_DP)
    assert p.premiums(t) == pytest.approx(prem, abs=CENT)
    assert p.zulagen(t) == pytest.approx(zul, abs=CENT)
    assert p.int_credited(t) == pytest.approx(intc, abs=CENT)
    assert p.claims(t, "DEATH") == pytest.approx(cd, abs=CENT)
    assert p.claims(t, "LAPSE") == pytest.approx(cl, abs=CENT)
    assert p.claims(t, "TRANSFER") == pytest.approx(ct, abs=CENT)
    assert p.claims(t, "COMMUTATION") == pytest.approx(ccom, abs=CENT)
    assert p.claims(t, "LUMPSUM") == 0.0
    assert p.claims(t, "ANNUITY") == 0.0
    assert p.expenses(t) == pytest.approx(exp, abs=CENT)
    assert p.commissions(t) == pytest.approx(comm, abs=CENT)
    assert p.net_cf(t) == pytest.approx(net, abs=CENT)


def test_variant_fixed_totals_and_the_subsidy_share(riester_rente):
    """609,80 EUR from the saver against 1 926,26 EUR from the state over the projection.

    The Zulage is 76 % of the contribution on this cell, which is why a statement folding
    ``zulagen`` into ``premiums`` would be describing a different product.
    """
    p = riester_rente.Projection[5]
    df = p.result_cf()
    for column, total in VARIANT_FIXED_TOTALS.items():
        assert df[column].sum() == pytest.approx(total, abs=CENT), column
    share = df["zulagen"].sum() / (df["zulagen"].sum() + df["premiums"].sum())
    assert share == pytest.approx(0.76, abs=0.005)
    assert p.mindesteigenbeitrag_pp(1) == pytest.approx(60.00, abs=CENT)
    assert p.income_ref(1) == 0.0
    assert p.check_net_cf() is True


# ---------------------------------------------------------------------------
# Pitfall 1 -- the two subsidy lags are different lags


def test_the_two_subsidy_lags_are_not_one_lag(riester_rente, de_riester_anchor):
    """income_ref looks back one *calendar* year; zulage_pp one *projection* year.

    ``income_ref(1) = income_init`` and ``income_ref(t) = income_schedule[t - 1]``, while
    ``zulage_pp(t) = zulage_granted_pp(t - 1)``.  The visible consequence on the anchor is
    that ``zulagen`` falls at t = 4 while ``premiums`` rises at t = 3: the entitlement drops
    a year before the credit does, and the § 86 minimum is 4 % of income *less* the
    entitlement, so a Zulage that stops is a contribution the saver must make good.
    """
    p = de_riester_anchor
    schedule = riester_rente.Data.income_schedule()
    assert p.income_ref(1) == pytest.approx(p.income_init(), rel=1e-12)
    for t in (2, 5, 10, 17):
        assert p.income_ref(t) == pytest.approx(
            float(schedule.at[(p.income_id(), t - 1), "income"]), rel=1e-12)
    assert p.zulage_pp(1) == pytest.approx(p.zulage_init_pp(), rel=1e-12)
    for t in range(2, p.t_conv() + 1):
        assert p.zulage_pp(t) == pytest.approx(p.zulage_granted_pp(t - 1), rel=1e-12)
    # The entitlement steps down at t = 3 and the credit only at t = 4.
    assert p.zulage_entitlement_pp(2) == pytest.approx(475.00, abs=CENT)
    assert p.zulage_entitlement_pp(3) == pytest.approx(175.00, abs=CENT)
    assert p.zulage_pp(3) == pytest.approx(475.00, abs=CENT)
    assert p.zulage_pp(4) == pytest.approx(175.00, abs=CENT)
    assert p.zulagen(3) > p.zulagen(4)
    assert p.premiums(3) > p.premiums(2)
    assert p.check_zulage_lag() is True
    assert all(p.check_zulage_lag_resid(t) == pytest.approx(0.0, abs=1e-9)
               for t in (1, 2, 3, 4, 17, 18, 19, 61))


# ---------------------------------------------------------------------------
# Pitfall 2 -- the final contribution year's Zulage lands in the conversion year


def test_the_last_contribution_years_zulage_is_credited_at_conversion(de_riester_anchor):
    """Contributions stop at t_conv() - 1; the Zulage they earned is credited at t_conv().

    It must be credited, guaranteed and converted before the *Beitragsgarantie* is tested.
    Stopping the Zulage with the contribution removes a full year's subsidy from the
    account **and** from the guarantee, which is 175,00 EUR on this cell.
    """
    p = de_riester_anchor
    T = p.t_conv()
    assert p.eigenbeitrag_pp(T - 1) > 0.0
    assert p.eigenbeitrag_pp(T) == 0.0
    assert p.zulage_pp(T) == pytest.approx(175.00, abs=CENT)
    assert p.zulagen(T) == pytest.approx(134.33, abs=CENT)
    assert p.zulage_pp(T + 1) == 0.0
    # It is in the guarantee accumulator ...
    assert p.guar_pp(T + 1) - p.guar_pp(T) == pytest.approx(175.00, abs=CENT)
    # ... and inside the conversion account, through the conversion year's Sparbeitrag.
    assert p.prem_to_av_pp(T) == pytest.approx(156.00, abs=CENT)
    assert p.account_conv_pp() - (p.dk_pp(T) + p.surplus_acct_pp(T)
                                  + p.slueb_pp() + p.bewres_pp()) == pytest.approx(
        156.00, abs=CENT)


# ---------------------------------------------------------------------------
# Pitfall 3 -- the Mindesteigenbeitrag is not a cliff


def test_the_kuerzung_is_proportional_and_not_a_cliff(riester_rente):
    """Model point 7 pays half the § 86 minimum and draws exactly half the Zulagen.

    Not zero, and not the full amount: § 86 reduces the subsidy in the ratio of the
    contribution paid to the minimum.  A model treating the minimum as a cliff misstates
    every path in which the saver reduces contributions, and the German book is full of
    them.
    """
    p = riester_rente.Projection[7]
    assert p.contrib_ratio() == 0.5
    for t in (1, 2, 3, 5, 10):
        assert p.eigenbeitrag_pp(t) == pytest.approx(
            0.5 * p.mindesteigenbeitrag_pp(t), rel=1e-12)
        assert p.zulage_granted_pp(t) == pytest.approx(
            0.5 * p.zulage_entitlement_pp(t), rel=1e-12)
        assert p.zulage_granted_pp(t) > 0.0
    assert p.zulage_entitlement_pp(1) == pytest.approx(475.00, abs=CENT)
    assert p.zulage_granted_pp(1) == pytest.approx(237.50, abs=CENT)
    # Paying the minimum in full draws it in full, on the same entitlement path.
    full = riester_rente.Projection[1]
    assert full.contrib_ratio() == 1.0
    assert full.zulage_granted_pp(1) == pytest.approx(475.00, abs=CENT)
    assert p.zulage_granted_pp(1) == pytest.approx(
        0.5 * full.zulage_granted_pp(1), rel=1e-12)


# ---------------------------------------------------------------------------
# Pitfall 4 -- the Zulage is a contribution, not a benefit


def test_the_zulage_is_a_positive_income_column_of_its_own(de_riester_anchor):
    """It is paid by the ZfA to the provider and credited to the contract.

    So it is published beside ``premiums`` and never folded into it, it never appears with
    a negative sign, and ``premiums`` excludes it: ``premiums(t)`` is the *Eigenbeitrag*
    after the *Ratenzuschlag* plus any unsubsidised contribution, and nothing else.
    """
    p = de_riester_anchor
    df = p.result_cf()
    assert "zulagen" in df.columns and "premiums" in df.columns
    assert (df["zulagen"] >= 0.0).all()
    assert (df.loc[1:18, "zulagen"] > 0.0).all()
    assert (df.loc[19:, "zulagen"] == 0.0).all()
    for t in (1, 5, 17):
        assert p.zulagen(t) == pytest.approx(p.zulage_pp(t) * p.pols_if(t), rel=1e-12)
        assert p.premiums(t) == pytest.approx(
            p.eigenbeitrag_paid_pp(t) * p.pols_if(t), rel=1e-12)
        assert p.premiums(t) != pytest.approx(
            (p.eigenbeitrag_paid_pp(t) + p.zulage_pp(t)) * p.pols_if(t), abs=CENT)
    # It is a contribution: it enters the guarantee accumulator and the subsidised pool.
    assert p.guar_pp(2) - p.guar_pp(1) == pytest.approx(
        p.eigenbeitrag_pp(1) + p.zulage_pp(1), abs=CENT)
    assert p.pool_gefoerdert_pp(1) == pytest.approx(
        p.eigenbeitrag_pp(1) + p.zulage_pp(1), abs=CENT)


# ---------------------------------------------------------------------------
# Pitfall 5 -- the Günstigerprüfung is not a contract cash flow


def test_the_guenstigerpruefung_has_no_cells_and_no_column(riester_rente):
    """Only the Zulage reaches the policy; the § 10a advantage is a personal tax refund.

    A model that credited the contract with the *Sonderausgabenabzug* would be crediting it
    with money that never arrives.  The absent names are asserted, because they are exactly
    what a reader who has just read the tax section would add.
    """
    names = set(riester_rente.Projection.cells) | set(riester_rente.Projection.refs)
    for absent in ("guenstigerpruefung", "guenstiger_pruefung", "sonderausgabenabzug",
                   "sonderausgaben_pp", "tax_relief_pp", "steuervorteil_pp",
                   "marginal_tax_rate", "tax_refund", "foerderung_10a_pp",
                   "rueckzahlungsbetrag_pp", "einkommensteuer"):
        assert absent not in names, absent
    columns = riester_rente.Projection[1].result_cf().columns
    assert not [c for c in columns if "tax" in c or "steuer" in c or "guenstig" in c]
    # The reclaimable Zulage limb *is* published, as a diagnostic and nothing more.
    assert "zulage_cum_pp" in names


# ---------------------------------------------------------------------------
# Pitfall 6 -- the two Kinderzulage rates are a birth-cohort split


def test_both_kinderzulage_rates_run_at_once(riester_rente):
    """Model point 3 has a child born in 2006 and one born in 2010, so it draws both.

    ``175 + 185 + 300 = 660,00 EUR`` in years 1 and 2.  The split is permanent -- it is a
    birth-cohort rule, not a transition -- so a single rate misprices every family cell
    spanning the 2008 boundary.
    """
    p = riester_rente.Projection[3]
    schedule = riester_rente.Data.zulage_schedule()
    row = schedule.loc[(p.zulage_id(), 1)]
    assert float(row["n_kinder_pre2008"]) == 1.0
    assert float(row["n_kinder_post2008"]) == 1.0
    assert p.zulage_entitlement_pp(1) == pytest.approx(175.0 + 185.0 + 300.0, abs=CENT)
    assert p.zulage_entitlement_pp(2) == pytest.approx(660.00, abs=CENT)
    # The pre-2008 child's Kindergeld stops first, so the entitlement falls to 475,00.
    assert p.zulage_entitlement_pp(3) == pytest.approx(175.0 + 300.0, abs=CENT)
    # A single-rate implementation would give 175 + 2 x 300 or 175 + 2 x 185 instead.
    assert p.zulage_entitlement_pp(1) != pytest.approx(175.0 + 2 * 300.0, abs=CENT)
    assert p.zulage_entitlement_pp(1) != pytest.approx(175.0 + 2 * 185.0, abs=CENT)
    # And the anchor's own child, born in 2010, draws the post-2008 rate alone.
    anchor = riester_rente.Projection[1]
    assert anchor.zulage_entitlement_pp(1) == pytest.approx(175.0 + 300.0, abs=CENT)


# ---------------------------------------------------------------------------
# Pitfall 7 -- the Beitragsgarantie is tested once, at Rentenbeginn


def test_the_guarantee_is_tested_only_at_rentenbeginn(de_riester_anchor):
    """The anchor opens 358,94 EUR under water and no benefit is floored at the guarantee.

    ``garantieluecke_pp(t)`` is a diagnostic: it peaks at 567,69 EUR at t = 3 and reaches
    zero at t = 7, and through all of it the death benefit is the account value, the
    *Rückkaufswert* is 98 % of it, and the transfer value is it less 50,00 EUR -- every one
    of them **below** ``guar_pp(t)`` in the early durations.
    """
    p = de_riester_anchor
    assert p.garantieluecke_pp(1) == pytest.approx(358.94, abs=CENT)
    assert p.garantieluecke_pp(3) == pytest.approx(567.69, abs=CENT)
    assert p.garantieluecke_pp(7) == 0.0
    assert p.guar_pp(1) > p.av_pp(1)
    for t in (1, 2, 3):
        assert p.db_pp(t) == pytest.approx(p.av_pp_at(t, "AFT_INT"), rel=1e-12)
        assert p.cv_pp(t) == pytest.approx(0.98 * p.av_pp_at(t, "AFT_INT"), rel=1e-12)
        assert p.transfer_value_pp(t) == pytest.approx(
            p.av_pp_at(t, "AFT_INT") - 50.0, rel=1e-12)
        assert p.db_pp(t) < p.guar_pp(t + 1)      # not floored, and visibly so
        assert p.cv_pp(t) < p.db_pp(t)
    # The one place the guarantee bites is the conversion.
    assert p.capital_conv_pp() == pytest.approx(
        max(p.account_conv_pp(), p.guar_pp(p.t_conv() + 1)), rel=1e-12)
    assert p.check_guar_roll_fwd() is True


# ---------------------------------------------------------------------------
# Pitfall 8 -- the biometric carve-out and its 20 % cap


def test_the_rider_carve_out_is_capped_at_twenty_per_cent(riester_rente):
    """Model point 9 sits exactly on the cap: 400,00 EUR of rider premium carves out 240,00.

    ``kappa = min(rider, 0.20 x (E + Z + extra + rider)) = 0.20 x 1 200,00 = 240,00``,
    **strictly less than** the rider premium, so 160,00 EUR of it does not shrink the
    guarantee at all.  An implementation that carved out the whole rider premium would
    understate the guarantee accumulator by that much every year.
    """
    p = riester_rente.Projection[9]
    assert p.rider_prem_pp() == 400.0
    for t in (1, 2, 5, 10):
        base = (p.eigenbeitrag_pp(t) + p.zulage_pp(t) + p.contrib_extra_pp()
                + p.rider_prem_pp())
        assert p.guar_carve_out_pp(t) == pytest.approx(0.20 * base, rel=1e-12)
        assert p.guar_carve_out_pp(t) < p.rider_prem_pp()
    assert p.guar_carve_out_pp(1) == pytest.approx(240.00, abs=CENT)
    assert p.rider_prem_pp() - p.guar_carve_out_pp(1) == pytest.approx(160.00, abs=CENT)
    # The accumulator steps by E + Z - kappa, not by E + Z - rider.
    assert p.guar_pp(2) - p.guar_pp(1) == pytest.approx(
        625.0 + 175.0 - 240.0, abs=CENT)
    assert p.guar_pp(2) - p.guar_pp(1) != pytest.approx(
        625.0 + 175.0 - 400.0, abs=CENT)
    assert p.check_guar_roll_fwd() is True
    # And the rider premium is not a cash flow of this model at all.
    assert p.premiums(1) == pytest.approx(
        p.eigenbeitrag_paid_pp(1) * p.pols_if(1), rel=1e-12)
    anchor = riester_rente.Projection[1]
    assert anchor.rider_prem_pp() == 0.0
    assert all(anchor.guar_carve_out_pp(t) == 0.0 for t in (1, 5, 17))


# ---------------------------------------------------------------------------
# Pitfall 9 -- unsubsidised contributions are inside the guarantee


def test_unsubsidised_contributions_enter_the_guarantee(riester_rente):
    """Model point 8 pays 900,00 EUR a year above the § 10a ceiling.

    The undertaking is on the *Altersvorsorgebeiträge* paid in and does not distinguish the
    pools, so the accumulator steps by ``1 925 + 175 + 900 = 3 000,00`` while the
    entitlement never moves off the *Grundzulage*.  The two pools are tracked separately
    because the benefit's taxation forks between them.
    """
    p = riester_rente.Projection[8]
    assert p.contrib_extra_pp() == 900.0
    for t in (1, 2, 5):
        assert p.guar_pp(t + 1) - p.guar_pp(t) == pytest.approx(
            p.eigenbeitrag_pp(t) + p.zulage_pp(t) + 900.0, abs=CENT)
        assert p.zulage_entitlement_pp(t) == pytest.approx(175.00, abs=CENT)
    assert p.guar_pp(2) - p.guar_pp(1) == pytest.approx(3000.00, abs=CENT)
    # The two pools diverge, and only the subsidised one carries the Zulage.
    assert p.pool_ungefoerdert_pp(3) == pytest.approx(3 * 900.0, abs=CENT)
    assert p.pool_gefoerdert_pp(3) == pytest.approx(3 * (1925.0 + 175.0), abs=CENT)
    assert p.premiums(1) == pytest.approx((1925.0 + 900.0) * p.pols_if(1), abs=CENT)
    # On the anchor the two pools coincide, which is why it is the plain cell.
    anchor = riester_rente.Projection[1]
    assert anchor.contrib_extra_pp() == 0.0
    assert all(anchor.pool_ungefoerdert_pp(t) == 0.0 for t in (1, 5, 17))


# ---------------------------------------------------------------------------
# Pitfall 10 -- the declared rate includes the Rechnungszins


def test_the_declared_rate_includes_and_is_not_added_to_the_guaranteed_rate(
        de_riester_anchor):
    """int_credited_pp(t) = j(t) x (D + S + U) exactly, never (i + j) x anything.

    The *Deckungskapital* bears ``i`` in ``int_guar_pp`` and only the excess ``j - i`` in
    ``int_surplus_pp``; the *Überschussguthaben* bears the whole declared rate, having no
    guarantee to carve out of it.  Adding the two rates would credit 2,55 % instead of
    2,30 % -- an 11 % overstatement of the interest credit, compounding for seventeen years.
    """
    p = de_riester_anchor
    for t in (1, 5, 10, 17):
        j, i = p.laufende_verz(t), p.rechnungszins()
        assert j == pytest.approx(0.023, rel=1e-12)
        assert i == pytest.approx(0.0025, rel=1e-12)
        base = p.dk_pp(t) + p.prem_to_av_pp(t)
        assert p.int_guar_pp(t) == pytest.approx(i * base, rel=1e-12)
        assert p.int_surplus_pp(t) == pytest.approx(
            (j - i) * base + j * p.surplus_acct_pp(t), rel=1e-12)
        assert p.int_credited_pp(t) == pytest.approx(
            j * (base + p.surplus_acct_pp(t)), rel=1e-9)
        wrong = (i + j) * (base + p.surplus_acct_pp(t))
        assert wrong > p.int_credited_pp(t) * 1.10
    assert p.int_credited(1) == pytest.approx(
        p.int_credited_pp(1) * p.pols_if(1), rel=1e-12)


def test_setting_the_declared_rate_to_the_guaranteed_rate_empties_the_surplus_leg():
    """With j = i the *Deckungskapital* leg of int_surplus_pp is exactly zero.

    Swapped in through the input file, not through a formula change, which is the point of
    keeping the scenario outside the model.  It also makes the anchor's own guarantee bind:
    with no surplus at all the account falls 269,01 EUR short at *Rentenbeginn*.
    """
    import pandas as pd

    model = mx.read_model(MODEL_DIR, name="Riester_DE_A_flat_j")
    alt = None
    try:
        scenario = pd.read_csv(model.Data.input_dir() / "surplus_scenario.csv")
        scenario.loc[scenario["scenario_id"] == "base", "laufende_verz"] = 0.0025
        alt = model.Data.input_dir() / "surplus_scenario_flat.csv"
        scenario.to_csv(alt, index=False)
        model.Data.surplus_file = alt.name
        model.Data.clear_all()
        model.Projection.clear_all()
        p = model.Projection[1]
        assert p.laufende_verz(1) == pytest.approx(p.rechnungszins(), rel=1e-12)
        assert p.int_surplus_pp(1) == pytest.approx(
            p.laufende_verz(1) * p.surplus_acct_pp(1), rel=1e-12)
        assert p.int_credited_pp(1) == pytest.approx(
            p.int_guar_pp(1) + p.int_surplus_pp(1), rel=1e-12)
        assert p.garantieluecke_conv_pp() == pytest.approx(269.01, abs=CENT)
        assert p.check_av_roll_fwd() is True
    finally:
        if alt is not None:
            alt.unlink(missing_ok=True)
        model.close()


# ---------------------------------------------------------------------------
# Pitfall 11 -- the Ratenzuschlag is a charge and never a credit


def test_the_frequency_loading_is_charged_and_never_credited(riester_rente):
    """Model point 3 is monthly: the saver pays E x 1,03 and only E reaches the account.

    ``admin_charge_pp`` takes the loading straight back out and strikes its percentage on
    the **unloaded** contribution, so the *Sparbeitrag* is algebraically independent of the
    payment frequency while ``premiums`` is larger by exactly ``E(t) x 0,03``.
    """
    p = riester_rente.Projection[3]
    assert p.prem_freq() == "monthly" and p.prem_freq_load() == 1.03
    for t in (1, 2, 3, 5):
        e, z = p.eigenbeitrag_pp(t), p.zulage_pp(t)
        assert p.eigenbeitrag_paid_pp(t) == pytest.approx(1.03 * e, rel=1e-12)
        assert p.premiums(t) == pytest.approx(1.03 * e * p.pols_if(t), rel=1e-12)
        assert p.contrib_total_pp(t) == pytest.approx(1.03 * e + z, rel=1e-12)
        # The administration charge is 4 % of the *unloaded* base plus 12,00 plus the
        # loading itself, so the Sparbeitrag carries no phi at all.
        assert p.admin_charge_pp(t) == pytest.approx(
            0.04 * (e + z) + 12.0 + e * 0.03, rel=1e-9)
        assert p.prem_to_av_pp(t) == pytest.approx(
            (e + z) - p.acq_charge_pp(t) - (0.04 * (e + z) + 12.0), rel=1e-9)
    anchor = riester_rente.Projection[1]
    assert anchor.prem_freq() == "annual" and anchor.prem_freq_load() == 1.0
    assert anchor.eigenbeitrag_paid_pp(1) == pytest.approx(
        anchor.eigenbeitrag_pp(1), rel=1e-12)


def test_removing_the_loading_moves_premiums_and_nothing_else():
    """Swap the loading table for a flat one: only ``premiums`` moves.

    ``prem_to_av_pp``, ``guar_pp`` and every benefit are identical to the last bit, which
    is the invariance the notes' pitfall 11 asserts and the reason the loading is deducted
    exactly once rather than twice.
    """
    import pandas as pd

    model = mx.read_model(MODEL_DIR, name="Riester_DE_A_flat_phi")
    alt = None
    try:
        p = model.Projection[3]
        before_prem = [p.premiums(t) for t in (1, 2, 3)]
        before_sav = [p.prem_to_av_pp(t) for t in (1, 2, 3)]
        before_guar = [p.guar_pp(t) for t in (1, 2, 3)]
        before_claims = [p.claims(t, "DEATH") for t in (1, 2, 3)]
        before_e = [p.eigenbeitrag_pp(t) for t in (1, 2, 3)]
        before_pols = [p.pols_if(t) for t in (1, 2, 3)]

        table = pd.read_csv(model.Data.input_dir() / "freq_loading.csv",
                            index_col="prem_freq")
        table["load"] = 1.0
        alt = model.Data.input_dir() / "freq_loading_flat.csv"
        table.to_csv(alt)
        model.Data.freq_loading_file = alt.name
        model.Data.clear_all()
        model.Projection.clear_all()

        q = model.Projection[3]
        assert q.prem_freq_load() == 1.0
        for k, t in enumerate((1, 2, 3)):
            assert q.prem_to_av_pp(t) == pytest.approx(before_sav[k], rel=1e-12)
            assert q.guar_pp(t) == pytest.approx(before_guar[k], rel=1e-12)
            assert q.claims(t, "DEATH") == pytest.approx(before_claims[k], rel=1e-12)
            assert q.pols_if(t) == pytest.approx(before_pols[k], rel=1e-12)
            assert before_prem[k] - q.premiums(t) == pytest.approx(
                0.03 * before_e[k] * before_pols[k], rel=1e-9)
        assert q.premiums(1) == pytest.approx(1020.00, abs=CENT)
    finally:
        if alt is not None:
            alt.unlink(missing_ok=True)
        model.close()


# ---------------------------------------------------------------------------
# Pitfall 12 -- the acquisition charge is spread, and survives Beitragsfreistellung


def test_the_acquisition_charge_is_spread_over_five_contract_years(
        riester_rente, de_riester_anchor):
    """Equal in contract years 1 to 5 and zero afterwards, on the **contract** clock.

    The anchor is in force at duration 3, so projection years 1 and 2 are contract years 4
    and 5 and carry 168,00 EUR each; from year 3 the charge is over.  Model point 2 is the
    same contract from its own inception and carries it in projection years 1 to 5.
    """
    p = de_riester_anchor
    assert p.duration_init() == 3
    assert [p.duration(t) for t in (1, 2, 3)] == [4, 5, 6]
    assert p.acq_charge_pp(1) == pytest.approx(168.00, abs=CENT)
    assert p.acq_charge_pp(2) == pytest.approx(168.00, abs=CENT)
    assert all(p.acq_charge_pp(t) == 0.0 for t in (3, 4, 10, 17))
    # 168,00 of the Sparbeitrag's rise between t = 2 and t = 3 is the charge ending.
    assert p.prem_to_av_pp(3) - p.prem_to_av_pp(2) == pytest.approx(488.90, abs=CENT)
    at_issue = riester_rente.Projection[2]
    assert at_issue.duration_init() == 0
    assert all(at_issue.acq_charge_pp(t) == pytest.approx(168.00, abs=CENT)
               for t in range(1, 6))
    assert at_issue.acq_charge_pp(6) == 0.0
    assert sum(at_issue.acq_charge_pp(t) for t in range(1, 7)) == pytest.approx(
        0.025 * 33600.0, abs=CENT)


def test_the_acquisition_charge_survives_beitragsfreistellung(riester_rente):
    """Model point 10 goes paid-up at t = 4 and the charge keeps biting.

    ``prem_to_av_pp(4) = 175,00 - 168,00 - 19,00 = -12,00``: the last Zulage arrives, the
    acquisition charge and the fixed administration charge do not stop, and the
    *Deckungskapital* falls.  Stopping the charge at *Beitragsfreistellung* would hide the
    mechanic this model point exists to show.
    """
    p = riester_rente.Projection[10]
    assert p.bfs_year() == 4
    assert p.duration(4) == 5
    assert p.acq_charge_pp(4) == pytest.approx(168.00, abs=CENT)
    assert p.eigenbeitrag_pp(4) == 0.0
    assert p.zulage_pp(4) == pytest.approx(175.00, abs=CENT)
    assert p.admin_charge_pp(4) == pytest.approx(0.04 * 175.0 + 12.0, abs=CENT)
    assert p.prem_to_av_pp(4) == pytest.approx(-12.00, abs=CENT)
    assert p.prem_to_av_pp(5) == pytest.approx(-12.00, abs=CENT)
    assert p.acq_charge_pp(5) == 0.0          # contract year 6, the window is over
    assert p.prem_to_av_pp(4) < 0.0 and p.prem_to_av_pp(3) > 0.0


# ---------------------------------------------------------------------------
# Pitfall 13 -- an Anbieterwechsel is not a surrender


def test_a_transfer_is_a_separate_decrement_from_a_surrender(
        riester_rente, de_riester_anchor):
    """Full account less a flat 50,00 EUR, with no *Stornoabzug*, and its own column.

    The *Wechselrecht* carries none of the *schädliche Verwendung* consequences a
    *Kündigung* does, so the transfer rate is set above the surrender rate at every
    duration and the two produce different benefits from the same account.
    """
    p = de_riester_anchor
    for t in (1, 5, 12, 17):
        a = p.av_pp_at(t, "AFT_INT")
        assert p.cv_pp(t) == pytest.approx(0.98 * a, rel=1e-12)
        assert p.transfer_value_pp(t) == pytest.approx(a - 50.0, rel=1e-12)
        assert p.transfer_value_pp(t) > p.cv_pp(t)
        assert p.transfer_rate(t) > p.lapse_rate(t)
    lapse = riester_rente.Data.lapse_table()
    assert (lapse["transfer_rate"] > lapse["lapse_rate"]).all()
    assert list(lapse.loc[1]) [:2] == [0.008, 0.012]
    df = p.result_cf()
    assert "claims_lapse" in df.columns and "claims_transfer" in df.columns
    assert (df["claims_transfer"].loc[1:17] > df["claims_lapse"].loc[1:17]).all()
    assert df["claims_transfer"].sum() == pytest.approx(2250.97, abs=CENT)
    assert df["claims_lapse"].sum() == pytest.approx(1481.42, abs=CENT)
    # The charge the insurer retains differs in kind: a percentage against a flat euro fee.
    assert p.exit_charge_pp(1) == pytest.approx(
        0.02 * p.av_pp_at(1, "AFT_INT") * p.pols_lapse(1)
        + 50.0 * p.pols_transfer(1), rel=1e-12)


# ---------------------------------------------------------------------------
# Pitfall 14 -- Beitragsfreistellung is a state change, not a termination


def test_beitragsfreistellung_is_a_state_change(riester_rente):
    """Model point 10: ``pols_if`` continuous, guarantee frozen, Zulagen stopped, account rolling.

    Nothing leaves the in-force at ``bfs_year``; the ordinary decrements carry on and the
    roll-forward closes.  The guarantee freezes only once the **last** Zulage has landed --
    one year after the contribution stops -- which is the same one-year arrear that makes
    pitfall 2 a pitfall.
    """
    p = riester_rente.Projection[10]
    b = p.bfs_year()
    # The in-force is continuous: the year of the switch decrements like any other.
    assert p.pols_if(b) == pytest.approx(
        p.pols_if(b - 1) * (1.0 - p.mort_rate(b - 1)) * (1.0 - p.lapse_rate(b - 1))
        * (1.0 - p.transfer_rate(b - 1)), rel=1e-12)
    assert p.pols_if(b) > 0.9 * p.pols_if(b - 1)
    assert p.check_pols_roll_fwd() is True
    # Contributions stop; the Zulage lands once more and then stops.
    assert p.eigenbeitrag_pp(b - 1) > 0.0
    assert all(p.eigenbeitrag_pp(t) == 0.0 for t in range(b, p.t_conv()))
    assert p.premiums(b) == 0.0
    assert p.zulage_pp(b) > 0.0
    assert all(p.zulage_pp(t) == 0.0 for t in range(b + 1, p.t_conv() + 1))
    # The guarantee freezes after that last credit, and the account keeps rolling.
    frozen = p.guar_pp(b + 1)
    assert all(p.guar_pp(t) == pytest.approx(frozen, abs=CENT)
               for t in (b + 2, 10, p.t_conv() + 1))
    assert p.av_pp(b + 2) > 0.0 and p.av_pp(p.t_conv()) > p.av_pp(b)
    assert p.check_guar_roll_fwd() is True


# ---------------------------------------------------------------------------
# Pitfall 15 -- two mortality bases, and a generational annuity table


def test_the_two_phases_use_different_mortality_bases(de_riester_anchor):
    """The basis switches at t_conv(), and the two factors run in opposite directions.

    Accumulation is the DAV 2008 T proxy at ``mort_be_factor = 0.80``; payout is the
    generational DAV 2004 R proxy at ``annuity_mort_be_factor = 1.15``.  A first-order
    death table assumes mortality higher than expected and a first-order annuity table
    lower, so the best estimate sits below the one and above the other.
    """
    p = de_riester_anchor
    T = p.t_conv()
    for t in (1, 5, 17):
        assert p.mort_rate(t) == pytest.approx(
            p.mort_rate_at_age(p.age(t)) * 0.80, rel=1e-12)
    for t in (T, T + 1, 40):
        assert p.mort_rate(t) == pytest.approx(
            p.annuity_mort_rate(p.age(t), p.calendar_year(t)) * 1.15, rel=1e-12)
    # At the boundary the two bases give materially different rates for the same life.
    assert p.mort_rate_at_age(67) * 0.80 != pytest.approx(p.mort_rate(T), rel=1e-3)


def test_the_annuity_basis_is_generational(de_riester_anchor):
    """annuity_mort_rate(x, tau) depends on **both** arguments and falls with tau.

    A period-table proxy would price a seventeen-year-deferred annuitisation on 2027
    mortality instead of 2044 mortality, understating it by a margin that dwarfs every
    other assumption in the model: at age 67 the two differ by a quarter.
    """
    p = de_riester_anchor
    q2027 = p.annuity_mort_rate(67, 2027)
    q2044 = p.annuity_mort_rate(67, 2044)
    assert q2044 < q2027
    assert p.annuity_mort_rate(67, 2045) < q2044
    assert q2044 / q2027 == pytest.approx((1.0 - 0.0171) ** 17, rel=1e-9)
    assert 1.0 - q2044 / q2027 == pytest.approx(0.254, abs=0.005)
    # ann_factor() is struck on the conversion year, calendar 2044, at factor 1.00.
    assert p.calendar_year(p.t_conv()) == 2044
    assert p.ann_factor() == pytest.approx(20.87222879, abs=5e-9)
    # Both tables are forced to 1 at omega_age so the closure identity is exact.
    assert p.mort_rate_at_age(110) == 1.0
    assert p.annuity_mort_rate(110, 2044) == 1.0


# ---------------------------------------------------------------------------
# Pitfall 16 -- the Kleinbetragsrente test


def test_the_kleinbetragsrente_is_tested_after_the_lump_sum(riester_rente,
                                                            de_riester_anchor):
    """The test is applied to the annuity payable **after** the elected 30 %, on a flat
    threshold, and the commutation is computed rather than assumed.

    Model point 5's capital of 4 537,22 EUR would buy 9,21 EUR a month after the lump sum,
    against a 39,55 EUR threshold, so it commutes; the anchor's 92,89 EUR clears it.  A
    commuted contract pays the **whole** capital as an *Abfindung* and no lump sum and no
    annuity beside it, and the payment discharges the contract outright.
    """
    small = riester_rente.Projection[5]
    T = small.t_conv()
    assert small.capital_conv_pp() == pytest.approx(4537.217342, abs=CENT)
    test_annuity = (1.0 - small.teilkapital_share()) * small.capital_conv_pp() \
        / 10000.0 * small.rentenfaktor_applied()
    assert test_annuity == pytest.approx(9.21, abs=CENT)
    assert test_annuity <= 39.55
    assert small.is_kleinbetrag() is True
    assert small.commutation_pp() == pytest.approx(small.capital_conv_pp(), rel=1e-12)
    assert small.teilkapital_pp() == 0.0
    assert small.annuity_capital_pp() == 0.0
    assert small.annuity_pp(T) == 0.0
    assert small.claims(T, "COMMUTATION") == pytest.approx(3828.31, abs=CENT)
    assert small.claims(T, "LUMPSUM") == 0.0
    assert all(small.claims(t, "ANNUITY") == 0.0 for t in range(T, small.proj_len() + 1))
    # The Abfindung discharges the contract: no decrement removes the population.
    assert small.pols_if(T + 1) == 0.0
    assert small.pols_death(T) == 0.0
    assert small.check_pols_roll_fwd() is True
    assert small.result_cf().index[-1] == small.proj_len() == 55
    # The anchor clears the threshold, and the threshold is flat in nominal terms.
    p = de_riester_anchor
    assert p.annuity_month_pp() == pytest.approx(92.885458, abs=CENT)
    assert p.is_kleinbetrag() is False
    assert riester_rente.Projection.kleinbetrag_threshold_mth == 39.55
    # Four of the thirteen model points commute, and they are the small-capital ones.
    commuting = [n for n in (4, 5, 10, 13)
                 if riester_rente.Projection[n].is_kleinbetrag()]
    assert commuting == [4, 5, 10, 13]


# ---------------------------------------------------------------------------
# Pitfall 17 -- the Rentengarantiezeit changes the count, not the payment


def test_the_rentengarantiezeit_changes_who_is_paid_and_never_how_much(
        riester_rente, de_riester_anchor):
    """pols_annuity_pay is pols_conv() inside the guarantee period and pols_if after it.

    The instalment does not move: ``annuity_pp(t)`` is 1 114,625493 EUR in every payout
    year of the anchor, guarantee period or not, and the cells does not read
    ``rentengarantie_years`` at all.  Model point 12 has no guarantee period and pays the
    same annuity per policy to a smaller count.
    """
    p = de_riester_anchor
    T, n = p.t_conv(), p.proj_len()
    assert p.rentengarantie_years() == 10
    for t in range(T, T + 10):
        assert p.pols_annuity_pay(t) == pytest.approx(p.pols_conv(), rel=1e-12)
        assert p.claims(t, "ANNUITY") == pytest.approx(855.572802, abs=CENT)
    for t in (T + 10, T + 11, n):
        assert p.pols_annuity_pay(t) == pytest.approx(p.pols_if(t), rel=1e-12)
    assert p.pols_annuity_pay(T + 9) > p.pols_if(T + 9)
    assert all(p.annuity_pp(t) == pytest.approx(1114.625493, abs=CENT)
               for t in (T, T + 5, T + 20, n))
    # The formula for the payment does not mention the guarantee period; the count's does.
    cells = riester_rente.Projection.cells
    assert "rentengarantie_years()" not in cells["annuity_pp"].formula.source
    assert "rentengarantie_years()" in cells["pols_annuity_pay"].formula.source
    # Model point 12: no guarantee period, and no lump sum either, so the whole capital is
    # annuitised and the annuity is the anchor's divided by 0.70.
    pure = riester_rente.Projection[12]
    assert pure.rentengarantie_years() == 0 and pure.teilkapital_share() == 0.0
    assert all(pure.pols_annuity_pay(t) == pytest.approx(pure.pols_if(t), rel=1e-12)
               for t in (pure.t_conv(), pure.t_conv() + 5, pure.proj_len()))
    assert pure.annuity_capital_pp() == pytest.approx(pure.capital_conv_pp(), rel=1e-12)
    assert pure.annuity_pp(pure.t_conv()) == pytest.approx(
        p.annuity_pp(T) / 0.70, rel=1e-9)
    assert pure.claims(pure.t_conv(), "LUMPSUM") == 0.0


# ---------------------------------------------------------------------------
# Pitfall 18 -- benefits are gross of the Rückzahlungsbetrag


def test_benefits_are_published_gross_of_the_rueckzahlungsbetrag(riester_rente,
                                                                 de_riester_anchor):
    """The provider withholds the Zulagen and the § 10a relief and remits them to the ZfA.

    That is a tax collection, not a reduction in the insurer's obligation, so
    ``claims_death`` is the whole account value and netting the reclaimable amount out of
    it would understate the outgo -- by 4 050,00 EUR of cumulative Zulagen alone on this
    cell by the conversion year.
    """
    p = de_riester_anchor
    for t in (1, 5, 17):
        assert p.claims(t, "DEATH") == pytest.approx(
            p.av_pp_at(t, "AFT_INT") * p.pols_death(t), rel=1e-12)
        assert p.claims(t, "LAPSE") == pytest.approx(
            0.98 * p.av_pp_at(t, "AFT_INT") * p.pols_lapse(t), rel=1e-12)
        assert p.db_pp(t) > p.zulage_cum_pp(t)      # nothing has been netted out
    assert p.zulage_cum_pp(1) == pytest.approx(475.00, abs=CENT)
    assert p.zulage_cum_pp(18) == pytest.approx(4050.00, abs=CENT)
    assert p.zulage_cum_pp(18) == pytest.approx(
        sum(p.zulage_pp(t) for t in range(1, 19)), abs=CENT)
    # It is a diagnostic and nothing more: no claim reads it, and no cells attempts the
    # § 10a limb, which contract data cannot support.
    names = set(riester_rente.Projection.cells) | set(riester_rente.Projection.refs)
    assert "zulage_cum_pp" in names
    assert "zulage_cum_pp" not in riester_rente.Projection.cells[
        "claims"].formula.source
    assert "zulage_cum_pp" not in riester_rente.Projection.cells["db_pp"].formula.source
    assert "zulage_cum_pp" not in riester_rente.Projection.cells["cv_pp"].formula.source
    assert "zulage_cum_pp" not in [c for c in p.result_cf().columns]


# ---------------------------------------------------------------------------
# The check identities


def test_every_check_identity_closes_on_the_anchor(de_riester_anchor):
    """All six checks, and their residuals at the periods where each could break.

    ``check_net_cf()`` is delib's first ruling: the cash flow statement reconstructs its
    own headline number from its published parts, so ``net_cf`` is not the one quantity
    nothing checks.
    """
    p = de_riester_anchor
    for check in ("check_net_cf", "check_av_roll_fwd", "check_guar_roll_fwd",
                  "check_pols_roll_fwd", "check_conversion", "check_zulage_lag"):
        value = getattr(p, check)()
        assert isinstance(value, bool), check
        assert value is True, check
    for t in (1, 2, 17, 18, 19, 30, 61):
        assert p.check_net_cf_resid(t) == pytest.approx(0.0, abs=1e-9)
        assert p.check_av_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-9)
        assert p.check_guar_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-9)
        assert p.check_pols_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-12)
        assert p.check_conversion_resid(t) == pytest.approx(0.0, abs=1e-9)
        assert p.check_zulage_lag_resid(t) == pytest.approx(0.0, abs=1e-9)


def test_check_net_cf_reconstructs_the_row_from_its_published_parts(de_riester_anchor):
    """The identity in one line, on the frame rather than on the cells.

    Every column of ``result_cf()`` but ``pols_if``, ``pols_annuity_pay``,
    ``int_credited`` and ``liability_cf`` is in it, each exactly once.
    """
    df = de_riester_anchor.result_cf()
    outgo = sum(df["claims_" + k.lower()] for k in CLAIM_KINDS)
    rebuilt = df["premiums"] + df["zulagen"] - outgo - df["expenses"] - df["commissions"]
    assert (rebuilt - df["net_cf"]).abs().max() == pytest.approx(0.0, abs=1e-9)
    # int_credited is reported and not summed in -- the tempting mistake, because it is
    # the largest number on an accumulation row.
    assert df["int_credited"].loc[10] > df["net_cf"].loc[10] * 0.30
    assert (rebuilt + df["int_credited"] - df["net_cf"]).abs().max() > 100.0
    # Commission is a separate column from expenses and is subtracted exactly once.
    assert (df["commissions"] > 0.0).any()
    assert (df["expenses"].loc[1:17] > df["commissions"].loc[1:17]).all()


def test_the_conversion_identity_ties_the_factor_to_the_annuity_basis(riester_rente):
    """rentenfaktor_curr() x 12 x ann_factor() = (1 - margin) x 10 000, on every point.

    It holds whether or not the current factor is the one applied, which is what makes it
    a check on the annuity basis rather than on the conversion outcome; it is what catches
    a Woolhouse correction applied twice or a factor struck on the second-order basis.
    """
    margin = riester_rente.Projection.rentenfaktor_margin
    assert margin == 0.30
    for point_id in (1, 5, 11, 12, 13):
        p = riester_rente.Projection[point_id]
        assert p.rentenfaktor_curr() * 12.0 * p.ann_factor() == pytest.approx(
            (1.0 - margin) * 10000.0, rel=1e-12)
        assert p.rentenfaktor_applied() == pytest.approx(
            max(p.rentenfaktor_guar(), p.rentenfaktor_curr()), rel=1e-12)
        assert p.capital_conv_pp() == pytest.approx(
            p.teilkapital_pp() + p.annuity_capital_pp() + p.commutation_pp(), abs=1e-9)
        assert p.check_conversion() is True


# ---------------------------------------------------------------------------
# Structure, documentation and inputs


def test_result_cf_shape_and_both_signs_of_the_net_flow(de_riester_anchor):
    """Fifteen columns in the notes' order, indexed by t, contiguous, ending at proj_len().

    ``pols_if`` leads and its first value is ``pols_if_init()`` exactly; there is no bare
    ``claims`` subtotal column beside the six parts; and ``liability_cf`` is ``net_cf``
    outgo-positive.
    """
    p = de_riester_anchor
    df = p.result_cf()
    assert list(df.columns) == RESULT_CF_COLUMNS
    assert "claims" not in df.columns
    assert list(df.index) == list(range(1, 62))
    assert df.index.name == "t"
    assert df.index[-1] == p.proj_len() == 61
    assert df["pols_if"].iloc[0] == pytest.approx(p.pols_if_init(), rel=1e-12)
    assert (df["net_cf"] + df["liability_cf"]).abs().max() == pytest.approx(0.0, abs=1e-9)
    assert df.notna().all().all()
    # The shape of the cell: positive while it accumulates, then the conversion payment,
    # then a long thin annuity tail.
    assert (df["net_cf"].loc[1:17] > 0.0).all()
    assert df["net_cf"].loc[18] == pytest.approx(-11276.67, abs=CENT)
    assert (df["net_cf"].loc[19:] < 0.0).all()


def test_claims_totals_and_the_kind_argument(de_riester_anchor):
    """claims(t) is the sum over the six kinds, and an unknown kind raises."""
    p = de_riester_anchor
    for t in (1, 17, 18, 30):
        assert p.claims(t) == pytest.approx(
            sum(p.claims(t, k) for k in CLAIM_KINDS), rel=1e-12)
    assert p.claims(18) == pytest.approx(10536.610861 + 855.572802, abs=CENT)
    with pytest.raises(FormulaError):
        p.claims(1, "SURRENDER")
    with pytest.raises(FormulaError):
        p.pols_if_at(1, "AFTER_LAPSE")
    with pytest.raises(FormulaError):
        p.av_pp_at(1, "AFT_DECR")


def test_the_within_year_reads_are_consistent(de_riester_anchor):
    """pols_if_at and av_pp_at name the points the notes' timing convention defines."""
    p = de_riester_anchor
    for t in (1, 5, 17):
        assert p.pols_if_at(t, "BEF_DECR") == pytest.approx(p.pols_if(t), rel=1e-12)
        assert p.pols_if_at(t, "AFT_DECR") == pytest.approx(p.pols_if(t + 1), rel=1e-12)
        assert p.av_pp_at(t, "BEF_PREM") == pytest.approx(p.av_pp(t), rel=1e-12)
        assert p.av_pp_at(t, "AFT_PREM") == pytest.approx(
            p.av_pp(t) + p.prem_to_av_pp(t), rel=1e-12)
        assert p.av_pp_at(t, "AFT_INT") == pytest.approx(p.av_pp(t + 1), rel=1e-12)
        assert p.av_at(t, "BEF_PREM") == pytest.approx(
            p.av_pp(t) * p.pols_if(t), rel=1e-12)
    assert p.av_pp(1) == pytest.approx(p.dk_pp_init() + p.surplus_pp_init(), rel=1e-12)
    assert p.av_pp(1) == pytest.approx(4010.98, abs=CENT)


def test_the_model_point_is_read_and_sex_reaches_no_rate(riester_rente,
                                                         de_riester_anchor):
    """Riester tariffs are unisex from a 2006 vintage, so ``sex`` drives nothing.

    Model point 7 is the same age and entitlement path as the anchor with a male life; its
    mortality rate and its *Rentenfaktor* are the anchor's to the last bit, and only the
    contribution ratio and the payment frequency differ.
    """
    p = de_riester_anchor
    assert p.sex() == "F"
    assert p.issue_age() == 47 and p.duration_init() == 3
    assert p.age(1) == 50 and p.calendar_year(1) == 2027 and p.duration(1) == 4
    assert p.rentenbeginn_age() == 67 and p.t_conv() == 18
    assert p.proj_len() == 110 - 50 + 1
    male = riester_rente.Projection[7]
    assert male.sex() == "M" and male.age(1) == p.age(1)
    assert male.mort_rate(1) == pytest.approx(p.mort_rate(1), rel=1e-12)
    assert male.rentenfaktor_curr() == pytest.approx(p.rentenfaktor_curr(), rel=1e-12)
    assert "sex" not in riester_rente.Projection.cells["mort_rate"].formula.source
    assert "sex" not in riester_rente.Projection.cells["ann_factor"].formula.source


def test_docstrings_describe_the_current_structure(riester_rente):
    """Specifics a reader would rely on, asserted so they cannot go stale silently."""
    doc = riester_rente.doc
    assert "Riester" in doc
    assert "mechanics demonstration" in doc
    assert "external" in doc                     # inputs are not stored in the model
    assert "once per model" in doc               # why Data exists
    assert "Beitragsgarantie" in doc
    assert "Zulage" in doc
    assert "Data" in doc and "Projection" in doc
    proj = riester_rente.Projection.doc
    assert "Notes symbol" in proj
    for cells in ("proj_len", "model_point", "zulage_pp", "guar_pp", "t_conv",
                  "prem_to_av_pp", "pols_annuity_pay", "garantieluecke_conv_pp"):
        assert cells in proj, cells
    data = riester_rente.Data.doc
    assert "TradLife_A" in data
    for cells in ("input_dir", "model_point_table", "annuity_mort_table",
                  "zulage_schedule"):
        assert cells in data, cells
    # Every cells in both Spaces is documented.
    undocumented = [f"{s}.{c}" for s in riester_rente.spaces
                    for c in riester_rente.spaces[s].cells
                    if not riester_rente.spaces[s].cells[c].doc]
    assert not undocumented, undocumented


def test_the_savings_chassis_vocabulary_is_present(riester_rente):
    """Names shared with RV_DE_A, Basis_DE_A and Sofort_DE_S must mean the same thing."""
    shared = {
        "model_point", "proj_len", "age", "duration", "calendar_year",
        "pols_if", "pols_if_init", "pols_if_at", "pols_death", "pols_lapse",
        "mort_rate", "lapse_rate", "claims", "expenses", "commissions",
        "net_cf", "liability_cf", "result_cf",
        "av_pp", "av_pp_at", "av_at", "prem_to_av_pp", "dk_pp", "surplus_acct_pp",
        "rechnungszins", "laufende_verz", "t_conv", "is_accum", "is_payout",
        "ann_factor", "rentenfaktor_guar", "rentenfaktor_applied", "annuity_pp",
        "check_net_cf", "check_net_cf_resid",
    }
    names = set(riester_rente.Projection.cells) | set(riester_rente.Projection.refs)
    assert shared <= names, f"missing: {sorted(shared - names)}"
    # And the Schicht-2 vocabulary this product adds.
    riester = {
        "zulage_entitlement_pp", "zulage_granted_pp", "zulage_pp", "zulage_cum_pp",
        "zulagen", "mindesteigenbeitrag_pp", "eigenbeitrag_pp", "eigenbeitrag_paid_pp",
        "guar_pp", "guar_carve_out_pp", "garantieluecke_pp", "garantieluecke_conv_pp",
        "pool_gefoerdert_pp", "pool_ungefoerdert_pp", "is_kleinbetrag",
        "teilkapital_pp", "commutation_pp", "transfer_rate", "transfer_value_pp",
    }
    assert riester <= names, f"missing: {sorted(riester - names)}"


def test_the_shipped_tables_mark_their_own_provenance():
    """Eight CSVs beside run.py, and every one but the model point table says where its
    numbers came from -- delib's second ruling, asserted here on the values as well.

    The two decrement tables are **[std]** proxies: DAV 2008 T and DAV 2004 R are
    proprietary and are cited by name, never shipped.  The anchors a substitute must
    preserve are ``qx`` at age 50 and the generational structure of the annuity table.
    """
    import pandas as pd

    expected = {"model_point_table.csv", "mort_table_accum.csv",
                "annuity_mort_table.csv", "lapse_table.csv", "zulage_schedule.csv",
                "income_schedule.csv", "surplus_scenario.csv", "freq_loading.csv"}
    assert expected == {p.name for p in INPUT_DIR.iterdir() if p.suffix == ".csv"}

    mort = pd.read_csv(INPUT_DIR / "mort_table_accum.csv", index_col="age")
    assert all(p.startswith("[std]") for p in mort["provenance"])
    assert "DAV 2008 T" in mort["provenance"].iloc[0]
    assert float(mort.loc[50, "qx"]) == 0.0015
    assert float(mort.loc[51, "qx"]) / float(mort.loc[50, "qx"]) == pytest.approx(
        1.10, rel=1e-6)
    assert float(mort.loc[110, "qx"]) == 1.0
    assert list(mort.index) == list(range(16, 111))

    annuity = pd.read_csv(INPUT_DIR / "annuity_mort_table.csv", index_col="age")
    assert set(annuity.columns) == {"qx_base", "improvement", "provenance"}
    assert all("DAV 2004 R" in p for p in annuity["provenance"])
    assert float(annuity.loc[65, "qx_base"]) == 0.006
    assert float(annuity.loc[65, "improvement"]) == 0.018
    assert float(annuity.loc[110, "qx_base"]) == 1.0
    assert (annuity["improvement"] >= 0.002).all()

    lapse = pd.read_csv(INPUT_DIR / "lapse_table.csv", index_col="duration")
    assert (lapse["transfer_rate"] > lapse["lapse_rate"]).all()
    assert all("[std]" in p for p in lapse["provenance"])

    surplus = pd.read_csv(INPUT_DIR / "surplus_scenario.csv")
    assert set(surplus["scenario_id"]) == {"base", "low"}
    assert set(surplus.loc[surplus["scenario_id"] == "base", "laufende_verz"]) == {0.023}
    assert set(surplus.loc[surplus["scenario_id"] == "low", "laufende_verz"]) == {0.005}
    assert all(p.startswith("[std]") for p in surplus["provenance"])
    assert all("Rechnungszins" in p
               for p in surplus.loc[surplus["scenario_id"] == "base", "provenance"])
    assert all("stress" in p
               for p in surplus.loc[surplus["scenario_id"] == "low", "provenance"])

    freq = pd.read_csv(INPUT_DIR / "freq_loading.csv", index_col="prem_freq")
    assert list(freq["load"]) == [1.0, 1.01, 1.02, 1.03]
    assert all("[std]" in p for p in freq["provenance"])

    points = pd.read_csv(INPUT_DIR / "model_point_table.csv", index_col="point_id")
    assert "provenance" not in points.columns      # the one exempt file
    assert list(points.index) == list(range(1, 14))
    assert points.loc[1, "scenario_id"] == "base"
    assert points.loc[11, "scenario_id"] == "low"
    assert (points["teilkapital_share"] <= 0.30).all()
    assert (points["rentenbeginn_age"] >= 62).all()


def test_an_input_can_be_swapped_without_touching_formulas():
    """What a production user does with a company or licensed mortality basis.

    Point ``Data.annuity_mort_file`` at a same-schema file with a heavier annuitant table
    and the conversion follows: a shorter annuity factor lifts the current *Rentenfaktor*,
    and once it passes the guaranteed 29,00 it becomes the factor applied.
    """
    import pandas as pd

    model = mx.read_model(MODEL_DIR, name="Riester_DE_A_swap")
    alt = None
    try:
        base_factor = model.Projection[1].ann_factor()
        base_applied = model.Projection[1].rentenfaktor_applied()
        assert base_applied == 29.0

        heavier = pd.read_csv(INPUT_DIR / "annuity_mort_table.csv", index_col="age")
        heavier["qx_base"] = (heavier["qx_base"] * 2.0).clip(upper=1.0)
        alt = model.Data.input_dir() / "annuity_mort_table_heavy.csv"
        heavier.to_csv(alt)
        model.Data.annuity_mort_file = alt.name
        model.Data.clear_all()
        model.Projection.clear_all()

        p = model.Projection[1]
        assert p.ann_factor() < base_factor
        assert p.rentenfaktor_curr() > 29.0
        assert p.rentenfaktor_applied() == pytest.approx(p.rentenfaktor_curr(), rel=1e-12)
        assert p.annuity_month_pp() > 92.885458
        assert p.check_conversion() is True
    finally:
        if alt is not None:
            alt.unlink(missing_ok=True)
        model.close()


def test_round_trip_is_stable(tmp_path):
    """read -> write -> re-read reproduces the goldens and the same file set.

    Inputs are external, so they must travel with the model: the CSVs are copied to the
    new parent before re-reading, which is exactly the trade-off this layout makes.
    """
    import shutil

    model = mx.read_model(MODEL_DIR, name="Riester_DE_A_rt_src")
    try:
        dest = tmp_path / MODEL_DIR.name
        mx.write_model(model, str(dest), backup=False)
    finally:
        model.close()

    for csv in INPUT_DIR.glob("*.csv"):
        shutil.copy(csv, tmp_path / csv.name)

    reread = mx.read_model(dest, name="Riester_DE_A_rt")
    try:
        p = reread.Projection[1]
        for t, row in WORKED_EXAMPLE.items():
            assert p.pols_if(t) == pytest.approx(row[0], abs=SIX_DP)
            assert p.premiums(t) == pytest.approx(row[1], abs=CENT)
            assert p.zulagen(t) == pytest.approx(row[2], abs=CENT)
            assert p.net_cf(t) == pytest.approx(row[11], abs=CENT)
        assert p.garantieluecke_pp(1) == pytest.approx(358.94, abs=CENT)
        assert p.capital_conv_pp() == pytest.approx(45756.383140, abs=CENT)
        assert "Notes symbol" in reread.Projection.doc
        assert p.check_net_cf() is True
        assert p.check_conversion() is True
    finally:
        reread.close()

    assert model_files(dest) == model_files(MODEL_DIR)
    assert pathlib.Path(dest, "_system.json").is_file()
