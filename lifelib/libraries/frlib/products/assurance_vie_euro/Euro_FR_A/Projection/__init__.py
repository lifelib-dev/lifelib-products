# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.Euro_FR_A` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the worked example's anchor cell
    >>> Projection[7].result_pb()          # the same cell on the low scenario

``t`` counts **policy years from the valuation date**, 1-based, so ``t = 1`` is the
first projected year whatever the model point's completed duration. The attained age in
year ``t`` is ``issue_age + duration_init + t - 1`` and the completed policy duration at
the 31 December of year ``t`` — which is when the surrender decrement acts, and which
the lapse table is indexed by — is ``duration_init + t``.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent
directory, ``products/assurance_vie_euro/``, read at run time rather than stored inside
the model. The model folder therefore holds nothing but formulas — no ``_data/``, no
IOSpec, no embedded values — so a diff of the model shows logic changes only, and an
input can be edited or swapped without rewriting the model. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``Euro_FR_A`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

Each table has a filename Reference and a reader Cells, both on
:mod:`~.Euro_FR_A.Data`, reached here through the ``data`` Reference:

======================  ==============================  ==========================
Reference               Cells                           File
======================  ==============================  ==========================
model_point_file        data.model_point_table()        model_point_table.csv
mort_table_file         data.mort_table()               mort_table.csv
lapse_table_file        data.lapse_table()              lapse_table.csv
fin_rate_file           data.fin_rate_table()           fin_rate_table.csv
======================  ==============================  ==========================

.. rubric:: Naming

Cells names follow lifelib's ``savings.CashValue_SE`` and ``basiclife.BasicTerm_S``
wherever those models have an analogue — ``av_pp_at(t, timing)`` for the within-year
account value, ``pols_*`` for policy counts, plural nouns for cash flows, ``*_rate`` for
rates, ``*_pp`` for per-policy amounts, ``claims(t, kind)`` with an uppercase ``kind``
string. The technical notes use compact symbols instead. The mapping is:

=========================  ==============================  ==========================
Notes symbol               Cells                           Meaning
=========================  ==============================  ==========================
t                          (the cells argument)            Policy year from valuation
(the row)                  model_point()                   The selected model point
x                          issue_age()                     Age at `adhésion` (ALB)
x + d + t - 1              age(t)                          Attained age in year t
d                          duration_init()                 Completed years at valuation
d + t                      duration(t)                     Completed years at 31 Dec
(none)                     proj_len()                      Last projected policy year
AV(t)                      av_pp(t)                        `Épargne acquise`, start of t
(the steps)                av_pp_at(t, timing)             The balance inside year t
(fund level)               av_at(t, timing)                The same times pols_if(t)
P_g(t)                     prem_gross_pp(t)                `Versements` before charges
P(t)                       prem_to_av_pp(t)                `Versements` credited
W(t)                       withdrawals_pp(t)               `Rachats partiels` paid
B(t)                       pm_avg_pp(t)                    `Pro rata temporis` base
c, F(t)                    fee_rate(), fee_pp(t)           `Frais de gestion sur encours`
E(t)                       expenses_pp(t)                  Insurer expenses
r(t)                       r_fin(t)                        Fund financial return
Phi(t)                     fin_acct_pp(t)                  `Compte financier` balance
T(t)                       tech_acct_pp(t)                 `Compte technique` balance
s(t)                       insurer_tech_share_pp(t)        Insurer's technical share
A(t)                       pb_acct_pp(t)                   `Compte de participation`
A+(t)                      pb_min_pp(t)                    Statutory minimum PB
s*                         ts_target()                     Target `taux servi`
(target amount)            pb_target_pp(t)                 What the target costs
Q(t)                       ppb_pp(t)                       PPB, start of year t
Q_v(t)                     ppb_vintage_pp(t, v)            The vintage ledger
(ledger total)             ppb_ledger_pp(t)                The ledger rebuilt
D(t)                       ppb_dotation_pp(t)              PPB dotation in year t
(discretionary)            ppb_discr_rel_pp(t)             Release the target wants
(the clock)                ppb_forced_pp(t)                Release the clock forces
R(t)                       ppb_release_pp(t)               max of the two
(FIFO draw)                ppb_vintage_release_pp(t, v)    Which vintage paid it
X(t)                       pb_credited_pp(t)               PB credited, gross of F(t)
(before the floor)         ts_raw(t)                       Rate that implies
g                          tmg_rate()                      `Taux minimum garanti`
(the floor's cost)         insurer_topup_pp(t)             What the TMG costs the insurer
sigma(t)                   ts_net(t)                       `Taux servi` credited
s^(t)                      ts_stat(t)                      Statutory floor rate
I(t)                       int_credited_pp(t)              Net revalorisation credited
L(t)                       soc_levy_pp(t)                  `Prélèvements sociaux`
(cumulative)               soc_levy_cum_pp(t)              The levy ledger
(cumulative)               pb_cum_pp(t)                    The `effet cliquet` ledger
G(t)                       guar_floor_pp(t)                Contractual capital floor
q(t)                       mort_rate(t)                    Annual mortality rate
w(t)                       lapse_rate(t)                   Annual surrender rate
(table)                    lapse_rate_base(t)              Base rate by duration
(dynamic)                  lapse_dyn_add(t)                The `taux servi` gap term
l(t)                       pols_if(t)                      In force, start of year t
(none)                     pols_if_at(t, timing)           BEF_DECR / BEF_LAPSE / AFT_DECR
(none)                     pols_death(t), pols_lapse(t)    Decrements in year t
DB(t)                      db_pp(t)                        Death benefit per policy
CV(t)                      cv_pp(t)                        Surrender value per policy
(payout)                   claim_pp(t, kind)               Either of the two, by kind
(weighted)                 claims(t, kind)                 Benefit outgo
CF(t)                      liability_cf(t)                 The notes' outgo-positive flow
(none)                     net_cf(t)                       Its negative, income-positive
=========================  ==============================  ==========================

Five names needed care.

``pm_avg_pp`` is the notes' ``B(t)``, and it is not an average of anything the model
computes: it is ``AV(t) + 0.5 P(t) - 0.5 W(t)``, the `pro rata temporis` base struck on
the convention that `versements` and `rachats partiels` are spread evenly through the
year. Calling it ``av_avg_pp`` would suggest it was derived from ``av_pp_at``; it is an
assumption about *when* money moved, and the name says which provision it stands in for.

``ts_stat`` and ``ts_net`` are both rates **net of the management charge**, and that is
the single likeliest place to go wrong. ``pb_min_pp`` is gross of ``fee_pp`` because the
charge is a credit to the `compte technique`; the charge is subtracted **once**, on the
way from the PB amount to the rate the account actually grows by. Applying
``(1 + ts_net) (1 - fee_rate)`` afterwards would cost the policyholder 0.60% a year that
was already taken.

``ts_raw`` and ``insurer_topup_pp`` are the two halves of the notes'
``max(tmg_rate, ...)``. ``ts_raw`` is what the allocation alone produces; ``ts_net`` is
that floored at the TMG; and ``insurer_topup_pp`` is the difference in euros — what the
guarantee costs the insurer out of its own resources in a year the allocation cannot
fund it. It is nil on every model point shipped here, and see below for why no
positive-TMG cell is shipped.

``withdrawals`` is an **owner election, not a claim**. A `rachat partiel` is money the
policyholder asked for out of a balance the policyholder owns; a `rachat total` is the
same money, but it ends the contract and is a decrement, so it appears as
``claims_lapse``. Both leave the fund and both are in ``liability_cf``; keeping them
apart is what lets a reader see the difference between elective drawdown and exit.

``claims_lapse`` rather than ``claims_surr``: the column is named for the ``kind``
argument that produces it, and the decrement that produces it is the library's
``pols_lapse``.

.. rubric:: The crediting rule is an allocation with three levers

::

    fin_acct_pp(t)           = r_fin(t) (pm_avg_pp(t) + ppb_pp(t))
    tech_acct_pp(t)          = fee_pp(t) - expenses_pp(t)
    insurer_tech_share_pp(t) = max(0.10 max(tech_acct_pp(t), 0), 0.045 prem_gross_pp(t))
    pb_acct_pp(t)            = 0.85 fin_acct_pp(t) + tech_acct_pp(t)
                               - insurer_tech_share_pp(t)
    pb_min_pp(t)             = max(0, pb_acct_pp(t) - tmg_rate() pm_avg_pp(t))

Four points of substance, each of which is a listed pitfall.

**The 85% attaches to the financial account and the 90% to the technical account, not
the other way round.** "90% of the financial account and 85% of the technical result" is
the popular form and it is wrong.

**The insurer's technical share has two limbs and the 4.5%-of-premiums limb often
binds.** In the worked example's year 6 it is EUR 108.00 against EUR 28.43 for the 10%
limb. Two model points identical but for their premium stream credit different rates,
and that is the article working as written: the premiums limb vanishes on a paid-up
contract and can exceed the whole technical result on a heavily premium-paying one.

**The PPB sits inside the financial base**, because art. A132-14 computes the financial
result on average technical provisions and the PPB is one of them. Omitting it
understates the distributable amount by ``0.85 r_fin ppb_pp`` — EUR 41.81 in
worked-example year 6. The mirror error is *accreting the vintages as well*, which
distributes the PPB's return twice: :func:`ppb_vintage_pp` changes only by releases.

**``ts_stat`` is net of the charge.** For the euro support the underwriting result is nil
— the death benefit is the account value — so ``tech_acct_pp`` is the loading result
alone.

Then the three levers::

    pb_target_pp(t)      = ts_target() pm_avg_pp(t) + fee_pp(t)
    ppb_dotation_pp(t)   = max(0, pb_min_pp(t) - pb_target_pp(t))
    ppb_discr_rel_pp(t)  = min(max(0, pb_target_pp(t) - pb_min_pp(t)), ppb_pp(t))
    ppb_forced_pp(t)     = sum of the vintages whose eight years are up
    ppb_release_pp(t)    = max(ppb_discr_rel_pp(t), ppb_forced_pp(t))
    pb_credited_pp(t)    = pb_min_pp(t) - ppb_dotation_pp(t) + ppb_release_pp(t)

The **statutory floor** is what the year's result alone obliges the insurer to credit.
The **PPB** moves the credited rate above or below it: a dotation parks this year's
excess, a release spends an earlier year's. The **TMG** is a hard floor under the result,
and because it guarantees technical interest *plus* PB together it is a floor on
``ts_net``, not a separate credit stacked on top. A dotation and a forced release can
coexist in one year — this year's excess goes in while an eight-year-old vintage comes
out — and both happen in the worked example's first three rows.

Note what a dotation year does: it credits **less** than ``ts_stat(t)``, and that is
legal, because the balance goes to the PPB and not to the insurer. The invariant is an
allocation identity, not a rate inequality, and :func:`check_pb_allocation` states it as
one.

.. rubric:: The PPB vintage ledger, and why it is a ledger

A dotation carried in financial year ``v`` must be applied to mathematical provisions or
paid to policyholders **within the eight financial years following**. The model
therefore carries :func:`ppb_vintage_pp`, a per-vintage balance released FIFO by
:func:`ppb_vintage_release_pp`, so that ``v + 8`` is a real deadline on a real balance.
A single-pot PPB with an average age satisfies the rule on average and breaches it on
every vintage; :func:`check_ppb_clock` asserts that nothing survives the year after its
deadline.

The opening balance is split into ``ppb_vintages_init`` equal vintages carried in years
``0, -1, ... , 1 - ppb_vintages_init``, so eight equal vintages fall due in projection
years 8, 7, ... , 1 — a steady-state construction, and **[std]**, since no insurer
publishes its vintage profile. It matters: model point 6 carries the same EUR 4 000 in
four vintages instead of eight, and nothing is forced out until year 5.

The vintages do **not** accrete. The return on PPB assets enters the `compte financier`
through :func:`fin_acct_pp`, which is struck on ``pm_avg_pp + ppb_pp``; accreting the
vintages as well would distribute that return twice.

.. rubric:: The `effet cliquet` is not "the account never falls"

What is ratcheted is **credited PB**, not the balance. Under the `garantie nette` the
account falls by the management charge in a nil-PB year — the tables insurers publish
for exactly that case prove it — and the ratchet does not undo that.
:func:`check_cliquet` therefore asserts the ledger :func:`pb_cum_pp` is non-decreasing
and that ``int_credited_pp(t) >= 0`` and ``ts_net(t) >= tmg_rate()``, while
:func:`check_guar_floor` separately asserts the weaker contractual floor. The floor is
compared to ``av_pp(t) + soc_levy_cum_pp(t)``, because the published minimum
surrender-value tables are stated **before** social and tax levies.

.. rubric:: Behaviour keys on the gap, not on the level

::

    lapse_dyn_add(t) = lapse_dyn_a max(0, ref_rate(t) - ts_net(t) - lapse_dyn_tol)
    lapse_rate(t)    = min(lapse_cap, lapse_rate_base(t) + lapse_dyn_add(t))

French surrender behaviour keys on the gap between the `taux servi` and the rate
available elsewhere, most visibly the Livret A. The term is **one-sided**: a `taux servi`
above the reference rate does not push surrenders below the base, because the base
already reflects needs-driven withdrawals. The sign of the relationship is observed — in
2025 the euro rate was 2.63% against a 2.20% Livret A average and euro supports turned to
a net inflow after five years of net outflow — but the **magnitude** has no public
calibration and ``lapse_dyn_a``, ``lapse_dyn_tol`` and ``lapse_cap`` are the most
consequential standardizations in the model. Because the credited rate and the surrender
rate move together, the model has a feedback loop the deterministic run only samples
once.

.. rubric:: What is out of scope, and why

**No positive-TMG model point is shipped.** No contract in the source set publishes a
TMG — the two Suravenir notices state no guaranteed rate at all, BoursoVie names a TMG
without its value, MACSF names a board-set art. A132-3 rate without giving it, Afer names
a `Taux Plancher Garanti` without giving it — so the composite's TMG is 0.00% and every
model point carries it. The lever is implemented as the notes specify, and at
``tmg_rate() = 0`` the two things the notes call the TMG coincide: the art. A132-12
subtraction of "interest already credited to mathematical provisions", which belongs to a
`taux technique` fixed at subscription, and the floor on the year's total revalorisation,
which is what art. A132-3 actually guarantees. Above zero they are different quantities
and a model point would have to choose; the product specification is explicit that the
`taux technique` must not be substituted for the TMG, so no such cell is shipped and
``insurer_topup_pp`` is nil throughout.

Also out of scope, per the notes: the HCSF surrender-suspension power, which is precisely
what would change a mass-lapse answer, so a mass-lapse run here is a
**pre-management-action** result; the exceptional PPB `reprise` of art. A132-16-1, a
supervised recovery measure with no published trigger; `avances`, whose terms all three
insurers push into a separate document, so :func:`avance_on` validates rather than
guesses; `arbitrages` to and from the UC compartment, which is the sibling product; the
UC-holding bonus, since no contract publishes its grid; and the in-year `pro rata
temporis` floor rate a mid-year `dénouement` actually receives, which on an annual grid
is compressed into the full year's `taux servi` — generous to exiting policies by up to
one year's rate, concentrated in the high-lapse years, and said so rather than hidden.

There is **no maturity decrement**: the euro support has no term, and the contract's
stated maturity, where one exists, is renewable annually without limit. The projection
simply stops at :func:`proj_len`, and the survivors there are paid nothing, because that
ending is a modelling truncation and not a contractual event.
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
    """The model point's policy identifier, for reporting."""
    return str(model_point()["policy_id"])


def sex():
    """The sex (M / F) of the model point; the mortality table is sex-distinct."""
    v = model_point()["sex"]
    if v not in ("M", "F"):
        raise ValueError("invalid sex")
    return v


def issue_age():
    """x: the age at `adhésion`, age last birthday **[std]**.

    No retrieved French document fixes an age basis, and it matters little here:
    mortality drives the *timing* of the `dénouement`, not the benefit amount, because
    the death benefit is the `épargne acquise` itself.
    """
    return int(model_point()["issue_age"])


def duration_init():
    """d: completed policy years at the valuation date; 0 on a new-business cell.

    The anchor cell is five years in, so the eighth policy anniversary - the tax
    threshold that drives the surrender step - falls inside the projection, at ``t = 3``.
    """
    return int(model_point()["duration_init"])


def pols_if_init():
    """l(1): policies represented by the model point; 1.0 on a single-policy cell.

    Model point 11 carries 250 instead, which is the only difference between it and the
    anchor cell: every per-policy amount is identical and every cash flow is 250 times
    as large.
    """
    return float(model_point()["pols_if_init"])


def av_pp_init():
    """AV(1): the `épargne acquise` per policy at the valuation date."""
    return float(model_point()["av_pp_init"])


def ppb_pp_init():
    """Q(1): the PPB attributed to the model point at the valuation date.

    4.0% of the account value on the anchor cell, the ACPR's end-2025 ratio for
    individual contracts.  The PPB is **collective** and is not attributed to individual
    contracts in law; attributing a per-policy share is the device that makes the
    eight-year clock visible at model-point level **[std]**.
    """
    return float(model_point()["ppb_pp_init"])


def ppb_vintages_init():
    """The number of equal open vintages the opening PPB is split across.

    Eight on the anchor cell - a steady-state construction, since a fund that has run the
    art. A132-16 clock for eight years carries roughly one eighth of its PPB in each open
    vintage - and four on model point 6, which is the same money in younger vintages and
    therefore no forced release before year 5.  **[std]**: no insurer publishes its own
    vintage profile, and this is the assumption that decides *when* the clock bites.
    """
    n = int(model_point()["ppb_vintages_init"])
    if n < 1:
        raise ValueError("ppb_vintages_init must be at least 1")
    return n


def prem_charge_rate():
    """The `frais sur versement` (entry charge) deducted from each `versement`.

    0.00% on the composite, which is what the bank-distributed and direct contracts
    charge; 0.50% on model point 9, the observed association-contract level.
    """
    return float(model_point()["prem_charge_rate"])


def wd_prog_pp():
    """The `rachat partiel programmé` elected per year, before it starts running.

    :func:`withdrawals_pp` is what is actually paid: nil before ``wd_start_year`` and
    capped at the balance it comes out of.
    """
    return float(model_point()["wd_pp"])


def wd_start_year():
    """The first projection year in which the programmed `rachat partiel` runs."""
    return int(model_point()["wd_start_year"])


def fee_rate():
    """c: the `frais de gestion sur encours`, per year of the euro-support balance.

    0.60% on the composite - a real contract rate in the middle of the observed 0.475% to
    0.80% band, and close to the ACPR's *actual* ratio of charges paid to average
    mathematical provisions, 0.63% for individual contracts in 2025.  The level is
    **[std]**; the charge itself and its 31 December pro rata temporis timing are
    sourced.
    """
    return float(model_point()["fee_rate"])


def tmg_rate():
    """g: the `taux minimum garanti`, a floor on the year's credited rate.

    0.00% on every model point shipped here.  **No public figure exists for the TMG of
    any contract in the source set**, and the nearest public anchor - the ACPR's average
    `taux technique` of 0.32% - is a different quantity, the maximum rate at which the
    insurer's commitments are discounted, and must not be substituted.  See the Space
    docstring for why no positive-TMG cell is shipped.
    """
    return float(model_point()["tmg_rate"])


def ts_target():
    """s*: the insurer's target `taux servi`, net of charges on the balance.

    2.30% on the composite: the **bottom of the band covering 50% of encours** in 2025
    (2.3% to 2.9%), which is where an unbonused contract sits when the market mean is
    2.63%.  A target, not an outcome - the model credits it only where the statutory
    floor and the PPB allow.  Model point 3 targets 2.90%, the top of that band, and
    drains its PPB in a handful of years trying to pay it.  **[std]**: no insurer's
    forward crediting policy is public.
    """
    return float(model_point()["ts_target"])


def soc_levy_rate():
    """The `prélèvements sociaux` rate, 17.2%, withheld as interest is credited."""
    return float(model_point()["soc_levy_rate"])


def guarantee_form():
    """``net`` or ``gross``: which capital guarantee the contract carries.

    ``net`` is the `garantie nette` - the floor is `versements` net of entry charges
    **less** the annual management charges - and is the modern design, the one whose
    arithmetic the published minimum surrender-value tables actually show.  ``gross``
    drops the charge term.  The retrieved documents split cleanly between the two, and
    both designs run inside one insurer and even inside one notice, so the model carries
    the choice on the model point rather than fixing it.
    """
    v = model_point()["guarantee_form"]
    if v not in ("net", "gross"):
        raise ValueError("invalid guarantee_form")
    return v


def avance_on():
    """Whether an `avance` (policy loan) is outstanding; always False here.

    Every retrieved notice pushes the `avance` terms - the rate, the ceiling, the
    duration - into a separate document that was not retrieved, so a model point electing
    one would have to invent them.  This validates rather than guessing.
    """
    v = int(model_point()["avance_on"])
    if v != 0:
        raise ValueError("avance terms are unpublished; no avance cell is supported")
    return False


def scenario_id():
    """The financial scenario the model point runs on: ``base``, ``low`` or ``high``."""
    v = str(model_point()["scenario_id"])
    if v not in tuple(data.fin_rate_table().index.levels[0]):        # noqa: F821
        raise ValueError("unknown scenario_id")
    return v


def proj_len():
    """The last projected policy year: 40 **[std]**.

    The euro support has no term, so the horizon is a modelling choice rather than a
    contract fact.  Forty years carries the anchor cell from attained age 60 to 99 and
    covers five full turns of the eight-year PPB clock.
    """
    return proj_years                                                # noqa: F821


def age(t):
    """The attained age in policy year t: ``issue_age + duration_init + t - 1``."""
    return issue_age() + duration_init() + t - 1


def duration(t):
    """Completed policy years at the 31 December of year t: ``duration_init + t``.

    This is the index the lapse table is read by, and the reason is the tax threshold:
    the eight-year clock that switches on the reduced rate and the annual allowance runs
    from the contract's inception, not from the valuation date, and the surrender
    decrement acts at the year end.  On the anchor cell, at duration 5 in, duration 8
    falls in projection year 3.
    """
    return duration_init() + t


def r_fin(t):
    """r(t): the fund's financial return rate in year t, from the scenario path.

    A **scenario**, not a forecast.  The base path is anchored to the ACPR's observed
    `taux de rendement de l'actif` and to the reinvestment picture behind it: the 10-year
    OAT averaged 3.4% in 2025 while about 60% of fixed-coupon bonds maturing within four
    years still carried a coupon below 3%.  It dominates everything downstream - it sets
    the `compte financier`, hence the statutory floor, hence how fast the PPB drains.
    """
    tbl = data.fin_rate_table().loc[scenario_id()]                   # noqa: F821
    return float(tbl.loc[min(t, int(tbl.index.max())), "r_fin"])


def ref_rate(t):
    """The market reference rate the dynamic surrender term keys off, in year t.

    2.20% throughout, the 2025 average Livret A rate.  It is carried in the scenario
    table rather than as a Reference because in a different financial scenario the rate
    available elsewhere is a different rate too.
    """
    tbl = data.fin_rate_table().loc[scenario_id()]                   # noqa: F821
    return float(tbl.loc[min(t, int(tbl.index.max())), "ref_rate"])


def prem_gross_pp(t):
    """P_g(t): the `versements libres programmés` received in year t, before charges.

    Level, and nil on a paid-up cell.  It is not only premium income: it is the base of
    the **4.5%-of-premiums limb** of the insurer's technical share, so a paid-up contract
    and a premium-paying one credit different rates on identical funds.
    """
    return float(model_point()["prem_gross_pp"])


def prem_to_av_pp(t):
    """P(t): the `versements` credited to the account, net of the `frais sur versement`."""
    return prem_gross_pp(t) * (1.0 - prem_charge_rate())


def withdrawals_pp(t):
    """W(t): the `rachat partiel` paid during year t, per policy.

    Nil before ``wd_start_year``, then the programmed amount, spread evenly through the
    year.  Capped at the balance it comes out of - a physical constraint rather than a
    product rule, but an uncapped level election against a fund being run down eventually
    drives the account negative and every number downstream of it stays plausible enough
    to read past.

    This is an **owner election, not a claim**.  The money leaves the fund and is in
    ``liability_cf``, but it comes out of a balance the policyholder owns and it does not
    end the contract; a `rachat total` does, and appears as ``claims_lapse``.
    """
    if t < wd_start_year():
        return 0.0
    return min(wd_prog_pp(), max(0.0, av_pp(t) + prem_to_av_pp(t)))


def pm_avg_pp(t):
    """B(t): the crediting base, ``AV(t) + 0.5 P(t) - 0.5 W(t)`` **[std]**.

    The `pro rata temporis` base.  The PB is allocated "weighted by the time the sums
    were present on the fund during the year", so a payment made evenly through the year
    earns half a year's interest; crediting on the closing balance instead would give a
    full year's interest on a December payment.  The same base carries the management
    charge, which is what reproduces the published minimum surrender-value tables.

    It can reach zero only if a withdrawal election has emptied the account, in which case
    every rate below is nil rather than undefined.
    """
    return av_pp(t) + 0.5 * prem_to_av_pp(t) - 0.5 * withdrawals_pp(t)


def fee_pp(t):
    """F(t): the `frais de gestion sur encours` charged in year t, ``c B(t)``.

    Levied at 31 December value date on the average balance.  It is **inside**
    :func:`ts_net`, not a further deduction from it - see the Space docstring.
    """
    return fee_rate() * pm_avg_pp(t)


def inflation_factor(t):
    """The expense inflation factor in policy year t: ``(1 + pi)^(t-1)`` **[std]**."""
    return (1.0 + expense_inflation) ** (t - 1)                      # noqa: F821


def expenses_pp(t):
    """E(t): the insurer's expenses in year t, per policy **[std]**.

    EUR 24 a policy a year inflating at 1.5%, plus 0.35% of the average balance.  Actual
    unit expenses are not public.  The proportional part is sized so that the loading
    margin leaves the statutory `compte technique` small relative to the `compte
    financier`, which is what the market outturn implies: a 0.63% average charge rate
    against a 2.8% asset return and a 2.63% credited rate leaves little technical margin
    once distribution costs on encours are paid.  The fixed/proportional split is a
    modelling choice, and it is why a small-balance model point credits materially less:
    the fixed part dominates its `compte technique`.
    """
    return (expense_prop_rate * pm_avg_pp(t)                         # noqa: F821
            + expense_maint * inflation_factor(t))                   # noqa: F821


def fin_acct_pp(t):
    """Phi(t): the `compte financier` balance, ``r(t) (B(t) + Q(t))``.

    **The PPB is inside the base.**  Art. A132-14 computes the financial result on
    average technical provisions and the PPB is one of them, so PPB assets earn inside
    this account.  Omitting it understates the distributable amount by
    ``0.85 r_fin ppb_pp``.  The mirror error is accreting the vintage balances as well,
    which would distribute the same return twice; :func:`ppb_vintage_pp` changes only by
    releases.
    """
    return r_fin(t) * (pm_avg_pp(t) + ppb_pp(t))


def tech_acct_pp(t):
    """T(t): the `compte technique` balance, ``F(t) - E(t)``.

    For the euro support the underwriting result is nil - the death benefit is the
    `épargne acquise` and nothing more - so this is the loading result alone.
    """
    return fee_pp(t) - expenses_pp(t)


def insurer_tech_share_pp(t):
    """s(t): the insurer's share of the technical account, art. A132-11.

    ``max(0.10 max(T(t), 0), 0.045 P_g(t))``: **the greater of** 10% of the credit
    balance and 4.5% of annual premiums.  The second limb is the one implementations
    drop, and with a small technical result and a live premium stream it takes the larger
    bite - EUR 108.00 against EUR 28.43 in the worked example's year 6.  It vanishes on a
    paid-up contract, leaving the insurer only 10% of the technical result, and it can
    exceed the whole technical result on a heavily premium-paying one, which is the
    article working as written.
    """
    return max(0.10 * max(tech_acct_pp(t), 0.0),
               0.045 * prem_gross_pp(t))


def pb_acct_pp(t):
    """A(t): the `compte de participation aux résultats`, art. A132-11.

    ``0.85 Phi(t) + T(t) - s(t)``.  **The 85% attaches to the financial account** and the
    90% - what is left after the 10% limb - to the technical account, not the other way
    round.  A contract with a contractual PB percentage, 90% at Suravenir Rendement or
    100% on Afer's `Fonds Garanti`, would replace the first term with that percentage of
    the ring-fenced fund's net financial profits; the composite keeps the insurer's
    discretion and floors it at the statutory minimum.
    """
    return (0.85 * fin_acct_pp(t) + tech_acct_pp(t)
            - insurer_tech_share_pp(t))


def pb_min_pp(t):
    """A+(t): the statutory minimum `participation aux bénéfices`, art. A132-12.

    The credit balance of the participation account, less interest already credited to
    mathematical provisions, floored at zero.  With ``tmg_rate() = 0`` on every model
    point shipped here the subtraction is nil and this is ``max(0, pb_acct_pp(t))``.
    """
    return max(0.0, pb_acct_pp(t) - tmg_rate() * pm_avg_pp(t))


def ts_stat(t):
    """s^(t): the statutory floor rate, ``(A+(t) - F(t)) / B(t)``.

    What the year's result alone obliges the insurer to credit, expressed as a rate the
    account grows by - so **net of the management charge**, which is subtracted once here
    because ``pb_min_pp`` is gross of it.

    Note that ``ts_net(t) >= ts_stat(t)`` is **not** an invariant.  A dotation year
    credits less than this and that is legal: the balance goes to the PPB, not to the
    insurer.  It happens to hold on every row of the worked example only because the
    forced release always exceeds the dotation there.
    """
    if pm_avg_pp(t) <= 0.0:
        return 0.0
    return (pb_min_pp(t) - fee_pp(t)) / pm_avg_pp(t)


def pb_target_pp(t):
    """What crediting the target `taux servi` would cost, ``s* B(t) + F(t)``.

    Gross of the management charge, because ``pb_min_pp`` is, so that the two are
    comparable and the dotation and discretionary release fall out of their difference.
    """
    return ts_target() * pm_avg_pp(t) + fee_pp(t)


def ppb_pp(t):
    """Q(t): the PPB attributed to the model point at the start of year t.

    ``Q(t+1) = Q(t) + D(t) - R(t)``.  Bounded below by zero, and it never has to be
    floored: both candidate releases are bounded by the balance, so the recursion cannot
    take it negative.  A negative PPB is not a permitted state, and the exceptional
    `reprise` of art. A132-16-1 - available only on a negative technical account **and**
    an uncovered SCR, under an ACPR-approved recovery plan - is a supervised recovery
    measure, not a projection lever.

    This is the aggregate balance.  :func:`ppb_ledger_pp` rebuilds the same number from
    the vintage ledger, and :func:`check_ppb_roll_fwd` asserts the two agree - which is
    the point of keeping them separate.
    """
    if t <= 1:
        return ppb_pp_init()
    return ppb_pp(t - 1) + ppb_dotation_pp(t - 1) - ppb_release_pp(t - 1)


def ppb_vintage_first():
    """The oldest vintage index the ledger carries: ``1 - ppb_vintages_init()``.

    Eight equal opening vintages are carried in years 0, -1, ... , -7 and fall due in
    projection years 8, 7, ... , 1.
    """
    return 1 - ppb_vintages_init()


def ppb_vintage_pp(t, v):
    """Q_v(t): the remaining balance of the vintage carried in year v, at the start of t.

    The opening vintages are seeded equal.  A vintage opened by a dotation in year ``v``
    carries ``D(v)`` at the start of year ``v + 1`` and is drawn down by
    :func:`ppb_vintage_release_pp` thereafter.

    It **changes only by releases**.  The return on PPB assets is earned inside the
    `compte financier`, which is struck on ``pm_avg_pp + ppb_pp``; accreting the vintages
    as well would distribute that return twice.
    """
    if v < ppb_vintage_first() or v >= t:
        return 0.0
    if t <= 1:
        return ppb_pp_init() / ppb_vintages_init()
    if v == t - 1:
        return ppb_dotation_pp(t - 1)
    return ppb_vintage_pp(t - 1, v) - ppb_vintage_release_pp(t - 1, v)


def ppb_vintage_release_pp(t, v):
    """How much of year t's release is drawn from the vintage carried in year v.

    **FIFO, oldest vintage first.**  The statute prescribes no release order, but FIFO is
    the only order that satisfies the eight-year constraint without slack, and it is what
    makes the ledger testable: releasing LIFO would let an old vintage age past its
    deadline behind a young one that keeps being spent.
    """
    if v < ppb_vintage_first() or v >= t:
        return 0.0
    drawn = sum(ppb_vintage_release_pp(t, u)
                for u in range(ppb_vintage_first(), v))
    return min(max(0.0, ppb_release_pp(t) - drawn), ppb_vintage_pp(t, v))


def ppb_ledger_pp(t):
    """The PPB rebuilt from the vintage ledger: the sum of the open vintages.

    Computed independently of :func:`ppb_pp`, which runs its own aggregate recursion, so
    that :func:`check_ppb_roll_fwd` compares two things rather than restating one.
    """
    return sum(ppb_vintage_pp(t, v)
               for v in range(ppb_vintage_first(), max(t, 1)))


def ppb_dotation_pp(t):
    """D(t): the dotation carried to the PPB in year t, ``max(0, A+(t) - target)``.

    The excess of the year's statutory minimum over what the target `taux servi` costs.
    It opens vintage ``t``, whose eight-year clock starts running now.  No insurer
    publishes its dotation policy; only the outer bounds are public **[std]**.
    """
    return max(0.0, pb_min_pp(t) - pb_target_pp(t))


def ppb_discr_rel_pp(t):
    """The release the target `taux servi` wants, capped at the PPB balance.

    ``min(max(0, target - A+(t)), Q(t))``: what the insurer would choose to spend to
    reach its target.  When the PPB is exhausted this is nil and the model credits
    ``ts_stat(t)`` - which is exactly what happens from year 9 of the worked example, and
    the step down is a model result, not a market forecast.
    """
    return min(max(0.0, pb_target_pp(t) - pb_min_pp(t)), ppb_pp(t))


def ppb_forced_pp(t):
    """The release the eight-year clock forces in year t.

    The sum of every vintage carried in a year ``v`` with ``v + 8 <= t``: sums carried to
    the PPB must be applied to mathematical provisions or paid to policyholders within
    the eight financial years following the one they were carried in.  This is a
    **deadline**, and it can exceed what the insurer would have chosen to release - which
    is the whole reason the ledger is per vintage.
    """
    return sum(ppb_vintage_pp(t, v)
               for v in range(ppb_vintage_first(), t - 7))


def ppb_release_pp(t):
    """R(t): the PPB released in year t, ``max(discretionary, forced)``.

    A dotation and a forced release can coexist in one year - this year's excess goes in
    while an eight-year-old vintage comes out - and both happen in the worked example's
    first three rows.  Where the forced release wins, the credited rate goes **above** the
    target: year 6 of the worked example wants EUR 426.99 and must release EUR 500.00.
    """
    return max(ppb_discr_rel_pp(t), ppb_forced_pp(t))


def pb_credited_pp(t):
    """X(t): the `participation aux bénéfices` credited in year t, gross of F(t).

    ``A+(t) - D(t) + R(t)``.  The whole of the year's statutory minimum is allocated -
    credited, or carried to the PPB - and nothing of it is lost: that identity, not a
    rate inequality, is what :func:`check_pb_allocation` asserts.
    """
    return pb_min_pp(t) - ppb_dotation_pp(t) + ppb_release_pp(t)


def ts_raw(t):
    """The credited rate the allocation alone produces, before the TMG floor.

    ``(X(t) - F(t)) / B(t)``.  The management charge is subtracted **once**, here, on the
    way from a PB amount to the rate the account actually grows by; the charge is a credit
    to the `compte technique` and is already inside ``X(t)``.
    """
    if pm_avg_pp(t) <= 0.0:
        return 0.0
    return (pb_credited_pp(t) - fee_pp(t)) / pm_avg_pp(t)


def ts_net(t):
    """sigma(t): the `taux servi` credited for year t, ``max(g, ts_raw(t))``.

    A **net** rate in the ACPR's sense - net of charges on the balance and before social
    levies - and the `frais de gestion sur encours` is *inside* it.  Applying
    ``(1 + ts_net) (1 - fee_rate)`` afterwards would cost the policyholder 0.60% a year
    that was already taken, which is the likeliest implementation error on this product.

    The TMG enters as a floor rather than as a separate credit, because it guarantees
    technical interest *plus* PB together.
    """
    return max(tmg_rate(), ts_raw(t))


def insurer_topup_pp(t):
    """What the TMG floor costs the insurer out of its own resources in year t.

    ``(sigma(t) - ts_raw(t)) B(t)``: the amount the allocation could not fund and the
    guarantee obliges the insurer to add.  Nil on every model point shipped here, because
    every one carries ``tmg_rate() = 0``; it is published so that the floor's cost is a
    number rather than an invisible adjustment, and so that
    :func:`check_pb_allocation` can close exactly when it is not nil.
    """
    return (ts_net(t) - ts_raw(t)) * pm_avg_pp(t)


def int_credited_pp(t):
    """I(t): the net revalorisation credited at 31 December, ``sigma(t) B(t)``.

    The amount the contract's value actually rises by, and the base of the
    `prélèvements sociaux`.
    """
    return ts_net(t) * pm_avg_pp(t)


def soc_levy_pp(t):
    """L(t): the `prélèvements sociaux` withheld in year t, ``0.172 max(I(t), 0)``.

    Taken **as the interest is credited**, every year, whether or not anything is
    withdrawn, because the rights are expressed in euros; only the UC part is deferred to
    `dénouement`.  Levying it only at surrender is the commonest foreign-model error on
    this product, and levying it on the *account* rather than on the year's interest is
    the next one: 17.2% of EUR 100 000 is EUR 17 200, while 17.2% of the worked example's
    year-1 interest is EUR 486.35.

    The base is the interest actually inscribed on the contract, i.e. **net** of the
    management charge, which is **[std]**: art. L136-7 fixes the timing but not the base,
    and no retrieved product document says which it is.
    """
    return soc_levy_rate() * max(int_credited_pp(t), 0.0)


def soc_levy_cum_pp(t):
    """Cumulative `prélèvements sociaux` deducted before the start of year t.

    Non-decreasing.  It is added back to the account in :func:`check_guar_floor`, because
    the published minimum surrender-value tables are stated **before** social and tax
    levies.
    """
    if t <= 1:
        return 0.0
    return soc_levy_cum_pp(t - 1) + soc_levy_pp(t - 1)


def pb_cum_pp(t):
    """The `effet cliquet` ledger: PB credited since the valuation date, before year t.

    Non-decreasing by construction, since credited PB is definitively acquired and cannot
    be called back.  What is ratcheted is **this**, not the account balance - see
    :func:`check_cliquet`.
    """
    if t <= 1:
        return 0.0
    return pb_cum_pp(t - 1) + max(pb_credited_pp(t - 1), 0.0)


def av_pp_at(t, timing):
    """The `épargne acquise` per policy at a point inside policy year t.

    ``"BEF_PREM"``
        the opening balance, ``AV(t)``; the same number as :func:`av_pp`.

    ``"AFT_PREM"``
        after the year's `versements`, credited net of the entry charge.

    ``"AFT_WD"``
        after the year's `rachats partiels`.

    ``"AFT_INT"``
        after the 31 December revalorisation.  **The `frais de gestion`
        is inside** ``I(t)``, not a further deduction from this balance.

    The `prélèvements sociaux` are withheld after this last point, and
    ``av_pp(t + 1) = av_pp_at(t, "AFT_INT") - soc_levy_pp(t)``.  The levy is not given a
    timing string of its own because it is not a movement on the contract in the same
    sense: it is a tax the insurer withholds and remits, and keeping it out of the timing
    ladder is what keeps it out of ``net_cf``.
    """
    if timing == "BEF_PREM":
        return av_pp(t)
    if timing == "AFT_PREM":
        return av_pp(t) + prem_to_av_pp(t)
    if timing == "AFT_WD":
        return av_pp_at(t, "AFT_PREM") - withdrawals_pp(t)
    if timing == "AFT_INT":
        return av_pp_at(t, "AFT_WD") + int_credited_pp(t)
    raise ValueError("invalid timing")


def av_pp(t):
    """AV(t): the `épargne acquise` per policy at the start of policy year t.

    ``AV(t+1) = AV(t) + P(t) - W(t) + I(t) - L(t)``.  The social levy is **inside** this
    recursion, because it is money that genuinely leaves the contract each year; a model
    that defers it to surrender overstates the account and every benefit measured on it.
    """
    if t <= 1:
        return av_pp_init()
    return av_pp_at(t - 1, "AFT_INT") - soc_levy_pp(t - 1)


def av_at(t, timing):
    """The fund-level `épargne acquise` at a point inside year t: per policy times l(t).

    Every aggregate in this model is the per-policy amount times the start-of-year in
    force, which is what makes :func:`check_av_roll_fwd` an exact identity: claims are
    struck on ``av_pp(t + 1)``, the same balance the survivors carry forward.
    """
    return av_pp_at(t, timing) * pols_if(t)


def av(t):
    """The fund-level `épargne acquise` at the start of policy year t."""
    return av_pp(t) * pols_if(t)


def guar_floor_pp(t):
    """G(t): the contractual capital guarantee floor at the start of year t.

    ``G(t+1) = G(t) + P(t) - W(t) - F(t)`` on the `garantie nette`, which is the
    composite's form: `versements` net of entry charges, **less** the annual management
    charges.  The ``gross`` variant drops the charge term.

    For an in-force cell the premium history before the valuation date is not carried on
    the model point, so the floor is seeded at ``av_pp_init()`` **[std]** - deliberately
    conservative, since the true floor on a five-year-old contract sits below its account
    value by the interest already credited.
    """
    if t <= 1:
        return av_pp_init()
    prev = (guar_floor_pp(t - 1) + prem_to_av_pp(t - 1)
            - withdrawals_pp(t - 1))
    if guarantee_form() == "net":
        prev = prev - fee_pp(t - 1)
    return prev


def mort_rate(t):
    """q(t): the annual best-estimate mortality rate in policy year t **[std]**.

    The shipped table rate times ``mort_be_factor``.  Both are placeholders: the
    statutory tables annexed to the arrêté du 1er août 2006 are cited in the documents
    but not redistributed here, so the table is an INSEE-shaped population proxy and the
    factor a crude allowance for population mortality being heavier than insured
    experience.  The two together give the notes' placeholder ``q = 0.0060`` at male age
    60 exactly.

    Mortality here is a **timing** assumption, not an amount assumption: the death
    benefit is the `épargne acquise`, so the basis affects only *when* the account is
    released - far less than in any protection product.
    """
    x = min(age(t), omega_age)                                       # noqa: F821
    return min(1.0, float(data.mort_table().loc[                     # noqa: F821
        (sex(), x), "mort_rate"]) * mort_be_factor)                  # noqa: F821


def lapse_rate_base(t):
    """The table annual surrender rate at the year-end policy duration **[std]**.

    4% at durations 1-7, **8% at duration 8**, 5% at durations 9 and beyond; durations
    past the table take its last row.  The duration-8 step is the tax threshold, not a
    behavioural guess.
    """
    tbl = data.lapse_table()                                         # noqa: F821
    return float(tbl.loc[min(duration(t), int(tbl.index.max())),
                         "lapse_rate_base"])


def lapse_dyn_add(t):
    """The dynamic surrender addition in year t **[std]**.

    ``a max(0, ref_rate(t) - ts_net(t) - tol)``: additive in the gap between the market
    reference rate and the `taux servi`.  **One-sided** - a `taux servi` above the
    reference rate does not push surrenders below the base, because the base already
    reflects needs-driven withdrawals.  A two-sided variant is a scenario switch, not the
    base.

    ``a`` and ``tol`` have no public calibration and are the largest unanchored numbers
    in this model.
    """
    return lapse_dyn_a * max(0.0, ref_rate(t) - ts_net(t)            # noqa: F821
                             - lapse_dyn_tol)                        # noqa: F821


def lapse_rate(t):
    """w(t): the annual `rachat total` rate applied at the end of year t.

    The base rate plus the dynamic addition, capped.  The cap is what stops a wide
    `taux servi` gap producing a surrender rate no fund could meet in an orderly way -
    and a mass-lapse run here is a **pre-management-action** number, because the HCSF's
    power to freeze surrenders for up to six consecutive months is precisely what would
    change the answer and is not modelled.
    """
    return min(lapse_cap, lapse_rate_base(t) + lapse_dyn_add(t))     # noqa: F821


def pols_if(t):
    """l(t): the number of policies in force at the **start** of policy year t."""
    if t <= 1:
        return pols_if_init()
    return pols_if_at(t - 1, "AFT_DECR")


def pols_if_at(t, timing):
    """The number of policies in force at a point inside policy year t.

    ``"BEF_DECR"``
        the start of the year, before any decrement; :func:`pols_if`.

    ``"BEF_LAPSE"``
        after deaths, before `rachats totaux` - the processing order is
        death before surrender **[std]**.

    ``"AFT_DECR"``
        the end-of-year count.

    Both decrements act at 31 December **after** crediting, so an exiting policy takes the
    full year's `taux servi`.  That follows the contracts that credit the annual PB to
    sums surrendered during the year, and the alternative - the announced floor rate
    `pro rata temporis`, which with a zero TMG is no in-year interest at all - is a
    documented departure rather than the base.
    """
    if timing == "BEF_DECR":
        return pols_if(t)
    if timing == "BEF_LAPSE":
        return pols_if(t) * (1.0 - mort_rate(t))
    if timing == "AFT_DECR":
        return pols_if_at(t, "BEF_LAPSE") * (1.0 - lapse_rate(t))
    raise ValueError("invalid timing")


def pols_death(t):
    """Deaths in policy year t, against the start-of-year in force."""
    return pols_if(t) * mort_rate(t)


def pols_lapse(t):
    """`Rachats totaux` at the end of policy year t, from the survivors of mortality."""
    return pols_if_at(t, "BEF_LAPSE") * lapse_rate(t)


def db_pp(t):
    """DB(t): the death benefit per policy, the `épargne acquise` and nothing more.

    ``av_pp(t + 1)``: the balance after the year's crediting, because the decrement acts
    at 31 December after the revalorisation.  There is **no additional death guarantee**
    on the euro support - the optional riders price the *UC* capital at risk - and adding
    an uplift here is a listed pitfall.
    """
    return av_pp(t + 1)


def cv_pp(t):
    """CV(t): the surrender value per policy, with **no penalty**.

    The same balance as the death benefit.  The `frais de rachat` is 0.00% on every
    retrieved contract, and settlement is two months by statute and thirty days by
    contract.
    """
    return av_pp(t + 1)


def claim_pp(t, kind):
    """The payout per claim in policy year t, by kind.

    ``"DEATH"``
        :func:`db_pp` - the `épargne acquise`, no uplift.

    ``"LAPSE"``
        :func:`cv_pp` - the same amount, no penalty.

    They are equal, and that equality is the product statement: on the euro support the
    death benefit *is* the surrender value.  Both are computed so that an implementation
    which quietly added a death uplift or a surrender charge would show up as a
    difference rather than disappear into a shared cells.

    There is no ``"MATURITY"``: the euro support has no term.
    """
    if kind == "DEATH":
        return db_pp(t)
    if kind == "LAPSE":
        return cv_pp(t)
    raise ValueError("invalid kind")


def claims(t, kind=None):
    """Benefit outgo in policy year t, by kind; the total when kind is omitted.

    ``"DEATH"`` and ``"LAPSE"`` weight :func:`claim_pp` by the corresponding decrement.
    `Rachats partiels` are **not** here: they are an owner election and live in
    :func:`withdrawals`.
    """
    if kind is None:
        return sum(claims(t, k) for k in ("DEATH", "LAPSE"))
    if kind == "DEATH":
        return claim_pp(t, "DEATH") * pols_death(t)
    if kind == "LAPSE":
        return claim_pp(t, "LAPSE") * pols_lapse(t)
    raise ValueError("invalid kind")


def premiums(t):
    """`Versements` credited to the fund in policy year t, an inflow."""
    return prem_to_av_pp(t) * pols_if(t)


def withdrawals(t):
    """`Rachats partiels` paid in policy year t - an owner election, not a claim."""
    return withdrawals_pp(t) * pols_if(t)


def expenses(t):
    """The insurer's expenses in policy year t, weighted by the in force."""
    return expenses_pp(t) * pols_if(t)


def int_credited(t):
    """The revalorisation credited to the fund in policy year t.

    A **state movement**, reported beside the flows and not summed into
    :func:`liability_cf`: it moves the liability, it does not settle it.
    """
    return int_credited_pp(t) * pols_if(t)


def soc_levy(t):
    """The `prélèvements sociaux` withheld in policy year t.

    Reported in its own column and **excluded from** :func:`net_cf`, because it is a
    policyholder tax the insurer withholds and remits to the State - neither a benefit nor
    an insurer expense.  A fund-level asset projection adds it back as an outflow in one
    step.
    """
    return soc_levy_pp(t) * pols_if(t)


def liability_cf(t):
    """CF(t): the notes' **outgo-positive** liability cash flow in policy year t.

    ``claims_death + claims_lapse + withdrawals + expenses - premiums``.  The
    revalorisation and the social levy are not in it: the first is a state movement and
    the second is a tax.
    """
    return (claims(t, "DEATH") + claims(t, "LAPSE") + withdrawals(t)
            + expenses(t) - premiums(t))


def net_cf(t):
    """The net cash flow of policy year t, **income positive**: ``-liability_cf(t)``.

    The library's sign convention.  Both orientations are published so that neither the
    notes' reader nor the library's has to negate anything in their head.
    """
    return -liability_cf(t)


def check_av_roll_fwd_resid(t):
    """The fund-level `épargne acquise` roll-forward residual in year t; zero everywhere.

    ``av(t) + premiums - withdrawals + int_credited - soc_levy - claims_death
    - claims_lapse - av(t+1)``, rebuilt from the reported cash flows rather than from the
    per-policy recursion.
    """
    return (av(t) + premiums(t) - withdrawals(t) + int_credited(t)
            - soc_levy(t) - claims(t, "DEATH") - claims(t, "LAPSE")
            - av(t + 1))


def check_av_roll_fwd():
    """True when the fund-level account roll-forward closes in every projected year.

    This is the check that catches a **misindexed recursion**.  The identity is exact only
    because claims are struck on ``av_pp(t + 1)`` - the same balance the survivors carry
    forward - and only because both decrements act after the year's crediting.  Strike
    the claims on ``av_pp(t)`` instead, or apply a decrement before the revalorisation,
    and the residual is the year's interest on the exiting policies: a number small enough
    to look like rounding and large enough to be wrong.
    """
    scale = max(av_pp_init() * pols_if_init(), 1.0)
    return all(abs(check_av_roll_fwd_resid(t)) <= 1e-9 * scale
               for t in range(1, proj_len() + 1))


def check_ppb_roll_fwd_resid(t):
    """The PPB residual in year t: the ledger tie plus the balance roll-forward.

    Both terms are zero when the model is right.  They are reported as one signed number
    and asserted separately in :func:`check_ppb_roll_fwd`, so that a cancellation between
    them cannot pass.
    """
    roll = (ppb_pp(t + 1) - ppb_pp(t) - ppb_dotation_pp(t)
            + ppb_release_pp(t))
    tie = ppb_ledger_pp(t) - ppb_pp(t)
    return roll + tie


def check_ppb_roll_fwd():
    """True when the PPB balance and its vintage ledger agree, every year.

    Two independent statements, asserted separately.  The **balance** runs its own
    recursion ``Q(t+1) = Q(t) + D(t) - R(t)``; the **ledger** is the sum of the per-vintage
    balances, each rolled forward by its own FIFO draw.  Nothing forces them to agree, and
    a release that drew more or less than the aggregate said - the ordinary consequence of
    an off-by-one in the FIFO loop - breaks the tie while leaving both numbers plausible.
    The PPB is also asserted non-negative here.
    """
    for t in range(1, proj_len() + 1):
        if ppb_pp(t) < -1e-9:
            return False
        if abs(ppb_ledger_pp(t) - ppb_pp(t)) > 1e-8:
            return False
        if abs(ppb_pp(t + 1) - ppb_pp(t) - ppb_dotation_pp(t)
               + ppb_release_pp(t)) > 1e-8:
            return False
    return True


def check_ppb_clock_resid(t):
    """What is left at the start of year t in vintages whose eight years are up; zero.

    A vintage carried in year ``v`` must be exhausted by the end of year ``v + 8``, so at
    the start of year ``t`` nothing may survive in any vintage with ``v <= t - 9``.  Note
    the index: a vintage with ``v = t - 8`` is due *during* year t and is still standing at
    its start - that is what :func:`ppb_forced_pp` is about to take out.
    """
    return sum(ppb_vintage_pp(t, v)
               for v in range(ppb_vintage_first(), t - 8))


def check_ppb_clock():
    """True when no PPB vintage survives the year after its eight-year deadline.

    This is the check that catches a **LIFO release**.  Releasing newest-first meets the
    aggregate PPB recursion exactly and satisfies :func:`check_ppb_roll_fwd`, while
    letting an old vintage sit past its statutory deadline behind young ones that keep
    being spent - a breach that is invisible in the balance and obvious in the ledger.
    """
    return all(abs(check_ppb_clock_resid(t)) <= 1e-8
               for t in range(1, proj_len() + 1))


def check_pols_roll_fwd_resid(t):
    """The in-force roll-forward residual in policy year t; zero everywhere."""
    return (pols_if(t) - pols_if(t + 1) - pols_death(t) - pols_lapse(t))


def check_pols_roll_fwd():
    """True when the in-force roll-forward closes in every projected year.

    Rebuilt from the decrements rather than from :func:`pols_if_at`, so that the
    processing order - deaths first, then surrenders on the survivors - is asserted
    rather than assumed.  Applying both decrements to the start-of-year count instead
    understates the exits by ``q w l(t)`` a year.
    """
    scale = max(pols_if_init(), 1.0)
    return all(abs(check_pols_roll_fwd_resid(t)) <= 1e-10 * scale
               for t in range(1, proj_len() + 1))


def check_pb_allocation_resid(t):
    """The allocation residual in policy year t; zero everywhere.

    ``I(t) + F(t) + D(t) - R(t) - A+(t) - topup(t)``: the whole of the year's statutory
    minimum is either credited or carried to the PPB, plus whatever an earlier year's
    vintage released, plus whatever the TMG obliged the insurer to add.
    """
    return (int_credited_pp(t) + fee_pp(t) + ppb_dotation_pp(t)
            - ppb_release_pp(t) - pb_min_pp(t) - insurer_topup_pp(t))


def check_pb_allocation():
    """True when the year's statutory minimum PB is fully accounted for, every year.

    **This residual is zero by construction in a correct implementation**, since
    ``pb_credited_pp`` is defined as ``A+(t) - D(t) + R(t)`` and ``int_credited_pp`` is
    that less the charge.  What it catches is the ways of getting there that are not
    correct, because the identity is stated in terms of the *rate* round trip rather than
    of the amounts: deducting the management charge a second time inside ``ts_net``,
    striking the rate on the closing balance instead of the `pro rata temporis` base,
    stacking the TMG on top of the allocation instead of flooring it, or dropping a
    dotation on the floor. Each of those leaves every printed number plausible and this
    residual non-zero.

    Note what the invariant is **not**.  ``ts_net(t) >= ts_stat(t)`` is not an invariant:
    a dotation year credits less than the statutory floor rate and that is legal, because
    the balance goes to the PPB and not to the insurer.
    """
    scale = max(av_pp_init(), 1.0)
    return all(abs(check_pb_allocation_resid(t)) <= 1e-9 * scale
               for t in range(1, proj_len() + 1))


def check_cliquet_resid(t):
    """The `effet cliquet` residual in policy year t; zero everywhere.

    Three violations rolled into one signed number, each of which can only push it above
    zero: a break in the cumulative-PB ratchet, negative credited interest, and a
    credited rate below the TMG.
    """
    ratchet = (pb_cum_pp(t + 1) - pb_cum_pp(t)
               - max(pb_credited_pp(t), 0.0))
    return (ratchet - min(0.0, int_credited_pp(t))
            - min(0.0, ts_net(t) - tmg_rate()) * pm_avg_pp(t))


def check_cliquet():
    """True when credited PB is never negative and the ratchet never falls.

    Credited `participation aux bénéfices` is definitively acquired and cannot be called
    back, so the credited interest can never be negative.  **In this implementation the
    non-negativity is enforced by construction**, by the ``max(tmg_rate(), ...)`` in
    :func:`ts_net`, so that half of the residual cannot move; the check is published
    because the constraint is a contractual fact about the product and a re-implementation
    that let a bad year claw back interest - by netting the management charge against the
    revalorisation, say, or by carrying a negative ``pb_acct_pp`` through to the account -
    would break it. The ratchet half is not by construction: it compares two independent
    recursions.

    What this does **not** say is that the account never falls.  Under the `garantie
    nette` the balance falls by the management charge in a nil-PB year, and the tables
    insurers publish for exactly that case prove it.  Testing the cliquet as "``av_pp`` is
    non-decreasing" is a listed pitfall; :func:`check_guar_floor` is the weaker and
    correct statement about the balance.
    """
    return all(abs(check_cliquet_resid(t)) <= 1e-8
               for t in range(1, proj_len() + 1))


def check_guar_floor_resid(t):
    """The capital-guarantee shortfall in policy year t; zero when the floor holds.

    ``max(0, G(t) - (AV(t) + cumulative levies))``.  The floor is compared to the account
    **before** cumulative social levies, because the published minimum surrender-value
    tables are stated before social and tax levies.
    """
    return max(0.0, guar_floor_pp(t)
               - (av_pp(t) + soc_levy_cum_pp(t)))


def check_guar_floor():
    """True when the contractual capital floor is met in every projected year.

    A genuine inequality rather than an identity: nothing in the recursions enforces it,
    and on a path with a `taux servi` at or near zero for long enough the `garantie nette`
    floor and the account converge and then cross.  On the shipped scenarios it never
    binds, and knowing that it does not bind is the reason to check it.
    """
    return all(check_guar_floor_resid(t) <= 1e-6
               for t in range(1, proj_len() + 1))


def result_cf():
    """Result table of cash flows, indexed by policy year t.

    ``pols_if`` is the start-of-year count that weights every flow on the row.
    ``int_credited`` and ``soc_levy`` are published beside the flows and are **not** in
    ``net_cf``: the first is a state movement and the second is a policyholder tax the
    insurer remits.  ``net_cf`` is income-positive; ``liability_cf`` is the notes'
    outgo-positive orientation, verbatim.
    """
    ts = list(range(1, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "withdrawals": [withdrawals(t) for t in ts],
            "claims_death": [claims(t, "DEATH") for t in ts],
            "claims_lapse": [claims(t, "LAPSE") for t in ts],
            "expenses": [expenses(t) for t in ts],
            "int_credited": [int_credited(t) for t in ts],
            "soc_levy": [soc_levy(t) for t in ts],
            "liability_cf": [liability_cf(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_pb():
    """Result table of the crediting machinery, per policy, indexed by policy year t.

    The two tables of the notes' worked example side by side: the `compte de
    participation aux résultats` and the statutory floor rate it implies, the PPB
    dotation, release and balance, the `taux servi` actually credited, and the
    `épargne acquise` the whole apparatus moves.
    """
    ts = list(range(1, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "r_fin": [r_fin(t) for t in ts],
            "pm_avg_pp": [pm_avg_pp(t) for t in ts],
            "fin_acct_pp": [fin_acct_pp(t) for t in ts],
            "tech_acct_pp": [tech_acct_pp(t) for t in ts],
            "insurer_tech_share_pp": [insurer_tech_share_pp(t) for t in ts],
            "pb_min_pp": [pb_min_pp(t) for t in ts],
            "ts_stat": [ts_stat(t) for t in ts],
            "ppb_dotation_pp": [ppb_dotation_pp(t) for t in ts],
            "ppb_release_pp": [ppb_release_pp(t) for t in ts],
            "ppb_pp": [ppb_pp(t + 1) for t in ts],
            "ts_net": [ts_net(t) for t in ts],
            "av_pp": [av_pp(t) for t in ts],
            "int_credited_pp": [int_credited_pp(t) for t in ts],
            "soc_levy_pp": [soc_levy_pp(t) for t in ts],
            "guar_floor_pp": [guar_floor_pp(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

proj_years = 40

omega_age = 120

mort_be_factor = 0.8

expense_maint = 24.0

expense_inflation = 0.015

expense_prop_rate = 0.0035

lapse_dyn_a = 4.0

lapse_dyn_tol = 0.0025

lapse_cap = 0.3

pd = ("Module", "pandas")
