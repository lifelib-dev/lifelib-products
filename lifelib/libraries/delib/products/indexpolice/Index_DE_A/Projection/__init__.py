# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.Index_DE_A` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the worked example's anchor cell
    >>> Projection.point_id = 8            # or switch the default

``t`` counts **policy years from issue**, 1-based: policy year ``t`` runs from the
``(t-1)``-th anniversary to the ``t``-th and covers attained age ``entry_age + t - 1``.
A **new-business** point starts at ``t = 1``; an **in-force** point starts at
``t = dur_init + 1``, because ``t`` is the policy's own duration and not an offset from
the valuation date. ``proj_len() = ann_start_age - entry_age`` is the **last projected
policy year** in either case — the library's reading of ``proj_len()``, so
``result_cf().index[-1] == proj_len()`` and the frame of an in-force point at
``dur_init = 8`` has 19 rows while still reporting ``proj_len() = 27``.

At the end of policy year ``proj_len()`` the accumulation contract ends: the capital
falls due at *Rentenbeginn* as ``claims(n, "MATURITY")``, and whether it is taken as a
*Kapitalabfindung* or converted at the *Rentenfaktor* changes what is **reported**, not
the cash flow. The *Rentenphase* itself is ``products/sofortrente/``.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent directory,
``products/indexpolice/``, read at run time rather than stored inside the model. The
model folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded
values — so a diff of the model shows logic changes only, and an input can be edited or
swapped without rewriting the model. This follows ``annuallife.TradLife_A``; contrast
``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``Index_DE_A`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

Each table has a filename Reference and a reader Cells, both on
:mod:`~.Index_DE_A.Data`, reached here through the ``data`` Reference:

=====================  =================================  ==========================
Reference              Cells                              File
=====================  =================================  ==========================
model_point_file       data.model_point_table()           model_point_table.csv
index_return_file      data.index_return_table()          index_return_table.csv
index_param_file       data.index_param_table()           index_param_table.csv
surplus_rate_file      data.surplus_rate_table()          surplus_rate_table.csv
election_file          data.election_table()              election_table.csv
mort_file              data.mort_table()                  mort_table.csv
lapse_file             data.lapse_table()                 lapse_table.csv
freq_load_file         data.freq_load_table()             freq_load_table.csv
=====================  =================================  ==========================

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` and ``savings.CashValue_SE``
wherever those models have an analogue — ``pols_*`` for policy counts, ``av_pp`` and
``av_pp_at(t, timing)`` for the account value and its within-year reads, plural nouns for
cash flows, ``*_rate`` for rates, ``*_pp`` for per-policy amounts, ``claims(t, kind)``
with an uppercase ``kind`` string. The technical notes use compact actuarial symbols
instead. The mapping is:

=========================  ==============================  ===========================
Notes symbol               Cells                           Meaning
=========================  ==============================  ===========================
(none)                     model_point()                   The selected model point row
n = ann_start - entry      proj_len()                      Last projected policy year
t0 = dur_init + 1          t_start()                       First projected policy year
x(t)                       age(t)                          Attained age in year t
l(t)                       pols_if(t)                      In force at the start of t
l(t)(1-q), l(t+1)          pols_if_at(t, timing)           BEF_DECR / AFT_DEATH /
                                                           AFT_LAPSE
q_d(t)                     mort_rate(t)                    Annual death rate
w_l(t)                     lapse_rate(t)                   Annual surrender rate applied
(table)                    lapse_rate_base(t)              The table rate before the
                                                           terminal-year override
phi                        freq_load()                     Ratenzahlungszuschlag
P_b(t)                     prem_base_pp(t)                 Annual-mode premium due
P(t)                       prem_gross_pp(t)                Premium actually collected
BS                         prem_sum()                      Beitragssumme
alpha(t)                   prem_charge_acq_pp(t)           Acquisition charge, tariff
alpha_5(t)                 prem_charge_acq_min_pp(t)       The same on the 5-year spread
beta P(t)                  prem_charge_adm_pp(t)           Premium administration charge
P+(t)                      prem_to_av_pp(t)                Premium credited to the account
Pi(t)                      prem_paid_pp(t)                 Cumulative annual-mode premium
A(t)                       av_pp(t)                        Deckungskapital at the start
(within year)              av_pp_at(t, timing)             BEF_PREM / AFT_PREM /
                                                           AFT_CHARGE / AFT_GUAR /
                                                           AFT_CREDIT
gamma, F(t)                exp_av_rate, av_charge_pp(t)    Reserve charge rate; amount
i_g, I(t)                  guar_rate(), guar_int_pp(t)     Rechnungszins; guaranteed
                                                           interest
(shadow)                   av_min_pp(t), av_min_pp_at(..)  The 169 Abs. 3 account
G(t)                       index_base_pp(t)                Participating capital of the
                                                           Indexjahr
b(t)                       surplus_rate(t)                 Declared Ueberschussanteilsatz
w(t)                       elect_index(t)                  Fraction elected to the index
B(t)                       opt_budget_pp(t)                Option budget, spent
U(t)                       surplus_credit_pp(t)            Safe-arm credit
r(t,m)                     index_return(t, m)              The month's index return
C(t), q(t)                 index_cap(t), index_quote(t)    Monthly Cap; Partizipationsquote
min(r, C)                  index_return_capped(t, m)       Capped above, not floored below
S(t)                       index_sum(t)                    Sum of the twelve capped months
Y(t)                       index_return_year(t)            Compounded raw year return
rho(t)                     index_credit_rate(t)            The Indexrendite
X(t)                       index_credit_pp(t)              The Indexgutschrift
(diagnostic)               index_budget_ratio()            Credits over budget
K(t)                       credit_cum_pp(t)                Hoechststandsicherung ledger
guar_level Pi(t)           guar_floor_pp(t)                The Beitragsgarantie
Gamma(t)                   guar_cap_pp(t)                  Guaranteed capital
D(t)                       db_pp(t)                        Death benefit
V(t)                       cv_pp(t)                        Surrender value
(169 Abs. 3)               min_surr_pp(t)                  Minimum surrender value
(Stornoabzug)              surr_charge_pp(t)               Surrender charge
M(n)                       mat_pp(t)                       Benefit at Rentenbeginn
claims_death, ...          claims(t, kind)                 Benefit outgo by kind
(released)                 av_released(t)                  Account taken out by the exits
E(t)                       expenses(t)                     Insurer expense outgo
net_cf(t)                  net_cf(t)                       Net cash flow, income positive
liability_cf(t)            liability_cf(t)                 The same stream, outgo positive
=========================  ==============================  ===========================

.. rubric:: Charges and expenses are two different things

A **charge** is a deduction from the policyholder's *Deckungskapital*
(``prem_charge_acq_pp``, ``prem_charge_adm_pp``, ``av_charge_pp``); an **expense** is the
insurer's own cash outgo and appears in ``net_cf`` (``exp_acq_pp``, ``exp_maint_pp``).
They are of the same order here by construction, so the *Kostenüberschuss* is small. The
model does **not** close the MindZV loop — it does not compute a cost result, return half
of it to the policyholder and raise the declared rate — so changing an expense assumption
changes ``net_cf`` without changing what the policyholder receives. That is a stated
limitation of the reference implementation, not an oversight.

.. rubric:: The two steps that define the product

**Step 2 of the annual processing order:** the participating base is struck on the
**opening** balance, ``index_base_pp(t) = av_pp(t)``, *before* the year's premium. That
is why a new-business point credits nothing in policy year 1 however well the index does,
and it is a **[std]** reading — whether the base is the whole *Deckungskapital*, an
index-participating sub-account or the accumulated *Überschussguthaben* alone was not
established, and a different reading rescales every credit in the model.

**Step 12:** the credit lands *after* the decrements and goes to the **survivors**,
``pols_if_at(t, "AFT_LAPSE")``, while the premium, the charges and the guaranteed
interest are struck on the opening in-force ``pols_if(t)``. The decrementing lives paid
the premium and earned the guaranteed interest before they left; they did not see the
*Indexjahr* out. ``av_released(t)`` is the account those exits carry out of the fund, and
it exists as a cells precisely so that ``check_av_roll_fwd()`` is exact rather than
approximate.

The asymmetry that follows is the product's own rule, and a model that pays two exits at
the same instant the same amount has lost it: death and surrender are struck on
``av_pp_at(t, "AFT_GUAR")``, the account **before** the year's credits, because a
mid-year exit forfeits the running *Indexjahr* **[std]**; the maturity is struck on
``av_pp(n + 1)``, **including** them, because that contract ran the *Indexjahr* to its
end, and it is then floored at the *Beitragsgarantie* plus the whole locked-in ledger.

.. rubric:: What is deliberately not here

No unit account, unit price or fund value — the capital is in the *Sicherungsvermögen*
and the surrender value is a reserve. No *Beitragsfreistellung* sub-population: German
lapse is a three-way decrement and this model carries surrender only. No *Dynamik*, no
*Zuzahlungen*, no *Rentengarantiezeit*, no *Schlussüberschussanteil* and no
*Bewertungsreserven* share. No dynamic surrender: on this contract the account cannot
fall from the index, so the usual driver is absent, and the driver that *is* present — a
run of zero *Indexjahre* — has no published calibration, so inventing one would put a
large unevidenced number at the centre of the result. No discounting, no
*Deckungsrückstellung*, no *Zinszusatzreserve*, no technical provisions and no tax.
"""

from modelx.serialize.jsonvalues import *

_formula = lambda point_id: None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

# --- the model point ---------------------------------------------------------

def model_point():
    """The selected model point as a Series."""
    return data.model_point_table().loc[point_id]                    # noqa: F821


def policy_id():
    """The policy identifier of the selected model point; reporting only."""
    return model_point()["policy_id"]


def sex():
    """``"M"`` or ``"F"``: the row of the best-estimate mortality table to read.

    **Never a rating factor.** Sex may not enter a premium, a charge or a benefit in a
    contract written after 21 December 2012, and none of them depends on it here; it
    selects a decrement only.  Because the death benefit of this product is the account
    value with a floor rather than a sum at risk, mortality is a **timing** assumption and
    the choice moves the result very little.
    """
    v = model_point()["sex"]
    if v not in ("M", "F"):
        raise ValueError("invalid sex")
    return v


def entry_age():
    """*Eintrittsalter*: age last birthday at inception, the origin of ``age(t)``."""
    return int(model_point()["entry_age"])


def dur_init():
    """Completed policy years at the valuation date; 0 for new business.

    The frame starts at ``t_start() = dur_init() + 1``, because ``t`` is the policy's own
    duration.  An in-force point brings its state with it — ``av_pp_init``,
    ``guar_locked_init``, ``prem_paid_init`` — rather than having it re-derived, which is
    what makes the in-force cells independent evidence about the recursion rather than a
    replay of it.
    """
    return int(model_point()["dur_init"])


def pols_if_init():
    """Policies in force at ``t_start()``: 1.0, a single-policy model point.

    Named rather than written as a literal because it is the scale of the roll-forward
    tolerances and the quantity ``result_cf()``'s first ``pols_if`` value must equal.
    """
    return float(model_point()["pols_if_init"])


def ann_start_age():
    """Attained age at *Rentenbeginn*, the end of the accumulation phase."""
    return int(model_point()["ann_start_age"])


def prem_form():
    """``"level"`` (*laufender Beitrag*) or ``"single"`` (*Einmalbeitrag*)."""
    v = model_point()["prem_form"]
    if v not in ("level", "single"):
        raise ValueError("invalid prem_form")
    return v


def prem_freq():
    """The payment frequency: annual, half_yearly, quarterly or monthly.

    It selects the *Ratenzahlungszuschlag* in :func:`freq_load` and does nothing else.
    """
    v = model_point()["prem_freq"]
    if v not in ("annual", "half_yearly", "quarterly", "monthly"):
        raise ValueError("invalid prem_freq")
    return v


def prem_term_y():
    """*Beitragszahlungsdauer* in policy years; 1 on a single premium."""
    return int(model_point()["prem_term_y"])


def av_pp_init():
    """The *Deckungskapital* per policy at ``t_start()``; 0 for new business."""
    return float(model_point()["av_pp_init"])


def guar_locked_init():
    """The *Höchststandsicherung* ledger already accumulated at ``t_start()``.

    Every credit — index or safe-arm — made before the valuation date.  Zero for new
    business.  It is carried separately from :func:`av_pp_init` because the two answer
    different questions: the account says what the policy is worth, the ledger says how
    much of it can never be lost.
    """
    return float(model_point()["guar_locked_init"])


def prem_paid_init():
    """Annual-mode premiums already paid at ``t_start()``; the base of the guarantee so far."""
    return float(model_point()["prem_paid_init"])


def guar_level():
    """*Garantieniveau*: the *Beitragsgarantie* as a fraction of the *Beitragssumme*.

    The wrapper sets the floor, not the index module: a *Schicht 3* contract may be sold
    at 60 %, 80 %, 90 % or 100 %, while a *Riester* contract must guarantee 100 % of
    contributions and allowances by statute.  Every euro of guarantee not promised is a
    euro that can back risk assets and therefore a larger option budget — a feedback this
    model does **not** carry, so the *Garantieniveau* sensitivity it reports is only the
    maturity-floor effect.
    """
    return float(model_point()["guar_level"])


def guar_rate():
    """``i_g``: the contract's *Rechnungszins*, a **cohort** fact and not today's rate.

    The *Höchstrechnungszins* history the shipped points span — 1.00 % for 2025-2026,
    0.90 % for a 2017-2021 cohort, 0.25 % for 2022-2024 — is why a book of this product
    cannot be projected on one rate.  At 0.25 % the rate equals the reserve charge and the
    account falls in a year that credits nothing, which is model point 13.
    """
    return float(model_point()["guar_rate"])


def payoff_form():
    """``"cap"`` (the monthly Cap design) or ``"quote"`` (the *Partizipationsquote*).

    The two designs are **not** interchangeable and fail differently: the Cap gives away
    the large monthly moves and is hurt by volatility even in a year that ends well, while
    the *Quote* gives away a constant fraction in every state.  Model points 1 and 2 run
    them on the identical index path so the difference is visible rather than argued.
    """
    v = model_point()["payoff_form"]
    if v not in ("cap", "quote"):
        raise ValueError("invalid payoff_form")
    return v


def index_id():
    """The key into *index_return_table.csv* and *index_param_table.csv*."""
    return model_point()["index_id"]


def elect_id():
    """The key into *election_table.csv*: this policy's *Wahlrecht* path."""
    return model_point()["elect_id"]


def death_min_rate():
    """The *Mindesttodesfallschutz* floor on the death benefit, as a fraction of ``BS``.

    0.50 on the shipped points that carry it: the standard formulation of the condition
    that a contract concluded from 1 April 2009 must satisfy for the favourable
    half-income treatment of a *Kapitalabfindung*.  It is a floor on the benefit and never
    a sum at risk added to it.
    """
    return float(model_point()["death_min_rate"])


def ann_option():
    """``"annuity"`` or ``"cash"``: how the terminal capital is **reported**.

    It changes :func:`ann_monthly_pp` and nothing else.  The *Kapitalwahlrecht* is a
    configuration of the model point, not a take-up rate: modelling it as a rate would
    stand in for a tax comparison this model does not perform.
    """
    v = model_point()["ann_option"]
    if v not in ("annuity", "cash"):
        raise ValueError("invalid ann_option")
    return v


def surr_charge_on():
    """1 if the contractual *Stornoabzug* applies to this policy, 0 if not.

    A *Stornoabzug* is effective only if it is agreed, appropriate **and quantified in the
    contract**, so a tariff without the clause is a real configuration and not a special
    case.
    """
    return int(model_point()["surr_charge_on"])


# --- the frame ---------------------------------------------------------------

def t_start():
    """``t0``: the first projected policy year, ``dur_init() + 1``.

    New business starts at 1; an in-force point starts partway through its own term.  The
    frame's *start* is a product fact and is not fixed per model, which is why the
    conventions suite asserts contiguity and the last index rather than the first.
    """
    return dur_init() + 1


def proj_len():
    """``n``: the **last projected policy year**, ``ann_start_age() - entry_age()``.

    The library's reading of ``proj_len()``, inherited from frlib and asserted in the
    conventions suite: ``result_cf().index[-1] == proj_len()``, whether the frame is
    0-based or 1-based and wherever it starts.  It is **not** a row count — an in-force
    point at ``dur_init = 8`` publishes 19 rows and still reports 27.

    Policy year ``n`` ends at *Rentenbeginn*, when the capital falls due.  There is no
    policy year ``n + 1``: ``pols_if(n + 1)`` is zero because the whole surviving cohort
    has matured, while ``av_pp(n + 1)`` and ``guar_cap_pp(n + 1)`` are defined, being the
    per-policy amounts the maturity benefit is struck on.
    """
    return ann_start_age() - entry_age()


def age(t):
    """``x(t)``: the attained age in policy year t, ``entry_age() + t - 1``.

    Age last birthday, the basis the delib registry fixes for the whole library.
    """
    return entry_age() + t - 1


# --- the premium and its charges ---------------------------------------------

def prem_sum():
    """``BS``: the *Beitragssumme*, on the **annual-mode** premium.

    ``prem_gross_pp x prem_term_y`` on the level form and the single premium itself on the
    single form — the premiums payable over the whole contract, counted from issue and not
    from ``t_start()``, because a *Beitragssumme* is a contract fact that an in-force
    point brings with it.

    The *Ratenzahlungszuschlag* does **not** enter it.  A frequency surcharge is the price
    of paying in instalments, not more insurance bought, so it may not inflate the
    acquisition charge or the *Mindesttodesfallschutz* floor: on model point 4 the premium
    collected is 2,520.00 EUR a year while ``prem_sum()`` is 2,400.00 x 32 = 76,800.00 EUR.
    Getting that wrong is a numbered pitfall.
    """
    if prem_form() == "single":
        return float(model_point()["prem_gross_pp"])
    return float(model_point()["prem_gross_pp"]) * prem_term_y()


def freq_load():
    """``phi``: the *Ratenzahlungszuschlag* multiplier for this policy's payment frequency.

    1.000 annual, 1.020 half-yearly, 1.030 quarterly, 1.050 monthly **[std]** — the market
    convention, no carrier tariff having been established.  It multiplies the premium
    **collected** and nothing else; see :func:`prem_sum`.
    """
    return float(data.freq_load_table().loc[                         # noqa: F821
        prem_freq(), "freq_load"])


def prem_base_pp(t):
    """``P_b(t)``: the annual-mode premium due in policy year t, per policy.

    The level form pays ``prem_gross_pp`` in every policy year up to ``prem_term_y()``,
    which may be shorter than the projection — model point 13 stops paying at year 12 and
    runs to year 22.  The single form pays the whole premium in the first projected year
    and nothing afterwards.
    """
    if t < t_start() or t > proj_len():
        return 0.0
    if prem_form() == "single":
        return float(model_point()["prem_gross_pp"]) if t == t_start() else 0.0
    return float(model_point()["prem_gross_pp"]) if t <= prem_term_y() else 0.0


def prem_gross_pp(t):
    """``P(t)``: the premium actually collected in policy year t, ``P_b(t) x phi``.

    Annual in advance, at the start of the policy year.  This is the amount that reaches
    :func:`premiums` and out of which the contractual charges are taken; the amount that
    drives the *Beitragssumme* is :func:`prem_base_pp`.
    """
    return prem_base_pp(t) * freq_load()


def prem_charge_acq_pp(t):
    """``alpha(t)``: the acquisition charge deducted from the premium in policy year t.

    ``min(acq_cost_rate, zill_cap_rate) x BS`` spread evenly over the first
    ``min(zill_years, prem_term_y())`` premium-paying years — 2.5 % of the *Beitragssumme*
    at the DeckRV *Höchstzillmersatz* of 25 per mille, over five years, so 324.00 EUR a
    year on the anchor's 64,800.00 EUR.  On a single premium it is taken in full in the
    first projected year, there being only one premium to take it from.

    This is a **charge**, a deduction from the policyholder's account.  The insurer's own
    acquisition **expense** is :func:`exp_acq_pp`, falls in one lump at inception, and is
    the *Zillmer* strain the five-year recovery works off.
    """
    if t < t_start() or t > proj_len():
        return 0.0
    charge = min(acq_cost_rate, zill_cap_rate) * prem_sum()          # noqa: F821
    if prem_form() == "single":
        return charge if t == t_start() else 0.0
    spread = min(zill_years, prem_term_y())                          # noqa: F821
    return charge / spread if t <= spread else 0.0


def prem_charge_acq_min_pp(t):
    """``alpha_5(t)``: the same charge on the **five-year** spread of § 169 Abs. 3 VVG.

    Acquisition and distribution costs must be spread over at least the first five years
    for the purpose of the *Mindestrückkaufswert*, whatever the tariff does — so this
    profile is written with the literal 5 and not with ``zill_years``, which is a tariff
    parameter and not a statutory one.  With ``zill_years = 5`` the two coincide exactly
    and the floor is a no-op, which is the point: delib's charge profile is already at the
    statutory floor.  Set ``zill_years = 1`` and the floor bites.

    A single premium is taken once, so there is no second premium over which to spread
    anything and the two profiles coincide there by construction rather than by parameter.
    """
    if t < t_start() or t > proj_len():
        return 0.0
    charge = min(acq_cost_rate, zill_cap_rate) * prem_sum()          # noqa: F821
    if prem_form() == "single":
        return charge if t == t_start() else 0.0
    spread = min(5, prem_term_y())
    return charge / spread if t <= spread else 0.0


def prem_charge_adm_pp(t):
    """``beta P(t)``: the premium-based administration charge, 3 % of the premium collected.

    *Verwaltungskosten* taken as the premium is credited.  **[std]**: no German insurer
    publishes a charge level for this product.
    """
    return exp_prem_rate * prem_gross_pp(t)                          # noqa: F821


def prem_to_av_pp(t):
    """``P+(t)``: the part of the premium credited to the account.

    ``P(t) - alpha(t) - beta P(t)``.  On the anchor's first five years that is
    ``2,400.00 - 324.00 - 72.00 = 2,004.00 EUR``, and 2,328.00 EUR thereafter.  Negative
    values are possible in principle on a tariff whose charges exceed the premium; none of
    the shipped points is one.
    """
    return prem_gross_pp(t) - prem_charge_acq_pp(t) - prem_charge_adm_pp(t)


def prem_to_av(t):
    """The premium credited to the account at fund level: ``P+(t) x l(t)``.

    Struck on the **opening** in-force, because the lives that decrement during the year
    have already paid the year's premium in advance.
    """
    return prem_to_av_pp(t) * pols_if(t)


def prem_paid_pp(t):
    """``Pi(t)``: cumulative annual-mode premiums paid to the **start** of policy year t.

    Starts at ``prem_paid_init()`` and adds ``P_b(t)`` each year, so ``Pi(n + 1)`` is the
    whole *Beitragssumme* for a policy that pays throughout.  Non-decreasing by
    construction, which is half of why :func:`guar_cap_pp` is monotone.
    """
    if t <= t_start():
        return prem_paid_init()
    return prem_paid_pp(t - 1) + prem_base_pp(t - 1)


def premiums(t):
    """Premium income in policy year t, an inflow: ``P(t) x l(t)``.

    Annual in advance on the opening in-force.  Not further multiplied by ``(1 - q_d)``:
    decrements fall at the **end** of the year, so a life that dies in year t has paid
    year t's premium, and applying the cessation rule here as well would understate income.
    """
    return prem_gross_pp(t) * pols_if(t)


# --- the surplus, the election and the option budget -------------------------

def surplus_rate(t):
    """``b(t)``: the declared *Überschussanteilsatz* for policy year t.

    2.50 % a year of ``G(t)``, level over the projection **[std]**.  **This rate is the
    option budget.**  The insurer earns a return on the *Sicherungsvermögen*, the MindZV
    forces at least 90 % of the excess over the guarantee into the policyholders' share,
    the insurer declares a rate out of that, and a contract in the index arm has the
    declared amount spent on options instead of credited as interest.  An Indexpolice
    therefore has **exactly the same risk budget** as a classic contract of the same
    vintage and spends it differently.

    Holding it level is the strongest single simplification in this model: in reality the
    rate moves with the investment result, and the feedback from the *Garantieniveau*
    through the asset mix to the declared rate is not modelled at all.
    """
    return float(data.surplus_rate_table().loc[t, "surplus_rate"])   # noqa: F821


def elect_index(t):
    """``w(t)``: the fraction of year t's declared surplus directed to the index arm.

    The *Wahlrecht*, read from this policy's election path.  A fraction in [0, 1] rather
    than a flag, because some tariffs permit a partial election and all-or-nothing is then
    the special case ``w in {0, 1}``.  It is a **behavioural** assumption and not a
    contractual one: whether real policyholders revisit the election at all is not
    established, and ``always_index`` is a modelling choice made so that the base run
    demonstrates the index mechanic rather than a claim about behaviour.
    """
    return float(data.election_table().loc[                          # noqa: F821
        (elect_id(), t), "w"])


def index_base_pp(t):
    """``G(t)``: the participating capital of *Indexjahr* t — the **opening** balance.

    ``av_pp(t)``, struck **before** the year's premium and before the year's charges.
    Two consequences, both intended: a new-business point credits nothing in policy year 1
    however well the index does, because the base is zero; and a premium paid during a
    year participates only from the following one.

    Whether the base is the whole *Deckungskapital*, a defined index-participating
    sub-account or the accumulated *Überschussguthaben* alone **was not established** for
    any carrier.  delib takes the whole capital **[std]**.  This is the largest
    unquantified uncertainty in the product file: a different reading rescales every credit
    in the model, and it is a documentary gap rather than a modelling choice.
    """
    return av_pp(t)


def opt_budget_pp(t):
    """``B(t)``: the option budget of *Indexjahr* t, ``w(t) b(t) G(t)``.

    The money the insurer spends buying the option package that replicates the promised
    payoff.  It is **spent, not credited**: if the *Indexjahr* ends at or below zero it has
    bought options that expired worthless, and that — the opportunity cost of one year's
    surplus — is the whole of the policyholder's downside.
    """
    return elect_index(t) * surplus_rate(t) * index_base_pp(t)


def surplus_credit_pp(t):
    """``U(t)``: the safe-arm credit of year t, ``(1 - w(t)) b(t) G(t)``.

    The part of the declared surplus **not** elected to the index arm, credited to the
    account as interest and guaranteed from the moment it is credited.  Zero throughout on
    the anchor, which elects the index arm in every year; the whole of the surplus on model
    point 11, which reduces the contract to a *klassische Rentenversicherung*.
    """
    return (1.0 - elect_index(t)) * surplus_rate(t) * index_base_pp(t)


def surplus_credit(t):
    """The safe-arm credit at fund level: ``U(t) x pols_if_at(t, "AFT_LAPSE")``.

    On the **survivors**, not on the opening in-force: like the index credit, it is struck
    at the end of the *Indexjahr*, and the lives that died or surrendered during the year
    were not there for it.
    """
    return surplus_credit_pp(t) * pols_if_at(t, "AFT_LAPSE")


# --- the Indexjahr -----------------------------------------------------------

def index_return(t, m):
    """``r(t, m)``: the index return of month m of *Indexjahr* t, as a decimal.

    Read from row ``(index_id(), t)`` of *index_return_table.csv*, column ``m01`` ...
    ``m12``.  The *Indexjahr* is aligned with the policy year **[std]**: the contractual
    *Indexstichtag* need not fall on the policy anniversary, no carrier's convention was
    established, and an annual-grid model has no other defensible alignment.
    """
    return float(data.index_return_table().loc[                      # noqa: F821
        (index_id(), t), "m%02d" % m])


def index_cap(t):
    """``C(t)``: the monthly Cap of *Indexjahr* t.

    3.00 % on the equity path **[std]**, the midpoint of an argued 1.5-5.0 % band that no
    carrier document could confirm; 6.00 % on the low-volatility house path, which is
    cheaper to buy options on.  The Cap is fixed before the *Indexjahr* begins and is then
    binding for its whole length.

    **It is not a marketing parameter but the solution of a pricing equation**: given the
    option budget, the index's implied volatility and dividend yield and the risk-free
    rate, there is exactly one Cap at which the twelve-month capped-sum payoff costs the
    budget.  That is why caps move from year to year with no change in the contract, and it
    is why the Cap and :func:`surplus_rate` may not be chosen independently — see
    :func:`index_budget_ratio`.
    """
    return float(data.index_param_table().loc[                       # noqa: F821
        (index_id(), t), "cap"])


def index_quote(t):
    """``q(t)``: the *Partizipationsquote* of *Indexjahr* t, used by the ``quote`` design.

    60 % on the equity path and 100 % on the house path **[std]**.  A participation rate
    near or above 100 % on a volatility-targeted index is not generosity: it is what the
    same budget buys when the underlying is engineered to be cheap, and it moves the
    give-up from somewhere the purchaser can see to somewhere they cannot.
    """
    return float(data.index_param_table().loc[                       # noqa: F821
        (index_id(), t), "quote"])


def index_return_capped(t, m):
    """``min(r(t, m), C(t))``: the month's return **capped above and not floored below**.

    The asymmetry is the product, and it must never be softened.  A month in which the
    index rises 8 % contributes ``C``; a month in which it falls 8 % contributes the whole
    -8 %.  An implementation that floors the month at zero credits something in every year
    with an up-month in it, and gets the research file's Example B — where the sum is
    -2.60 % and the correct credit is nothing — spectacularly wrong.
    """
    return min(index_return(t, m), index_cap(t))


def index_sum(t):
    """``S(t)``: the **sum** of the twelve capped monthly returns of *Indexjahr* t.

    Summed, not compounded.  Summation is close to compounding for small numbers and is
    not the same thing, and the contractual formula is a sum: on the research file's
    Example A the twelve capped returns sum to exactly **+8.90 %** while compounding the
    same twelve gives 8.9599 %, an error small enough to look like rounding and large
    enough to be wrong at every duration.
    """
    return sum(index_return_capped(t, m) for m in range(1, 13))


def index_return_year(t):
    """``Y(t)``: the compounded **raw** index return of the year, ``prod(1 + r) - 1``.

    The uncapped, unfloored movement of the index itself.  It drives the
    *Partizipationsquote* design and is otherwise a diagnostic — and the diagnostic that
    matters most, because on the research file's Example B ``Y(10) = +6.4402 %`` while the
    Cap design credits **zero**.  The index rose and the credit was nothing; that is the
    feature the product is most criticised for and the one most often misdescribed.
    """
    out = 1.0
    for m in range(1, 13):
        out = out * (1.0 + index_return(t, m))
    return out - 1.0


def index_credit_rate(t):
    """``rho(t)``: the *Indexrendite* of *Indexjahr* t — the rate the credit is struck at.

    ``max(S(t), 0)`` in the Cap design, ``max(q(t) Y(t), 0)`` in the *Partizipationsquote*
    design.  **The floor is on the year, not on the month**, and in the Cap design it is on
    the *sum of capped returns* and not on the compounded raw return: applying it to ``Y``
    instead is a numbered pitfall that credits 6.44 % where the contract credits nothing.

    Never negative: the worst imaginable *Indexjahr* credits zero and leaves the capital
    untouched.  That floor is what makes this a life-insurance product rather than a bet,
    and it is the only reason the arm has a positive expectation at all — with a 3 % cap on
    a 17 %-volatility index the expected value of a *capped month* is negative.
    """
    if payoff_form() == "quote":
        return max(index_quote(t) * index_return_year(t), 0.0)
    return max(index_sum(t), 0.0)


def index_credit_pp(t):
    """``X(t)``: the *Indexgutschrift* per policy, ``rho(t) w(t) G(t)``.

    Credited at the end of the *Indexjahr* and **locked in**: once made it is permanently
    part of the guaranteed capital, earns the guaranteed rate thereafter like any other
    part of the *Deckungskapital*, and enters the base of every later *Indexjahr*.  That is
    the *Höchststandsicherung*, and it is what makes a year-by-year floor add up to a
    path-independent guarantee.

    Zero in policy year 1 of a new-business point even when ``index_credit_rate(1)`` is
    positive, because ``G(1) = 0``.
    """
    if t < t_start() or t > proj_len():
        return 0.0
    return index_credit_rate(t) * elect_index(t) * index_base_pp(t)


def index_credit(t):
    """The *Indexgutschrift* at fund level: ``X(t) x pols_if_at(t, "AFT_LAPSE")``.

    On the **survivors** of both decrements.  A life that died or surrendered during the
    *Indexjahr* forfeits it **[std]**: the payoff exists only at the year end, and whether
    a carrier pro-rates it, refunds the unspent option budget or simply keeps it was not
    established.  Crediting the year to the lives that left is a numbered pitfall and is
    caught by :func:`check_av_roll_fwd`.
    """
    return index_credit_pp(t) * pols_if_at(t, "AFT_LAPSE")


def index_budget_ratio():
    """Total index credits over total option budget, per policy, over the projection.

    The diagnostic that answers the one question the shipped parameters cannot: **are the
    Cap and the declared surplus rate mutually consistent?**  They are not free parameters
    — the Cap is the level at which the option strip costs the budget — so on a long
    enough path the credits should average the budget and this ratio should sit near 1.

    A value far from 1 means the pair is off, and it says which way: **above 1** the model
    is handing the policyholder more than the budget could buy, **below 1** it is charging
    for options it does not deliver.  On a single deterministic path the ratio is also
    sampling noise, so read it as an order-of-magnitude check and not as a calibration.
    Returns 0.0 where nothing was elected to the index arm, there being no budget to
    compare against.
    """
    budget = sum(opt_budget_pp(t) for t in range(t_start(), proj_len() + 1))
    if budget <= 0.0:
        return 0.0
    credits = sum(index_credit_pp(t) for t in range(t_start(), proj_len() + 1))
    return credits / budget


# --- the account -------------------------------------------------------------

def av_pp(t):
    """``A(t)``: the *Deckungskapital* per policy at the **start** of policy year t.

    ``av_pp_init()`` at ``t_start()``, then ``av_pp_at(t - 1, "AFT_CREDIT")``.  Defined at
    ``t = proj_len() + 1``, where it is the balance the maturity benefit is struck on.

    **Not monotone, and it must not be asserted to be.**  What ratchets is the ledger of
    credits, not the balance: with the reserve charge at or above the guaranteed rate the
    account falls in a year that credits nothing, which is exactly model point 13's 0.25 %
    cohort once its premiums stop.  Testing the lock-in as "the account never falls" is a
    numbered pitfall.
    """
    if t < t_start() or t > proj_len() + 1:
        return 0.0
    if t == t_start():
        return av_pp_init()
    return av_pp_at(t - 1, "AFT_CREDIT")


def av_pp_at(t, timing):
    """The *Deckungskapital* per policy at a point inside policy year t.

    ``"BEF_PREM"``
        ``A(t)``, the opening balance — and the base ``G(t)`` the *Indexjahr*
        is struck on.

    ``"AFT_PREM"``
        after the premium net of its charges has been credited.

    ``"AFT_CHARGE"``
        after the reserve charge ``gamma`` on the post-premium balance.

    ``"AFT_GUAR"``
        after the guaranteed interest ``i_g``.  **This is the balance every
        exit is measured on**: a death or a surrender takes the account
        before the year's index and safe-arm credits, because a mid-year
        exit forfeits the running *Indexjahr* **[std]**.

    ``"AFT_CREDIT"``
        after the *Indexgutschrift* and the safe-arm credit, i.e. ``A(t + 1)``.
        The maturity benefit is struck here and the two other exits are not,
        which is the product's own asymmetry and not a rounding of it.
    """
    if timing == "BEF_PREM":
        return av_pp(t)
    if timing == "AFT_PREM":
        return av_pp(t) + prem_to_av_pp(t)
    if timing == "AFT_CHARGE":
        return av_pp_at(t, "AFT_PREM") - av_charge_pp(t)
    if timing == "AFT_GUAR":
        return av_pp_at(t, "AFT_CHARGE") + guar_int_pp(t)
    if timing == "AFT_CREDIT":
        return (av_pp_at(t, "AFT_GUAR")
                + index_credit_pp(t) + surplus_credit_pp(t))
    raise ValueError("invalid timing")


def av_charge_pp(t):
    """``F(t)``: the reserve charge, ``gamma`` on the post-premium balance.

    0.25 % a year of ``av_pp_at(t, "AFT_PREM")`` **[std]** — *Verwaltungskosten* taken
    from the account rather than from the premium.  A **charge**, not an expense: it
    reduces the policyholder's *Deckungskapital* and does not appear in ``net_cf``.
    """
    return exp_av_rate * av_pp_at(t, "AFT_PREM")                     # noqa: F821


def av_charge(t):
    """The reserve charge at fund level: ``F(t) x l(t)``, on the opening in-force."""
    return av_charge_pp(t) * pols_if(t)


def guar_int_pp(t):
    """``I(t)``: the guaranteed interest of policy year t, ``i_g`` on the post-charge balance.

    The *Rechnungszins* of the policy's own cohort.  This is the **only** interest an
    Indexpolice credits in the index arm: the declared surplus is not added on top of it,
    it is spent.  A model that credits the guarantee *and* the declared rate *and* the
    index payoff has spent the same money three times.
    """
    return guar_rate() * av_pp_at(t, "AFT_CHARGE")


def guar_int(t):
    """The guaranteed interest at fund level: ``I(t) x l(t)``.

    On the **opening** in-force, because the decrementing lives earned the year's
    guaranteed interest before they left — their benefit is struck on
    ``av_pp_at(t, "AFT_GUAR")``, which includes it.
    """
    return guar_int_pp(t) * pols_if(t)


def av_at(t, timing):
    """The account at fund level at a within-year point: ``av_pp_at(t, timing) x l(t)``.

    Struck on the opening in-force at every timing, so that the difference between two
    timings is a movement of the same population.  The count changes at the year end, and
    that change is carried by :func:`av_released` rather than by re-weighting the balance.
    """
    return av_pp_at(t, timing) * pols_if(t)


def av(t):
    """The *Deckungskapital* at fund level at the start of policy year t: ``A(t) x l(t)``.

    Zero at ``t = proj_len() + 1``, the whole surviving cohort having matured — which is
    why :func:`check_av_roll_fwd` closes in the final year only if the maturity is
    accounted for in :func:`av_released`.

    A **balance**, not a cash flow.  It is published in ``result_cf()`` because a reader
    cannot follow this product without it, and it is **not** summed into ``net_cf``.
    """
    return av_pp(t) * pols_if(t)


def av_released(t):
    """The account the year's exits carry **out of the fund** in policy year t.

    ``av_pp_at(t, "AFT_GUAR") x (pols_death(t) + pols_lapse(t)) + av_pp(t + 1) x
    pols_maturity(t)``: deaths and surrenders take the balance before the year's credits,
    maturities take it after them.

    This is deliberately **not** what the exits are *paid*.  The death floor pays more
    than the account releases, the *Stornoabzug* pays less, and the *Beitragsgarantie* at
    *Rentenbeginn* pays more.  Those three differences are insurer money and they belong in
    ``net_cf``, not in the account roll-forward — which is exactly what makes
    :func:`check_av_roll_fwd` an exact identity rather than an approximate one.
    """
    return (av_pp_at(t, "AFT_GUAR") * (pols_death(t) + pols_lapse(t))
            + av_pp(t + 1) * pols_maturity(t))


# --- the § 169 Abs. 3 shadow account -----------------------------------------

def av_min_pp(t):
    """The shadow *Deckungskapital* on the statutory five-year acquisition-cost spread.

    The same recursion as :func:`av_pp` with :func:`prem_charge_acq_min_pp` in place of the
    tariff charge — the credits are identical, so only the acquisition profile differs.  It
    exists to produce :func:`min_surr_pp`, the § 169 Abs. 3 VVG floor under the surrender
    value, and it is a *shadow*: it is not the reserve, it is not published in the cash
    flow statement, and it never touches a death or a maturity benefit.

    An in-force point starts it at ``av_pp_init()`` for want of a second opening state in
    the model point table.  That understates the floor for a policy whose first five years
    are behind it, and it is a stated simplification rather than a claim.
    """
    if t < t_start() or t > proj_len() + 1:
        return 0.0
    if t == t_start():
        return av_pp_init()
    return av_min_pp_at(t - 1, "AFT_CREDIT")


def av_min_pp_at(t, timing):
    """The shadow account at a point inside policy year t; timings as :func:`av_pp_at`.

    Identical in structure, so that a reader comparing the two accounts is comparing one
    number — the acquisition charge — and not two recursions.
    """
    if timing == "BEF_PREM":
        return av_min_pp(t)
    if timing == "AFT_PREM":
        return (av_min_pp(t) + prem_gross_pp(t) - prem_charge_acq_min_pp(t)
                - prem_charge_adm_pp(t))
    if timing == "AFT_CHARGE":
        return av_min_pp_at(t, "AFT_PREM") * (1.0 - exp_av_rate)     # noqa: F821
    if timing == "AFT_GUAR":
        return av_min_pp_at(t, "AFT_CHARGE") * (1.0 + guar_rate())
    if timing == "AFT_CREDIT":
        return (av_min_pp_at(t, "AFT_GUAR")
                + index_credit_pp(t) + surplus_credit_pp(t))
    raise ValueError("invalid timing")


# --- the Höchststandsicherung ledger and the guarantee -----------------------

def credit_cum_pp(t):
    """``K(t)``: the *Höchststandsicherung* ledger — every credit ever made, cumulated.

    ``guar_locked_init()`` at ``t_start()``, then ``K(t) = K(t - 1) + X(t - 1) +
    U(t - 1)``.  Both index and safe-arm credits enter it, because both are guaranteed
    from the moment they are credited.  Monotone non-decreasing by construction, credits
    being non-negative.

    This is the quantity that makes the annual floor add up to something: a plain maturity
    guarantee lets the insurer recover a bad year with a good one, while here every
    credited amount is permanent, so **the cost of the guarantee rises with every good
    year**.  It is also what the *Deckungsrückstellung* means by "profit shares already
    allocated".
    """
    if t <= t_start():
        return guar_locked_init()
    return credit_cum_pp(t - 1) + index_credit_pp(t - 1) + surplus_credit_pp(t - 1)


def guar_floor_pp(t):
    """The *Beitragsgarantie* accrued to the start of policy year t.

    ``guar_level() x prem_paid_pp(t)`` — a fraction of the premiums **actually paid so
    far**, so it grows with the premium stream and is complete only once the last premium
    is in.  On the anchor it reaches ``0.90 x 64,800.00 = 58,320.00 EUR`` at
    ``t = proj_len() + 1``.
    """
    return guar_level() * prem_paid_pp(t)


def guar_cap_pp(t):
    """``Gamma(t)``: the guaranteed capital, ``guar_floor_pp(t) + credit_cum_pp(t)``.

    The *Beitragsgarantie* plus every locked-in credit — the second term dominating after
    a few good years.

    **It is owed at *Rentenbeginn* and at no earlier date.**  That is what *Neue Klassik*
    means, and it is the reason the insurer can hold a materially riskier asset mix behind
    it and generate the surplus that becomes the option budget.  A model that reserves this
    product as though it guaranteed ``i_g`` on the reserve at every balance date overstates
    the guarantee; a model that lets ``guar_cap_pp`` into a death or surrender benefit has
    made the same mistake in the cash flows.  ``av_pp(t) < guar_cap_pp(t)`` at intermediate
    ``t`` is permitted and is ordinary.
    """
    return guar_floor_pp(t) + credit_cum_pp(t)


# --- decrements --------------------------------------------------------------

def mort_rate(t):
    """``q_d(t)``: the annual death rate at the attained age of policy year t.

    A **[std]** Gompertz proxy anchored at ``qx(M, 40) = 0.001200``; DAV 2008 T and DAV
    2004 R are proprietary and are cited by name rather than shipped.  Mortality here is a
    **timing** assumption: the death benefit is the account value with a floor, not a sum
    at risk, so the rate decides when capital leaves and hardly at all how much.
    """
    return float(data.mort_table().loc[(sex(), age(t)), "qx"])       # noqa: F821


def lapse_rate_base(t):
    """The table surrender rate for policy year t, **before** the terminal-year override.

    5 % in years 1-2, 3 % in years 3-11, **6 % in year 12**, 2 % from year 13 **[std]**.
    The year-12 step is the § 20 Abs. 1 Nr. 6 EStG threshold, at which only half the
    *Unterschiedsbetrag* becomes taxable and at the personal rate rather than by final
    withholding — the strongest single driver of German surrender behaviour, and the reason
    a rate flat in duration is a numbered pitfall.  The mean over the anchor's 27 years is
    about 2.6 %, inside the market-wide GDV band; no index-specific rate exists at all.
    """
    return float(data.lapse_table().loc[t, "lapse_rate"])            # noqa: F821


def lapse_rate(t):
    """``w_l(t)``: the surrender rate actually applied in policy year t.

    :func:`lapse_rate_base` except in the final policy year, where it is **0** **[std]**:
    the end of policy year ``n`` *is* *Rentenbeginn*, so a surrender and a maturity would
    be the same event at the same instant, and the whole surviving cohort is booked as a
    maturity.

    Unlike a term product, where the two paid the same nothing, **here they pay different
    amounts** — a surrender carries the *Stornoabzug* and forfeits the running *Indexjahr*,
    a maturity carries neither and takes the *Beitragsgarantie* floor — so this convention
    moves real money and is a modelling decision rather than bookkeeping.
    """
    if t == proj_len():
        return 0.0
    return lapse_rate_base(t)


def pols_if(t):
    """``l(t)``: policies in force at the **start** of policy year t.

    ``pols_if_init()`` at ``t_start()``, then ``pols_if_at(t - 1, "AFT_LAPSE")``.  This is
    the weight on every cash flow of the same ``result_cf()`` row, which is what makes it a
    start-of-period count: no decrement has been applied when a period opens, so the frame
    opens at ``pols_if_init()`` exactly.

    ``pols_if(proj_len() + 1)`` is **zero**, not the surviving cohort: at the end of the
    last policy year the survivors mature and leave through :func:`pols_maturity`.  Zero
    outside ``t_start() .. proj_len() + 1``.
    """
    if t < t_start() or t > proj_len() + 1:
        return 0.0
    if t == t_start():
        return pols_if_init()
    if t == proj_len() + 1:
        return 0.0
    return pols_if_at(t - 1, "AFT_LAPSE")


def pols_if_at(t, timing):
    """The number of policies in force at a point inside policy year t.

    ``"BEF_DECR"``
        ``l(t)``, the start of the year, before any decrement — the same
        number as :func:`pols_if` and the weight on that year's premiums,
        charges, guaranteed interest and expenses.

    ``"AFT_DEATH"``
        after the year's deaths, before surrenders.  Death and surrender are
        **sequential and not competing** here: the surrender rate is applied
        to the survivors of death **[std]**.

    ``"AFT_LAPSE"``
        after both, and so the population the *Indexjahr* credit is given to.
        In the final policy year the surrender rate is zero, so this is the
        maturing cohort.
    """
    if timing == "BEF_DECR":
        return pols_if(t)
    if timing == "AFT_DEATH":
        return pols_if(t) - pols_death(t)
    if timing == "AFT_LAPSE":
        return pols_if_at(t, "AFT_DEATH") - pols_lapse(t)
    raise ValueError("invalid timing")


def pols_death(t):
    """``l(t) q_d(t)``: expected deaths in policy year t, claimed at the end of the year."""
    return pols_if(t) * mort_rate(t)


def pols_lapse(t):
    """Expected surrenders in policy year t, taken from the survivors of death.

    Zero in the final policy year, where the survivors leave as maturities instead.
    """
    return pols_if_at(t, "AFT_DEATH") * lapse_rate(t)


def pols_maturity(t):
    """The cohort reaching *Rentenbeginn*: the survivors of both decrements at ``t = n``.

    Zero in every other policy year.  The name is the library's — a count whose cover ends
    at the scheduled end of the contract, whether or not anything is paid for it — and here
    something very much is paid for it.
    """
    if t != proj_len():
        return 0.0
    return pols_if_at(t, "AFT_LAPSE")


# --- benefits ----------------------------------------------------------------

def db_pp(t):
    """``D(t)``: the death benefit per policy in policy year t.

    ``max(av_pp_at(t, "AFT_GUAR"), death_min_rate() x BS)`` — the account **before** the
    year's index and safe-arm credits, floored at the *Mindesttodesfallschutz* fraction of
    the *Beitragssumme*.

    Two things this is not.  It is **not** a sum at risk: the standard *Todesfallleistung*
    in the *Aufschubphase* of a German deferred annuity is a return of the accumulated
    capital, which is why the *Risikoüberschuss* is small, underwriting is light and the
    three-year suicide exclusion is close to inoperative.  And it carries **no pro-rata
    index credit**: the payoff exists only at the *Indexjahr* end **[std]**, so a death in
    month 7 forfeits it.
    """
    return max(av_pp_at(t, "AFT_GUAR"), death_min_rate() * prem_sum())


def min_surr_pp(t):
    """The § 169 Abs. 3 VVG *Mindestrückkaufswert* per policy in policy year t.

    ``av_min_pp_at(t, "AFT_GUAR")``: the account with acquisition costs spread evenly over
    the first five contract years, so that an early surrender value cannot be extinguished
    by front-loaded costs.  A floor under the tariff value, not a value in its own right.

    It is a different rule from the DeckRV *Höchstzillmersatz* with a different function —
    the DeckRV governs what may be **reserved**, § 169 VVG what must be **paid** — and
    conflating the two is a numbered pitfall.  With ``zill_years = 5`` they coincide and
    this floor is a no-op.
    """
    return av_min_pp_at(t, "AFT_GUAR")


def surr_charge_pp(t):
    """The *Stornoabzug* deducted from the surrender value in policy year t.

    2 % of the floored base **[std]**, applied only where the model point carries
    ``surr_charge_on = 1``.  A *Stornoabzug* is effective only if it is agreed, appropriate
    and **quantified in the contract**; one carrier's retrieved structure in the sibling
    research was a 5 % base deduction plus a capital-market-dependent component, and the
    observed band runs from 0 % to 20 %, so 2 % is a deliberately mild **[std]**.
    """
    return (storno_rate * surr_charge_on()                           # noqa: F821
            * max(av_pp_at(t, "AFT_GUAR"), min_surr_pp(t)))


def cv_pp(t):
    """``V(t)``: the surrender value per policy in policy year t.

    ``max(av_pp_at(t, "AFT_GUAR"), min_surr_pp(t)) - surr_charge_pp(t)``.  A
    **general-account reserve**, not a unit value: locked-in index credits are inside it,
    because by then they are guaranteed capital, while the running *Indexjahr* is not,
    because its payoff is determined only at the year end.

    A behavioural incentive the annual grid quietly assumes away: with no credit in the
    year of exit the product rewards surrendering just **after** an *Indexjahr* ends and
    penalises surrendering just before one, and an annual grid with exits at the year end
    silently gives every surrender the favourable date.
    """
    return max(av_pp_at(t, "AFT_GUAR"), min_surr_pp(t)) - surr_charge_pp(t)


def mat_pp(t):
    """``M(n)``: the benefit per policy at *Rentenbeginn*; zero in every other year.

    ``max(av_pp(n + 1), guar_cap_pp(n + 1))`` — the account **including** the final
    *Indexjahr*'s credits, floored at the *Beitragsgarantie* plus the whole locked-in
    ledger.  This is the one date at which the guarantee is owed, and the only benefit in
    the model that sees it.

    On the anchor the floor does not bind; on model point 9, whose 100 % guarantee is
    written against a flat index path, it does — and a model with no floor and a model with
    a floor that never binds look identical on every other point.
    """
    if t != proj_len():
        return 0.0
    return max(av_pp(proj_len() + 1), guar_cap_pp(proj_len() + 1))


def claims(t, kind=None):
    """Benefit outgo in policy year t, by kind; the total when kind is omitted.

    ``"DEATH"``
        ``D(t) x pols_death(t)``, the account before the year's credits with
        the *Mindesttodesfallschutz* floor.

    ``"LAPSE"``
        ``V(t) x pols_lapse(t)``, the § 169 Abs. 3-floored reserve less the
        *Stornoabzug*.  Zero in the final policy year by construction.

    ``"MATURITY"``
        ``M(n) x pols_maturity(n)``, the capital falling due at
        *Rentenbeginn*, and zero everywhere else.

    All three fall at the **end** of the policy year.  Two exits at the same instant take
    different amounts — the maturity includes the year's *Indexjahr* and the other two do
    not — and that is the product's own rule.
    """
    if kind is None:
        return sum(claims(t, k) for k in ("DEATH", "LAPSE", "MATURITY"))
    if kind == "DEATH":
        return db_pp(t) * pols_death(t)
    if kind == "LAPSE":
        return cv_pp(t) * pols_lapse(t)
    if kind == "MATURITY":
        return mat_pp(t) * pols_maturity(t)
    raise ValueError("invalid kind")


def rentenfaktor():
    """The *Rentenfaktor* applied at *Rentenbeginn*: the **greater** of the two.

    ``max(rentenfaktor_guar, rentenfaktor_curr)`` — a guarantee with upside, the chassis
    rule of the German deferred annuity.  The two are set equal in the base run **[std]**
    so that the max-of-two rule is exercised by a test rather than by the base path.
    """
    return max(rentenfaktor_guar, rentenfaktor_curr)                 # noqa: F821


def ann_monthly_pp():
    """The monthly *Leibrente* the terminal capital buys, per policy; **reported, not paid**.

    ``M(n) / 10,000 x rentenfaktor()`` where the *Kapitalwahlrecht* is not exercised, and
    0.00 where it is.  It is not a cash flow of this model: the *Rentenphase* is a separate
    contract state and a separate model.

    **Neither this number nor the factor behind it is authoritative.**  The factor is a
    **[std]** 25.00 EUR per 10,000 EUR and the mortality it is quoted against is a **[std]**
    period-table proxy, while the real basis is DAV 2004 R, generational in age *and*
    calendar year.  A period proxy priced at a 40-year-old's annuitisation twenty-seven
    years out understates the liability by a margin that dwarfs every other assumption here,
    which is why the model **reports** an annuity and does not compute one.
    """
    if ann_option() != "annuity":
        return 0.0
    return mat_pp(proj_len()) / 10000.0 * rentenfaktor()


# --- expenses and the cash flow statement ------------------------------------

def exp_acq_pp(t):
    """The insurer's acquisition expense per policy: 2.5 % of ``BS`` at inception **[std]**.

    Incurred **in full at ``t_start()``** and only for a new-business point — an in-force
    point's acquisition expense was paid before the valuation date.  This is the *Zillmer*
    strain: the insurer pays it at once and recovers it through
    :func:`prem_charge_acq_pp` over five years, and setting the expense equal to the charge
    is what makes the strain visible in ``net_cf`` rather than assumed away.
    """
    if t != t_start() or dur_init() != 0:
        return 0.0
    return acq_expense_rate * prem_sum()                             # noqa: F821


def exp_maint_pp(t):
    """Maintenance expense per policy: 36.00 EUR a year inflating at 1.5 % **[std]**.

    *Stückkosten*, ``exp_fixed_pp x (1 + exp_infl)^(t - 1)``, inflated from **issue** and
    not from the valuation date, so an in-force point carries the inflation its duration
    has already accumulated.
    """
    return exp_fixed_pp * (1.0 + exp_infl) ** (t - 1)                # noqa: F821


def expenses(t):
    """Total insurer expense outgo in policy year t, at the start of the year.

    ``(exp_acq_pp(t) + exp_maint_pp(t)) x l(t)``.  No claim expense is modelled: no source
    gives one and it would be immaterial beside a benefit that is the account value.

    An **expense**, not a charge: this is the insurer's own cash going out, and it is the
    only expense line in ``net_cf``.  The deductions from the policyholder's account —
    ``prem_charge_acq_pp``, ``prem_charge_adm_pp``, ``av_charge_pp`` — are charges and
    appear nowhere in this cells.
    """
    return (exp_acq_pp(t) + exp_maint_pp(t)) * pols_if(t)


def net_cf(t):
    """The net liability cash flow of policy year t, **income positive**.

    Premiums less death, surrender and *Rentenbeginn* benefits less expenses — the
    library's sign convention, applied to every model in it.

    The shape to expect is a large first-year strain, the acquisition expense falling in
    one lump against one year's premium, then thin positive years while the account builds,
    then a very large negative final year when the whole surviving cohort's capital falls
    due at once.  ``guar_int``, ``surplus_credit``, ``index_credit`` and ``av`` are
    reported beside it and are **not** in it: they are movements of the policyholder's
    account, and they reach the insurer's cash flow only later, through a benefit.
    """
    return (premiums(t) - claims(t, "DEATH") - claims(t, "LAPSE")
            - claims(t, "MATURITY") - expenses(t))


def liability_cf(t):
    """The same stream as :func:`net_cf`, outgo positive: ``-net_cf(t)`` exactly.

    The orientation a valuation layer consumes: a Solvency II best estimate is
    ``sum v(t) liability_cf(t)`` over the relevant risk-free term structure, plus a risk
    margin.  Published as a column beside ``net_cf`` so the sign convention is verifiable
    in the frame rather than only in prose.
    """
    return -net_cf(t)


# --- the published identities ------------------------------------------------

def check_net_cf_resid(t):
    """The cash flow statement's reconciliation residual in policy year t; zero everywhere.

    ``net_cf(t) - [ premiums(t) - claims(t) - expenses(t) ]``, with ``claims(t)`` the
    kind-less total.  :func:`net_cf` names the three kinds one by one while this identity
    takes the total, so the two agree only if the ``claims(t, kind)`` dispatch and the cash
    flow statement carry the **same** list of kinds.

    What it catches is therefore a benefit that exists in the model and not in the
    statement — a fourth kind added to :func:`claims` and forgotten in :func:`net_cf` — and,
    read against ``result_cf()``, the pitfall this product invites above all: adding
    ``guar_int``, ``surplus_credit`` or ``index_credit`` into ``net_cf``.  Those are
    movements of the policyholder's account, not the insurer's cash, and any of them
    entering here would leave a residual the size of the credit.

    delib requires this cells of every model in the library: no model's headline number may
    be reconciled only in prose.
    """
    return net_cf(t) - (premiums(t) - claims(t) - expenses(t))


def check_net_cf():
    """True when the cash flow statement reconciles in every projected policy year.

    The library-wide form: no argument, one bool over all ``t``;
    :func:`check_net_cf_resid` gives the signed residual of the year that failed.
    """
    return bool(all(abs(check_net_cf_resid(t)) <= roll_fwd_tol       # noqa: F821
                    * max(abs(premiums(t)), abs(claims(t)),
                          abs(expenses(t)), 1.0)
                    for t in range(t_start(), proj_len() + 1)))


def check_av_roll_fwd_resid(t):
    """The account roll-forward residual at fund level in policy year t; zero everywhere.

    ``av(t + 1) - [ av(t) + prem_to_av(t) - av_charge(t) + guar_int(t) + surplus_credit(t)
    + index_credit(t) - av_released(t) ]``.

    This is the identity the product is most easily got wrong on, because every term is
    struck on a **different population**.  The premium, the charge and the guaranteed
    interest are on the opening in-force, the two credits are on the survivors of both
    decrements, and ``av_released`` carries the balance the exits took with them — at
    ``AFT_GUAR`` for a death or a surrender and at ``AFT_CREDIT`` for a maturity.  Give the
    *Indexjahr* credit to ``pols_if(t)`` instead of to ``pols_if_at(t, "AFT_LAPSE")`` and
    the residual is exactly the credit the leavers should not have had.

    It closes in the final policy year too, where ``av(n + 1)`` is zero and the whole
    balance leaves through the maturity term of :func:`av_released`.
    """
    return av(t + 1) - (av(t) + prem_to_av(t) - av_charge(t) + guar_int(t)
                        + surplus_credit(t) + index_credit(t) - av_released(t))


def check_av_roll_fwd():
    """True when the account roll-forward closes in every projected policy year.

    Tolerance is relative to the balance, the account running to five figures while the
    residual should be zero to machine precision.
    """
    return bool(all(abs(check_av_roll_fwd_resid(t)) <= roll_fwd_tol  # noqa: F821
                    * max(abs(av(t)), 1.0)
                    for t in range(t_start(), proj_len() + 1)))


def check_pols_roll_fwd_resid(t):
    """The in-force roll-forward residual in policy year t; zero everywhere.

    ``pols_if(t) - pols_if(t + 1) - pols_death(t) - pols_lapse(t) - pols_maturity(t)``.
    The recursion applies the two rates in sequence while the three exits are formed
    separately, so the two agree by algebra when — and only when — every one of them is
    read at the same ``t``.  What it catches is a **misindexed recursion**: rolling forward
    with ``w_l(t - 1)`` or ``q_d(t + 1)``, or applying the surrender rate to the opening
    in-force instead of to the survivors of death.

    In the final policy year ``pols_if(n + 1)`` is zero, ``pols_lapse`` is zero and the
    survivors leave through ``pols_maturity``, so the identity closes there as well — and
    that is the year in which an implementation that lets the cohort simply vanish, or that
    double-counts it as both a lapse and a maturity, fails.
    """
    return (pols_if(t) - pols_if(t + 1)
            - pols_death(t) - pols_lapse(t) - pols_maturity(t))


def check_pols_roll_fwd():
    """True when the decrements roll forward **and** close over the whole projection.

    Two conditions, not one: the per-year residual above is zero at every ``t``, and the
    three exits summed over the projection account for the whole opening cohort,
    ``sum(deaths + surrenders + maturities) == pols_if_init()``.  The second is the
    stronger statement — it is built by direct summation over the exit cells, with no
    reference to the recursion that produced ``pols_if`` — and it is what catches a life
    that leaves twice or never leaves at all.
    """
    ts = range(t_start(), proj_len() + 1)
    closure = sum(pols_death(t) + pols_lapse(t) + pols_maturity(t)
                  for t in ts) - pols_if_init()
    tol = roll_fwd_tol * max(pols_if_init(), 1.0)                    # noqa: F821
    return bool(abs(closure) <= tol
                and all(abs(check_pols_roll_fwd_resid(t)) <= tol for t in ts))


def check_surplus_alloc_resid(t):
    """The surplus-allocation residual in policy year t; zero everywhere.

    ``opt_budget_pp(t) + surplus_credit_pp(t) - surplus_rate(t) x index_base_pp(t)``.

    **This is the product's whole economics in one line.**  The year's declared surplus is
    either spent on the option package or credited as interest — never both, and never
    neither.  An implementation that credits the declared rate *and* runs the index
    participation has spent one budget twice, and the result looks entirely plausible until
    this residual is taken: it is exactly the surplus that was double-counted.
    """
    return (opt_budget_pp(t) + surplus_credit_pp(t)
            - surplus_rate(t) * index_base_pp(t))


def check_surplus_alloc():
    """True when the declared surplus is allocated exactly once in every policy year."""
    return bool(all(abs(check_surplus_alloc_resid(t)) <= roll_fwd_tol  # noqa: F821
                    * max(abs(index_base_pp(t)), 1.0)
                    for t in range(t_start(), proj_len() + 1)))


def check_lock_in_resid(t):
    """The *Höchststandsicherung* violation in policy year t; zero when the ratchet holds.

    The sum of three one-sided terms, each zero unless it is breached: the fall in
    ``guar_cap_pp`` from ``t`` to ``t + 1``, a negative *Indexgutschrift*, and a negative
    safe-arm credit.  Negative when the lock-in fails, and its size is the size of the
    breach.

    What it must **not** be is a statement about the account balance.  It is the *credits*
    that ratchet, not ``av_pp``: with the reserve charge at or above the guaranteed rate
    the balance falls in a year that credits nothing, which is ordinary and is model point
    13.  Writing this check on ``av_pp`` would make a correct implementation fail and a
    wrong one — one that let a bad *Indexjahr* claw back a credit — pass.
    """
    return (min(0.0, guar_cap_pp(t + 1) - guar_cap_pp(t))
            + min(0.0, index_credit_pp(t))
            + min(0.0, surplus_credit_pp(t)))


def check_lock_in():
    """True when the guaranteed capital is monotone and no credit is negative."""
    return bool(all(abs(check_lock_in_resid(t)) <= roll_fwd_tol      # noqa: F821
                    * max(abs(guar_cap_pp(t)), 1.0)
                    for t in range(t_start(), proj_len() + 1)))


def check_index_credit_resid(t):
    """The payoff-bound violation in policy year t; zero when the *Indexrendite* is in range.

    ``0 <= rho(t) <= 12 C(t)`` in the Cap design — the year cannot credit less than nothing
    and cannot credit more than twelve capped months — and ``0 <= rho(t) <= q(t) max(Y(t),
    0)`` in the *Partizipationsquote* design.  Returns the sum of the two one-sided
    breaches, so it is zero when both hold and negative otherwise.

    It is the arithmetic guard on the payoff formula itself.  An implementation that floors
    each month at zero stays inside the upper bound and is still wrong, which is why the
    Example B assertions in the product's own test module sit beside this check rather than
    being replaced by it; but one that compounds the capped returns, or that applies the
    Cap to the annual return instead of the monthly one, or that forgets the floor
    altogether, breaks a bound here.
    """
    if payoff_form() == "quote":
        upper = index_quote(t) * max(index_return_year(t), 0.0)
    else:
        upper = 12.0 * index_cap(t)
    return (min(0.0, index_credit_rate(t))
            + min(0.0, upper - index_credit_rate(t)))


def check_index_credit():
    """True when the *Indexrendite* is inside its contractual bounds in every year."""
    return bool(all(abs(check_index_credit_resid(t)) <= roll_fwd_tol  # noqa: F821
                    for t in range(t_start(), proj_len() + 1)))


# --- the result table --------------------------------------------------------

def result_cf():
    """Result table of cash flows and account movements, indexed by policy year t.

    The frame runs ``t = t_start() ... proj_len()``, contiguous, and stops: policy year
    ``proj_len()`` ends at *Rentenbeginn*, where the capital falls due as
    ``claims_maturity``.

    ``pols_if`` is the start-of-year count and the weight on every cash flow of the same
    row, so the first row's value is ``pols_if_init()`` exactly.  ``premiums``,
    ``claims_death``, ``claims_lapse``, ``claims_maturity`` and ``expenses`` are the cash
    flow statement and sum to ``net_cf``.

    **The four columns after ``expenses`` are state movements, not cash flows.**
    ``guar_int``, ``surplus_credit`` and ``index_credit`` are credits to the policyholder's
    account that reach the insurer's cash flow only later, through a benefit, and ``av`` is
    a balance.  They are published because a reader cannot follow this product without
    them — the whole point of the contract is what happens to the account — and they are
    **not** summed into ``net_cf``.  Adding them is a numbered pitfall, and
    :func:`check_net_cf` is what catches it.

    ``liability_cf`` is ``net_cf`` outgo-positive, published so the sign convention is
    verifiable in the frame.
    """
    ts = list(range(t_start(), proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "claims_death": [claims(t, "DEATH") for t in ts],
            "claims_lapse": [claims(t, "LAPSE") for t in ts],
            "claims_maturity": [claims(t, "MATURITY") for t in ts],
            "expenses": [expenses(t) for t in ts],
            "guar_int": [guar_int(t) for t in ts],
            "surplus_credit": [surplus_credit(t) for t in ts],
            "index_credit": [index_credit(t) for t in ts],
            "av": [av(t) for t in ts],
            "liability_cf": [liability_cf(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

acq_cost_rate = 0.025

acq_expense_rate = 0.025

zill_years = 5

zill_cap_rate = 0.025

exp_prem_rate = 0.03

exp_av_rate = 0.0025

exp_fixed_pp = 36.0

exp_infl = 0.015

storno_rate = 0.02

rentenfaktor_guar = 25.0

rentenfaktor_curr = 25.0

roll_fwd_tol = 1e-08

pd = ("Module", "pandas")
