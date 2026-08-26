# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.PER_FR_A` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the notes' worked example
    >>> Projection[1].result_state()       # the glide path and the two supports
    >>> Projection.point_id = 6            # the cell whose annuity is not commuted

``t`` counts **plan years** from the valuation date, 1-based. ``proj_len()`` is the
declared horizon, ``retirement_age - age(0)``, and the projection stops there: the plan
is liquidated at the horizon and nothing this model projects happens after it.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent directory,
``products/per_assurance/``, read at run time rather than stored inside the model. The
model folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded
values — so a diff of the model shows logic changes only, and an input can be edited or
swapped without rewriting the model. This follows ``annuallife.TradLife_A``; contrast
``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model through modelx's
IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``PER_FR_A`` folder without its parent's CSVs produces a model that reads and then fails
on first evaluation.

Each table has a filename Reference and a reader Cells, both on :mod:`~.PER_FR_A.Data`,
reached here through the ``data`` Reference:

======================  ==================================  ==========================
Reference               Cells                               File
======================  ==================================  ==========================
model_point_file        data.model_point_table()            model_point_table.csv
allocation_grid_file    data.allocation_grid()              allocation_grid.csv
mort_table_file         data.mort_table()                   mort_table.csv
exit_table_file         data.exit_table()                   exit_table.csv
annuity_factor_file     data.annuity_factor_table()         annuity_factor.csv
======================  ==================================  ==========================

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` and ``savings.CashValue_SE``
wherever those models have an analogue — ``pols_*`` for policy counts, ``av_*`` for
account values, plural nouns for cash flows, ``*_rate`` for rates, ``*_pp`` for
per-policy amounts, ``*_at(t, timing)`` for a quantity read at a point inside the year,
``claims(t, kind)`` and ``claim_pp(t, kind)`` with an uppercase ``kind`` string. The
technical notes use compact symbols instead. The mapping is:

=========================  ==================================  ==========================
Notes symbol               Cells                               Meaning
=========================  ==================================  ==========================
(the row of the table)     model_point()                       The selected model point
t                          (the cells argument)                Plan year, 1-based
n                          proj_len()                          The declared horizon
k(t)                       years_to_horizon(t)                 Years to the horizon at BOY
a(t)                       alloc_euro(t)                       Target euro share for year t
1 - a(t)                   alloc_uc(t)                         Target UC share, from the file
(profile)                  allocation_profile()                Which ladder of the grid
x                          age_init()                          Attained age at t = 0
x + t                      age(t)                              Attained age at the end of t
duration_ifo               duration_ifo()                      Completed years at t = 0
duration(t)                duration(t)                         Completed years since V(1)
V                          premium_pp(t)                       Gross versement at BOY
V_net                      prem_to_av_pp(t)                    Versement net of the loading
load                       load_rate                           Entry loading, 2.50%
m(t)                       switch_pp(t)                        Amount switched at the BOY
arb(t)                     arbitrage_charge_pp(t)              Charge on the switch
arb_rate                   arb_rate                            0.30% of the amount switched
E_eu(t)                    av_euro_pp_at(t, "BOY")             Euro balance after the BOY steps
E_uc(t)                    av_uc_pp_at(t, "BOY")               UC balance after the BOY steps
r_eu, r_uc                 return_euro, return_uc              Gross asset returns
c_eu, c_uc                 charge_euro, charge_uc              Management charges
(gross return credited)    inv_income_pp(t)                    Investment return in year t
(charges levied)           mgmt_charge_pp(t)                   Management charge in year t
A(t)                       av_pp(t)                            Account value at EOY t
A-(t) = A(t-1)             av_pp(t - 1)                        Value carried into year t
(the steps)                av_pp_at(t, timing)                 BOY / EOY inside year t
l(t) x A(t)                av_at(t, timing)                    In-force weighted account
g(t)                       death_floor_pp(t)                   Garantie plancher base
(cover in force)           floor_in_force(t)                   False from the 70th birthday
max(A(t), g(t))            death_benefit_pp(t)                 Death benefit, floored
q(t)                       mort_rate(t)                        Annual mortality rate
w_e(t)                     early_release_rate(t)               Deblocage anticipe decrement
w_r(t)                     transfer_out_rate(t)                Transfer-out decrement
iota(t)                    transfer_indemnity_rate(t)          1% while duration < 5
l(t-1)                     pols_if(t)                          In force at the START of year t
l(t)                       pols_if_at(t, "AFT_DECR")           In force at the END of year t
(intra-year l)             pols_if_at(t, timing)               BEF_DECR / BEF_RELEASE /
                                                               BEF_TRANSFER / AFT_DECR
d_death(t)                 pols_death(t)                       Deaths in year t
d_release(t)               pols_release(t)                     Early releases in year t
d_transfer(t)              pols_transfer(t)                    Transfers out in year t
l(n)                       pols_maturity(t)                    Survivors settling at t = n
theta                      annuity_share()                     Share converted to a rente
a_x                        annuity_factor()                    Conversion factor, undiscounted
capital_leg                capital_leg_pp()                    (1 - theta) A(n)
annuity_cap                annuity_cap_pp()                    theta A(n)
rente_gross                rente_gross_pp()                    annuity_cap / a_x
rente_net                  rente_net_pp()                      After the frais d'arrerages
c_arr                      arrear_charge_rate                  1.50% of each instalment
C_thr                      commute_threshold_mth               EUR 110 a month
(the test)                 is_commuted()                       Whether the annuity commutes
commuted                   commuted_pp()                       The commutation lump sum
(instalment)               capital_instalment_pp()             Capital leg / instalments
(payouts)                  claim_pp(t, kind)                   Benefit per policy by kind
(cash flows)               premiums, claims, expenses          Probability-weighted flows
annuity_conversion         annuity_conversion(t)               Capital handed to Rente_FR_S
E(t)                       expenses(t)                         Maintenance expense
CF(t)                      liability_cf(t)                     The notes' outgo-positive CF
(none)                     net_cf(t)                           Its negative, income-positive
=========================  ==================================  ==========================

Five names needed care.

**There is no** ``lapse_rate`` **and there is no** ``claims_lapse``, and that is a
product statement rather than an omission. The house vocabulary reserves those names for
a contractual surrender right, and this contract has none: the accumulation phase carries
no surrender right except in the statutory cases, the plan being blocked until the
L. 224-1 maturity. The two exits are named for what they are —
:func:`early_release_rate` and :func:`transfer_out_rate`, paying
``claims_early_release`` and ``claims_transfer`` — because they are not the same event
and they do not pay the same amount. An early release requires a listed triggering event,
bears **no charge**, may be partial, and has its main-residence limb closed to
compartment 3. A transfer out ends the plan for this insurer but does **not** take the
savings out of the regime: the *blocage*, the compartments and the exit conditions travel
with the money, and it pays a transfer value that differs from the release amount by the
1% indemnity in the first five years. Using one decrement for both, or calling either a
lapse, silently attaches the wrong payment formula to half the exits.

``pols_if(t)`` is the in force at the **start** of plan year ``t``, with
``pols_if(1) = pols_if_init()``, and it is the weight on that same ``result_cf()`` row's
cash flows. This is the library's settled convention, shared with ``MYGA_US_S``,
``WP_UK_A`` and every other model in the four country libraries: divide a flow by its own
row's ``pols_if`` and you get a per-policy amount for the same period.

**The end-of-year count was renamed.** The technical notes index the in-force probability
at the **end** of the year and call it ``l(t)``; every identity in the notes is written
against that indexing, and the notes' worked-example table prints it. It used to be
published here as ``pols_if(t)``, which put the *next* period's exposure on each
``result_cf()`` row while the flows beside it were weighted, correctly, by the period's
own. Nothing raised and nothing went NaN — the failure was silent, and a reader dividing
a cash flow by that row's ``pols_if`` got a one-period-stale exposure. The quantity
survives unchanged as ``pols_if_at(t, "AFT_DECR")``, in the house ``BEF_*`` / ``AFT_DECR``
timing vocabulary of ``savings.CashValue_SE``, and :func:`result_state` publishes it as
the ``pols_if_eoy`` column so that the notes' table can still be read off the model. The
two series are one period apart: ``pols_if_at(t, "AFT_DECR") == pols_if(t + 1)``. No cash
flow changed: the maturity settlement is taken at ``pols_if_at(n, "AFT_DECR")`` and the
*versement* and the expense at ``pols_if(t)``, exactly the counts they were taken at
before.

``switch_pp`` is signed, and the sign decides which balance bears the arbitrage charge,
because the charge is taken from the **source** support in both directions. Under a
de-risking profile ``alloc_euro`` is non-decreasing and the euro support grows more
slowly than the UC bucket, so the switch is positive — UC to euro — in almost every year
of almost every cell. It turns negative where a cell arrives holding **more** euro
support than the grid's minimum asks for, which is what an incoming transfer can do:
model point 2 opens at 40% euro against a 20% minimum nine years out, and its first
rebalancing sells euro down to the grid. See :func:`check_euro_share_min` for what that
direction costs.

``annuity_factor`` is an **undiscounted expected-instalment count**, not a discounted
annuity factor, because a PER tariff may not use a technical rate above 0%. Nothing in
this model discounts it, and :func:`rente_gross_pp` is a plain division. A 2% rate would
shorten the factor to 17.66 and so inflate the annuity — which is ``annuity_cap`` divided
by the factor — by roughly a quarter on the anchor cell, which is the whole reason the
cap exists.

``annuity_conversion`` is an **outgo**, not a memo item. Where the annuity is not
commuted the converted capital leaves this model and is handed to ``Rente_FR_S``, so it
sits inside :func:`liability_cf` alongside the claims. Where it *is* commuted the same
money leaves as ``claims_maturity`` instead, and ``annuity_conversion`` is nil. The two
are mutually exclusive by construction and only one of them is ever non-zero on a cell.

.. rubric:: The glide path is an input table

::

    k(t) = n - t + 1
    a(t) = allocation_grid[allocation_profile, k(t)].euro_share

The *équilibré* ladder is 0% for ``k > 10``, 20% for ``10 >= k > 5``, 50% for
``5 >= k > 2`` and 70% for ``k <= 2``, and **the boundary belongs to the tighter band**
**[std]**. That convention is the model's own. The arrêté's part (a) grid *was* extracted,
percentages and band headings both, but the headings as rendered read "≥ 10 years out"
and "from 10 years out" — which overlap at ``k = 10`` and so do not say which side of a
boundary year belongs to which band. Reading the boundaries the other way understates the
euro share for a full year at each of three transitions. :func:`alloc_euro` reads the file
rather than computing anything, so an insurer ladder on twenty one-year bands, or one of
the other three qualified profiles, substitutes without touching a formula.

"Low risk" is realised wholly as the euro support **[std]**. The definition of *actifs
présentant un profil d'investissement à faible risque* is delegated to an arrêté that was
not retrieved, and the two contract definitions found disagree — SRRI at most 3 against
at most 2 including the euro fund. Realising the bucket as the euro support is the most
conservative reading of both and keeps the model to two supports.

.. rubric:: The rebalancing, and which support pays for it

::

    m(t)   = a(t) A(t-1) - av_euro_pp(t-1)
    arb(t) = arb_rate |m(t)|
    E_eu   = av_euro_pp(t-1) + m(t)          + a(t) V_net           (m >= 0)
    E_uc   = av_uc_pp(t-1)   - m(t) - arb(t) + (1 - a(t)) V_net

with the roles of the two supports exchanged when ``m(t) < 0``. Two conventions, both
**[std]** and both load-bearing.

The arbitrage charge is taken from the **source** support, so the destination receives
the full switch and, on a de-risking switch, the post-rebalancing euro share lands at or
just above the regulatory minimum rather than just below it. On the anchor cell's year-8
band crossing the BOY euro share is 50.04% against a 50% target, and taking the charge
from the destination instead would put it under, at every crossing, by the charge.

The two halves of that sentence come apart on a **reverse** switch, and the notes do not
say which half wins. Where the euro support is the source, charging the source leaves the
share below the minimum by ``(1 - a) arb`` — 9.60 on 19 988 for model point 2, which is
0.05% of the balance. This model implements the notes' formula literally, symmetric in
the two supports, rather than quietly charging the UC side in both directions to keep the
share above the line; :func:`check_euro_share_min` therefore asserts the property that is
actually true, direction by direction, instead of one that holds only one way. A firm
resolving the gap the other way would change one branch of :func:`av_euro_pp_at` and
nothing else.

The *versement* is allocated **directly at the target mix** and bears no arbitrage
charge: new money is not a switch. :func:`arbitrage_charge_pp` is therefore nil in a year
where the account opens exactly on target even though a *versement* was paid — years 1
and 2 of the anchor cell, where the *équilibré* grid asks for no euro support at all.

The minimum binds **at the rebalancing date**, not continuously. Between dates the mix
drifts with relative performance: the anchor cell is at 70.00% euro after its year-12
rebalancing and 69.67% at the year end. Re-imposing the target continuously would invent
a rebalancing frequency the annual grid does not have.

.. rubric:: The garantie plancher is not a floor at gross premiums

::

    g(t) = g(t-1) + V_net - arb(t) - mgmt_charge_pp(t)

*Versements* net of entry loading, less the management charges levied over the plan's
life, less benefits already paid. That is **one of two contractual draftings in the
sample** and the one this model implements: the anchor contract's, with no interest limb,
and another contract says expressly that its guarantee is not a floor at gross premiums.
A second contract drafts the same guarantee with the euro fund's interest net of
management charges *added*, which accumulates faster and is not what is computed here —
the technical notes carry the comparison. It follows that

::

    A(t) - g(t) = [A(0) - g(0)] + sum of gross investment return credited to date

so the floor bites only where cumulative investment return is negative.
:func:`check_floor_identity` asserts that, and it is the check that catches the wrong
drafting: a floor accumulated at gross ``V`` rather than ``V_net``, or one that forgets
the arbitrage charge, or one charged something other than what the account was actually
charged, all break the identity in the first year. On the anchor cell the floor never
bites — the gap is 22 821.04 at the horizon against an opening gap of 600.00 — and model
point 10 is the same cell with a higher opening floor, where it bites for two years until
cumulative investment return overtakes it.

The cover ceases at the member's **70th birthday** and is capped at €762 245 across
contracts. Both are contractual, both are in :func:`death_benefit_pp`, and the age-70
cliff is not incidental: it is also the age at which a PER death benefit stops being
taxed as life insurance and enters the inheritance-duty base in its entirety.

.. rubric:: Settlement: a capital leg, and a rente that usually is not one

At ``t = n`` the survivors settle. The capital leg bears **no exit charge**. The annuity
leg is converted at :func:`annuity_factor`, charged the *frais d'arrérages*, and then
tested against the €110 monthly *quittance* threshold — remembering that €110 is a
**monthly** figure scaled by the months in the payment period, so an annual frequency
tests against €1 320.

Commuting at the conversion basis returns the converted capital less the *arrérage*
charge exactly::

    commuted = rente_net a_x = annuity_cap (1 - c_arr)

:func:`check_commutation_identity` asserts it. Commutation is therefore nearly
value-neutral, which is why it is common — a quarter of 2024 individual-PER benefit
amounts were small annuities commuted at outset — and why commuting at a *book* value
instead would manufacture a gain out of nothing. On the anchor cell the annuity is
€78.45 a month against the €110 threshold and duly commutes; the cliff sits at
``annuity_share = 42.06%``, and model point 6 is the same cell at 50%, where the annuity
is €130.75 a month, is not commuted, and leaves as ``annuity_conversion``.

.. rubric:: What is simplified, and where the rest of it lives

**The rente is cross-referenced, not re-implemented.** Where the annuity is not commuted
this model hands ``annuity_conversion`` to ``Rente_FR_S`` and records the amount. The
annuity reserve, the 0.80% p.a. charge on annuity reserves, reversion, *annuités
garanties* and revaluation through the profit-sharing account are specified in
``products/rente_viagere/technical-notes.md``, and duplicating the payout chassis here
would give the library two of them to keep in step.

**Staged capital is settled at the horizon.** The *capital fractionné* option changes
*when* the capital leg is paid, not how much: there is no exit charge, and the technical
notes fix ``proj_len`` at the declared horizon. The model therefore records the whole
capital leg at ``t = n``, publishes the instalment size as
:func:`capital_instalment_pp`, and credits nothing to the unpaid balance — a **[std]**
simplification that is exact on an undiscounted gross-cash-flow basis and is not exact
for anything that discounts. A discounting layer consuming these flows needs the
schedule, and this is where it would go.

**No PPB stock.** The euro support is credited at the asset return and charged on the
post-crediting balance; no *provision pour participation aux bénéfices* is carried. The
effective euro rate net of charge is ``1.0338 x 0.9930 - 1 = 2.6563%`` — not
``3.38 - 0.70 = 2.68%``, and not the 2.75% actually served in 2025, whose extra seven
basis points came from a PPB release this model does not carry. A PER's PPB release
horizon is fifteen years rather than eight, because the commitments sit in a
*comptabilité auxiliaire d'affectation*; modelling that stock is a fund-level scenario
extension, and four of the seven sampled contracts have no contractual profit-sharing
clause at all.

The machinery this stands in for is implemented next door in ``Euro_FR_A`` and specified
in ``products/assurance_vie_euro/technical-notes.md`` — the *compte de participation aux
résultats*, the PPB dotation-and-release lever and its vintage clock. Two things change on
the way across: the release deadline is eight years there and fifteen here, and a PER euro
fund carries a *garantie plancher* and a glide path that the euro-fund product does not.
Take the crediting chassis from those notes, not the liability.

**Tax is outside the projection.** The deductibility election changes the *holder's* exit
taxation, not the insurer's gross benefit. :func:`deduction_elected` is carried on the
model point so a downstream tax layer can find it and enters no cash flow anywhere in
this Space.

Also out of scope, per the notes: partial early release leaving the plan in force, the
15% transfer-value reduction on euro-denominated rights, profile and horizon changes
during the projection — which is the largest behavioural lever on this product and has no
public calibration — the unlisted-asset minimum inside the UC bucket, and the *provision
de diversification* supports, which are the ``eurocroissance`` product.
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


def policy_id():
    """The policy identifier of the model point; printed, never used in a formula."""
    return str(model_point()["policy_id"])


def sex():
    """The sex (M / F) of the member, the key into the mortality and annuity tables."""
    v = str(model_point()["sex"])
    if v not in ("M", "F"):
        raise ValueError("invalid sex")
    return v


def age_init():
    """x: the attained age of the member at ``t = 0``, integer **[std]**.

    Attained age at the valuation date, incremented once per plan year.  No retrieved
    French document fixes a model age basis; the regulatory non-annuity tables are
    applied with the annexed *décalage d'âge* age shifts, which the shipped proxy does
    not reproduce.
    """
    return int(model_point()["age"])


def retirement_age():
    """The declared *horizon* — the retirement age the member has declared.

    The holder may move it at any time, which re-cuts the whole allocation immediately;
    the base model holds it fixed and a scenario overlay would shift it and re-read the
    grid.  It is the single most important number on the model point: it sets both the
    length of the projection and, through ``years_to_horizon``, every year's target mix.
    """
    return int(model_point()["retirement_age"])


def duration_ifo():
    """Completed years since the **first *versement*** at the valuation date.

    Not the same thing as elapsed projection years, and the distinction is the whole
    content of the transfer indemnity window: the 1% indemnity runs to the fifth
    anniversary of the first *versement*, not of the projection start.  The anchor cell
    carries 2, so its window closes after two projected years rather than five.
    """
    return int(model_point()["duration_ifo"])


def compartment():
    """``c1``, ``c2`` or ``c3`` — the origin of the money, and two operative rules.

    Compartment 3 holds rights arising from compulsory contributions, and it changes two
    things rather than one: those rights may be delivered **only** as a life annuity, so
    :func:`exit_form` refuses any other election on a c3 cell; and they are **excluded**
    from the main-residence early-release case, which is the only discretionary limb of
    the seven, so ``exit_table.csv`` carries a lower ``early_release_rate`` for them.
    """
    v = str(model_point()["compartment"])
    if v not in ("c1", "c2", "c3"):
        raise ValueError("invalid compartment")
    return v


def allocation_profile():
    """The *gestion pilotée par horizon* profile: which ladder of the grid applies.

    ``prudent``, ``equilibre``, ``dynamique`` or ``offensif`` — the four qualified
    profiles of the de-risking arrêté.  Validated against the shipped grid rather than
    against a hard-coded list, so adding an insurer profile to ``allocation_grid.csv``
    is enough to make it usable.
    """
    v = str(model_point()["allocation_profile"])
    if v not in set(data.allocation_grid().index.get_level_values(0)):  # noqa: F821
        raise ValueError("allocation_profile not in allocation_grid.csv")
    return v


def premium_init():
    """V: the gross annual *versement*, paid at the start of each plan year.

    Zero on a cell that has stopped contributing — a c2 or c3 compartment reached by an
    incoming transfer holds acquired rights and receives nothing further.
    """
    return float(model_point()["premium"])


def av_euro_init():
    """The per-policy euro-support balance carried into the projection."""
    return float(model_point()["av_euro_init"])


def av_uc_init():
    """The per-policy *unités de compte* balance carried into the projection."""
    return float(model_point()["av_uc_init"])


def death_floor_init():
    """g(0): the *garantie plancher* base carried into the projection.

    On the anchor cell it is €16 000 against a €16 600 balance, and the €600 gap is the
    investment return accumulated before the valuation date.  A cell whose accumulated
    return is *negative* carries a base **above** its balance, which is the only state in
    which the floor bites; model point 10 is that cell.
    """
    return float(model_point()["death_floor_init"])


def death_floor_flag():
    """Whether the *garantie plancher* is in force on this cell at all.

    Included as standard in two sampled contracts, optional in three and an age-rated
    rider in one, so it is a model point column rather than a product constant.
    """
    return bool(model_point()["death_floor_flag"])


def exit_form():
    """``capital_single``, ``capital_staged``, ``annuity`` or ``mixed``.

    The statutory exit menu: capital "libéré en une fois ou de manière fractionnée", a
    *rente viagère*, or a mix.  A compartment-3 cell **must** elect the annuity — those
    rights may be delivered no other way — and a model point that says otherwise raises
    here rather than projecting a settlement the contract cannot make.
    """
    v = str(model_point()["exit_form"])
    if v not in ("capital_single", "capital_staged", "annuity", "mixed"):
        raise ValueError("invalid exit_form")
    if compartment() == "c3" and v != "annuity":
        raise ValueError(
            "compartment 3 rights may be delivered only as a life annuity")
    return v


def annuity_share():
    """theta: the share of the settlement balance converted to a *rente viagère*.

    Derived from :func:`exit_form` and cross-checked against the model point column, so
    the table cannot say ``capital_single`` in one column and 30% in the next.  A
    ``mixed`` election must be strictly between the two ends; at either end it is one of
    the pure forms and should say so.
    """
    theta = float(model_point()["annuity_share"])
    form = exit_form()
    if form == "mixed":
        if not 0.0 < theta < 1.0:
            raise ValueError("a mixed exit needs 0 < annuity_share < 1")
        return theta
    expected = 1.0 if form == "annuity" else 0.0
    if abs(theta - expected) > 1e-12:
        raise ValueError("annuity_share contradicts exit_form")
    return expected


def capital_instalments():
    """The number of annual instalments the capital leg is paid in.

    1 under ``capital_single``, and the *fractionné* count under ``capital_staged``.  It
    changes :func:`capital_instalment_pp` and nothing else — see the Space docstring on
    why staged capital is settled at the horizon.
    """
    j = int(model_point()["capital_instalments"])
    if j < 1:
        raise ValueError("capital_instalments must be at least 1")
    if j > 1 and exit_form() != "capital_staged":
        raise ValueError("only a capital_staged exit is paid in instalments")
    return j


def deduction_elected():
    """Whether the holder deducted the *versements* from taxable income.

    **Carried and never used.**  The election is the pivot of the whole exit tax
    treatment — pension regime with the 10% abatement against *rente viagère à titre
    onéreux* on an age-graded fraction — but it changes what the holder keeps, not what
    the insurer pays.  It appears in no recursion in this Space and exists so a
    downstream tax layer can find it.
    """
    return bool(model_point()["deduction_elected"])


def mort_basis():
    """``flat`` or ``table``: which mortality basis this cell is run on.

    ``flat`` reads the model point's own :func:`mort_rate_flat`, which is what the
    technical notes' worked example specifies — a flat 0.00500 placeholder, held constant
    across the twelve years so that the printed ``pols_if`` column can be re-derived by
    hand.  ``table`` reads the shipped **[std]** proxy at the attained age.

    The two are anchored to agree in the anchor cell's **first** year: the table's level
    is set so that ``mort_be_factor x q(M, 52)`` is exactly 0.00500.  They diverge after
    that, because a table has a slope and a placeholder does not.
    """
    v = str(model_point()["mort_basis"])
    if v not in ("flat", "table"):
        raise ValueError("invalid mort_basis")
    return v


def mort_rate_flat():
    """The flat annual mortality rate of a ``flat``-basis cell **[std]**.

    0.00500 on the worked-example cells.  No sampled contract publishes a mortality
    basis, and the one published rate card in the sample is a *gross premium* scale on a
    no-underwriting death rider, which must not be read as one.
    """
    return float(model_point()["mort_rate_flat"])


def pols_if_init():
    """l(0): the in-force probability carried in; 1.0 on a single-policy model point."""
    return float(model_point()["pols_if_init"])


def proj_len():
    """n: the last projected plan year — the declared horizon.

    ``retirement_age - age(0)``.  The plan is liquidated there and nothing this model
    projects happens afterwards: no *versement* arrives, ``years_to_horizon`` does not go
    negative, and a staged capital settlement is still recorded at ``t = n``.
    :func:`check_horizon` asserts it.
    """
    n = retirement_age() - age_init()
    if n < 1:
        raise ValueError("the declared horizon is not in the future")
    return n


def age(t):
    """The attained age at the **end** of plan year t: ``x + t``.

    The mortality rate for year ``t`` is read at ``age(t - 1)``, the age at the start of
    the year, and the *garantie plancher* ceases when ``age(t)`` reaches 70.
    """
    return age_init() + t


def duration(t):
    """Completed years since the first *versement* at the end of plan year t.

    ``duration_ifo + t``.  It keys the exit decrements and, through
    :func:`transfer_indemnity_rate`, the five-year transfer indemnity window.
    """
    return duration_ifo() + t


def years_to_horizon(t):
    """k(t): the years remaining to the declared horizon at the **start** of year t.

    ``n - t + 1``, so ``k(1) = n`` and ``k(n) = 1``.  Floored at zero rather than
    allowed to go negative, because a plan does not run past its own horizon and a
    negative key into the glide path is a symptom rather than a value.
    """
    return max(0, proj_len() - t + 1)


def alloc_euro(t):
    """a(t): the target euro (low-risk) share for plan year t, read from the grid.

    A lookup, not a formula.  The *équilibré* ladder is 0 / 20 / 50 / 70% as the horizon
    closes, and **the boundary belongs to the tighter band** — ``k = 10`` reads 20%,
    ``k = 5`` reads 50%, ``k = 2`` reads 70% — a **[std]** convention, because the
    arrêté's band headings as extracted overlap at each boundary year and do not settle
    which band it falls in.

    Years beyond the last row of the grid take that row, which is the ``k > 10`` band in
    the shipped file.
    """
    grid = data.allocation_grid().loc[allocation_profile()]          # noqa: F821
    k = max(1, min(years_to_horizon(t), int(grid.index.max())))
    return float(grid.loc[k, "euro_share"])


def alloc_uc(t):
    """1 - a(t): the target *unités de compte* share, read from the grid's own column.

    Read rather than computed, so that the file's two columns are both live and a grid
    whose rows do not close is caught by :func:`check_glide_path_closes` instead of being
    silently half-ignored.
    """
    grid = data.allocation_grid().loc[allocation_profile()]          # noqa: F821
    k = max(1, min(years_to_horizon(t), int(grid.index.max())))
    return float(grid.loc[k, "uc_share"])


def premium_pp(t):
    """V: the gross *versement* received at the start of plan year t.

    Nil after the horizon.  A plan that has been liquidated takes no further
    contributions, and from 1 January 2026 contributions after the holder's 70th birthday
    stop being deductible in any case.
    """
    if t < 1 or t > proj_len():
        return 0.0
    return premium_init()


def prem_to_av_pp(t):
    """V_net: the *versement* net of the entry loading, available to allocate.

    ``V (1 - load)``, at 2.50% **[std]**.  The sampled entry loadings span 0% to 4.80%
    and the *encadré* discloses maxima rather than capping levels, so this is a
    standardization and not a contractual constant.  It is also the amount that accrues
    to the *garantie plancher* base — the guarantee is a floor at *versements net of
    loading*, never at gross premiums.
    """
    return premium_pp(t) * (1.0 - load_rate)                         # noqa: F821


def switch_pp(t):
    """m(t): the gross amount switched between supports at the BOY rebalancing.

    ``a(t) A(t-1) - av_euro_pp(t-1)``: what it takes to bring the balance carried into
    the year onto the year's target mix.  **Signed** — positive on the ordinary
    de-risking switch from UC to euro, negative if the euro support has run above target
    — and the sign decides which support bears :func:`arbitrage_charge_pp`.

    Note what it is measured on: the **carried-in balance alone**.  The year's
    *versement* is allocated at the target mix directly and is not part of the switch,
    which is why a year that opens exactly on target carries no arbitrage charge however
    large the contribution.
    """
    return alloc_euro(t) * av_pp(t - 1) - av_euro_pp(t - 1)


def arbitrage_charge_pp(t):
    """arb(t): the *frais d'arbitrage* on the year's rebalancing.

    ``arb_rate |m(t)|`` at 0.30% **[std]**.  Horizon arbitrage is free at five of the
    eight sampled contracts and charged at 0.30% and 1% at the other two; a non-nil rate
    makes the cost of the glide path a visible line rather than an invisible one.

    Taken from the **source** support — see :func:`av_euro_pp_at`.
    """
    return arb_rate * abs(switch_pp(t))                              # noqa: F821


def av_euro_pp_at(t, timing):
    """The per-policy euro-support balance at a point inside plan year t.

    ``"BOY"``
        after the rebalancing and the allocation of the year's *versement*.
        The switch arrives in full and the arbitrage charge is deducted here
        **only when the euro support is the source**, that is when
        ``m(t) < 0``.

    ``"EOY"``
        after the year's investment return and the management charge taken
        on the post-crediting balance; the same number as
        :func:`av_euro_pp`.

    The euro support is **not** monotone under this convention, and it is worth being
    exact about why.  The 0% of A. 142-1 is the *maximum* technical rate a PER tariff may
    use, not a floor on what is credited; what the sampled contracts guarantee is a
    capital floor gross of charges plus profit sharing, not an accumulation rate.  Since
    the charge is taken on the post-crediting balance, the balance grows only while
    ``r_eu > charge_euro / (1 - charge_euro)`` — 0.7049% here.  The base run's 3.38%
    clears that comfortably, so the euro support does rise every year; at a credited rate
    of 0% it would fall by the 0.70% charge.
    """
    if timing == "BOY":
        m = switch_pp(t)
        boy = av_euro_pp(t - 1) + m + alloc_euro(t) * prem_to_av_pp(t)
        if m < 0.0:
            boy -= arbitrage_charge_pp(t)
        return boy
    if timing == "EOY":
        return (av_euro_pp_at(t, "BOY") * (1.0 + return_euro)        # noqa: F821
                * (1.0 - charge_euro))                               # noqa: F821
    raise ValueError("invalid timing")


def av_uc_pp_at(t, timing):
    """The per-policy *unités de compte* balance at a point inside plan year t.

    Same two timings as :func:`av_euro_pp_at`, and the mirror image of it: the UC bucket
    bears the arbitrage charge on the ordinary de-risking switch, where it is the source.

    There is no guarantee on this bucket at all.  The insurer commits to the **number**
    of units, not to their value, and ``return_uc`` is stated net of the fund-level
    charges inside the units, which are large relative to the wrapper charge.
    """
    if timing == "BOY":
        m = switch_pp(t)
        boy = av_uc_pp(t - 1) - m + alloc_uc(t) * prem_to_av_pp(t)
        if m >= 0.0:
            boy -= arbitrage_charge_pp(t)
        return boy
    if timing == "EOY":
        return (av_uc_pp_at(t, "BOY") * (1.0 + return_uc)            # noqa: F821
                * (1.0 - charge_uc))                                 # noqa: F821
    raise ValueError("invalid timing")


def av_pp_at(t, timing):
    """A(t) at a point inside plan year t: the two supports added together.

    ``"BOY"`` is the balance the year invests and ``"EOY"`` the balance the year's
    decrements are valued on.  The BOY split is what
    :func:`check_euro_share_min` measures the regulatory minimum against, because the
    minimum binds at the rebalancing date and not continuously.
    """
    return av_euro_pp_at(t, timing) + av_uc_pp_at(t, timing)


def av_euro_pp(t):
    """The per-policy euro-support balance at the end of plan year t."""
    if t <= 0:
        return av_euro_init()
    return av_euro_pp_at(t, "EOY")


def av_uc_pp(t):
    """The per-policy *unités de compte* balance at the end of plan year t."""
    if t <= 0:
        return av_uc_init()
    return av_uc_pp_at(t, "EOY")


def av_pp(t):
    """A(t): the per-policy account value at the end of plan year t.

    **Per policy, and already net of decrements in the sense that matters**: it is the
    balance one surviving plan holds, not the balance the block holds.  Multiplying a
    claims column by ``pols_if`` again understates every benefit by the square of the
    survival factor, which is the quietest way to get this product wrong.
    :func:`av_at` is the in-force weighted quantity where one is wanted.
    """
    if t <= 0:
        return av_euro_init() + av_uc_init()
    return av_pp_at(t, "EOY")


def av_at(t, timing):
    """The in-force weighted account value at a point inside plan year t.

    ``av_pp_at(t, timing)`` times the in force at that point — ``pols_if(t)``, the
    start-of-year count, at BOY, and ``pols_if_at(t, "AFT_DECR")``, the end-of-year
    count, at EOY.  Published for a reader who wants a block-level balance; no cash flow
    in this model reads it, because every claim is already the product of a decrement and
    a per-policy amount.
    """
    if timing == "BOY":
        return av_pp_at(t, timing) * pols_if(t)
    if timing == "EOY":
        return av_pp_at(t, timing) * pols_if_at(t, "AFT_DECR")
    raise ValueError("invalid timing")


def inv_income_pp(t):
    """The gross investment return credited to the two supports in plan year t.

    ``E_eu r_eu + E_uc r_uc``, before the management charge.  It is the only term that
    opens the gap between the account value and the *garantie plancher* base, which is
    what :func:`check_floor_identity` uses it for.
    """
    return (av_euro_pp_at(t, "BOY") * return_euro                    # noqa: F821
            + av_uc_pp_at(t, "BOY") * return_uc)                     # noqa: F821


def mgmt_charge_pp(t):
    """The management charge levied on the two supports in plan year t.

    Taken on the **end-of-year balance after crediting**, at 0.70% on each support
    **[std]**.  Charge timing differs across the sample and is load-bearing — monthly on
    an end-of-month balance, quarterly on UC and annually on the euro fund, daily accrual
    with annual levy — and an annual grid can carry only one of them.

    The same amount is deducted from the *garantie plancher* base, because the guarantee
    is stated net of charges levied over the plan's life.
    """
    return (av_euro_pp_at(t, "BOY") * (1.0 + return_euro)            # noqa: F821
            * charge_euro                                            # noqa: F821
            + av_uc_pp_at(t, "BOY") * (1.0 + return_uc)              # noqa: F821
            * charge_uc)                                             # noqa: F821


def death_floor_pp(t):
    """g(t): the *garantie plancher* base at the end of plan year t.

    ``g(t-1) + V_net - arb(t) - mgmt_charge_pp(t)``: *versements* net of entry loading,
    less the charges levied over the plan's life.  **Not a floor at gross premiums** —
    one contract says so expressly — and not a floor at the account value either.  It is
    the anchor contract's drafting; a second contract in the sample adds the euro fund's
    interest net of charges to the base, and implementing that means adding a term here
    and dropping :func:`check_floor_identity`, not moving a parameter.

    It is a *base*, not a benefit: :func:`death_benefit_pp` applies the cessation at 70
    and the €762 245 cap to it.  The recursion itself keeps running past both, because
    the cover can be reinstated by a model point that carries the flag while the base
    cannot be reconstructed once it has stopped being accumulated.
    """
    if t <= 0:
        return death_floor_init()
    return (death_floor_pp(t - 1) + prem_to_av_pp(t)
            - arbitrage_charge_pp(t) - mgmt_charge_pp(t))


def floor_in_force(t):
    """Whether the *garantie plancher* covers a death in plan year t.

    The cell must carry the cover, and the member must still be under 70 at the end of
    the year: the guarantee **ceases at the 70th birthday**.  That is the same birthday
    at which a PER death benefit stops being taxed as life insurance and enters the
    inheritance-duty base in its entirety, and from 2026 the same one at which
    contributions stop being deductible — one cliff edge, three consequences.
    """
    return bool(death_floor_flag() and age(t) < floor_cease_age)     # noqa: F821


def death_benefit_pp(t):
    """The per-policy death benefit for a death in plan year t.

    The account value, floored by the *garantie plancher* while the cover is in force,
    the floor itself capped at €762 245 across contracts.  Death **closes the plan**, so
    this is the whole benefit and not a sum at risk.
    """
    if not floor_in_force(t):
        return av_pp(t)
    return max(av_pp(t), min(death_floor_pp(t), death_floor_cap))    # noqa: F821


def mort_rate(t):
    """q(t): the annual mortality rate applied in plan year t.

    On a ``flat`` cell the model point's own placeholder; on a ``table`` cell the shipped
    **[std]** proxy at ``age(t - 1)`` — the attained age at the **start** of the year —
    times ``mort_be_factor``.

    Both are placeholders.  TH 00-02 and TF 00-02 govern the death benefit during
    accumulation and are cited rather than shipped, their *décalage d'âge* age shifts are
    not reproduced, and no sampled contract publishes a mortality basis at all.
    """
    if mort_basis() == "flat":
        return mort_rate_flat()
    x = min(age(t - 1), omega_age)                                   # noqa: F821
    return min(1.0, float(data.mort_table().loc[                     # noqa: F821
        (sex(), x), "mort_rate"]) * mort_be_factor)                  # noqa: F821


def early_release_rate(t):
    """w_e(t): the *déblocage anticipé* decrement for plan year t **[std]**.

    **Not a lapse rate.**  A release requires one of the seven listed triggering events —
    death of a spouse, invalidity, serious illness of a dependent child,
    over-indebtedness, exhaustion of unemployment rights, business liquidation, purchase
    of the main residence — bears **no charge**, and may be partial, leaving the plan in
    force.  The base model treats it as a full exit paying the whole account value.

    Only the last of the seven cases is discretionary and none of them responds to
    investment performance, so a dynamic moneyness multiplier would be a category error
    on this decrement.  It is read from ``exit_table.csv`` at (``compartment``,
    ``duration``), and compartment 3 carries a lower rate because the main-residence
    limb is closed to it.
    """
    tbl = data.exit_table().loc[compartment()]                       # noqa: F821
    d = max(1, min(duration(t), int(tbl.index.max())))
    return float(tbl.loc[d, "early_release_rate"])


def transfer_out_rate(t):
    """w_r(t): the transfer-out decrement for plan year t **[std]**.

    **Not a lapse rate either.**  The plan ends for this insurer but the savings do not
    leave the regime: rights under accumulation are transferable to any other PER, and
    the transfer does not alter the surrender or liquidation conditions.  It pays a
    transfer value, not a surrender value, and differs from the release amount by
    :func:`transfer_indemnity_rate`.

    Flat in the base run.  The indemnity falls to nil at the fifth anniversary and a
    rational holder waits, so the reference behavioural shape is a multiplier of 0.7 in
    the years before the anniversary and 1.3 in the anniversary year **[std]**, the pair
    chosen so that the two adjacent years average to 1.00 and the flat calibration is not
    quietly raised by turning the shape on.  It is switched off here so that the worked
    example stays transparent.  Note that the pair is mean-preserving over those two years
    only: applied over a longer pre-anniversary run it is below 1 on average, and a
    calibration that spans one would have to rescale.
    """
    tbl = data.exit_table().loc[compartment()]                       # noqa: F821
    d = max(1, min(duration(t), int(tbl.index.max())))
    return float(tbl.loc[d, "transfer_out_rate"])


def transfer_indemnity_rate(t):
    """iota(t): the transfer indemnity, 1% of acquired rights and then nil.

    The fee "ne peuvent excéder 1 % des droits acquis" and is nil **five years after the
    first *versement* in the plan** — not five years after the projection starts.  That
    is what :func:`duration` is for, and the anchor cell shows the difference: it carries
    ``duration_ifo = 2``, so its window closes at the end of projected year 2.

    The separate 15% reduction of euro-denominated transfer values, available where the
    transfer value exceeds the asset share backing it, is **off** in the base run: it is
    a management action conditional on a market state the base scenario does not produce,
    and in a rising-rate scenario it dominates this 1% by an order of magnitude.
    """
    if duration(t) < transfer_indemnity_years:                       # noqa: F821
        return transfer_indemnity                                    # noqa: F821
    return 0.0


def pols_if(t):
    """The in-force probability at the **start** of plan year t, before any decrement.

    ``pols_if(1) = pols_if_init()``, and this is the weight on plan year ``t``'s own cash
    flows — the *versement*, the expense, and the exposure every decrement of the year is
    taken against.  It is the library's settled convention: ``pols_if(t)`` is the count
    the row opens with, so a ``result_cf()`` flow divided by that row's ``pols_if``
    returns a per-policy amount for the same period.

    The technical notes' ``l(t)`` is the count the year **ends** with, which is one step
    further on.  It is :func:`pols_if_at` at ``"AFT_DECR"``; see the Space docstring on
    why it no longer carries this name.
    """
    if t <= 1:
        return pols_if_init()
    return pols_if_at(t - 1, "AFT_DECR")


def pols_if_at(t, timing):
    """The in-force probability at a point inside plan year t.

    ``"BEF_DECR"``
        the start of the year, before any decrement; :func:`pols_if`.
        This is the weight on the year's *versement* and expense.

    ``"BEF_RELEASE"``
        after mortality, before early releases.

    ``"BEF_TRANSFER"``
        after early releases, before transfers out.

    ``"AFT_DECR"``
        after transfers out: the end-of-year count, which is the technical
        notes' own ``l(t)``.

    The order — death, then early release, then transfer out — is an ordered
    dependent-decrement convention **[std]**, matching the library's house treatment.
    Exposing the steps is what makes the ordering inspectable rather than implied by the
    shape of three multiplications.

    The timing strings are the house ``BEF_*`` / ``AFT_DECR`` vocabulary of
    ``savings.CashValue_SE`` and of the other frlib models.  The account-value cells keep
    ``"BOY"`` / ``"EOY"``: those mark points in the year's *investment* sequence — the
    rebalancing, the crediting, the charge — and not points in this decrement chain.
    """
    if timing == "BEF_DECR":
        return pols_if(t)
    if timing == "BEF_RELEASE":
        return pols_if(t) * (1.0 - mort_rate(t))
    if timing == "BEF_TRANSFER":
        return pols_if_at(t, "BEF_RELEASE") * (1.0 - early_release_rate(t))
    if timing == "AFT_DECR":
        return pols_if_at(t, "BEF_TRANSFER") * (1.0 - transfer_out_rate(t))
    raise ValueError("invalid timing")


def pols_death(t):
    """d_death(t): deaths in plan year t, against the start-of-year in force."""
    return pols_if(t) * mort_rate(t)


def pols_release(t):
    """d_release(t): *déblocages anticipés* in plan year t, from the survivors."""
    return pols_if_at(t, "BEF_RELEASE") * early_release_rate(t)


def pols_transfer(t):
    """d_transfer(t): transfers out in plan year t, after death and release."""
    return pols_if_at(t, "BEF_TRANSFER") * transfer_out_rate(t)


def pols_maturity(t):
    """l(n): the survivors settling at the declared horizon; nil in every other year.

    ``pols_if_at(n, "AFT_DECR")`` — the count the final plan year **ends** with, after
    that year's own decrements, not the count it opened with.  A real contractual event
    rather than a modelling truncation: the plan reaches its L. 224-1 maturity and the
    rights are liquidated, so the survivors are paid.
    """
    if t != proj_len():
        return 0.0
    return pols_if_at(t, "AFT_DECR")


def annuity_factor():
    """a_x: the annuity conversion factor at the horizon **[std]**.

    Read from ``annuity_factor.csv`` at (``sex``, ``retirement_age``), and anchored at
    22.0000 for a male aged 64 — annual in arrears, no reversion.

    **It is an undiscounted expected-instalment count.**  A PER tariff is established
    "d'après un taux d'intérêt technique au plus égal à 0 %", so the factor collapses to
    the tariff table's expected number of instalments and nothing in this model discounts
    it: :func:`rente_gross_pp` is a plain division.  A 2% technical rate would shorten the
    factor by a fifth, from 22.0000 to 17.66, and so inflate the annuity by roughly a
    quarter on the anchor cell — the factor falls 19.7%, the annuity rises 24.6%.

    No sampled insurer publishes an annuity rate card and TGH05 / TGF05 are not shipped,
    so the ladder is a placeholder to be replaced before any quantitative use.
    """
    return float(data.annuity_factor_table().loc[                    # noqa: F821
        (sex(), retirement_age()), "annuity_factor"])


def capital_leg_pp():
    """The capital settled at the horizon, per surviving policy: ``(1 - theta) A(n)``.

    **No exit charge.**  Every sampled contract settles capital at 0%, so this is the
    account value itself and not a surrender value.
    """
    return (1.0 - annuity_share()) * av_pp(proj_len())


def capital_instalment_pp():
    """The size of one instalment of the capital leg under a *fractionné* settlement.

    ``capital_leg_pp() / capital_instalments()``.  Published rather than paid: the model
    records the whole capital leg at ``t = n``, because the option changes *when* the leg
    is paid and not how much, and the technical notes fix ``proj_len`` at the horizon.
    See the Space docstring for what that simplification costs.
    """
    return capital_leg_pp() / capital_instalments()


def annuity_cap_pp():
    """The capital converted to a *rente viagère*, per surviving policy: ``theta A(n)``."""
    return annuity_share() * av_pp(proj_len())


def rente_gross_pp():
    """The gross annual annuity instalment: ``annuity_cap / a_x``.

    A plain division, because :func:`annuity_factor` is undiscounted.  Annual in arrears
    is forced by the grid; the sample pays quarterly or monthly, and the commutation test
    below is applied on the monthly equivalent for exactly that reason.
    """
    return annuity_cap_pp() / annuity_factor()


def rente_net_pp():
    """The annual instalment net of the *frais d'arrérages*: ``rente_gross (1 - c_arr)``.

    1.50% of each gross instalment **[std]**.  Observed *arrérage* charges run from 0% to
    3% across the sample; charged on every instalment for life, the level moves the
    capital at which the commutation test bites.
    """
    return rente_gross_pp() * (1.0 - arrear_charge_rate)             # noqa: F821


def is_commuted():
    """Whether the annuity is commuted to a single capital payment at the horizon.

    The insurer may substitute a capital payment, with the annuitant's agreement, where
    the monthly *quittance d'arrérages* does not exceed €110 including statutory
    increases, **multiplied by the number of months in the payment period**.  The
    threshold is monthly, so an annual frequency tests against €1 320, and testing €110
    against an annual instalment would commute almost nothing.

    The base model commutes deterministically whenever the test passes; a
    ``commutation_agreement_rate`` is the natural refinement **[std]**.  A cell electing
    no annuity has nothing to commute and reads False.
    """
    if annuity_cap_pp() <= 0.0:
        return False
    return bool(rente_net_pp() / payment_mths                        # noqa: F821
                <= commute_threshold_mth)                            # noqa: F821


def commuted_pp():
    """The commutation lump sum, per surviving policy; nil where the annuity is paid.

    ``rente_net a_x``, which is ``annuity_cap (1 - c_arr)`` exactly — commuting at the
    conversion basis returns the converted capital less the *arrérage* charge, and
    nothing else.  :func:`check_commutation_identity` asserts it, because commuting at a
    book value instead manufactures a gain out of nothing.
    """
    if not is_commuted():
        return 0.0
    return rente_net_pp() * annuity_factor()


def annuity_conversion_pp():
    """The capital handed to ``Rente_FR_S``, per surviving policy.

    ``annuity_cap`` where the annuity is paid as a *rente*, nil where it is commuted.
    The annuity's own reserve, its 0.80% p.a. charge, reversion, *annuités garanties* and
    revaluation are specified in ``products/rente_viagere/technical-notes.md``; this
    model hands over an amount and records it.
    """
    if is_commuted():
        return 0.0
    return annuity_cap_pp()


def claim_pp(t, kind):
    """The benefit paid per exiting policy in plan year t, by kind.

    ``"DEATH"``
        :func:`death_benefit_pp` — the account value floored by the
        *garantie plancher* while the cover is in force.  Death closes the
        plan.

    ``"EARLY_RELEASE"``
        the **whole** account value, with **no charge**.  There is no
        surrender charge and no market value adjustment on this product,
        because there is no surrender.

    ``"TRANSFER"``
        ``A(t) (1 - iota(t))`` — the account value less the 1% indemnity
        while the plan is under five years old, and the account value
        itself afterwards.

    ``"MATURITY"``
        the capital leg plus any commutation lump sum, at ``t = n`` only.
        Where the annuity is *not* commuted its capital leaves as
        :func:`annuity_conversion` instead, so the two never overlap.
    """
    if kind == "DEATH":
        return death_benefit_pp(t)
    if kind == "EARLY_RELEASE":
        return av_pp(t)
    if kind == "TRANSFER":
        return av_pp(t) * (1.0 - transfer_indemnity_rate(t))
    if kind == "MATURITY":
        if t != proj_len():
            return 0.0
        return capital_leg_pp() + commuted_pp()
    raise ValueError("invalid kind")


def claims(t, kind=None):
    """Benefit outgo in plan year t, by kind; the total when kind is omitted.

    Each kind weights :func:`claim_pp` by its own decrement, so a benefit is never
    multiplied by ``pols_if`` twice.  ``annuity_conversion`` is **not** in here: it is
    not a benefit paid to the policyholder but capital handed to the annuity model, and
    it carries its own line in :func:`result_cf`.
    """
    if kind is None:
        return sum(claims(t, k) for k in
                   ("DEATH", "EARLY_RELEASE", "TRANSFER", "MATURITY"))
    if kind == "DEATH":
        return claim_pp(t, kind) * pols_death(t)
    if kind == "EARLY_RELEASE":
        return claim_pp(t, kind) * pols_release(t)
    if kind == "TRANSFER":
        return claim_pp(t, kind) * pols_transfer(t)
    if kind == "MATURITY":
        return claim_pp(t, kind) * pols_maturity(t)
    raise ValueError("invalid kind")


def annuity_conversion(t):
    """The capital converted to a *rente* and handed to ``Rente_FR_S`` in plan year t.

    Non-zero at ``t = n`` only, and only on a cell whose annuity is not commuted.  It is
    an **outgo** of this model: the money leaves the accumulation projection, and a
    reader who nets it out would be double-counting the annuity against itself.
    """
    return annuity_conversion_pp() * pols_maturity(t)


def inflation_factor(t):
    """The expense inflation factor in plan year t: ``(1 + pi)^(t-1)`` at 1.80% **[std]**."""
    return (1.0 + inflation_rate) ** (t - 1)                         # noqa: F821


def premiums(t):
    """*Versement* income at the start of plan year t, an inflow.

    Weighted by the in force at the **start** of the year, ``pols_if(t)``: a contribution
    is paid by a plan that is still there to pay it.
    """
    return premium_pp(t) * pols_if(t)


def expenses(t):
    """E(t): the maintenance expense in plan year t **[std]**.

    €30 a plan a year inflating at 1.80%, on the in force at the start of the year.  No
    insurer's unit cost is public; only the charge cap is, and the €20 association fee
    the sample publishes is a one-off at adhesion and nil for an in-force cell.
    """
    return expense_maint * inflation_factor(t) * pols_if(t)           # noqa: F821


def liability_cf(t):
    """CF(t): the net liability cash flow of plan year t, **outgo-positive**.

    The technical notes' own orientation, published verbatim: claims, plus the capital
    handed to the annuity model, plus expenses, less *versements*.  :func:`net_cf` is its
    negative.
    """
    return (claims(t) + annuity_conversion(t) + expenses(t) - premiums(t))


def net_cf(t):
    """The net cash flow of plan year t, **income positive**, per the house convention.

    Exactly ``-liability_cf(t)``, so that ``result_cf()["net_cf"]`` can be compared and
    summed across the library without checking which product it came from.
    """
    return -liability_cf(t)


def check_pols_roll_fwd_resid(t):
    """The in-force roll-forward residual in plan year t; zero everywhere.

    ``l(t-1) - d_death(t) - d_release(t) - d_transfer(t) - l(t)``, which in cells names is
    ``pols_if(t)`` less the three decrement flows less ``pols_if_at(t, "AFT_DECR")``.
    Rebuilt from the three decrement flows rather than from the chain of survival factors
    that defines the timings, so an exit counted twice — the classic error when two
    decrements are both applied to the start-of-year in force instead of in sequence —
    shows up here.
    """
    return (pols_if(t) - pols_death(t) - pols_release(t)
            - pols_transfer(t) - pols_if_at(t, "AFT_DECR"))


def check_pols_roll_fwd():
    """True when the in-force roll-forward closes in every projected year."""
    return bool(all(
        abs(check_pols_roll_fwd_resid(t)) <= roll_fwd_tol * max(pols_if_init(), 1.0)  # noqa: F821
        for t in range(1, proj_len() + 1)))


def check_av_roll_fwd_resid(t):
    """The account value roll-forward residual in plan year t; zero everywhere.

    ``A(t) - [A(t-1) + V_net - arb(t) + inv_income_pp(t) - mgmt_charge_pp(t)]``.

    This is a **conservation** statement, not the recursion restated: the switch does not
    appear in it, because a switch moves money between the two supports rather than into
    or out of the plan, and the only things that cross the boundary are the *versement*
    net of loading, the arbitrage charge, the return credited and the charge levied.  A
    switch that credits the destination without debiting the source, an arbitrage charge
    taken from one support and not deducted anywhere, or a management charge computed on
    a different balance from the one it is taken off, all break it — and all of them
    leave every printed number looking plausible.
    """
    built = (av_pp(t - 1) + prem_to_av_pp(t) - arbitrage_charge_pp(t)
             + inv_income_pp(t) - mgmt_charge_pp(t))
    return av_pp(t) - built


def check_av_roll_fwd():
    """True when the account value roll-forward closes in every projected year."""
    return bool(all(abs(check_av_roll_fwd_resid(t)) <= 1e-8
                    for t in range(1, proj_len() + 1)))


def check_floor_identity_resid(t):
    """The *garantie plancher* identity residual in plan year t; zero everywhere.

    ``[A(t) - g(t)] - [A(t-1) - g(t-1)] - inv_income_pp(t)``: the gap between the account
    value and the guarantee base widens by the gross investment return credited and by
    nothing else, because the *versement* net of loading, the arbitrage charge and the
    management charge all enter both sides.

    It is **zero by construction** given the recursion in :func:`death_floor_pp` — and
    that is the point of writing it out.  What it catches is the *wrong* recursion: a
    base accumulated at gross ``V`` rather than ``V_net``, which is the single most
    common misreading of this guarantee and which one sampled contract explicitly warns
    against; a base that forgets the arbitrage charge; and a base charged something other
    than what the account was actually charged.  Each of those breaks the identity in the
    first year in which it is wrong.
    """
    return ((av_pp(t) - death_floor_pp(t))
            - (av_pp(t - 1) - death_floor_pp(t - 1)) - inv_income_pp(t))


def check_floor_identity():
    """True when the *garantie plancher* identity closes in every projected year."""
    return bool(all(abs(check_floor_identity_resid(t)) <= 1e-8
                    for t in range(1, proj_len() + 1)))


def check_euro_share_min_resid(t):
    """The regulatory de-risking minimum residual at the BOY of plan year t.

    ``av_euro_pp_at(t, "BOY") - a(t) av_pp_at(t, "BOY")``.  On a de-risking switch it
    must be **non-negative**: the grid is a minimum, and taking the arbitrage charge from
    the source — the UC bucket — is what keeps the post-rebalancing share at or just
    above it.  Taking the charge from the destination instead would leave it under, by
    ``(1 - a) arb``, at every band crossing.

    Note where it is measured.  The minimum binds at the **rebalancing date**; between
    dates the mix drifts with relative performance, and re-imposing the target at the
    year end would invent a rebalancing frequency the annual grid does not have.  The
    anchor cell is at 70.00% euro after its year-12 rebalancing and 69.67% at the year
    end, and only the first of those two numbers is a compliance statement.
    """
    return av_euro_pp_at(t, "BOY") - alloc_euro(t) * av_pp_at(t, "BOY")


def euro_share_min_bound(t):
    """The lowest residual the source-charging convention permits in plan year t.

    Zero on a de-risking switch, where the UC bucket is the source and the euro
    destination receives the switch in full.  On a **reverse** switch the euro support is
    itself the source, so the charge comes out of the balance being measured and the
    share lands ``(1 - a) arb`` below the minimum — a gap the technical notes leave open,
    because they ask both for a symmetric formula and for a share at or above the line
    and the two cannot both hold in that direction.
    """
    if switch_pp(t) >= 0.0:
        return 0.0
    return -(1.0 - alloc_euro(t)) * arbitrage_charge_pp(t)


def check_euro_share_min():
    """True when the post-rebalancing euro share meets the grid minimum every year.

    Measured against :func:`euro_share_min_bound` rather than against zero, so that
    the check states what the source-charging convention actually guarantees in each
    direction.  It still catches the pitfall it exists for: charging the **destination**
    on a de-risking switch puts the residual at ``-(1 - a) arb`` where the bound is zero,
    and fails here at the first band crossing.
    """
    return bool(all(
        check_euro_share_min_resid(t) >= euro_share_min_bound(t) - 1e-8
        for t in range(1, proj_len() + 1)))


def check_glide_path_closes():
    """True when the glide path's two shares add to one in every year read.

    An input check rather than a model check.  ``alloc_uc`` reads the file's own
    ``uc_share`` column instead of computing ``1 - euro_share``, so a grid whose rows do
    not close would silently invest a fraction of each *versement* nowhere, or twice.
    """
    return bool(all(abs(alloc_euro(t) + alloc_uc(t) - 1.0) <= 1e-12
                    for t in range(1, proj_len() + 1)))


def check_commutation_identity():
    """True when the commutation returns the converted capital less the charge.

    ``commuted = rente_net a_x = annuity_cap (1 - c_arr)``.  Zero by construction while
    the commutation and the conversion use the same ``a_x`` — which is exactly what it
    is asserting.  Commuting on a *different* basis from the conversion, or at a book
    value, manufactures a gain or a loss out of nothing, and this is the line that would
    catch it.  On a cell that pays the annuity, both sides are nil.
    """
    if not is_commuted():
        return bool(commuted_pp() == 0.0)
    target = annuity_cap_pp() * (1.0 - arrear_charge_rate)           # noqa: F821
    return bool(abs(commuted_pp() - target) <= 1e-8)


def check_horizon():
    """True when the projection stops at the declared horizon.

    No *versement* arrives after settlement, ``years_to_horizon`` does not go negative,
    and the maturity claim falls in exactly one year.  A plan run past its own horizon
    keeps compounding a balance that has already been paid out, and every number after
    the horizon then looks like a projection rather than like the error it is.
    """
    n = proj_len()
    if premium_pp(n + 1) != 0.0 or years_to_horizon(n + 1) != 0:
        return False
    maturity_years = [t for t in range(1, n + 1) if pols_maturity(t) > 0.0]
    return bool(maturity_years == [n])


def result_cf():
    """Result table of cash flows, indexed by plan year t.

    ``pols_if`` is the in force at the **start** of the year, which is the weight the
    flows on that same row carry: dividing a flow by the row's ``pols_if`` returns a
    per-policy amount for the same period.  The end-of-year count the technical notes
    call ``l(t)`` is ``pols_if_at(t, "AFT_DECR")``, published in :func:`result_state` as
    ``pols_if_eoy``.

    ``av_pp`` is published beside them because it is what every benefit is measured
    against — but it is a **per policy** state variable, not a cash flow, and it is not
    part of ``net_cf``.  Multiplying it by ``pols_if`` and comparing that to a claims
    column is the mistake this layout is arranged to make visible.
    """
    ts = list(range(1, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "av_pp": [av_pp(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "claims_death": [claims(t, "DEATH") for t in ts],
            "claims_early_release": [claims(t, "EARLY_RELEASE") for t in ts],
            "claims_transfer": [claims(t, "TRANSFER") for t in ts],
            "claims_maturity": [claims(t, "MATURITY") for t in ts],
            "annuity_conversion": [annuity_conversion(t) for t in ts],
            "expenses": [expenses(t) for t in ts],
            "liability_cf": [liability_cf(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_state():
    """Result table of the glide path and the two supports, indexed by plan year t.

    The technical notes' worked-example table: years to horizon, the target euro share,
    the *versement* net of loading, the arbitrage charge, the two support balances, the
    account value, the *garantie plancher* base and the in force.  Every column is **per
    policy** except ``pols_if_eoy``.

    That last column is the notes' ``l(t)``, the count the year **ends** with, and it is
    named ``pols_if_eoy`` rather than ``pols_if`` so that it cannot be confused with the
    start-of-year exposure :func:`result_cf` publishes under the house name.  The two are
    one period apart: ``result_state()["pols_if_eoy"].loc[t]`` equals
    ``result_cf()["pols_if"].loc[t + 1]``.
    """
    ts = list(range(1, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "years_to_horizon": [years_to_horizon(t) for t in ts],
            "alloc_euro": [alloc_euro(t) for t in ts],
            "prem_to_av_pp": [prem_to_av_pp(t) for t in ts],
            "switch_pp": [switch_pp(t) for t in ts],
            "arbitrage_charge_pp": [arbitrage_charge_pp(t) for t in ts],
            "av_euro_pp": [av_euro_pp(t) for t in ts],
            "av_uc_pp": [av_uc_pp(t) for t in ts],
            "av_pp": [av_pp(t) for t in ts],
            "death_floor_pp": [death_floor_pp(t) for t in ts],
            "pols_if_eoy": [pols_if_at(t, "AFT_DECR") for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_settlement():
    """The settlement at the horizon, as a Series of per-policy amounts.

    The notes' second worked-example table: the balance settled, the capital leg, the
    capital converted, the gross and net *rente*, its monthly equivalent, the commutation
    test and its outcome, and the two mutually exclusive ways the annuity leg leaves —
    ``commuted_pp`` if the test passes and ``annuity_conversion_pp`` if it does not.
    """
    n = proj_len()
    return pd.Series(                                                # noqa: F821
        {
            "av_pp": av_pp(n),
            "annuity_factor": annuity_factor(),
            "annuity_share": annuity_share(),
            "capital_leg_pp": capital_leg_pp(),
            "capital_instalment_pp": capital_instalment_pp(),
            "annuity_cap_pp": annuity_cap_pp(),
            "rente_gross_pp": rente_gross_pp(),
            "rente_net_pp": rente_net_pp(),
            "rente_net_mth": rente_net_pp() / payment_mths,          # noqa: F821
            "is_commuted": float(is_commuted()),
            "commuted_pp": commuted_pp(),
            "annuity_conversion_pp": annuity_conversion_pp(),
            "death_floor_pp": death_floor_pp(n),
            "pols_if_eoy": pols_if_at(n, "AFT_DECR"),
        },
        name="settlement",
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

omega_age = 120

mort_be_factor = 0.85

load_rate = 0.025

charge_euro = 0.007

charge_uc = 0.007

arb_rate = 0.003

arrear_charge_rate = 0.015

return_euro = 0.0338

return_uc = 0.05

transfer_indemnity = 0.01

transfer_indemnity_years = 5

floor_cease_age = 70

death_floor_cap = 762245.0

commute_threshold_mth = 110.0

payment_mths = 12

expense_maint = 30.0

inflation_rate = 0.018

roll_fwd_tol = 1e-10

pd = ("Module", "pandas")
