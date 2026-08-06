# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

from modelx.serialize.jsonvalues import *

_formula = lambda point_id: None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def mp():
    """The model point row selected by point_id."""
    return model_point_table.loc[point_id]                          # noqa: F821


def issue_age():
    return int(mp()["issue_age"])


def sex():
    return mp()["sex"]


def rate_class():
    return mp()["rate_class"]


def plan():
    return mp()["plan"]


def face_amount():
    return float(mp()["face_amount"])


def policy_count():
    return float(mp()["policy_count"])


def band():
    """Face-amount band 1-4 **[std]**; the anchor cell is band 1."""
    f = face_amount()
    return 1 if f < 250000 else 2 if f < 500000 else 3 if f < 1000000 else 4


def n():
    """Level period in years, from the plan code."""
    return int(plan()[1:])


def max_t():
    """Last policy year: expiry is attained age 95 = end of year (95 - issue age)."""
    return omega - issue_age()                                      # noqa: F821


def attained_age(t):
    """Attained age at the START of policy year t (= issue age + completed years)."""
    return issue_age() + t - 1


def AP(t):
    """Annualized guaranteed gross premium for policy year t, policy fee included."""
    key = (plan(), sex(), rate_class(), band(), t)
    return float(premium_rates.loc[key, "annual_premium"])           # noqa: F821


def J():
    """Initial premium jump ratio AP(n+1)/AP(n), fee included [R4][R2 convention]."""
    return AP(n() + 1) / AP(n())


def M1_formula():
    """The technical notes' rule: M(1) = min(8.0, 1 + 0.55*(J-1)) **[std]**.

    NOT used when the model point supplies m1_override.  For the anchor cell this
    returns 3.4514 while the worked example pins 3.50 - a documented divergence.
    """
    return min(8.0, 1.0 + 0.55 * (J() - 1.0))


def M1():
    """M(1) actually used: the model point's override if given, else the formula."""
    o = mp()["m1_override"]
    return M1_formula() if pd.isna(o) else float(o)                  # noqa: F821


def M_plt(d):
    """PLT mortality multiplier at PLT duration d = t - n; grades to 2.00 **[std]**."""
    return max(2.0, M1() - 0.15 * (d - 1)) if d >= 1 else 1.0


def class_factor():
    return float(class_factors.loc[rate_class(), "factor"])          # noqa: F821


def q_base(t):
    """Best-estimate base mortality at attained age x+t-1."""
    return float(mort_best_estimate.loc[attained_age(t), "qx"])      # noqa: F821


def q(t):
    """Best-estimate mortality: base x class factor x PLT deterioration."""
    d = t - n()
    return q_base(t) * class_factor() * (M_plt(d) if d >= 1 else 1.0)


def shock_lapse():
    """Shock lapse at the end of the level period, keyed on J **[std]**."""
    j = J()
    for _, r in shock_lapse_table.iterrows():                        # noqa: F821
        if r["j_lo"] < j <= r["j_hi"] or (j <= 0 and r["j_lo"] == 0.0):
            return float(r["shock"])
    return float(shock_lapse_table.iloc[-1]["shock"])                # noqa: F821


def w(t):
    """Annual lapse rate for policy year t **[std]** (technical notes, footnote B).

    Level period: 6%, 5%, 4% for years 3..n-2, 6% anticipatory at n-1, shock at n.
    PLT: 30%, 15%, then 10%.
    """
    nn = n()
    if t < nn:
        if t == 1:
            return 0.06
        if t == 2:
            return 0.05
        if t == nn - 1:
            return 0.06
        return 0.04
    if t == nn:
        return shock_lapse()
    d = t - nn
    return 0.30 if d == 1 else 0.15 if d == 2 else 0.10


def conv_elig(t):
    """Convertible while within the level period and attained age < 70 [S2][S3][S6]."""
    return t <= n() and attained_age(t) < 70


def cv(t):
    """Conversion rate **[std]**; zero outside the eligibility window."""
    if not conv_elig(t):
        return 0.0
    return conv_rate_final if not conv_elig(t + 1) else conv_rate    # noqa: F821


def phase(t):
    if t > max_t():
        return "EXPIRED"
    return "LEVEL" if t <= n() else "PLT"


def l(t):
    """In-force at the start of policy year t; l(1) = policy_count."""
    if t == 1:
        return policy_count()
    if t > max_t():
        return 0.0
    return l(t - 1) * (1 - q(t - 1)) * (1 - cv(t - 1)) * (1 - w(t - 1))


def d_death(t):
    """Deaths in year t."""
    return l(t) * q(t)


def surv(t):
    """Survivors to the end of year t, before voluntary decrements."""
    return l(t) * (1 - q(t))


def c(t):
    """Conversions at the end of year t."""
    return surv(t) * cv(t)


def x(t):
    """Lapses (including the shock lapse) at the end of year t."""
    return surv(t) * (1 - cv(t)) * w(t)


def expiry(t):
    """Policies terminating because coverage ends at attained age 95.

    Not a decrement - the contract simply runs out [S2][S3][S5][S6].  Exposed as its
    own cells so the in-force roll-forward closes exactly:
        l(t) - l(t+1) = d_death(t) + x(t) + c(t) + expiry(t)
    Without it the final year appears to lose lives with no cause.
    """
    if t != max_t():
        return 0.0
    return l(t) * (1 - q(t)) * (1 - cv(t)) * (1 - w(t))


def k_comm(t):
    """Commission rate **[std]**: 80% year 1, 5% years 2..n, 2% in PLT."""
    return 0.80 if t == 1 else (0.05 if t <= n() else 0.02)


def G(t):
    """Premium income, beginning of year."""
    return AP(t) * l(t)


def K(t):
    """Commission, beginning of year **[std]**."""
    return k_comm(t) * G(t)


def X_tax(t):
    """Premium tax **[std]**."""
    return prem_tax_rate * G(t)                                      # noqa: F821


def E(t):
    """Acquisition (year 1) plus inflating maintenance expense **[std]**."""
    acq = acq_expense if t == 1 else 0.0                             # noqa: F821
    return acq + maint_expense * (1 + expense_infl) ** (t - 1) * l(t)  # noqa: F821


def DC(t):
    """Death claims, end of year."""
    return face_amount() * d_death(t)


def CV(t):
    """Conversion credit outflow: one annual premium, after year 1 [S6]."""
    return AP(t) * c(t) if t > 1 else 0.0


def NetCF(t):
    return G(t) - K(t) - X_tax(t) - E(t) - DC(t) - CV(t)


def result_cf():
    """Tidy cash flow statement for policy years 1..max_t."""
    ts = list(range(1, max_t() + 1))
    return pd.DataFrame(
        {
            "l": [l(t) for t in ts],
            "premium_G": [G(t) for t in ts],
            "claims_DC": [DC(t) for t in ts],
            "commission_K": [K(t) for t in ts],
            "expense_E": [E(t) for t in ts],
            "premium_tax_X": [X_tax(t) for t in ts],
            "conv_credit_CV": [CV(t) for t in ts],
            "net_cf": [NetCF(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),
    )


# ---------------------------------------------------------------------------
# References

model_point_table = ("IOSpec", 1)  # PandasData path='model_point_table.csv' file_type='csv'

premium_rates = ("IOSpec", 2)  # PandasData path='premium_rates.csv' file_type='csv'

mort_best_estimate = ("IOSpec", 3)  # PandasData path='mort_best_estimate.csv' file_type='csv'

class_factors = ("IOSpec", 4)  # PandasData path='class_factors.csv' file_type='csv'

shock_lapse_table = ("IOSpec", 5)  # PandasData path='shock_lapse_table.csv' file_type='csv'

point_id = 1

omega = 95

prem_tax_rate = 0.02

acq_expense = 300.0

maint_expense = 30.0

expense_infl = 0.02

conv_rate = 0.0

conv_rate_final = 0.0

pd = ("Module", "pandas")