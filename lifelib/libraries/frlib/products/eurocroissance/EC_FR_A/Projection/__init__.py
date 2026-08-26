# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.EC_FR_A` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_provisions()   # the worked example, Chassis A
    >>> Projection.point_id = 2             # Chassis B, same asset path

``t`` counts **policy years** from issue and is **0-based**: ``t = 0`` is the issue
point, where the initial *versement* net of the entry charge creates the rights and the
two provisions are first struck. A new-business cell therefore starts at
``proj_start() = 0``; an in-force cell at ``duration_ifo``, where the extract's assets,
parts and guaranteed amount are seeded and the *provision mathématique* is re-derived
rather than read. The projection ends at ``proj_len() = policy_term()``, the *échéance*.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent
directory, ``products/eurocroissance/``, read at run time rather than stored inside the
model. The model folder therefore holds nothing but formulas — no ``_data/``, no
IOSpec, no embedded values — so a diff of the model shows logic changes only, and an
input can be edited or swapped without rewriting the model. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``EC_FR_A`` folder without its parent's CSVs produces a model that reads and then fails
on first evaluation.

Each table has a filename Reference and a reader Cells, both on :mod:`~.EC_FR_A.Data`,
reached here through the ``data`` Reference:

======================  ==============================  ==========================
Reference               Cells                           File
======================  ==============================  ==========================
model_point_file        data.model_point_table()        model_point_table.csv
mort_table_file         data.mort_table()               mort_table.csv
lapse_table_file        data.lapse_table()              lapse_table.csv
scenario_table_file     data.scenario_table()           scenario_table.csv
tec_curve_file          data.tec_curve()                tec_curve.csv
======================  ==============================  ==========================

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` wherever that model has an
analogue — ``pols_*`` for policy counts, plural nouns for cash flows, ``*_rate`` for
rates, ``*_pp`` for per-policy amounts, ``claims(t, kind)`` and ``claim_pp(t, kind)``
with an uppercase ``kind`` string. The technical notes use compact symbols instead. The
mapping is:

=========================  ==============================  ==========================
Notes symbol               Cells                           Meaning
=========================  ==============================  ==========================
engagement_modality        chassis()                       euro_and_parts or parts_only
(the 1° test)              is_euro_leg()                   True on Chassis A
t                          (the cells argument)            Policy year, 0-based
x                          issue_age()                     Entry age (âge atteint)
x + t                      age(t)                          Attained age
duration_ifo               duration_inforce()              Completed years at valuation
(none)                     proj_start()                    First projected policy year
n                          policy_term()                   Years to the échéance
(none)                     proj_len()                      Last projected policy year, = n
g                          guarantee_rate()                Share of net versements guaranteed
P(t)                       premium_gross_pp(t)             Scheduled versement, BOY
P_net(t)                   prem_after_charge_pp(t)               Net of the R. 134-3 1° charge
(free versement)           premium_top_up_gross_pp(t)      Free versement, EOY
(free versement, net)      premium_top_up_net_pp(t)        Net of the entry charge
f_e                        entry_charge_rate()             Entry charge, base 1°
f_p                        parts_charge_rate()             Parts levy p.a., base 4°
f_perf                     perf_charge_rate()              Performance levy, base 5°
f_x                        exit_charge_rate()              Exit charge, base 6°
(indemnity)                surrender_indemnity(t)          R. 132-5-3 indemnity, capped
mg(t)                      mg(t)                           Guaranteed amount at n
(cumulative net premiums)  cum_prem_net(t)                 Death-floor base
TEC(n-t)                   tec_rate(t)                     Interpolated TEC
i_pm(t)                    i_pm(t)                         90% of TEC, floored at zero
(discount factor)          disc_factor(t)                  (1 + i_pm(t))^-(n-t)
r(t)                       asset_return(t)                 Gross asset return in year t
A(t)                       own_assets(t)                   Account assets, excluding C(t)
(the steps)                own_assets_at(t, timing)        The asset roll inside year t
pm(t)                      pm(t)                           Provision mathématique
(pre-versement)            pm_at(t, timing)                PM at the striking, before a top-up
pd(t)                      prov_div(t)                     Provision de diversification
(pre-versement)            prov_div_at(t, timing)          PD at the striking
N(t)                       parts(t)                        Number of parts
(the steps)                parts_at(t, timing)             Parts inside year t
u(t)                       part_value(t)                   Valeur de la part
(pre-versement)            part_value_at(t, timing)        Part value at the striking
u_min                      min_part_value()                Contractual floor on u
L(t)                       parts_levy(t)                   BOY levy, base 4°
I(t)                       invest_income(t)                Financial performance in year t
F(t)                       perf_levy(t)                    EOY levy, base 5°
(entry)                    entry_charge(t)                 Base 1° charge on a versement
C(t)                       insurer_contribution(t)         L. 134-3 outstanding contribution
G(t)                       pgt(t)                          Provision pour garantie à terme
D(t)                       pcdd(t)                         Provision collective de div. différée
(apport d'actifs)          apport(t)                       R. 134-12 contribution to the PCDD
(A. 134-3 tests)           gate_revalue_ok(t)              Whether a revaluation is permitted
(A. 134-4 headroom)        conversion_headroom(t)          Parts convertible into PM
(surrender base)           provision_value(t)              pm(t) + pd(t)
surrender_value(t)         surrender_value(t)              R. 134-5 value
death_value(t)             death_value(t)                  The current provision value
death_payout(t)            death_payout(t)                 After any garantie décès plancher
rider_claim(t)             rider_claim_pp(t)               The floor's cost, outside the account
maturity_value(n)          maturity_value(t)               R. 134-6 amount
(payouts)                  claim_pp(t, kind)               Payout per claim by kind
q(x+t)                     mort_rate(t)                    Annual mortality rate
w(t)                       lapse_rate(t)                   Full surrender rate, all overlays
(table)                    lapse_rate_base(t)              Table full surrender rate
(partial rachat)           wd_rate(t)                      Partial surrender rate
(partial rachat)           wd_pp(t)                        Partial surrender paid
(partial rachat, gross)    wd_gross_pp(t)                  Taken from the provision
(none)                     pols_if(t)                      In force at the **start** of year t
l(t)                       pols_if_at(t, "AFT_DECR")       In force at the **end** of year t
(none)                     pols_if_at(t, timing)           BEF_DECR / BEF_LAPSE / AFT_DECR
(none)                     pols_death(t)                   Deaths in year t
(none)                     pols_lapse(t)                   Full surrenders in year t
(none)                     pols_maturity(t)                Survivors reaching the échéance
(cash flows)               premiums, claims, withdrawals   Probability-weighted flows
E(t)                       expenses(t)                     Acquisition and maintenance
charges_taken(t)           charges_taken(t)                Insurer income, reported apart
CF(t)                      liability_cf(t)                 The notes' outgo-positive stream
(none)                     net_cf(t)                       Its negative, income positive
(none)                     model_point()                   The selected row as a Series
=========================  ==============================  ==========================

Six names needed care.

``pols_if`` is the count at the **start** of policy year t — the exposure every cash flow
on that same :func:`result_cf` row is weighted by — so ``result_cf()["pols_if"].iloc[0]``
is ``pols_if_init()`` on every model point.  This model first published the notes' own
``l(t)``, the count at the **end** of the year, under that name, which put the exposure
column one year ahead of the flows beside it: a reader dividing ``claims_death`` by that
row's ``pols_if`` to recover a per-policy payout got a one-year-stale answer, and nothing
raised.  The end-of-year quantity survives unchanged and unrenamed in substance — it is
now reached as **``pols_if_at(t, "AFT_DECR")``**, the ``CashValue_SE`` timing form this
library uses for every other intra-period state — and every number in :func:`result_cf`
except the ``pols_if`` column is what it was before the change.  The notes, ``model.md``
and the test module index ``l(t)`` the same way.

``pm_ifo`` appears in the notes' model point attribute table but is **not** an input the
projection reads. The *provision mathématique* is re-struck from ``mg`` and the current
``i_pm`` every year, so an in-force cell that supplied one would be asserting a number
the rule already determines. The column is shipped and :func:`check_pm_restruck` compares
it against the re-strike — which is how a reader discovers that an extract was built by
accumulating the PM instead.

``lapse_rate`` is the **full** surrender (*rachat total*) and ``wd_rate`` the **partial**
one (*rachat partiel*). They are different events with different consequences: a full
surrender removes the policy, a partial one runs the guarantee, the parts and the assets
down pro rata and leaves the contract in force. Sharing one name would have merged a
decrement with an owner election.

``wd_gross_pp`` and ``wd_pp`` differ by the base 6° exit charge — what leaves the
provision and what reaches the saver. Both are needed, because the provision run-down
keys off the gross amount and the cash flow off the net one.

``provision_value`` is ``pm + pd``, the base of R. 134-5 and R. 134-6. It is the same
expression on both chassis because ``pm`` is identically zero on Chassis B, so the
surrender and death rules are one formula rather than two.

``pd`` is the one notes symbol this model could not keep. ``pd`` is **pandas** in every
model in this library, and shadowing it inside the one Space that has to build a
DataFrame is not worth a two-letter symmetry, so the *provision de diversification* is
:func:`prov_div` here while the *provision mathématique* keeps :func:`pm`, whose symbol
was free. The displayed formulas below stay in the notes' notation; the table above is
what maps them.

There is **no** ``av_pp_at`` in this model. A eurocroissance engagement is not an account
value: the saver's rights are a number of *parts* whose value is common to every
engagement of the auxiliary account, plus — on Chassis A — a share of a *provision
mathématique* that is a discounted promise rather than a fund. Naming either of them the
library's account value would assert something false about the contract.

.. rubric:: The provision mathématique is re-struck, never accumulated

::

    pm(t) = mg(t) (1 + i_pm(t))^-(n-t)          Chassis A
    pm(t) = 0                                    Chassis B

``i_pm(t)`` is 90% of the TEC, floored at zero (A. 134-1), read here at the **remaining**
maturity ``n - t`` — a **[std]** reading of the article's index maturity, which
:func:`tec_rate` sets out. It is **not** the A. 132-1 maximum technical rate and not the
A. 132-3 guaranteed rate ceiling, which are different and stricter objects. Rolling ``pm(t-1)`` forward at
last year's rate would silently remove the **rate effect**: in the notes' worked example
that is +587.44 of the +824.18 move in year 6, against a time effect of only +236.74.

At ``t = n`` the discount factor is 1, so ``pm(n) = mg(n)`` identically and the Chassis A
guarantee is pre-funded by construction. :func:`check_guarantee_funding` asserts it at
every ``t``, and it is the model's headline check.

.. rubric:: The annual rebalancing

::

    L(t) = f_p pd(t-1)                    A_a = A(t-1) - L(t) - W(t) + P_net(t)
    I(t) = A_a r(t)                       F(t) = f_perf max(I(t), 0)
    A(t) = A_a + I(t) - F(t)              N(t) = N(t-1)(1 - f_p)(1 - w_partial) + ...
    pd(t) = max(A(t) - pm(t), N(t) u_min)  u(t) = pd(t)/N(t)
    C(t)  = max(pm(t) + pd(t) - A(t), 0)

The diversification provision takes the **residual** and stops at the parts' contractual
floor. Where the floor binds, the two provisions together exceed the assets, and the
excess is exactly ``C(t)`` — the contribution the insurer must make under L. 134-3 to
complete the representation. The **surrender value therefore exceeds the account's own
assets by exactly ``C(t)``** while the contribution is outstanding: on the notes' year-6
shock, 12,384.73 paid against assets of 10,250.65.

``C(t)`` carries **no return to the savers**: :func:`own_assets` rolls forward from
``A(t-1)``, not from ``pm(t-1) + prov_div(t-1)``. Rolling the topped-up balance forward would
manufacture investment return out of the insurer's capital, and the shipped worked
example is the case that catches it — the year-7 asset roll starts from 10,250.65 and not
from 12,384.73.

.. rubric:: The Chassis B surrender value is not guaranteed

This is the single most important product fact. Before the *échéance* a 2° engagement
pays ``parts × part value`` and **nothing else** (R. 134-5). The guarantee bites only at
``t = n``, and only there does :func:`maturity_value` take ``max(parts × u, mg)``. On the
notes' year-6 shock, Chassis B surrenders for **9,899.22** — 84.18% of net *versements*
against a guarantee of 11,760.00. An implementation that floors the surrender value at
the guarantee, or at the discounted guarantee, is modelling a contract that does not
exist. :func:`check_own_funds_not_paid` asserts that no benefit before the term exceeds
the two provisions.

The shortfall against the guarantee is carried instead as the *provision pour garantie à
terme*, :func:`pgt` — the insurer's own funds, computed per auxiliary account on the
A. 132-18 tables at a rate at most 90% of the TEC, counting **no cash flows other than
guarantee maturities and mortality**. It sits outside the participation account, it is
not part of any benefit, and a model must not "improve" its deliberately narrow basis by
adding lapses or expenses to it. Of the article's two admitted drivers this model
implements only the guarantee maturity: :func:`pgt` applies **no survival factor**, a
prudent **[std]** simplification that the cells docstring quantifies.

.. rubric:: The death benefit is not the maturity guarantee

Chapter IV of the regulatory part contains no death valuation article. The death benefit
is the **current provision value**, and any *garantie décès plancher* is a complementary
guarantee provisioned **outside** the auxiliary account (R. 134-7). :func:`death_payout`
therefore floors the payout at cumulative net *versements* where the model point elects
the rider, and :func:`rider_claim_pp` reports the difference separately — 1,860.78 on the
notes' year-6 Chassis B death, which is not the account's money.

.. rubric:: The charge bases are not interchangeable

R. 134-3 permits six bases and no others, and base 3° — a levy on the *encours* of the
diversification provision — is available only in an auxiliary account holding **no** 1°
engagements. No base permits a levy on the *provision mathématique* at all. The recurring
charge here is therefore base 4°, a levy **in number of parts**: :func:`parts_levy` is
``f_p × prov_div(t-1)`` and :func:`parts_at` cancels ``f_p`` of the parts. On the worked
example's Chassis A that is **15.64** in year 1. An *encours* levy on ``pm + pd`` would
have been 78.40 — five times as much, and unlawful in a 1° account.

.. rubric:: Behaviour, and what is not modelled

All dynamic shapes are **[std]**: no eurocroissance lapse experience is public and the
product is too small and too young to have any. Three overlays sit on the base full
surrender rate:

- a **guarantee-imminent suppression** of 0.5 in the two years before the *échéance* on
  Chassis B, and only while the guarantee is in the money — a saver who surrenders in
  that state gives up the entire guarantee, which is the strongest exit deterrent the
  product creates;
- a **duration-8 spike** of 1.5 where ``n > 8``, because the assurance-vie annual
  *abattement* becomes available at eight years; and
- a **lock-up**, where ``lock_up_years > 0`` bars surrender entirely, the L. 132-23
  hardship exits not being separately modelled.

Out of scope, and held at zero or absent by design: the PCDD **piloting rule** (run the
fund at 30 bp above the insurer's own euro fund and carry the rest to the PCDD) and the
PCDD's release back into the participation account — :func:`pcdd` accumulates the
R. 134-12 *apport d'actifs* and nothing else; the conversion of parts into PM under
A. 134-4, whose headroom :func:`conversion_headroom` computes without exercising; the
revaluation of guarantees out of the participation account, whose two A. 134-3 gates
:func:`gate_revalue_ok` tests without exercising; the *rente viagère* option at the
*échéance*, which :func:`annuity_option_flag` rejects by name; and the statutory
arbitrage into an SRI ≤ 2 support that A. 134-6 makes the maturity default.

.. rubric:: What a single-policy annual model cannot say

The part value, the PCDD, the PGT and the *apport d'actifs* are all **account-level**
quantities. The part value in particular is common to every engagement of an auxiliary
account, so savers with different maturities and different guarantee levels in one
account earn the same rate and differentiation is possible only through the number of
parts. A per-policy model can only approximate that, and the *mémoire* records that
pooling two maturity cohorts in one account produces **no** mutualisation benefit at all.
Model points 1 and 2 are two separate accounts on the same asset path, and their part
values duly diverge; two engagements of one account would not.

The deterministic single scenario is the other limit. The maturity guarantee is a put on
the auxiliary account, its cost is convex in the asset shock and in the level of rates,
and a deterministic run understates it. What this model produces is exactly the
per-scenario cash flow vector a market-consistent stochastic valuation consumes.
"""

from modelx.serialize.jsonvalues import *

_formula = lambda point_id: None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def model_point():
    """The selected model point as a Series."""
    return data.model_point_table().loc[point_id]                    # noqa: F821


def chassis():
    """``euro_and_parts`` (1° engagement) or ``parts_only`` (2° engagement).

    L. 134-1 defines exactly these two modalities, and R. 134-2 to R. 134-6 give each of
    them its own provision structure, surrender value and maturity amount.  A value
    outside the pair is a data error and raises rather than defaulting to one of them.
    """
    v = model_point()["engagement_modality"]
    if v not in ("euro_and_parts", "parts_only"):
        raise ValueError("invalid engagement_modality: " + str(v))
    return v


def is_euro_leg():
    """True on Chassis A, the 1° engagement that carries a *provision mathématique*.

    On Chassis B ``pm`` is identically zero, the whole engagement is expressed in parts,
    and the guarantee is carried by the insurer's own funds until the *échéance*.
    """
    return chassis() == "euro_and_parts"


def issue_age():
    """x: the entry age of the model point, *âge atteint* (age last birthday) **[std]**.

    A. 335-1 applies the homologated tables with the annexed *décalages d'âge* rather than
    fixing a model age basis, so the basis is a standardization.
    """
    return int(model_point()["issue_age"])


def sex():
    """The sex (M / F) of the model point.

    A. 132-18 requires the mortality basis to be by sex, so the decrement table is
    sex-distinct even though the tariff itself may not be.
    """
    v = model_point()["sex"]
    if v not in ("M", "F"):
        raise ValueError("invalid sex: " + str(v))
    return v


def policy_term():
    """n: the years from issue to the *échéance*, at which the guarantee is payable.

    The retrieved market range is 8 to 40 years; the worked example uses 10.
    """
    return int(model_point()["policy_term"])


def duration_inforce():
    """Completed policy years at the valuation date; 0 on a new-business cell.

    An in-force cell is seeded from its extract's assets, parts and guaranteed amount and
    carries no accumulated *provision mathématique* — see :func:`pm_init`.
    """
    return int(model_point()["duration_ifo"])


def guarantee_rate():
    """g: the share of cumulative net *versements* guaranteed at the *échéance*.

    100% in the worked example; the retrieved market range is 80% to 100%, chosen by the
    saver.  This is the product's single largest dial: it sets how much of the account is
    locked into the guaranteed leg and therefore how much of it can bear risk.
    """
    return float(model_point()["guarantee_rate"])


def premium_gross_init():
    """The initial gross *versement* paid at issue; nil on an in-force cell."""
    return float(model_point()["premium_gross"])


def premium_regular_pp():
    """The scheduled annual gross *versement* paid at the start of each policy year.

    Zero on a single-*versement* cell, which is the ordinary eurocroissance shape.
    """
    return float(model_point()["premium_regular"])


def premium_regular_years():
    """The number of policy years over which the scheduled *versement* is paid."""
    return int(model_point()["premium_regular_years"])


def premium_top_up_pp():
    """The free additional gross *versement*, paid at the **end** of a stated policy year.

    The worked example's is €2 000.00 at the end of policy year 3, and it is what makes
    the *versement* split rule visible: paid immediately after the year's striking, it
    buys parts at the part value just struck and raises the guaranteed amount by ``g``
    times its net amount.
    """
    return float(model_point()["premium_top_up"])


def premium_top_up_year():
    """The policy year at whose end the free additional *versement* is paid; 0 if none."""
    return int(model_point()["premium_top_up_t"])


def entry_charge_rate():
    """f_e: the entry charge on each *versement*, R. 134-3 base 1° **[std]**.

    2.00% in the reference configuration; 4.50% is the only published maximum retrieved
    for any eurocroissance support.  It is deducted **before** rights are created, which
    is why the guarantee is a percentage of *net* *versements* — see :func:`mg`.
    """
    return float(model_point()["entry_charge_rate"])


def parts_charge_rate():
    """f_p: the recurring levy in number of parts p.a., R. 134-3 base 4° **[std]**.

    0.80% p.a., taken at the start of the policy year on the opening part value.  Base 4°
    is a levy **in number of parts**, not on an *encours*: R. 134-3 3° permits an encours
    levy only in an auxiliary account holding no 1° engagements, and no base permits any
    levy on the *provision mathématique*.
    """
    return float(model_point()["parts_charge_rate"])


def perf_charge_rate():
    """f_perf: the levy on positive financial performance, R. 134-3 base 5° **[std]**.

    10% of the year's positive financial-management performance and nothing at all on a
    negative one, which is why the worked example's year-6 performance levy is zero.
    """
    return float(model_point()["perf_charge_rate"])


def exit_charge_rate():
    """f_x: the exit charge on amounts leaving the account, R. 134-3 base 6° **[std]**.

    Zero in the reference configuration — the code permits it and neither retrieved
    insurer shows one.
    """
    return float(model_point()["exit_charge_rate"])


def surrender_indemnity_rate():
    """The *indemnité de rachat* rate on a full surrender **[std]**.

    Zero in the reference configuration.  R. 132-5-3 caps it at 5% of the present value of
    the mutual engagements and **permits** the contract to charge none at all once it has
    been in force more than ten years — a permission, not a prohibition.
    :func:`surrender_indemnity` takes that permission up unconditionally **[std]**.
    """
    return float(model_point()["surrender_indemnity_rate"])


def part_value_init():
    """u(0): the *valeur de la part* at the auxiliary account's inception.

    €10.0000 in the reference configuration.  It is a denomination rather than an
    assumption: what matters is the ratio of the part value to its floor, since that is
    how far the diversification provision can fall before the floor binds.
    """
    return float(model_point()["part_value_init"])


def min_part_value():
    """u_min: the contractual minimum *valeur de la part*, R. 134-1 **[std]**.

    €5.0000 in the reference configuration, and nowhere published for any insurer.  A
    debit balance on the participation account may reduce the part value only **within the
    limit of its minimum** (R. 134-4), so this level sets the floor of the diversification
    provision — and therefore both the Chassis A maturity payout and the point at which
    the insurer must start contributing assets.  Without it the worked example's Chassis A
    ``prov_div`` would go to **-1,095.35** in year 6.
    """
    return float(model_point()["min_part_value"])


def lock_up_years():
    """The non-surrender period in years; capped at ``min(n, 8)`` by R. 134-5.

    Zero in the reference configuration.  The L. 132-23 hardship exits are not separately
    modelled **[std]**.
    """
    v = int(model_point()["lock_up_years"])
    if v > min(policy_term(), lock_up_cap):                          # noqa: F821
        raise ValueError("lock_up_years exceeds the R. 134-5 cap")
    return v


def death_floor_flag():
    """Whether the model point carries a *garantie décès plancher*.

    A complementary guarantee provisioned **outside** the auxiliary account (R. 134-7),
    floored at cumulative net *versements*.  It is not the maturity guarantee and does not
    become payable because the saver died before the *échéance*.
    """
    return bool(model_point()["death_floor_flag"])


def annuity_option_flag():
    """Whether the model point elects conversion into a *rente viagère* at the *échéance*.

    R. 134-6 permits it, and it is **out of scope** here: an annuity conversion needs the
    TGH05 / TGF05 generational tables, which are cited by arrêté and never shipped, and a
    projection that continues past the *échéance*.  No shipped model point elects it, and
    a cell that did raises rather than being paid a lump sum in silence.
    """
    v = bool(model_point()["annuity_option_flag"])
    if v:
        raise ValueError("the rente viagère option at the échéance is out of scope")
    return v


def wd_factor():
    """The multiplier on the table partial-surrender rate; 0 switches *rachats partiels* off.

    The worked example takes none, which is what lets its provision path be read as the
    cash flow path.
    """
    return float(model_point()["wd_factor"])


def apport_rate():
    """The R. 134-12 *apport d'actifs*, as a fraction of the diversification provision.

    Capped at 10% by the article.  It enters the auxiliary account at realisation value
    and **endows the PCDD**; it is never credited to the savers' diversification
    provision, and switching it on changes no policyholder value by one cent.
    """
    return float(model_point()["apport_rate"])


def apport_year():
    """The policy year at whose end the *apport d'actifs* is made; 0 if none."""
    return int(model_point()["apport_t"])


def decrement_basis():
    """``table`` or ``none``: whether mortality and full surrender are applied.

    ``none`` is not a modelling shortcut but the worked example's stated configuration:
    with ``mort_rate = 0`` and ``lapse_rate = 0`` the in-force probability stays at 1 and
    the per-policy provision path **is** the cash flow path, which is what makes the
    notes' two tables readable as provisions rather than as expected values.
    """
    v = model_point()["decrement_basis"]
    if v not in ("table", "none"):
        raise ValueError("invalid decrement_basis: " + str(v))
    return v


def scenario():
    """The asset-return path and TEC curve the model point runs on.

    Both the return and the discount curve are drawn from the same scenario name, because
    the two move together: the year-6 double shock in the worked example — equities down
    and rates down at once — is what makes the rebalancing visible, and pairing an equity
    fall with an unchanged curve would understate the *provision mathématique* by the
    whole rate effect.
    """
    return model_point()["scenario"]


def own_assets_init():
    """A: the auxiliary-account assets attributable to the policy at the valuation date.

    At realisation value (R. 134-8) and **excluding** any outstanding insurer
    contribution, which is not the savers' money.  Zero on a new-business cell, where
    :func:`own_assets` seeds from the initial net *versement* instead.
    """
    return float(model_point()["own_assets_ifo"])


def parts_init():
    """N: the number of *parts de provision de diversification* at the valuation date."""
    return float(model_point()["parts_ifo"])


def mg_init():
    """mg: the guaranteed amount payable at the *échéance*, at the valuation date."""
    return float(model_point()["mg_ifo"])


def pm_init():
    """The *provision mathématique* the in-force extract reports; **not** an input.

    It is read by :func:`check_pm_restruck` alone.  R. 134-2 makes the PM the guaranteed
    amount discounted at the *current* A. 134-1 rate, so an extract cannot supply it and
    a projection cannot roll it forward — it is re-derived every year, and comparing the
    two is how a reader discovers an extract built by accumulation.
    """
    return float(model_point()["pm_ifo"])


def cum_prem_net_init():
    """The cumulative net *versements* at the valuation date: the death-floor base."""
    return float(model_point()["cum_prem_net_ifo"])


def pols_if_init():
    """Initial number of policies in force; 1.0 on a single-policy model point."""
    return float(model_point()["pols_if_init"])


def proj_start():
    """The first projected policy year: ``duration_inforce()``.

    Zero on a new-business cell, where ``t = 0`` is the issue point at which the initial
    *versement* creates the rights and both provisions are first struck.
    """
    return duration_inforce()


def proj_len():
    """The last projected policy year: the *échéance* at ``policy_term()``.

    The projection stops there because that is where the contract's guarantee is
    discharged.  A model point electing the *rente viagère* option would have to run past
    it, which is why :func:`annuity_option_flag` rejects one.
    """
    return policy_term()


def age(t):
    """The attained age (*âge atteint*) at the end of policy year t: ``x + t``."""
    return issue_age() + t


def asset_return(t):
    """r(t): the gross asset return of the auxiliary account in policy year t **[std]**.

    Net of asset management fees, which is the basis the notes quote it on.  A **scenario**
    level rather than a best estimate: the guarantee is a put on the account and its cost
    is convex in this number, so a deterministic run understates it.
    """
    tbl = data.scenario_table()                                      # noqa: F821
    y = min(t, int(tbl.index.get_level_values("year").max()))
    return float(tbl.loc[(scenario(), y), "asset_return"])


def tec_rate(t):
    """The *taux de l'échéance constante* at the remaining maturity ``n - t``.

    From A. 134-1: linear interpolation between the two bracketing maturities of the
    published curve, the longest rate held beyond the end of the curve, and the shortest
    held below its start — which is what ``t = n`` reaches, where the discount factor is 1
    and the rate is immaterial.  The method choice is irreversible per auxiliary account
    under the article; this model uses method 1°, the per-engagement one, throughout.

    **The index maturity is [std].**  The article as retrieved fixes it as the holder's
    guarantee maturity (method 1°) or the auxiliary account's 1°-engagement duration
    (method 2°), and says nothing about how that maturity is re-read at valuation dates
    after inception.  This model takes the **remaining** term ``n - t``, the horizon the
    guarantee is actually discounted over; holding ``n`` fixed at the original term would
    discount a one-year promise at a ten-year constant-maturity rate on the *échéance* row.
    ``technical-notes.md`` states the reading and is the source of truth for it;
    ``product-spec.md`` states the article as retrieved.  The two readings differ only on a
    sloped curve, which is what shipped model point 10 exercises.
    """
    tbl = data.tec_curve()                                           # noqa: F821
    y = min(t, int(tbl.index.get_level_values("year").max()))
    curve = tbl.loc[(scenario(), y), "tec_rate"]
    ms = [int(m) for m in curve.index]
    m = proj_len() - t
    if m <= ms[0]:
        return float(curve.iloc[0])
    if m >= ms[-1]:
        return float(curve.iloc[-1])
    for lo, hi in zip(ms[:-1], ms[1:]):
        if lo <= m <= hi:
            r_lo, r_hi = float(curve.loc[lo]), float(curve.loc[hi])
            return r_lo + (r_hi - r_lo) * (m - lo) / (hi - lo)
    raise ValueError("no bracketing maturity for " + str(m))


def i_pm(t):
    """The A. 134-1 discount rate for the *provision mathématique*: 90% of the TEC, floored.

    ``max(0, 0.90 x TEC(n - t))``, the 90% haircut and the zero floor from the article and
    the remaining-maturity reading of ``n`` **[std]** — see :func:`tec_rate`.  This is
    **not** the A. 132-1 maximum technical rate and
    **not** the A. 132-3 guaranteed-rate ceiling; those are different and stricter objects
    that apply to a tariff, while this one is a valuation ceiling for a provision the saver
    has no right to withdraw at.  The zero floor matters where the curve is negative: a
    model that let ``i_pm`` go negative would report a *provision mathématique* larger than
    the guarantee it discounts.
    """
    return max(0.0, tec_haircut * tec_rate(t))                       # noqa: F821


def disc_factor(t):
    """``(1 + i_pm(t))^-(n - t)``: the factor that turns the guarantee into the PM.

    One at ``t = n`` by construction, which is the whole point — see
    :func:`check_guarantee_funding`.
    """
    return (1.0 + i_pm(t)) ** -(proj_len() - t)


def premium_gross_pp(t):
    """P(t): the gross *versement* received at the start of policy year t.

    The initial *versement* at ``t = proj_start()`` on a new-business cell, and the
    scheduled annual one while it is payable.  Nil on an in-force cell's opening row,
    whose premium was paid before the valuation date.
    """
    if t == proj_start():
        return premium_gross_init() if duration_inforce() == 0 else 0.0
    if t <= proj_start() + premium_regular_years():
        return premium_regular_pp()
    return 0.0


def prem_after_charge_pp(t):
    """P_net(t): the start-of-year *versement* net of the R. 134-3 1° entry charge.

    **This is the base of the guarantee.**  The guarantee is a percentage of *versements*
    net of the entry charge, so a 2.00% charge on €12 000.00 of gross *versements* leaves
    a guaranteed amount of 11,760.00 and not 12,000.00.
    """
    return premium_gross_pp(t) * (1.0 - entry_charge_rate())


def premium_top_up_gross_pp(t):
    """The free additional gross *versement* paid at the **end** of policy year t."""
    if t > proj_start() and t == premium_top_up_year():
        return premium_top_up_pp()
    return 0.0


def premium_top_up_net_pp(t):
    """The free additional *versement* net of the entry charge."""
    return premium_top_up_gross_pp(t) * (1.0 - entry_charge_rate())


def total_premium_pp(t):
    """Every gross *versement* of policy year t, scheduled and free."""
    return premium_gross_pp(t) + premium_top_up_gross_pp(t)


def entry_charge(t):
    """The R. 134-3 1° charge taken from the year's *versements*: insurer income."""
    return entry_charge_rate() * total_premium_pp(t)


def parts_added_boy(t):
    """The parts a start-of-year *versement* buys, at the **last struck** part value.

    The *versement* splits under R. 134-2: ``g P_net`` discounted at the last struck
    ``i_pm`` goes to the *provision mathématique* and the remainder buys parts at the last
    struck part value.  On Chassis B nothing goes to the PM, so the whole net *versement*
    buys parts.
    """
    p = prem_after_charge_pp(t)
    if p <= 0.0 or t <= proj_start():
        return 0.0
    u = part_value(t - 1)
    if u <= 0.0:
        return 0.0
    pm_add = guarantee_rate() * p * disc_factor(t - 1) if is_euro_leg() else 0.0
    return (p - pm_add) / u


def parts_added_eoy(t):
    """The parts a free year-end *versement* buys, at the part value **just struck**.

    Paid immediately after the year's striking, so it is priced on ``u(t)`` before the
    top-up rather than on last year's value.  In the worked example the year-3 top-up of
    1 960.00 net splits into ``1 960.00 x 1.0225^-7 = 1,677.31`` of PM and 282.69 of
    diversification provision, buying ``282.69 / 12.8688 = 21.9672`` parts on Chassis A —
    and the whole 1 960.00 buying ``1 960.00 / 11.1193 = 176.2694`` parts on Chassis B.
    """
    p = premium_top_up_net_pp(t)
    if p <= 0.0:
        return 0.0
    u = part_value_at(t, "AFT_STRIKE")
    if u <= 0.0:
        return 0.0
    pm_add = guarantee_rate() * p * disc_factor(t) if is_euro_leg() else 0.0
    return (p - pm_add) / u


def wd_rate_base(t):
    """The table annual partial-surrender rate in policy year t **[std]**.

    6% of the provision in years 1-2 and 3% thereafter; the *mémoire* observes 6% then
    2%-4%.  Policy years beyond the table take its last row.
    """
    tbl = data.lapse_table()                                         # noqa: F821
    y = min(max(t, int(tbl.index.min())), int(tbl.index.max()))
    return float(tbl.loc[y, "wd_rate"])


def wd_rate(t):
    """The fraction of the provision taken as a *rachat partiel* at the start of year t.

    Nil while the decrements are switched off, inside a non-surrender period, and in the
    *échéance* year itself, where the contract is discharged in full instead.  Expressed
    as a fraction of the provision rather than as a cash amount, because a partial
    surrender takes the same proportion of every element of the engagement — the parts,
    the guaranteed amount and the death-floor base all run down pro rata with it.
    """
    if decrement_basis() == "none" or wd_factor() <= 0.0:
        return 0.0
    if t <= proj_start() or t <= lock_up_years() or t >= proj_len():
        return 0.0
    return min(1.0, wd_factor() * wd_rate_base(t))


def wd_gross_pp(t):
    """W(t): the amount a *rachat partiel* takes out of the provision, before the exit charge."""
    if t <= proj_start():
        return 0.0
    return wd_rate(t) * provision_value(t - 1)


def wd_pp(t):
    """The *rachat partiel* actually paid to the saver, net of the base 6° exit charge.

    An **owner election**, not a claim: the contract stays in force and the engagement
    continues on the reduced parts and the reduced guarantee.  It has its own cash flow
    column for that reason.
    """
    return wd_gross_pp(t) * (1.0 - exit_charge_rate())


def mg_at(t, timing):
    """mg at a point inside policy year t.

    ``"AFT_EXIT"``
        after a *rachat partiel* has run the guarantee down pro rata.

    ``"AFT_PREM"``
        after the start-of-year *versement* has raised it by ``g P_net``.
        This is the amount the year-end striking discounts.

    ``"AFT_TOP_UP"``
        after any free year-end *versement*; the year-end guaranteed amount,
        and the same number as :func:`mg`.
    """
    if timing == "AFT_EXIT":
        return mg(t - 1) * (1.0 - wd_rate(t))
    if timing == "AFT_PREM":
        return mg_at(t, "AFT_EXIT") + guarantee_rate() * prem_after_charge_pp(t)
    if timing == "AFT_TOP_UP":
        return (mg_at(t, "AFT_PREM")
                + guarantee_rate() * premium_top_up_net_pp(t))
    raise ValueError("invalid timing: " + str(timing))


def mg(t):
    """mg(t): the amount guaranteed at the *échéance*, as at the end of policy year t.

    ``g`` times cumulative *versements* **net of the R. 134-3 1° entry charge**, run down
    pro rata to any *rachat partiel*.  It is constant between *versements* in a
    single-policy expected-value projection: full surrenders and deaths remove the policy
    rather than the guarantee, so they reach the cash flows through ``pols_if`` instead.
    """
    if t < proj_start():
        return 0.0
    if t == proj_start():
        if duration_inforce() > 0:
            return mg_init()
        return guarantee_rate() * prem_after_charge_pp(t)
    return mg_at(t, "AFT_TOP_UP")


def cum_prem_net(t):
    """The cumulative net *versements* at the end of policy year t: the death-floor base.

    Equal to ``mg(t) / g`` here, and kept separate because they are different objects: the
    guaranteed amount is a contractual promise at a stated term and this is the base of a
    complementary death guarantee provisioned outside the account.  They coincide only
    because ``g`` is constant.
    """
    if t < proj_start():
        return 0.0
    if t == proj_start():
        if duration_inforce() > 0:
            return cum_prem_net_init()
        return prem_after_charge_pp(t)
    return (cum_prem_net(t - 1) * (1.0 - wd_rate(t))
            + prem_after_charge_pp(t) + premium_top_up_net_pp(t))


def parts_levy(t):
    """L(t): the R. 134-3 base 4° levy, taken at the start of policy year t.

    ``f_p x prov_div(t-1)`` — a levy **in number of parts**, valued at the opening part value.
    Base 3°, a levy on the *encours* of the diversification provision, is available only
    in an auxiliary account holding **no** 1° engagements, and no base permits a levy on
    the *provision mathématique* at all.  On the worked example's Chassis A the year-1
    levy is 15.64; an encours levy on ``pm + pd`` would have been 78.40.
    """
    if t <= proj_start():
        return 0.0
    return parts_charge_rate() * prov_div(t - 1)


def invest_income(t):
    """I(t): the year's financial performance, on the balance after the start-of-year steps."""
    return own_assets_at(t, "AFT_PREM") * asset_return(t)


def perf_levy(t):
    """F(t): the R. 134-3 base 5° levy on **positive** financial performance.

    ``f_perf x max(I(t), 0)`` — nothing at all in a year of negative performance, which is
    why the worked example's year-6 performance levy is zero on both chassis.
    """
    if t <= proj_start():
        return 0.0
    return perf_charge_rate() * max(invest_income(t), 0.0)


def own_assets_at(t, timing):
    """The account assets at a point inside policy year t.

    ``"AFT_LEVY"``
        ``A(t-1)`` less the base 4° parts levy.

    ``"AFT_EXIT"``
        less any *rachat partiel*, taken gross of the exit charge because
        the charge stays in the account.

    ``"AFT_PREM"``
        plus the start-of-year *versement* net of the entry charge.
        **This is the balance the year's return accrues on.**

    ``"AFT_RETURN"``
        after the year's asset return.

    ``"AFT_PERF"``
        after the base 5° performance levy; the balance the two
        provisions are struck against.

    ``"AFT_TOP_UP"``
        plus any free year-end *versement*; the year-end assets, and the
        same number as :func:`own_assets`.

    The steps are exposed individually because their order is fixed by R. 134-4 and
    R. 134-12 III — asset affectations completing the representation are made on the dates
    the participation account is struck, after its balance has been allocated — rather
    than being arithmetic convenience.
    """
    if timing == "AFT_LEVY":
        return own_assets(t - 1) - parts_levy(t)
    if timing == "AFT_EXIT":
        return own_assets_at(t, "AFT_LEVY") - wd_gross_pp(t)
    if timing == "AFT_PREM":
        return own_assets_at(t, "AFT_EXIT") + prem_after_charge_pp(t)
    if timing == "AFT_RETURN":
        return own_assets_at(t, "AFT_PREM") * (1.0 + asset_return(t))
    if timing == "AFT_PERF":
        return own_assets_at(t, "AFT_RETURN") - perf_levy(t)
    if timing == "AFT_TOP_UP":
        return own_assets_at(t, "AFT_PERF") + premium_top_up_net_pp(t)
    raise ValueError("invalid timing: " + str(timing))


def own_assets(t):
    """A(t): the auxiliary-account assets attributable to the policy at the end of year t.

    At realisation value (R. 134-8) and **excluding** any outstanding L. 134-3
    contribution, which is the insurer's capital and not the savers' money.  That
    exclusion is the point of the cells: :func:`own_assets_at` rolls forward from ``A(t-1)``
    and never from ``pm(t-1) + prov_div(t-1)``, so the contribution earns nothing for the savers.
    In the worked example the year-7 roll starts from 10,250.65, not from the 12,384.73 the
    contract would have surrendered for.
    """
    if t < proj_start():
        return 0.0
    if t == proj_start():
        if duration_inforce() > 0:
            return own_assets_init()
        return prem_after_charge_pp(t)
    return own_assets_at(t, "AFT_TOP_UP")


def parts_at(t, timing):
    """The number of parts at a point inside policy year t.

    ``"AFT_LEVY"``
        ``N(t-1)(1 - f_p)`` after the base 4° levy, which cancels parts
        rather than reducing their value.

    ``"AFT_EXIT"``
        after a *rachat partiel* has cancelled its pro-rata share.

    ``"AFT_PREM"``
        plus the parts a start-of-year *versement* bought.
        **This is the count the year-end striking divides by.**

    ``"AFT_TOP_UP"``
        plus the parts a free year-end *versement* bought at the just
        struck part value; the year-end count, and the same number as
        :func:`parts`.
    """
    if timing == "AFT_LEVY":
        return parts(t - 1) * (1.0 - parts_charge_rate())
    if timing == "AFT_EXIT":
        return parts_at(t, "AFT_LEVY") * (1.0 - wd_rate(t))
    if timing == "AFT_PREM":
        return parts_at(t, "AFT_EXIT") + parts_added_boy(t)
    if timing == "AFT_TOP_UP":
        return parts_at(t, "AFT_PREM") + parts_added_eoy(t)
    raise ValueError("invalid timing: " + str(timing))


def parts(t):
    """N(t): the number of *parts de provision de diversification* at the end of year t.

    The saver's rights are expressed in a **number of parts**, and R. 134-2 makes the
    insurer's commitment the number and not the value.  On the worked example the count
    closes on ``212.8127 x 0.992^7 = 201.1774``: seven years of the base 4° levy and
    nothing else.
    """
    if t < proj_start():
        return 0.0
    if t == proj_start():
        if duration_inforce() > 0:
            return parts_init()
        u = part_value_init()
        return max(own_assets(t) - pm(t), 0.0) / u if u > 0.0 else 0.0
    return parts_at(t, "AFT_TOP_UP")


def pm_at(t, timing):
    """The *provision mathématique* at the year-end striking, before and after a top-up.

    ``"AFT_STRIKE"``
        the guaranteed amount as it stands after the start-of-year steps,
        discounted at the current ``i_pm``.

    ``"AFT_TOP_UP"``
        the same after any free year-end *versement*; the year-end PM, and
        the same number as :func:`pm`.

    Identically zero on Chassis B, where the guarantee is not provisioned inside the
    account at all.
    """
    if not is_euro_leg():
        return 0.0
    if timing == "AFT_STRIKE":
        return mg_at(t, "AFT_PREM") * disc_factor(t)
    if timing == "AFT_TOP_UP":
        return mg_at(t, "AFT_TOP_UP") * disc_factor(t)
    raise ValueError("invalid timing: " + str(timing))


def pm(t):
    """pm(t): the *provision mathématique* at the end of policy year t.

    ``mg(t) (1 + i_pm(t))^-(n-t)`` on Chassis A and identically zero on Chassis B
    (R. 134-2).  **Re-struck every year, never accumulated.**  Rolling ``pm(t-1)`` forward
    at last year's rate removes the rate effect: in the worked example that is +587.44 of
    the +824.18 year-6 move, against a time effect of +236.74.

    At ``t = n`` the discount factor is 1, so ``pm(n) = mg(n)`` identically and the
    Chassis A guarantee is pre-funded by construction.
    """
    if t < proj_start() or not is_euro_leg():
        return 0.0
    if t == proj_start():
        return mg(t) * disc_factor(t)
    return pm_at(t, "AFT_TOP_UP")


def prov_div_at(t, timing):
    """The *provision de diversification* at the year-end striking, before and after a top-up.

    The **residual** of the account's assets over the *provision mathématique*, floored at
    the parts' minimum value: R. 134-4 permits a debit balance to reduce the part value
    only within the limit of its minimum.  Where the floor binds the two provisions
    together exceed the assets, and the excess is exactly the L. 134-3 contribution.
    """
    if timing == "AFT_STRIKE":
        return max(own_assets_at(t, "AFT_PERF") - pm_at(t, "AFT_STRIKE"),
                   parts_at(t, "AFT_PREM") * min_part_value())
    if timing == "AFT_TOP_UP":
        return max(own_assets_at(t, "AFT_TOP_UP") - pm_at(t, "AFT_TOP_UP"),
                   parts_at(t, "AFT_TOP_UP") * min_part_value())
    raise ValueError("invalid timing: " + str(timing))


def prov_div(t):
    """prov_div(t): the *provision de diversification* at the end of policy year t.

    The savers' individualised rights (R. 343-3 9°), and the only part of the engagement
    that bears investment risk.  On the worked example's year-6 shock the raw residual on
    Chassis A is ``10,250.65 - 11,346.00 = -1,095.35`` and the floor binds instead at
    ``207.7460 x 5.0000 = 1,038.73``.
    """
    if t < proj_start():
        return 0.0
    if t == proj_start():
        if duration_inforce() > 0:
            return max(own_assets(t) - pm(t), parts(t) * min_part_value())
        return max(own_assets(t) - pm(t), 0.0)
    return prov_div_at(t, "AFT_TOP_UP")


def part_value_at(t, timing):
    """The *valeur de la part* at the year-end striking, before and after a top-up.

    ``"AFT_STRIKE"`` is what a free year-end *versement* buys parts at.
    """
    if timing == "AFT_STRIKE":
        n_t = parts_at(t, "AFT_PREM")
        return prov_div_at(t, "AFT_STRIKE") / n_t if n_t > 0.0 else 0.0
    if timing == "AFT_TOP_UP":
        n_t = parts_at(t, "AFT_TOP_UP")
        return prov_div_at(t, "AFT_TOP_UP") / n_t if n_t > 0.0 else 0.0
    raise ValueError("invalid timing: " + str(timing))


def part_value(t):
    """u(t): the *valeur de la part* at the end of policy year t, ``prov_div(t) / N(t)``.

    **Common to every engagement of the auxiliary account** (R. 134-2), so savers with
    different maturities and different guarantee levels in one account earn the same rate;
    differentiation is possible only through the number of parts or through a
    differentiated PCDD distribution.  A per-policy model can only approximate that — the
    shipped model points are separate accounts, and their part values diverge as separate
    accounts' would.
    """
    if t < proj_start():
        return 0.0
    if t == proj_start():
        n_t = parts(t)
        return prov_div(t) / n_t if n_t > 0.0 else part_value_init()
    return part_value_at(t, "AFT_TOP_UP")


def provision_value(t):
    """``pm(t) + prov_div(t)``: the base of the R. 134-5 and R. 134-6 values.

    One expression on both chassis, because ``pm`` is identically zero on Chassis B.  It
    equals ``pm(t) + N(t) u(t)``, which is how the articles write it.
    """
    return pm(t) + prov_div(t)


def insurer_contribution(t):
    """C(t): the outstanding L. 134-3 contribution completing the representation.

    ``max(pm(t) + prov_div(t) - A(t), 0)``, and nil on Chassis B, where the shortfall against the
    guarantee is carried as a PGT instead.  It is the insurer's capital: it carries **no
    return to the savers** and is releasable as soon as the account's own assets cover the
    two provisions.  The surrender value exceeds the account's own assets by exactly this
    amount while it is outstanding — 2,134.08 on the worked example's year-6 shock.
    """
    if not is_euro_leg():
        return 0.0
    return max(provision_value(t) - own_assets(t), 0.0)


def apport(t):
    """The R. 134-12 *apport d'actifs* made at the end of policy year t.

    Capped at 10% of the diversification provision by the article.  It enters the account
    at realisation value and **endows the PCDD**; it is never credited to ``prov_div``, so it
    changes no policyholder value by one cent.  On the worked example's Chassis B a
    statutory-maximum *apport* at ``t = 6`` is 989.92 and cuts the PGT from 1,446.78 to
    456.86.
    """
    if t <= proj_start() or t != apport_year():
        return 0.0
    return min(apport_rate(), apport_cap) * prov_div(t)                    # noqa: F821


def pcdd(t):
    """D(t): the *provision collective de diversification différée* (R. 343-3 10°).

    Collective, with no individual rights, and released into the participation account
    within fifteen years (A. 132-16) — against eight for a euro fund's *provision pour
    participation aux bénéfices*.  This model accumulates the *apport d'actifs* into it and
    nothing else: the *mémoire*'s piloting rule, which runs the fund at 30 bp above the
    insurer's own euro fund and carries the rest here, is a fund-level discretion a
    single-policy model cannot express, and holding it at zero **understates the smoothing
    the real product delivers**.
    """
    if t < proj_start():
        return 0.0
    if t == proj_start():
        return 0.0
    return pcdd(t - 1) + apport(t)


def pgt(t):
    """G(t): the *provision pour garantie à terme* (A. 134-2, R. 343-3 11°).

    ``max(mg(t) (1 + i_pm(t))^-(n-t) - prov_div(t) - D(t), 0)`` on Chassis B and nil on Chassis A.
    Funded from the **insurer's own funds** and held **outside** the participation account,
    on a deliberately narrow basis: the A. 132-18 mortality tables at a rate at most 90% of
    the TEC, counting **no cash flows other than guarantee maturities and mortality**.  A
    model must not "improve" that basis by adding lapses or expenses to it, and must not
    let the provision reach a benefit or feed the profit-sharing computation.

    **Mortality, one of the article's two admitted drivers, is not implemented [std].**  The
    present value above applies no survival factor, so it is the amount for a guarantee
    certain to be reached: prudent, since it overstates the provision, and invisible on the
    worked example, where ``mort_rate`` is zero.  It is live on the decrement-bearing cells —
    on model point 6 at ``t`` = 7 this returns 2,739.35 against 2,477.36 with the five-year
    survival factor 0.972660 the shipped table gives.  In a single-policy model the decrement
    reaches the projection through ``pols_if`` in :func:`result_cf` instead; a fund-level
    implementation should carry the survival factor inside the present value, summed over the
    account's 2° engagements.
    """
    if is_euro_leg():
        return 0.0
    return max(mg(t) * disc_factor(t) - prov_div(t) - pcdd(t), 0.0)


def gate_revalue_ok(t):
    """Whether both A. 134-3 tests permit revaluing the guarantees out of the account.

    Test 1: the diversification provision exceeds 1.5 times the excess of the guaranteed
    amounts over the *provision mathématique*.  Test 2: the diversification provision less
    the parts at their minimum value exceeds 10% of the *provision mathématique*.  **Both**
    must pass.  Informational here — the reference credit-balance route raises the part
    value instead — but computed, because a model that revalued guarantees without testing
    the gates would be exercising a discretion the article does not allow.  On the worked
    example both pass at ``t`` = 5 and the second fails at ``t`` = 6, where the part-value
    floor has taken the headroom to nil.
    """
    if not is_euro_leg():
        return False
    t1 = prov_div(t) > revalue_gate1_factor * max(mg(t) - pm(t), 0.0)      # noqa: F821
    t2 = (prov_div(t) - parts(t) * min_part_value()
          > revalue_gate2_factor * pm(t))                            # noqa: F821
    return bool(t1 and t2)


def conversion_headroom(t):
    """The parts convertible into *provision mathématique* under A. 134-4.

    The article requires the diversification provision, net of the conversion and of the
    parts at their minimum value, to remain at least 15% of the resulting PM, and imposes
    a five-year cooling period besides.  Solving ``pd - C - N u_min = 0.15 (pm + C)`` gives
    ``C = (pd - N u_min - 0.15 pm) / 1.15`` — 474.52 on the worked example at ``t`` = 5.
    Computed, never exercised: the conversion is out of scope, and the 0.50% *frais de
    conversion* the market shows would take 2.37 of that.
    """
    if not is_euro_leg():
        return 0.0
    room = (prov_div(t) - parts(t) * min_part_value()
            - conv_headroom_rate * pm(t))                            # noqa: F821
    return max(room / (1.0 + conv_headroom_rate), 0.0)               # noqa: F821


def surrender_indemnity(t):
    """The R. 132-5-3 *indemnité de rachat* applying to a full surrender in year t.

    The article caps the indemnity at 5% of the present value of the mutual engagements
    (20% or 10% in narrow unlisted-asset cases) and **permits** the contract to provide for
    no indemnity at all once it has been in force more than ten years.  That is a
    permission, not a prohibition: the article does not forbid an indemnity beyond ten
    years.  The reference contract charges none at any duration, and this model returns zero
    beyond ``indemnity_max_years`` unconditionally, which is the permission taken up **[std]**
    rather than the article applied.
    """
    if t > indemnity_max_years:                                      # noqa: F821
        return 0.0
    return min(surrender_indemnity_rate(), indemnity_cap)            # noqa: F821


def surrender_value(t):
    """The R. 134-5 *valeur de rachat* at the end of policy year t.

    ``pm(t) + N(t) u(t)`` on Chassis A and ``N(t) u(t)`` on Chassis B, less the base 6°
    exit charge and any surrender indemnity.

    **There is no guarantee in it before the *échéance*.**  On the worked example's year-6
    shock Chassis A surrenders for 12,384.73 — 105.31% of net *versements*, because its
    *provision mathématique* has already been marked up by the fall in rates — while
    Chassis B surrenders for 9,899.22, **84.18%**, against a guarantee of 11,760.00 that
    does not apply.  A model that floors this at ``g`` times premiums, or at the discounted
    guarantee, is modelling a contract that does not exist.

    A real surrender is priced on a **forward** part value — the next striking, or the next
    monthly intermediate value under A. 134-5.  On an annual grid it is priced on the
    year-end striking, a recorded simplification.
    """
    return (provision_value(t) * (1.0 - exit_charge_rate())
            * (1.0 - surrender_indemnity(t)))


def death_value(t):
    """The current provision value, which is what a death before the *échéance* pays.

    Chapter IV contains **no death valuation article**, so the death benefit is the value
    of the engagement and the maturity guarantee does not apply.  No exit charge: the base
    6° charge is on amounts the saver elects to take out.
    """
    return provision_value(t)


def death_payout(t):
    """The death benefit actually paid, after any *garantie décès plancher*.

    ``max(death_value(t), cum_prem_net(t))`` where the model point carries the rider.  The
    floor is a **complementary guarantee provisioned outside the auxiliary account**
    (R. 134-7), not the maturity guarantee arriving early: it happens to equal ``mg`` here
    only because ``g`` is 100%, and at ``g`` = 80% the two would differ.
    """
    if death_floor_flag():
        return max(death_value(t), cum_prem_net(t))
    return death_value(t)


def rider_claim_pp(t):
    """The part of the death benefit the *garantie décès plancher* funds, per claim.

    ``death_payout(t) - death_value(t)`` — 1,860.78 on the worked example's year-6 Chassis B
    death.  Reported apart from the auxiliary-account columns because it is not the
    account's money: R. 134-7 puts complementary guarantees outside it.
    """
    return death_payout(t) - death_value(t)


def maturity_value(t):
    """The R. 134-6 amount payable at the *échéance*; nil at every other t.

    ``pm(n) + N(n) u(n)`` on Chassis A — **more** than the guarantee whenever the parts
    retain any value, 12,765.89 against 11,760.00 in the worked example — and
    ``max(N(n) u(n), mg(n))`` on Chassis B.  The ``max`` exists **only at ``t = n``** and
    **only on Chassis B**; applying it earlier, or on Chassis A at all, invents a guarantee
    the contract does not give.

    The statutory default at the *échéance* is in fact an arbitrage into an SRI <= 2
    support unless the holder decides otherwise (A. 134-6); this model pays the amount out
    and stops, and a "roll into a low-risk support" variant is the natural extension.
    """
    if t != proj_len():
        return 0.0
    if is_euro_leg():
        return provision_value(t)
    return max(provision_value(t), mg(t))


def claim_pp(t, kind):
    """The payout per claim in policy year t, by kind.

    ``"DEATH"``
        :func:`death_payout` — the current provision value, floored at
        cumulative net *versements* where the rider is carried.

    ``"LAPSE"``
        :func:`surrender_value` — the R. 134-5 value, with **no**
        guarantee before the *échéance*.

    ``"MATURITY"``
        :func:`maturity_value` at ``t = n`` and nil elsewhere.
    """
    if kind == "DEATH":
        return death_payout(t)
    if kind == "LAPSE":
        return surrender_value(t)
    if kind == "MATURITY":
        return maturity_value(t)
    raise ValueError("invalid kind: " + str(kind))


def mort_rate(t):
    """q(x+t): the annual best-estimate mortality rate for policy year t **[std]**.

    The shipped table rate times ``mort_be_factor``.  Both are placeholders: the
    homologated tables TH 00-02 / TF 00-02 are cited by arrêté and never shipped, A. 132-18
    permits an insurer's own certified table besides, and the proxy is INSEE-shaped
    population mortality with a factor for insured lives being lighter than the population.
    Nil where the model point switches the decrements off, which is the worked example's
    configuration.
    """
    if decrement_basis() == "none" or t <= proj_start():
        return 0.0
    x = min(age(t), omega_age)                                       # noqa: F821
    return min(1.0, float(data.mort_table().loc[                     # noqa: F821
        (sex(), x), "mort_rate"]) * mort_be_factor)                  # noqa: F821


def lapse_rate_base(t):
    """The table annual full-surrender (*rachat total*) rate in policy year t **[std]**.

    2.5% p.a. level; the *mémoire* observes 2%-3%.  Policy years beyond the table take its
    last row.
    """
    tbl = data.lapse_table()                                         # noqa: F821
    y = min(max(t, int(tbl.index.min())), int(tbl.index.max()))
    return float(tbl.loc[y, "lapse_rate"])


def guarantee_imminent(t):
    """0.5 in the two years before the *échéance* on Chassis B, while the guarantee bites.

    The gate matters.  A saver who surrenders a 2° engagement gives up the **entire**
    guarantee (R. 134-5), so the deterrent exists precisely while ``N u < mg`` and is worth
    nothing otherwise; applying it unconditionally would invent behaviour where there is
    none.  This is the strongest exit deterrent the product creates, and it is **[std]** —
    no eurocroissance lapse experience is public.
    """
    if is_euro_leg() or proj_len() - t > guarantee_imminent_years:    # noqa: F821
        return 1.0
    if parts(t) * part_value(t) < mg(t):
        return guarantee_imminent_factor                             # noqa: F821
    return 1.0


def duration8_spike(t):
    """1.5 in policy year 8 where ``n > 8`` **[std]**.

    The assurance-vie annual *abattement* becomes available at eight years, so surrender
    incentive spikes there — and only where the contract still has years to run, since a
    contract maturing at eight has no such choice to make.
    """
    if t == duration8_year and proj_len() > duration8_year:          # noqa: F821
        return duration8_factor                                      # noqa: F821
    return 1.0


def lapse_rate(t):
    """w(t): the annual full-surrender rate applied at the end of policy year t.

    The table rate times both behavioural overlays, capped at 1.  Nil while the decrements
    are switched off, inside a non-surrender period, and in the *échéance* year, where the
    survivors take the maturity amount instead — the base run assumes 100% of them do,
    as the *mémoire* also assumes.
    """
    if decrement_basis() == "none":
        return 0.0
    if t <= proj_start() or t <= lock_up_years() or t >= proj_len():
        return 0.0
    return min(1.0, lapse_rate_base(t) * guarantee_imminent(t)
               * duration8_spike(t))


def pols_if_at(t, timing):
    """The number of policies in force at a point inside policy year t.

    ``"BEF_DECR"``
        the start of the year, before any decrement — and the exposure
        every cash flow of the year is weighted by; :func:`pols_if`.

    ``"BEF_LAPSE"``
        after deaths, before surrenders: the processing order is death
        before surrender **[std]**.

    ``"AFT_DECR"``
        the notes' ``l(t)``: the end-of-year count, and zero in the
        *échéance* year, where the survivors mature.  This is the timing
        the end-of-period quantity is reached through, because the bare
        name ``pols_if`` belongs to the start-of-period count.
    """
    if timing == "BEF_DECR":
        if t < proj_start():
            return 0.0
        if t == proj_start():
            return pols_if_init()
        return pols_if_at(t - 1, "AFT_DECR")
    if timing == "BEF_LAPSE":
        return pols_if_at(t, "BEF_DECR") * (1.0 - mort_rate(t))
    if timing == "AFT_DECR":
        if t >= proj_len():
            return 0.0
        return pols_if_at(t, "BEF_LAPSE") * (1.0 - lapse_rate(t))
    raise ValueError("invalid timing: " + str(timing))


def pols_if(t):
    """The number of policies in force at the **start** of policy year t.

    This is the library's shared vocabulary: ``pols_if(t)`` is the exposure at the start of
    period t and the weight on that same :func:`result_cf` row's cash flows, so the opening
    row is ``pols_if_init()`` exactly — no decrement has been applied when a year opens.

    The notes' ``l(t)`` is the **end**-of-year count, with ``l(0) = 1`` and nil on the
    *échéance* row because everyone has matured by the end of it.  That quantity is
    unchanged and is reached as ``pols_if_at(t, "AFT_DECR")``; it is no longer published
    under this name, because doing so put the exposure column one year ahead of the flows
    printed beside it.
    """
    if t < proj_start() or t > proj_len():
        return 0.0
    return pols_if_at(t, "BEF_DECR")


def pols_death(t):
    """Deaths in policy year t, against the start-of-year in force."""
    if t <= proj_start():
        return 0.0
    return pols_if_at(t, "BEF_DECR") * mort_rate(t)


def pols_lapse(t):
    """Full surrenders at the end of policy year t, from the survivors of mortality."""
    if t <= proj_start():
        return 0.0
    return pols_if_at(t, "BEF_LAPSE") * lapse_rate(t)


def pols_maturity(t):
    """Survivors reaching the *échéance*; nil at every other t.

    The base run assumes 100% of them take the maturity amount **[std]**, as the *mémoire*
    also assumes; it notes that modelling annuitisation or reinvestment instead could
    amplify or damp its results.
    """
    if t != proj_len():
        return 0.0
    return pols_if_at(t, "BEF_LAPSE")


def premiums(t):
    """*Versement* income in policy year t, an inflow.

    Both the scheduled start-of-year *versement* and any free year-end one, gross of the
    entry charge — the charge is reported as insurer income in :func:`charges_taken`
    rather than netted out of the premium line.
    """
    return total_premium_pp(t) * pols_if_at(t, "BEF_DECR")


def withdrawals(t):
    """*Rachats partiels* paid at the start of policy year t.

    An **owner election** rather than a claim, which is why it has its own name and column:
    the contract stays in force and continues on the reduced parts and reduced guarantee.
    """
    return wd_pp(t) * pols_if_at(t, "BEF_DECR")


def claims(t, kind=None):
    """Benefit outgo in policy year t, by kind; the total when kind is omitted.

    ``"DEATH"``, ``"LAPSE"`` and ``"MATURITY"`` weight :func:`claim_pp` by the
    corresponding decrement.  The death line **includes** the *garantie décès plancher*'s
    contribution, which :func:`rider_claims` reports separately; it is a decomposition of
    this column and not a fourth kind.
    """
    if kind is None:
        return sum(claims(t, k) for k in ("DEATH", "LAPSE", "MATURITY"))
    if kind == "DEATH":
        return claim_pp(t, "DEATH") * pols_death(t)
    if kind == "LAPSE":
        return claim_pp(t, "LAPSE") * pols_lapse(t)
    if kind == "MATURITY":
        return claim_pp(t, "MATURITY") * pols_maturity(t)
    raise ValueError("invalid kind: " + str(kind))


def rider_claims(t):
    """The *garantie décès plancher*'s share of the year's death outgo.

    A memo line: it is **already inside** ``claims_death``, and it is published apart
    because R. 134-7 puts complementary guarantees outside the auxiliary account, so it is
    not paid out of the savers' provisions.
    """
    return rider_claim_pp(t) * pols_death(t)


def expenses(t):
    """E(t): the insurer's own expenses in policy year t **[std]**.

    Acquisition at 5% of *versements* plus an acquisition commission of 2% of the initial
    one, and maintenance at 0.20% p.a. of the two provisions.  All three levels come from
    the published *mémoire*, which is the only complete public parameterisation of this
    product.  They are the insurer's costs, not charges to the saver: the charges the
    contract permits are the six R. 134-3 bases, reported in :func:`charges_taken`.

    The two acquisition components are weighted by the start-of-year exposure like every
    other flow; the maintenance component is weighted by ``pols_if_at(t, "AFT_DECR")``,
    the survivors still on the books when the provisions are struck at year end.
    """
    acq = expense_acq_rate * total_premium_pp(t)                     # noqa: F821
    if t == proj_start() and duration_inforce() == 0:
        acq += expense_comm_rate * premium_gross_init()              # noqa: F821
    return (acq * pols_if_at(t, "BEF_DECR")
            + expense_maint_rate * provision_value(t)                # noqa: F821
            * pols_if_at(t, "AFT_DECR"))


def charges_taken(t):
    """The R. 134-3 charges the insurer takes in policy year t: income, reported apart.

    The base 4° parts levy, the base 5° performance levy, the base 1° entry charge and the
    base 6° exit charge together with any surrender indemnity.  They are **not** in
    ``net_cf``: they are transfers inside the account from the savers' provisions to the
    insurer, and the benefits they reduce are already net of them.  Publishing them beside
    the flows is what makes the charge structure auditable against R. 134-3.
    """
    inside = (parts_levy(t) + perf_levy(t) + entry_charge(t)
              + (wd_gross_pp(t) - wd_pp(t)))
    on_surr = (provision_value(t) - surrender_value(t)) * pols_lapse(t)
    return inside * pols_if_at(t, "BEF_DECR") + on_surr


def liability_cf(t):
    """CF(t): the year's liability cash flow, **outgo positive**, as the notes print it.

    Claims and *rachats partiels* and expenses out, *versements* in.  The two provisions
    appear nowhere in it — they are state variables, not cash flows — and neither do the
    insurer's own-funds items, which are capital rather than benefit.
    """
    return (claims(t) + withdrawals(t) + expenses(t) - premiums(t))


def net_cf(t):
    """The net cash flow of policy year t, **income positive**: ``-liability_cf(t)``.

    The library's sign convention, so that ``result_cf()["net_cf"]`` can be compared and
    summed across products without checking which one it came from.
    """
    return -liability_cf(t)


def check_assets_roll_fwd_resid(t):
    """The account-asset recursion residual in policy year t; zero everywhere.

    ``A(t) - {[A(t-1) - f_p prov_div(t-1) - W(t) + P_net(t)](1 + r) - f_perf max(I, 0) + top-up}``,
    rebuilt in **one expression** rather than through :func:`own_assets_at`, so that a
    mis-ordered step shows up here: a parts levy taken after the return instead of before
    it, a *versement* credited after the return rather than at the start of the year, or a
    performance levy struck on the wrong balance.
    """
    if t <= proj_start():
        return 0.0
    base = (own_assets(t - 1) - parts_charge_rate() * prov_div(t - 1)
            - wd_rate(t) * provision_value(t - 1) + prem_after_charge_pp(t))
    built = (base * (1.0 + asset_return(t))
             - perf_charge_rate() * max(base * asset_return(t), 0.0)
             + premium_top_up_net_pp(t))
    return own_assets(t) - built


def check_assets_roll_fwd():
    """True when the account-asset recursion closes in every projected year."""
    return all(abs(check_assets_roll_fwd_resid(t)) <= roll_fwd_tol   # noqa: F821
               for t in range(proj_start(), proj_len() + 1))


def check_parts_roll_fwd_resid(t):
    """The parts recursion residual in policy year t; zero everywhere.

    ``N(t) - {N(t-1)(1 - f_p)(1 - w_partial) + parts bought at BOY + parts bought at EOY}``,
    rebuilt in one expression.  The base 4° levy cancels parts rather than reducing their
    value, so a levy applied to the part value instead of to the count would leave the
    count unchanged and show up here; so would a *versement* priced at the wrong striking.
    On the worked example the count closes on ``212.8127 x 0.992^7 = 201.1774``.
    """
    if t <= proj_start():
        return 0.0
    built = (parts(t - 1) * (1.0 - parts_charge_rate()) * (1.0 - wd_rate(t))
             + parts_added_boy(t) + parts_added_eoy(t))
    return parts(t) - built


def check_parts_roll_fwd():
    """True when the parts recursion closes in every projected year."""
    return all(abs(check_parts_roll_fwd_resid(t)) <= roll_fwd_tol    # noqa: F821
               for t in range(proj_start(), proj_len() + 1))


def check_guarantee_roll_fwd_resid(t):
    """The guaranteed-amount recursion residual in policy year t; zero everywhere.

    ``mg(t) - {mg(t-1)(1 - w_partial) + g x net versements of the year}``, rebuilt in one
    expression.  It is the check that catches the guarantee being computed on **gross**
    *versements*: with a 2.00% entry charge, ``mg`` after the worked example's year-3
    top-up is 11,760.00 and not 12,000.00, and a model that used the gross figure would
    fail here in the year the top-up is paid rather than silently over-guaranteeing for
    seven years.
    """
    if t <= proj_start():
        return 0.0
    built = (mg(t - 1) * (1.0 - wd_rate(t))
             + guarantee_rate() * (prem_after_charge_pp(t) + premium_top_up_net_pp(t)))
    return mg(t) - built


def check_guarantee_roll_fwd():
    """True when the guaranteed-amount recursion closes in every projected year."""
    return all(abs(check_guarantee_roll_fwd_resid(t)) <= roll_fwd_tol  # noqa: F821
               for t in range(proj_start(), proj_len() + 1))


def check_pols_roll_fwd_resid(t):
    """The in-force roll-forward residual in policy year t; zero everywhere.

    The year opens at ``pols_if(t)`` and closes at ``pols_if_at(t, "AFT_DECR")``, the
    notes' ``l(t)``; the difference is the year's deaths, full surrenders and maturities.
    """
    if t < proj_start():
        return 0.0
    return (pols_if(t) - pols_if_at(t, "AFT_DECR") - pols_death(t)
            - pols_lapse(t) - pols_maturity(t))


def check_pols_roll_fwd():
    """True when the in-force roll-forward closes in every projected year."""
    return all(abs(check_pols_roll_fwd_resid(t))
               <= roll_fwd_tol * max(pols_if_init(), 1.0)            # noqa: F821
               for t in range(proj_start(), proj_len() + 1))


def check_guarantee_funding_resid(t):
    """``pm(t)`` accumulated to the *échéance* less the guaranteed amount; zero on Chassis A.

    This is the model's headline identity: the *provision mathématique* accumulated at the
    regulated rate reaches the guarantee **exactly** at the *échéance*, so
    ``pm(t)(1 + i_pm(t))^(n-t) = mg(t)`` at every t and ``pm(n) = mg(n)``.

    It is zero by construction under R. 134-2's re-strike rule, and that is the point of
    publishing it: an implementation that **accumulates** the PM instead — rolling
    ``pm(t-1)`` forward at last year's rate — breaks it the first year the rate moves.  On
    the worked example's path ``pm(5) x 1.0225 = 10,758.56`` against the 11,346.00 the
    re-strike gives, and the 587.44 difference is the rate effect it has silently dropped.

    Identically zero on Chassis B, where **both sides are nil**: a 2° engagement funds
    nothing inside the account against its guarantee, which is exactly why an early
    *rachat* there can pay less than the guaranteed amount.  The Chassis B funding
    statement is :func:`check_pgt_covers_guarantee` instead.
    """
    if not is_euro_leg():
        return 0.0
    return pm(t) * (1.0 + i_pm(t)) ** (proj_len() - t) - mg(t)


def check_guarantee_funding():
    """True when the *provision mathématique* funds the guarantee exactly, at every t."""
    return all(abs(check_guarantee_funding_resid(t)) <= funding_tol  # noqa: F821
               for t in range(proj_start(), proj_len() + 1))


def check_pgt_covers_guarantee_resid(t):
    """``pd + G + D`` less the discounted guarantee on Chassis B; non-negative everywhere.

    A. 134-2 makes the PGT the shortfall of the diversification provision and the PCDD
    against the discounted guarantees, floored at zero, so the three together always cover
    it — exactly where the PGT is positive and with a surplus where it is not.  It is the
    Chassis B counterpart of :func:`check_guarantee_funding`, and what it asserts is that
    the guarantee is funded **somewhere**: on the savers' side before a shock, and out of
    the insurer's own funds after one.

    Identically zero on Chassis A, which constitutes no PGT: there the L. 134-3
    contribution plays the analogous role and :func:`insurer_contribution` carries it.
    """
    if is_euro_leg():
        return 0.0
    return prov_div(t) + pgt(t) + pcdd(t) - mg(t) * disc_factor(t)


def check_pgt_covers_guarantee():
    """True when the diversification provision and the own-funds provisions cover the guarantee."""
    return all(check_pgt_covers_guarantee_resid(t) >= -funding_tol   # noqa: F821
               for t in range(proj_start(), proj_len() + 1))


def check_part_value_floor_resid(t):
    """``u(t) - u_min``: how far the part value sits above its contractual floor.

    Non-negative everywhere.  R. 134-4 permits a debit balance on the participation account
    to reduce the part value only **within the limit of its minimum**, and an implementation
    that omits the floor takes the worked example's Chassis A diversification provision to
    **-1,095.35** in year 6 — a negative provision, and with it a negative surrender value
    that every downstream number stays plausible enough to read past.
    """
    return part_value(t) - min_part_value()


def check_part_value_floor():
    """True when the part value stays at or above its contractual minimum, every year."""
    return all(check_part_value_floor_resid(t) >= -floor_tol         # noqa: F821
               for t in range(proj_start(), proj_len() + 1))


def check_own_funds_not_paid_resid(t):
    """The excess of the year's largest benefit over the two provisions; non-positive.

    Before the *échéance* every benefit is bounded by ``pm(t) + prov_div(t)``: the surrender value
    is that less charges and the death value is exactly it, the *garantie décès plancher*
    being funded outside the account and excluded here.  Neither the L. 134-3 contribution
    nor the PGT may reach a policyholder, and on the shipped Chassis B cells the PGT is
    positive for four consecutive years, so the check is live rather than decorative: an
    implementation that floored the Chassis B surrender value at the guarantee would pay
    11,760.00 against a bound of 9,899.22 and fail here.

    The residual is zero **at** ``t = n``, and that is not a gap.  The maturity guarantee on
    Chassis B legitimately exceeds the account's provisions, and paying it out of the PGT
    is precisely what the PGT was constituted for.
    """
    if t >= proj_len():
        return 0.0
    return max(surrender_value(t), death_value(t)) - provision_value(t)


def check_own_funds_not_paid():
    """True when no benefit before the *échéance* exceeds the savers' two provisions."""
    return all(check_own_funds_not_paid_resid(t) <= funding_tol      # noqa: F821
               for t in range(proj_start(), proj_len() + 1))


def check_pm_restruck_resid(t):
    """The in-force extract's *provision mathématique* against the re-strike; zero.

    R. 134-2 makes the PM the guaranteed amount discounted at the **current** A. 134-1 rate,
    so an extract cannot supply it independently: this compares what the extract reports
    against what the rule requires, at the valuation date.

    Zero by construction on a new-business cell, where there is no extract to check, and on
    Chassis B, which has no PM at all.  On the in-force cell it is a live cross-check, and
    what it catches is an extract built by **accumulating** the PM from issue rather than
    re-striking it — the same error :func:`check_guarantee_funding` catches inside the
    projection, arriving from the data side instead.
    """
    if (t != proj_start() or duration_inforce() == 0 or not is_euro_leg()):
        return 0.0
    return pm(t) - pm_init()


def check_pm_restruck():
    """True when a shipped in-force *provision mathématique* agrees with R. 134-2."""
    return all(abs(check_pm_restruck_resid(t)) <= inforce_tol        # noqa: F821
               for t in range(proj_start(), proj_len() + 1))


def result_cf():
    """Result table of cashflows, indexed by policy year t.

    ``pols_if`` is the **start**-of-year count, which is the exposure the flows on that same
    row are weighted by; the notes' end-of-year ``l(t)`` is ``pols_if_at(t, "AFT_DECR")``
    and is not published here.  ``charges_taken`` and ``rider_claims`` are
    memo lines outside ``net_cf`` — the first is a transfer inside the account from the
    savers to the insurer, and the second is already inside ``claims_death``.
    """
    ts = list(range(proj_start(), proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "claims_death": [claims(t, "DEATH") for t in ts],
            "claims_lapse": [claims(t, "LAPSE") for t in ts],
            "claims_maturity": [claims(t, "MATURITY") for t in ts],
            "withdrawals": [withdrawals(t) for t in ts],
            "expenses": [expenses(t) for t in ts],
            "charges_taken": [charges_taken(t) for t in ts],
            "rider_claims": [rider_claims(t) for t in ts],
            "liability_cf": [liability_cf(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_provisions():
    """Result table of the provision machinery, indexed by policy year t.

    The account's assets against the two provisions, the parts and their value, and the
    insurer's own-funds items beside them — reported, and never in a benefit.  This is the
    table the notes' two worked-example tables print.
    """
    ts = list(range(proj_start(), proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "i_pm": [i_pm(t) for t in ts],
            "asset_return": [asset_return(t) for t in ts],
            "parts_levy": [parts_levy(t) for t in ts],
            "perf_levy": [perf_levy(t) for t in ts],
            "own_assets": [own_assets(t) for t in ts],
            "mg": [mg(t) for t in ts],
            "pm": [pm(t) for t in ts],
            "prov_div": [prov_div(t) for t in ts],
            "parts": [parts(t) for t in ts],
            "part_value": [part_value(t) for t in ts],
            "insurer_contribution": [insurer_contribution(t) for t in ts],
            "pgt": [pgt(t) for t in ts],
            "pcdd": [pcdd(t) for t in ts],
            "surrender_value": [surrender_value(t) for t in ts],
            "death_payout": [death_payout(t) for t in ts],
            "maturity_value": [maturity_value(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

omega_age = 120

mort_be_factor = 0.8

tec_haircut = 0.9

lock_up_cap = 8

indemnity_cap = 0.05

indemnity_max_years = 10

apport_cap = 0.1

conv_headroom_rate = 0.15

revalue_gate1_factor = 1.5

revalue_gate2_factor = 0.1

guarantee_imminent_factor = 0.5

guarantee_imminent_years = 2

duration8_year = 8

duration8_factor = 1.5

expense_acq_rate = 0.05

expense_comm_rate = 0.02

expense_maint_rate = 0.002

roll_fwd_tol = 1e-08

funding_tol = 1e-07

floor_tol = 1e-09

inforce_tol = 0.005

pd = ("Module", "pandas")
