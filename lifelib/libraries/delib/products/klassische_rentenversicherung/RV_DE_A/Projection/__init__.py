# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.RV_DE_A` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the worked example's anchor cell
    >>> Projection.point_id = 6            # or switch the default

``t`` counts **policy years** from inception, 1-based: policy year ``t`` runs from the
anniversary at attained age ``issue_age + t - 1`` to the next, and the calendar year of the
row is ``issue_year + t - 1``. A new-business model point opens at ``t = 1``; an in-force
point that has already run ``duration_init`` complete policy years opens at
``t = duration_init + 1``, carrying its opening balances on the model point. That is what
lets one generational mortality surface and one declared-rate path serve a book of mixed
vintages.

``proj_len() = omega_age() - issue_age`` is the **last** projected policy year, so
``result_cf().index[-1] == proj_len()``. A life annuity has no term, so the projection ends
where the annuitant cannot survive further rather than at a fixed horizon: on the anchor
cell, ``t = 1 ... 71``, running to attained age 120.

The *Rentenbeginn* falls at the **end of policy year** ``n = aufschub_y``, which is the same
instant as the start of policy year ``n + 1``. Accumulation rows are ``t <= n``; payout rows
are ``t > n``. The *Kapitalabfindung* is paid in row ``n``; the first annuity instalment
falls in row ``n + 1``. On the anchor cell ``n = 17``, the *Rentengarantiezeit* covers
``t = 18 ... 27`` and the survivor-weighted annuity runs from ``t = 28`` to ``t = 71``.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent directory,
``products/klassische_rentenversicherung/``, read at run time rather than stored inside the
model. The model folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no
embedded values — so a diff of the model shows logic changes only, and an input can be
edited or swapped without rewriting the model. This follows ``annuallife.TradLife_A``;
contrast ``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``RV_DE_A`` folder without its parent's CSVs produces a model that reads and then fails on
first evaluation.

Each table has a filename Reference and a reader Cells, both on :mod:`~.RV_DE_A.Data`,
reached here through the ``data`` Reference:

========================  =================================  ==========================
Reference                 Cells                              File
========================  =================================  ==========================
model_point_file          data.model_point_table()           model_point_table.csv
mort_file                 data.mort_table()                  mort_table.csv
decl_rate_file            data.decl_rate_table()             decl_rate_table.csv
rentenfaktor_file         data.rentenfaktor_table()          rentenfaktor_table.csv
charge_file               data.charge_table()                charge_table.csv
lapse_file                data.lapse_table()                 lapse_table.csv
freq_load_file            data.freq_load_table()             freq_load_table.csv
param_file                data.param_table()                 param_table.csv
========================  =================================  ==========================

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` and ``savings.CashValue_SE``
wherever those models have an analogue — ``pols_*`` for policy counts, ``av_*`` for account
values, plural nouns for cash flows, ``*_rate`` for rates, ``*_pp`` for per-policy amounts,
``claims(t, kind)`` with an uppercase ``kind`` string, ``av_pp_at(t, timing)`` and
``pols_if_at(t, timing)`` for the within-year reads. The technical notes use compact
actuarial symbols instead. The mapping is:

==========================  ==============================  ==========================
Notes symbol                Cells                           Meaning
==========================  ==============================  ==========================
(none)                      model_point()                   The selected model point row
N = omega - issue_age       proj_len()                      Last policy year
t0 = duration_init + 1      (frame start)                   First projected policy year
x(t)                        age(t)                          Attained age in year t
tau(t)                      calendar_year(t)                Calendar year of year t
omega                       omega_age()                     Terminal age of the proxy
n                           (model point aufschub_y)        Deferment years
m                           (model point rgz_years)         Rentengarantiezeit years
kappa                       (model point kapitalwahl_rate)  Commutation take-up
l(t)                        pols_if(t)                      In force at the start of t
l(t) - D, l(t+1)            pols_if_at(t, timing)           BEF_DECR / BEF_LAPSE / AFT_DECR
a(t)                        pols_annuity(t)                 Count the instalment is paid on
P(t)                        prem_pp(t)                      Gross premium in year t
P_sched(t)                  prem_pp_sched(t)                The premium as written at issue
phi                         freq_load()                     Ratenzahlungszuschlag
(sum of P_sched)            beitragssumme_pp()              Zillmer base
alpha_total                 alpha_total_pp()                Total acquisition charge
alpha(t)                    charge_acq_pp(t)                Zillmered acquisition charge
alpha~(t)                   charge_acq_spread_pp(t)         Evenly spread acquisition charge
beta(t)                     charge_prem_pp(t)               Premium charge
gamma(t)                    charge_admin_pp(t)              Reserve-based charge
rho(t)                      charge_risk_pp(t)               Risikobeitrag
(none)                      nar_pp(t)                       Net amount at risk
S(t)                        prem_to_av_pp(t)                Sparbeitrag
C(t)                        charge_from_av_pp(t)            Charge met from the account
V(t)                        av_pp(t)                        Deckungskapital per policy
V after prem / after int    av_pp_at(t, timing)             BEF_PREM / AFT_PREM / AFT_INT
A(t)                        av_sur_pp(t)                    Ansammlungsguthaben per policy
Vtilde(t)                   av_spread_pp(t)                 Sec. 169(3) parallel account
Delta(t)                    spread_diff_pp(t)               Vtilde(t) - V(t)
i                           int_rate_guar()                 Rechnungszins
d(t)                        decl_rate(t)                    Declared laufende Verzinsung
b(t)                        bonus_rate(t)                   max(0, d(t) - i)
q*(t)                       mort_rate_guar(t)               First-order mortality
q(t)                        mort_rate(t)                    Best-estimate mortality
(table)                     mort_rate_at_age(x)             Base-year table rate at age x
(trend)                     improve_rate(x)                 Annual improvement at age x
w(t)                        lapse_rate(t)                   Surrender rate
Dcheck(t)                   db_base_pp(t)                   Start-of-year death measure
D(t)                        db_pp(t)                        Death benefit paid in year t
Rbar(t)                     cv_tariff_pp(t)                 Tariff surrender value
Runder(t)                   cv_floor_pp(t)                  Sec. 169(3) floor
R(t)                        cv_pp(t)                        Surrender value paid
K                           capital_conv_pp(t)              Conversion capital
f_g                         annuity_rate_guar()             Garantierter Rentenfaktor
f_c                         annuity_rate_curr()             Aktueller Rentenfaktor
f                           annuity_rate_appl()             max(f_g, f_c)
G                           annuity_guar_mth_pp()           Garantierte Rente, monthly
U(t)                        annuity_sur_mth_pp(t)           Ueberschussrente, monthly
12 (G + U(t))               annuity_pp(t)                   Annual annuity per policy
net_cf(t)                   net_cf(t)                       Net cash flow, income positive
liability_cf(t)             liability_cf(t)                 The same stream, outgo positive
==========================  ==============================  ==========================

Four namings needed care.

``db_base_pp`` and ``db_pp`` are two different quantities with deliberately similar names.
``db_base_pp(t)`` is the death benefit measured on **start-of-year** balances and exists
only to strike the *Risikobeitrag*, because a risk charge computed on the post-charge
balance would make the recursion circular. ``db_pp(t)`` is what a death claim actually pays,
on **end-of-year** balances. Both are published so the difference is visible rather than
buried.

``charge_*`` and ``expense_*`` are not synonyms. A **charge** is a deduction the tariff
makes from the premium or the *Deckungskapital*: it moves money inside the contract and
produces no cash flow. An **expense** is the insurer's own best-estimate outgo and is a cash
flow. ``expenses(t)`` is invariant to ``beta_rate`` and ``gamma_rate``; ``av_pp(t+1)`` is
not. Booking the *Kostenbeitrag* as an expense inflates outgo by the whole charge load and
is the commonest way to make a German model look conservative.

``av_pp`` and ``av_sur_pp`` are two accounts, not one balance split in two. The
*Deckungskapital* carries the guarantee and is credited at ``int_rate_guar()``; the
*Ansammlungsguthaben* is the *verzinsliche Ansammlung* side account and is credited at
``decl_rate(t)`` on its own balance plus ``bonus_rate(t)`` on the *Deckungskapital*'s
post-premium base. Each has its own roll-forward check.

``pols_if`` and ``pols_annuity`` differ inside the *Rentengarantiezeit* and nowhere else.
``pols_if(t)`` is the start-of-year count and the weight on every accumulation-phase cash
flow of the same ``result_cf()`` row; ``pols_annuity(t)`` is the count the annuity
instalment is *paid on*, which inside the guarantee window is the annuitised count and not
the survivors.

.. rubric:: The declared rate contains the guarantee

This is the first thing to get right about a German profit-participating contract and the
first listed modeling pitfall. The *laufende Verzinsung* is the *Garantieverzinsung* **plus**
the *laufende Zinsüberschussbeteiligung*, not a surplus on top of the guarantee, so::

    bonus_rate(t) = max(0, decl_rate(t) - int_rate_guar())

and the two credits together deliver ``decl_rate(t)`` on the post-premium *Deckungskapital*
and never more. On the anchor cell that is 1,00 % into ``int_credited_pp`` and 1,55 % into
``bonus_credited_pp`` against a 2,55 % declaration. On model point 6 — a 2,75 % legacy
vintage against the same declaration — ``bonus_rate(t)`` is **zero at every t** while
``int_credited_pp(t)`` is the largest in the table. A model that credits 1,00 % *and* 2,55 %
overstates the anchor cell's *Deckungskapital* by more than half.

.. rubric:: The guarantee vintage is a model-point attribute

``int_rate_guar()`` reads the model point, not a Reference. A German life book is a layered
stack of guarantee vintages: the *Höchstrechnungszins* applies to contracts concluded while
it is in force and existing contracts keep the rate they were written on. Points 1, 6 and 14
credit 1,00 %, 2,75 % and 0,90 % in the same run, from the same tables, and a single global
rate would change point 6's *Deckungskapital* at *Rentenbeginn* by more than a fifth.

.. rubric:: The within-year order, which no source fixes

Premium in advance, then the charges, then the *Rechnungszins* on what is left::

    av_pp_at(t, "AFT_PREM") = av_pp(t) + prem_to_av_pp(t) - charge_from_av_pp(t)
    int_credited_pp(t)      = int_rate_guar() * av_pp_at(t, "AFT_PREM")
    av_pp_at(t, "AFT_INT")  = av_pp_at(t, "AFT_PREM") + int_credited_pp(t)

**This ordering is a standardization.** No document in this product's corpus fixes the
sequence of premium credit, charge deduction and interest accrual, and it is the single most
consequential such choice in the model: crediting interest on the opening balance alone
changes year-one interest by the whole of ``i x (prem_to_av_pp(1) - charge_from_av_pp(1))``.

Two further conventions inside the decomposition are [std] and are worth naming.
``charge_risk_pp`` and ``charge_admin_pp`` are struck on **start-of-year** balances, or the
recursion is circular. And charges are met **from the premium where there is one and from
the *Deckungskapital* where there is not**: ``charge_from_av_pp(t)`` is what makes a
*Beitragsfreistellung* cost something instead of being free.

.. rubric:: The Sec. 169(3) floor, carried as a difference

The surrender value is floored at the *Deckungskapital* that results from spreading the
charged acquisition costs **evenly over the first five contract years**. The two accounts
differ only in that charge, so the model carries the difference rather than a second full
recursion::

    spread_diff_pp_at(t, "AFT_INT") = (Delta(t) + alpha(t) - alpha~(t)) * (1 + i)

with ``gamma`` and ``rho`` taken at the same euro amount in both accounts **[std]**, which
is what makes the difference exact. Two consequences are not obvious. The difference is
**large in the first five years** — on the anchor cell the whole 25 ‰ is taken in year 1
against one fifth of it — and it **never returns to zero**, because the spread account earns
the *Rechnungszins* on the amounts not yet deducted. So on a zillmered tariff with a positive
*Rechnungszins* the floor sits above the tariff *Deckungskapital* at every duration.

The floor is the § 169 Abs. 3 *Deckungskapital* **alone**: profit shares sit on top of the
statutory minimum rather than inside it. That reading lets the floor bind early and stop
binding once the *Ansammlungsguthaben* has outgrown the interest residual and the
*Stornoabzug*, so both branches of ``cv_pp(t) = max(cv_tariff_pp, cv_floor_pp)`` are
exercised on the anchor cell alone — it binds through ``t = 4`` and not after. The
alternative reading, in which the floor also carries the *Ansammlungsguthaben*, is **not
implemented** and would make the floor bind at every duration.

.. rubric:: Beitragsfreistellung is an election, not a decrement

*Beitragsfreistellung* is a **deterministic election** at ``pup_year`` rather than a rate: a
scalar per-policy account cannot carry two sub-populations with different *Deckungskapital*,
and no source establishes a rate. Both statutory branches are implemented and both are
exercised:

- **Conversion** (model point 7). ``prem_pp(t) = 0`` from ``pup_year``, the *Deckungskapital*
  is **reset to** ``pup_value_pp()`` — the § 165 rule that the paid-up benefit is computed on
  the § 169 Abs. 3–5 value — the *Ansammlungsguthaben* is untouched, ``spread_diff_pp`` is set
  to zero because the two accounts have merged, and ``charge_admin_pp`` switches to
  ``gamma_pup_rate``. No *Stornoabzug* is taken **[std]**: Abs. 5 is drafted for a payout on
  *Kündigung*, and here the contract continues. The reset is real money and is published as
  ``pup_uplift(t)``.
- **Cash-out** (model point 8). Where the paid-up annuity would fall below the
  *Mindestversicherungsleistung*, § 165 has the contract cashed out at the surrender value
  including profit shares instead of made paid-up. The whole surviving cohort then leaves at
  the end of year ``pup_year - 1`` through the surrender decrement, at ``cv_pp``.

``pup_uplift(t)`` is booked in the **transition** year ``t = pup_year - 1``, weighted by
``pols_if(pup_year)``, because that is the row whose roll-forward needs it: the uplift is the
step between ``av_pp_at(pup_year - 1, "AFT_INT")`` and the reset ``av_pp(pup_year)``, and
``check_av_roll_fwd()`` closes at every ``t`` only if it is credited there. The technical
notes describe the same amount from the receiving year's point of view.

A *Beitragsfreistellung* is not a lapse. The paid-up contract keeps its guarantee vintage and
its guaranteed *Rentenfaktor* and pays a reduced benefit; the surrendered one is gone for
cash. On point 7 ``pols_if`` is unbroken through ``pup_year`` and ``claims_lapse(pup_year)``
is zero.

.. rubric:: The Rentenbeginn

Everything happens at the end of policy year ``n``, on the survivors of that year's
decrements::

    capital_gross_pp = av_pp_at(n, "AFT_INT") + av_sur_pp_at(n, "AFT_INT")
    capital_conv_pp  = max(guar_capital_pp, capital_gross_pp + val_reserve_pp)
    annuity_rate_appl = max(annuity_rate_guar, annuity_rate_curr)
    annuity_guar_mth_pp = capital_conv_pp / 10 000 * annuity_rate_appl

``val_reserve_pp`` is the *Bewertungsreserven* crystallisation, which § 153 Abs. 3 VVG makes
*hälftig* and which the transition to annuity payment is a key point for; the **rate** is a
placeholder. The commuting policyholders receive ``capital_conv_pp`` — the same capital the
annuitants convert, *Bewertungsreserven* included: the corpus gives no basis for paying them
less, and inventing one would be a charge no source supports. Both account balances go to
zero from ``t = n + 1``.

The applied factor is ``max(garantierter, aktueller)``, guaranteed for the whole payment
period, and it is a **written option on the insurer's own future annuity tariff**. Both
branches ship: the current factor wins on the anchor cell at 32,00 € against 28,00 €, and
the guarantee binds on point 13, whose ``guar_capital_pp`` floor binds at the same time.

.. rubric:: The Rentengarantiezeit is paid to the dead

Inside the guarantee window the instalment is due whether or not the annuitant is alive, so
it is weighted by the **annuitised** count and not by survivors::

    pols_annuity(t) = pols_annuitization(n)   for n < t <= n + m
                    = pols_if(t)              for t > n + m

Because ``pols_if(t) <= pols_annuitization(n)`` throughout the payout phase this is
``max(pols_if(t), 1{n < t <= n+m} pols_annuitization(n))``, which is how
:func:`check_annuity_guarantee` states it — and stating it that way is what makes the check
independent of the definition it is checking. On the anchor cell the two differ at
``t = 18 ... 27`` and coincide from ``t = 28``.

.. rubric:: Modules that are recorded and not applied

- ``annuity_admin_rate`` ships in ``charge_table.csv`` at 1,5 % of each instalment and is
  **not applied**. The *Rentenfaktor* is exogenous here and already carries the tariff's
  payout loading, so deducting a further administration charge from the annuity would charge
  it twice. ``annuity_payments(t)`` is ``12 (G + U(t)) a(t)`` exactly.
- ``annuity_due_factor()`` is a **diagnostic and nothing else**. It is the annuity-due
  present value on the shipped mortality proxy at the guarantee interest basis, published so
  that the gap between the [std] *Rentenfaktor* and the [std] annuity table is visible rather
  than hidden. **They are not calibrated to each other, and the *Rentenfaktor* is
  authoritative**: it fixes the benefit amount, while the mortality proxy fixes only how long
  that amount is paid. No cash flow reads it.
- No *Bonusrente* ledger, no *Zuzahlung*, no survivor's-annuity or BU rider, no § 163 VVG
  adjustment of the guaranteed *Rentenfaktor*, no dynamic surrender, no premium-default path
  and no tax. Each is named in the technical notes where it belongs.
- **No death benefit after the *Rentenbeginn***. *Beitragsrückgewähr in der Rentenbezugsphase*
  was not established by any source in this product's corpus and is not asserted:
  ``claims(t, "DEATH")`` is zero for every ``t > n`` on every model point. What the corpus
  does establish for post-*Rentenbeginn* death is the *Rentengarantiezeit*, which is modelled.

.. rubric:: Sign convention

:func:`net_cf` is **income positive** — premiums in, benefits, annuity instalments and
expenses out — which is the notes' own orientation and the library-wide sign.
:func:`liability_cf` publishes the same stream outgo-positive, ``liability_cf(t) =
-net_cf(t)`` exactly, so a best estimate is ``sum v(t) liability_cf(t)`` over whatever
discount curve the valuation layer supplies. Both are columns of :func:`result_cf`, so the
identity is verifiable in the frame rather than only in prose.

``av``, ``av_sur``, ``prem_to_av``, ``int_credited`` and ``bonus_credited`` are **state
movements reported, not cash flows summed**: the *Sparbeitrag* and the two credits move money
inside the contract and never cross the boundary. The six that do are ``premiums``, the three
``claims_*``, ``annuity_payments`` and ``expenses``, and those six are exactly what
:func:`check_net_cf` reconciles.
"""

from modelx.serialize.jsonvalues import *

_formula = lambda point_id: None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells
#
# The model point and the frame


def model_point():
    """The selected model point as a Series, from *model_point_table.csv*.

    Thirty columns; the projection reads them through this one cells so that a model point
    is fetched once per ItemSpace.  Point 1 is the technical notes' worked-example anchor.
    """
    return data.model_point_table().loc[point_id]                    # noqa: F821


def omega_age():
    """The terminal age of the shipped mortality proxy, from *param_table.csv*.

    121 **[std]**.  ``mort_rate`` is 1 at ``omega_age - 1``, so the projection ends with no
    survivors and :func:`check_decrement_closure` closes on ``pols_if_init()`` exactly.
    """
    return int(data.param_table().at["omega_age", "value"])          # noqa: F821


def proj_len():
    """The **last** projected policy year index: ``omega_age() - issue_age``.

    This library's reading of ``proj_len()``, asserted in
    ``tests/test_model_conventions_de.py``: ``result_cf().index[-1] == proj_len()``, whether
    the frame is 0-based or 1-based.  A life annuity has no term, so the horizon is the age
    at which the annuitant cannot survive further rather than a fixed number of years —
    truncating one at, say, 40 years silently drops the tail the *Rentenfaktor* was priced
    for.  71 on the anchor cell.
    """
    return omega_age() - int(model_point()["issue_age"])


def age(t):
    """x(t): the attained age at the start of policy year t, ``issue_age + t - 1``."""
    return int(model_point()["issue_age"]) + t - 1


def calendar_year(t):
    """tau(t): the calendar year of policy year t, ``issue_year + t - 1``.

    The second index of the generational mortality surface and of the declared-rate path.
    Because it is derived from the model point's own ``issue_year``, one surface and one
    declared path serve a book of mixed vintages: policy year 1 of a 2005 contract and policy
    year 1 of a 2026 contract read different calendar years from the same table.
    """
    return int(model_point()["issue_year"]) + t - 1


def pols_if_init():
    """The number of policies the model point represents; ``pols_if`` at the frame's start."""
    return float(model_point()["pols_if_init"])


def int_rate_guar():
    """i: the contract's *Rechnungszins*, **read from the model point**.

    Not a global assumption.  The *Höchstrechnungszins* applies to contracts concluded while
    it is in force and an existing contract keeps the rate it was written on, so a German
    life book is a layered stack of guarantee vintages: 1,00 % on the 2026 points, 2,75 % on
    point 6 and 0,90 % on point 14, in one run from one set of tables.
    """
    return float(model_point()["int_rate_guar"])


def mort_be_factor():
    """The loading from the first-order table to the best estimate, from *param_table.csv*.

    1.15 **[std]**, and **above one on purpose**.  For an annuity, prudence means assuming
    mortality *lower* than expected, so the first-order (tariff) table sits below best
    estimate and the second-order rate is the tariff rate loaded upward.  The safety margin
    of the real construction runs in two dimensions, level and trend; only the level is
    reproduced here.
    """
    return float(data.param_table().at["mort_be_factor", "value"])   # noqa: F821


def roll_fwd_tol():
    """The relative tolerance the ``check_*`` identities close to, from *param_table.csv*.

    1e-9, scaled by the magnitude of the quantities being compared.  A float comparison
    tolerance, not an actuarial assumption.
    """
    return float(data.param_table().at["roll_fwd_tol", "value"])     # noqa: F821


# ----------------------------------------
# The premium and the Beitragssumme


def freq_load():
    """phi: the *Ratenzahlungszuschlag* for the model point's *Zahlweise* **[std]**.

    1,000 annual, 1,020 half-yearly, 1,030 quarterly, 1,050 monthly.  The annual grid charges
    the loaded annual amount at the start of the year; the instalments themselves are not
    modelled, so ``n_instalments`` in the table is documentation.
    """
    return float(data.freq_load_table().at[                          # noqa: F821
        model_point()["prem_freq"], "freq_load"])


def prem_pp_sched(t):
    """P_sched(t): the premium schedule **as written at inception**, per policy.

    Zero after the *Rentenbeginn* and after the paying term; the *Einmalbeitrag* in policy
    year 1 on the ``einmal`` form; otherwise the loaded gross premium grown by the *Dynamik*.

    It ignores any later *Beitragsfreistellung* on purpose.  The § 4 DeckRV zillmer base is
    the sum of all premiums payable under the contract **as written**, and a later election
    does not retrospectively shrink that base — which is why :func:`beitragssumme_pp` sums
    this cells and not :func:`prem_pp`.
    """
    mp = model_point()
    if t < 1 or t > int(mp["aufschub_y"]) or t > int(mp["prem_term_y"]):
        return 0.0
    if mp["premium_form"] == "einmal":
        return float(mp["premium_single_pp"]) if t == 1 else 0.0
    return (float(mp["prem_gross_pp"]) * freq_load()
            * (1.0 + float(mp["dynamik_rate"])) ** (t - 1))


def prem_pp(t):
    """P(t): the gross premium actually charged per policy in year t, at the **start** of it.

    The schedule, switched off from ``pup_year`` where the contract has been made premium
    free.  Not further multiplied by a survival factor: deaths and surrenders fall at the end
    of the year, so a claimant has already paid the year's premium.
    """
    return 0.0 if paid_up(t) else prem_pp_sched(t)


def beitragssumme_pp():
    """The *Beitragssumme*: the sum of the premiums payable under the contract as written.

    ``sum of P_sched(u) for u = 1 .. min(prem_term_y, aufschub_y)``, so the frequency loading
    is inside it.  51 000,00 € on the anchor cell.  This is the § 4 DeckRV base on which the
    acquisition charge is struck, and it is fixed at inception: a later
    *Beitragsfreistellung* does not shrink it.
    """
    mp = model_point()
    last = min(int(mp["prem_term_y"]), int(mp["aufschub_y"]))
    return sum(prem_pp_sched(u) for u in range(1, last + 1))


def alpha_total_pp():
    """The total acquisition charge: ``alpha_rate x beitragssumme_pp()``.

    The *Höchstzillmersatz* is 25 ‰ of the *Beitragssumme* for contracts concluded from
    1 January 2015 and 40 ‰ before, the rate at conclusion applying for the whole term; the
    model uses the cap itself **[std]**, which is what makes the year-one *Sparbeitrag* small
    and the § 169 Abs. 3 floor bite.  1 275,00 € on the anchor cell.
    """
    return (float(data.charge_table().at[                            # noqa: F821
        (model_point()["charge_id"], "alpha_rate"), "value"])
        * beitragssumme_pp())


def alpha_cum_pp(t):
    """The acquisition charge already amortised at the **start** of policy year t.

    ``alpha_amort_pp_init`` at the frame's start, then a running total of
    :func:`charge_acq_pp`.  It never exceeds :func:`alpha_total_pp`, which is what the
    ``max(0, .)`` in :func:`charge_acq_pp` guarantees.
    """
    t0 = int(model_point()["duration_init"]) + 1
    if t <= t0:
        return float(model_point()["alpha_amort_pp_init"])
    return alpha_cum_pp(t - 1) + charge_acq_pp(t - 1)


def prem_cum_pp(t):
    """The premiums paid per policy before the **start** of policy year t.

    ``prem_cum_pp_init`` at the frame's start, then a running total of :func:`prem_pp`.  The
    *Beitragsrückgewähr* base: on the ``prem_refund`` death-benefit form the benefit is
    ``prem_cum_pp(t) + prem_pp(t)``, the premiums paid including the year of death, because
    the year's premium fell due at the start of it.
    """
    t0 = int(model_point()["duration_init"]) + 1
    if t <= t0:
        return float(model_point()["prem_cum_pp_init"])
    return prem_cum_pp(t - 1) + prem_pp(t - 1)


def premiums(t):
    """Premium income in policy year t, an inflow: ``prem_pp(t) x pols_if(t)``."""
    return prem_pp(t) * pols_if(t)


# ----------------------------------------
# The premium decomposition


def charge_acq_pp(t):
    """alpha(t): the **zillmered** acquisition charge taken in policy year t.

    ``min(P(t), max(0, alpha_total_pp() - alpha_cum_pp(t)))`` — as much of the outstanding
    acquisition charge as the year's premium can meet, and no more.  On the anchor cell the
    whole 1 275,00 € comes out of the year-1 premium and nothing thereafter, which is what
    *Zillmerung* means and why the year-1 *Sparbeitrag* is thin.
    """
    return min(prem_pp(t), max(0.0, alpha_total_pp() - alpha_cum_pp(t)))


def charge_acq_spread_pp(t):
    """alpha~(t): the same charge spread **evenly over the first five contract years**.

    ``alpha_total_pp() / alpha_spread_years`` for ``t = 1 .. 5``, zero after.  This is the
    § 169 Abs. 3 VVG treatment, and it enters no account of its own: it drives
    :func:`spread_diff_pp`, the difference between the tariff *Deckungskapital* and the
    statutory surrender floor.  255,00 € on the anchor cell.
    """
    years = int(data.charge_table().at[                              # noqa: F821
        (model_point()["charge_id"], "alpha_spread_years"), "value"])
    return alpha_total_pp() / years if 1 <= t <= years else 0.0


def charge_prem_pp(t):
    """beta(t): the premium charge, ``beta_rate x P(t)`` **[std]**.

    4,0 % of each gross premium.  An internal deduction, not an expense: it reduces the
    *Sparbeitrag* and produces no cash flow.
    """
    return float(data.charge_table().at[                             # noqa: F821
        (model_point()["charge_id"], "beta_rate"), "value"]) * prem_pp(t)


def charge_admin_pp(t):
    """gamma(t): the reserve-based administration charge on the **start-of-year** balance.

    ``gamma_rate x av_pp(t)`` while premiums are being paid and ``gamma_pup_rate x av_pp(t)``
    while the contract is premium-free **[std]** — a paid-up contract still bears
    administration cost, and the higher premium-free rate is what makes
    *Beitragsfreistellung* cost something instead of being free.  Struck on the start-of-year
    balance so the recursion stays acyclic.
    """
    item = "gamma_pup_rate" if paid_up(t) else "gamma_rate"
    return float(data.charge_table().at[                             # noqa: F821
        (model_point()["charge_id"], item), "value"]) * av_pp(t)


def nar_pp(t):
    """The net amount at risk at the start of policy year t: ``max(0, db_base_pp - av_pp)``.

    What the insurer would have to find out of its own funds if the policyholder died: the
    death benefit less the reserve already held against it.  On the ``deckungskapital``
    death-benefit form it is **identically zero**, because the benefit *is* the reserve — a
    good invariance test, and the reason :func:`charge_risk_pp` vanishes on points 2 and 12.
    On the ``prem_refund`` form it falls towards zero as the *Deckungskapital* catches up
    with the premiums paid.
    """
    return max(0.0, db_base_pp(t) - av_pp(t))


def charge_risk_pp(t):
    """rho(t): the *Risikobeitrag*, ``mort_rate_guar(t) x nar_pp(t)``, accumulation phase only.

    On the **first-order** basis, not the best estimate: the tariff's own mortality fixes the
    risk charge and the guaranteed benefits, while the second-order basis drives the
    projection's decrements.  Using one basis for both is a listed pitfall.  Zero after the
    *Rentenbeginn*, where no death benefit is payable.
    """
    if t > int(model_point()["aufschub_y"]):
        return 0.0
    return mort_rate_guar(t) * nar_pp(t)


def charge_due_pp(t):
    """The total charge falling due in policy year t: ``alpha + beta + gamma + rho``.

    What the tariff deducts, before asking where it comes from.  :func:`charge_from_prem_pp`
    and :func:`charge_from_av_pp` split it between the premium and the *Deckungskapital*.
    """
    return (charge_acq_pp(t) + charge_prem_pp(t)
            + charge_admin_pp(t) + charge_risk_pp(t))


def charge_from_prem_pp(t):
    """The part of the year's charge the premium meets: ``min(P(t), charge_due_pp(t))``."""
    return min(prem_pp(t), charge_due_pp(t))


def charge_from_av_pp(t):
    """C(t): the part of the year's charge the premium could not meet, taken from the account.

    Zero while a premium is being paid that covers the charges; the whole of
    :func:`charge_due_pp` once the contract is premium-free, which is how a paid-up contract
    pays for its own administration **[std]**.
    """
    return charge_due_pp(t) - charge_from_prem_pp(t)


def prem_to_av_pp(t):
    """S(t): the *Sparbeitrag*, the premium net of what the charges took from it.

    ``P(t) - charge_from_prem_pp(t)``.  This is the amount credited to the
    *Deckungskapital* — the premium "insofar as it is not required for risk and expense
    cover".  1 600,63 € of the anchor cell's 3 000,00 € first premium, the rest being the
    whole zillmered acquisition charge.
    """
    return prem_pp(t) - charge_from_prem_pp(t)


def prem_to_av(t):
    """The *Sparbeitrag* for the model point as a whole: ``prem_to_av_pp(t) x pols_if(t)``.

    Reported in :func:`result_cf` as a **state movement, not a cash flow**: it moves money
    from the premium into the account and never crosses the contract boundary.
    """
    return prem_to_av_pp(t) * pols_if(t)


# ----------------------------------------
# The Deckungskapital


def av_pp(t):
    """V(t): the *Deckungskapital* per policy at the **start** of policy year t.

    ``av_pp_init`` at the frame's start, then :func:`av_pp_at` at ``"AFT_INT"`` of the
    previous year — with two exceptions.  At ``t = pup_year`` on a converting contract the
    balance is **reset** to :func:`pup_value_pp`, the § 165 paid-up value computed on the
    § 169 Abs. 3–5 basis.  And from ``t = n + 1`` it is **zero**: at the *Rentenbeginn* the
    whole balance is converted into the annuity or paid out as the *Kapitalabfindung*.
    """
    mp = model_point()
    t0 = int(mp["duration_init"]) + 1
    if t <= t0:
        return float(mp["av_pp_init"])
    if t > int(mp["aufschub_y"]):
        return 0.0
    if int(mp["pup_year"]) > 0 and t == int(mp["pup_year"]) and not pup_cashout():
        return pup_value_pp()
    return av_pp_at(t - 1, "AFT_INT")


def av_pp_at(t, timing):
    """The *Deckungskapital* per policy at a point inside policy year t.

    ``"BEF_PREM"``
        V(t), the opening balance; the same number as :func:`av_pp`.

    ``"AFT_PREM"``
        after the premium has been credited and the charges taken:
        ``av_pp(t) + prem_to_av_pp(t) - charge_from_av_pp(t)``.  This is the base the
        *Rechnungszins* and the interest surplus are both applied to.

    ``"AFT_INT"``
        the end-of-year balance, after the *Rechnungszins*.  It is the balance a death claim
        and a surrender are measured on, the balance that rolls into V(t+1), and — at
        ``t = n`` — half of the conversion capital.

    The order premium, then charges, then interest on what is left is a **standardization**:
    no document in this product's corpus fixes it, and it is the most consequential such
    choice in the model.
    """
    if timing == "BEF_PREM":
        return av_pp(t)
    if timing == "AFT_PREM":
        return av_pp(t) + prem_to_av_pp(t) - charge_from_av_pp(t)
    if timing == "AFT_INT":
        return av_pp_at(t, "AFT_PREM") + int_credited_pp(t)
    raise ValueError("invalid timing")


def int_credited_pp(t):
    """The *Rechnungszins* credited per policy: ``int_rate_guar() x av_pp_at(t, "AFT_PREM")``.

    The **guaranteed** part of the year's crediting.  The declared *laufende Verzinsung* is
    this plus :func:`bonus_credited_pp`'s interest-surplus component, never this plus the
    whole declared rate.
    """
    return int_rate_guar() * av_pp_at(t, "AFT_PREM")


def int_credited(t):
    """The *Rechnungszins* for the model point as a whole, a **state movement** not a cash flow."""
    return int_credited_pp(t) * pols_if(t)


def av(t):
    """The *Deckungskapital* for the model point as a whole at the start of year t."""
    return av_pp(t) * pols_if(t)


def av_at(t, timing):
    """The fund-level *Deckungskapital* at a point inside year t: ``av_pp_at x pols_if(t)``."""
    return av_pp_at(t, timing) * pols_if(t)


def av_release(t):
    """The *Deckungskapital* leaving the fund at the end of policy year t.

    The end-of-year balance carried out by the policies that leave — deaths and surrenders
    before the *Rentenbeginn*, and at ``t = n`` **the whole balance**, because the annuitants'
    account is converted into the annuity and the commuters' is paid out.  Zero in the payout
    phase, where there is no account left.  Read by :func:`check_av_roll_fwd` and by nothing
    else.
    """
    n = int(model_point()["aufschub_y"])
    if t > n:
        return 0.0
    if t == n:
        return av_pp_at(t, "AFT_INT") * pols_if(t)
    return av_pp_at(t, "AFT_INT") * (pols_if(t) - pols_if(t + 1))


# ----------------------------------------
# The Ansammlungsguthaben


def av_sur_pp(t):
    """A(t): the *Ansammlungsguthaben* per policy at the **start** of policy year t.

    The *verzinsliche Ansammlung* side account: a **second, parallel** balance holding the
    declared surplus, with its own credited rate, settling at year end and on exit.  Zero
    from ``t = n + 1``, the balance having gone into the conversion capital.  It is untouched
    by a *Beitragsfreistellung*.
    """
    mp = model_point()
    t0 = int(mp["duration_init"]) + 1
    if t <= t0:
        return float(mp["av_sur_pp_init"])
    if t > int(mp["aufschub_y"]):
        return 0.0
    return av_sur_pp_at(t - 1, "AFT_INT")


def av_sur_pp_at(t, timing):
    """The *Ansammlungsguthaben* per policy at a point inside policy year t.

    ``"BEF_PREM"`` and ``"AFT_PREM"`` are both the opening balance — no premium is credited
    to this account — and ``"AFT_INT"`` is the balance after the year's surplus credit, which
    is what a death claim including surplus, a surrender and the conversion all read.
    """
    if timing in ("BEF_PREM", "AFT_PREM"):
        return av_sur_pp(t)
    if timing == "AFT_INT":
        return av_sur_pp(t) + bonus_credited_pp(t)
    raise ValueError("invalid timing")


def bonus_credited_pp(t):
    """The surplus credited per policy at the end of policy year t.

    ``bonus_rate(t) x av_pp_at(t, "AFT_PREM") + decl_rate(t) x av_sur_pp(t)``: the interest
    surplus on the *Deckungskapital*'s post-premium base, plus the **full declared rate** on
    the side account's own balance **[std]**.

    The first term is where the German arithmetic lives.  ``bonus_rate`` is
    ``max(0, decl_rate - int_rate_guar)``, applied to the same base the guarantee is applied
    to, so the guarantee and the surplus together deliver the declared *laufende Verzinsung*
    and never more.  On a 2,75 % vintage against a 2,55 % declaration the term is zero at
    every t, and that is the correct answer rather than a missing credit.
    """
    if t > int(model_point()["aufschub_y"]):
        return 0.0
    return bonus_rate(t) * av_pp_at(t, "AFT_PREM") + decl_rate(t) * av_sur_pp(t)


def bonus_credited(t):
    """The surplus credit for the model point as a whole, a **state movement** not a cash flow."""
    return bonus_credited_pp(t) * pols_if(t)


def av_sur(t):
    """The *Ansammlungsguthaben* for the model point as a whole at the start of year t."""
    return av_sur_pp(t) * pols_if(t)


def av_sur_at(t, timing):
    """The fund-level *Ansammlungsguthaben* inside year t: ``av_sur_pp_at x pols_if(t)``."""
    return av_sur_pp_at(t, timing) * pols_if(t)


def av_sur_release(t):
    """The *Ansammlungsguthaben* leaving the fund at the end of policy year t.

    The same shape as :func:`av_release`: the balance carried out by the policies that leave,
    and the whole balance at ``t = n``.  Read by :func:`check_av_sur_roll_fwd` alone.
    """
    n = int(model_point()["aufschub_y"])
    if t > n:
        return 0.0
    if t == n:
        return av_sur_pp_at(t, "AFT_INT") * pols_if(t)
    return av_sur_pp_at(t, "AFT_INT") * (pols_if(t) - pols_if(t + 1))


# ----------------------------------------
# The Sec. 169(3) parallel account, carried as a difference


def spread_diff_pp(t):
    """Delta(t): ``av_spread_pp(t) - av_pp(t)`` at the start of policy year t.

    The two accounts differ **only** in the acquisition charge, so the model carries the
    difference rather than a second full recursion — with ``gamma`` and ``rho`` taken at the
    same euro amount in both **[std]**, which is what makes the difference exact.

    Zero at the frame's start.  That is exact for new business and is a **simplification for
    an in-force point**, where the interest the spread account earned on the amounts not yet
    deducted is discarded; every in-force model point therefore opens at
    ``duration_init >= alpha_spread_years``, once the charge is fully amortised under both
    treatments.  Zero again from ``t = pup_year`` on a converting contract, the two accounts
    having merged at the paid-up value.
    """
    mp = model_point()
    t0 = int(mp["duration_init"]) + 1
    if t <= t0:
        return 0.0
    if t > int(mp["aufschub_y"]):
        return 0.0
    if int(mp["pup_year"]) > 0 and t == int(mp["pup_year"]) and not pup_cashout():
        return 0.0
    return spread_diff_pp_at(t - 1, "AFT_INT")


def spread_diff_pp_at(t, timing):
    """The difference recursion inside policy year t.

    ``"AFT_INT"`` is ``(Delta(t) + alpha(t) - alpha~(t)) x (1 + i)``: the year's excess of the
    zillmered charge over the evenly spread one, added to the running difference and rolled
    forward at the *Rechnungszins*.  ``"BEF_PREM"`` and ``"AFT_PREM"`` are the opening
    difference.

    The difference is large in the first five years — on the anchor cell the whole 25 ‰ is
    taken in year 1 against one fifth of it — and it **never returns to zero**, because the
    spread account earns interest on what has not yet been deducted.
    """
    if timing in ("BEF_PREM", "AFT_PREM"):
        return spread_diff_pp(t)
    if timing == "AFT_INT":
        return ((spread_diff_pp(t) + charge_acq_pp(t) - charge_acq_spread_pp(t))
                * (1.0 + int_rate_guar()))
    raise ValueError("invalid timing")


def av_spread_pp(t):
    """Vtilde(t): the § 169 Abs. 3 *Deckungskapital* per policy at the start of year t."""
    return av_pp(t) + spread_diff_pp(t)


def av_spread_pp_at(t, timing):
    """The § 169 Abs. 3 *Deckungskapital* inside year t: ``av_pp_at + spread_diff_pp_at``."""
    return av_pp_at(t, timing) + spread_diff_pp_at(t, timing)


# ----------------------------------------
# Rates


def mort_rate_at_age(x):
    """The first-order base-year death rate at attained age x, for the model point's sex.

    ``q_base`` from *mort_table.csv*, a **[std]** Gompertz proxy anchored at
    ``q_base(M, 50) = 0.002000``.  The real basis is DAV 2004 R, which is the property of the
    Deutsche Aktuarvereinigung, is not public and is not redistributed here.
    """
    return float(data.mort_table().at[                               # noqa: F821
        (model_point()["sex"], int(x)), "q_base"])


def improve_rate(x):
    """The annual mortality improvement rate at attained age x, from *mort_table.csv*.

    1,5 % below age 60, grading linearly to 0,5 % at 100 and to zero at 110 **[std]** — a
    deliberate simplification of the *Starttrend* / *Zieltrend* structure the German
    construction uses, documented as one rather than presented as a replication.
    """
    return float(data.mort_table().at[                               # noqa: F821
        (model_point()["sex"], int(x)), "improve"])


def mort_rate_guar(t):
    """q*(t): the **first-order** annual death rate, on the generational surface.

    ``q_base(sex, x(t)) x (1 - improve(x(t)))^(tau(t) - mort_base_year)``.

    DAV 2004 R is a *Generationentafel*: mortality is indexed by birth cohort and the
    expected future improvement is built into the table rather than applied on top of it.
    That is why this cells depends on :func:`calendar_year` as well as :func:`age`.  A
    period-table proxy, priced at an annuitisation decades ahead, understates the liability
    by a margin that dwarfs every other assumption — on the anchor cell the annuitant reaches
    67 in 2043, thirty-eight improvement years after the proxy's 2005 base.

    This is the basis the *Risikobeitrag* and the guaranteed benefits are struck on, and
    **not** the basis the projection's decrements run on.
    """
    x = age(t)
    base_year = int(data.param_table().at["mort_base_year", "value"])  # noqa: F821
    return min(1.0, mort_rate_at_age(x)
               * (1.0 - improve_rate(x)) ** (calendar_year(t) - base_year))


def mort_rate(t):
    """q(t): the **best-estimate** annual death rate, ``mort_rate_guar(t) x mort_be_factor()``.

    The second-order basis, which drives :func:`pols_death` and hence every decrement.  The
    factor is above one because for an annuity prudence means assuming mortality *lower* than
    expected, so the first-order table sits below best estimate.  Capped at 1, and equal to 1
    at attained age ``omega_age() - 1``, which is what ends the projection with no survivors.
    """
    return min(1.0, mort_rate_guar(t) * mort_be_factor())


def decl_rate(t):
    """d(t): the declared *laufende Verzinsung* for the model point's scenario in year t.

    Read from *decl_rate_table.csv* at ``(decl_scenario_id, calendar_year(t))``, clamped to
    the table's calendar range so a projection running past its last declared year holds that
    year flat.  2,55 % level on the ``base`` path, 1,50 % on ``low`` **[std]**.

    **The declared rate contains the guarantee.**  It is the *Garantieverzinsung* plus the
    *laufende Zinsüberschussbeteiligung*, never a surplus on top of the guarantee.
    """
    tbl = data.decl_rate_table()                                     # noqa: F821
    scen = model_point()["decl_scenario_id"]
    years = tbl.loc[scen].index
    y = min(max(calendar_year(t), int(years.min())), int(years.max()))
    return float(tbl.at[(scen, y), "decl_rate"])


def bonus_rate(t):
    """b(t): the interest-surplus rate, ``max(0, decl_rate(t) - int_rate_guar())``.

    1,55 % on the anchor cell's 1,00 % vintage against a 2,55 % declaration; **zero at every
    t** on point 6's 2,75 % vintage against the same declaration, because a contract already
    guaranteed more than the declared rate receives no interest surplus.  That is a real and
    important German result, not a modelling artefact, and it is what the ``max(0, .)``
    exists to produce.
    """
    return max(0.0, decl_rate(t) - int_rate_guar())


def lapse_rate(t):
    """w(t): the annual surrender rate in policy year t.

    From *lapse_table.csv* by policy duration, holding the last row for durations beyond the
    table.  **Zero from the *Rentenbeginn***: there is no surrender in the payout phase.

    Every level is **[std]**; the one shaped feature is the **duration-12 step**, at the
    twelve-year threshold § 20 Abs. 1 Nr. 6 EStG puts on the halving of the taxable gain, so
    German Schicht-3 surrenders are suppressed approaching duration 12 and spike at it.

    It also carries the § 165 cash-out branch: where a *Beitragsfreistellung* would leave a
    paid-up annuity below the *Mindestversicherungsleistung*, the rate is 1 in the year
    before ``pup_year`` and the whole surviving cohort leaves at the surrender value.
    """
    mp = model_point()
    if t > int(mp["aufschub_y"]):
        return 0.0
    pup = int(mp["pup_year"])
    if pup > 0 and t == pup - 1 and pup_cashout():
        return 1.0
    tbl = data.lapse_table()                                         # noqa: F821
    return float(tbl.at[min(int(t), int(tbl.index.max())), "lapse_rate"])


# ----------------------------------------
# Benefits, values and the Beitragsfreistellung election


def db_base_pp(t):
    """Dcheck(t): the death benefit measured on **start-of-year** balances.

    Used for one thing only — striking the *Risikobeitrag* through :func:`nar_pp`.  A risk
    charge computed on the post-premium, post-charge balance would make the recursion
    circular, since that balance depends on the charge.  Compare :func:`db_pp`, which is what
    a claim actually pays and reads end-of-year balances: the two are different quantities
    with deliberately similar names.
    """
    mp = model_point()
    form = mp["death_benefit_form"]
    paid = prem_cum_pp(t) + prem_pp(t)
    if form == "prem_refund":
        return paid
    if form == "deckungskapital":
        return av_pp(t)
    if form == "max":
        return max(paid, av_pp(t))
    raise ValueError("invalid death_benefit_form")


def db_pp(t):
    """D(t): the death benefit per policy actually paid on a death in policy year t.

    Three documented designs, on **end-of-year** balances: *Beitragsrückgewähr* (the premiums
    paid, including the year's), the accumulated *Deckungskapital*, or the larger of the two;
    plus the *Ansammlungsguthaben* where ``db_incl_surplus`` is set.

    **Zero after the *Rentenbeginn*.**  *Beitragsrückgewähr in der Rentenbezugsphase* was not
    established by any source in this product's corpus, so it is not asserted; what the corpus
    does establish for post-*Rentenbeginn* death is the *Rentengarantiezeit*, which is
    modelled in :func:`pols_annuity`.
    """
    mp = model_point()
    if t > int(mp["aufschub_y"]):
        return 0.0
    form = mp["death_benefit_form"]
    paid = prem_cum_pp(t) + prem_pp(t)
    if form == "prem_refund":
        base = paid
    elif form == "deckungskapital":
        base = av_pp_at(t, "AFT_INT")
    elif form == "max":
        base = max(paid, av_pp_at(t, "AFT_INT"))
    else:
        raise ValueError("invalid death_benefit_form")
    if int(mp["db_incl_surplus"]):
        base = base + av_sur_pp_at(t, "AFT_INT")
    return base


def surr_charge_pp(t):
    """The *Stornoabzug*: ``stornoabzug_rate x (av_pp_at + av_sur_pp_at)`` at ``"AFT_INT"``.

    A **flat percentage of the pre-deduction value with no duration term**, which is the
    shape § 169 Abs. 5 VVG allows: a deduction is permitted only if agreed, quantified and
    appropriate, and an agreement of a deduction in respect of not-yet-amortised *Abschluss-
    und Vertriebskosten* is void.  A duration-graded deduction that unwound over the first
    years would be exactly the void kind.  2,0 % on ``zillmer_25`` and nil on ``zillmer_40``
    **[std]**; whatever it is set to, :func:`cv_pp` cannot fall below :func:`cv_floor_pp`.
    """
    return (float(data.charge_table().at[                            # noqa: F821
        (model_point()["charge_id"], "stornoabzug_rate"), "value"])
        * (av_pp_at(t, "AFT_INT") + av_sur_pp_at(t, "AFT_INT")))


def cv_tariff_pp(t):
    """Rbar(t): the tariff surrender value, both accounts net of the *Stornoabzug*."""
    return (av_pp_at(t, "AFT_INT") + av_sur_pp_at(t, "AFT_INT")
            - surr_charge_pp(t))


def cv_floor_pp(t):
    """Runder(t): the § 169 Abs. 3 VVG floor — the five-year-spread *Deckungskapital*.

    ``av_spread_pp_at(t, "AFT_INT")``, and the *Deckungskapital* **alone**: § 169 Abs. 3
    speaks of the reserve, and profit shares sit on top of the statutory minimum rather than
    inside it, which is the reading § 165 Abs. 2's "surrender value ... including profit
    shares" supports.  The alternative reading, in which the floor also carries the
    *Ansammlungsguthaben*, is not implemented and would make the floor bind at every duration.
    """
    return av_spread_pp_at(t, "AFT_INT")


def cv_pp(t):
    """R(t): the surrender value per policy, ``max(cv_tariff_pp(t), cv_floor_pp(t))``.

    On the anchor cell the **floor binds through t = 4** — the zillmered account has not yet
    caught up with the evenly spread one — and stops binding once the *Ansammlungsguthaben*
    has outgrown the interest residual and the *Stornoabzug*.  Both branches are therefore
    exercised on the anchor cell alone, which is why the floor is not merely present but
    tested.
    """
    return max(cv_tariff_pp(t), cv_floor_pp(t))


def paid_up(t):
    """True where the contract has been made premium-free by ``pup_year``.

    A **deterministic election** on the model point, not a decrement rate: a scalar
    per-policy account cannot carry two sub-populations with different *Deckungskapital*, and
    no source establishes a rate.  A portfolio model needs the sub-population split this one
    does not have.
    """
    pup = int(model_point()["pup_year"])
    return bool(pup > 0 and t >= pup)


def pup_value_pp():
    """The § 165 paid-up value: the § 169 Abs. 3–5 value at the end of year ``pup_year - 1``.

    ``max(av_pp_at, av_spread_pp_at)`` at ``"AFT_INT"`` of that year — the § 165 rule that the
    premium-free benefit is calculated on the calculation basis of the premium calculation,
    **on the basis of the surrender value under § 169 paragraphs 3 to 5**.  No *Stornoabzug*
    is taken on this route **[std]**: Abs. 5 is drafted for a payout on *Kündigung*, and here
    the contract continues.
    """
    pup = int(model_point()["pup_year"])
    if pup <= 0:
        return 0.0
    return max(av_pp_at(pup - 1, "AFT_INT"), av_spread_pp_at(pup - 1, "AFT_INT"))


def pup_cashout():
    """True where the paid-up annuity would fall below the *Mindestversicherungsleistung*.

    § 165 VVG gives the conversion right only where the agreed minimum insurance benefit is
    reached; below it the insurer must pay the surrender value attributable to the insurance,
    **including profit shares**, under § 169.  The test here is
    ``pup_value_pp() / 10 000 x annuity_rate_guar() < min_annuity_mth``: the monthly annuity
    the paid-up value would buy at the **guaranteed** factor, against a 30,00 € threshold
    **[std]**.  True on model point 8, whose paid-up value at duration 2 buys 5,45 € a month.
    """
    pup = int(model_point()["pup_year"])
    if pup <= 0:
        return False
    threshold = float(data.charge_table().at[                        # noqa: F821
        (model_point()["charge_id"], "min_annuity_mth"), "value"])
    return bool(pup_value_pp() / 10000.0 * annuity_rate_guar() < threshold)


def pup_uplift(t):
    """The *Deckungskapital* credited by the paid-up reset, booked in the transition year.

    ``(pup_value_pp() - av_pp_at(t, "AFT_INT")) x pols_if(t + 1)`` at ``t = pup_year - 1``,
    and zero everywhere else and on every point that never converts.  It is the step between
    the zillmered end-of-year balance and the § 169 Abs. 3–5 paid-up value the contract
    restarts from, and it is **real money** rather than a bookkeeping entry: without it the
    fund-level roll-forward of :func:`check_av_roll_fwd` would not close at that ``t``.

    Booked in year ``pup_year - 1`` because that is the row whose roll-forward needs it; the
    technical notes describe the same amount from the receiving year's point of view.
    """
    pup = int(model_point()["pup_year"])
    if pup <= 0 or t != pup - 1 or pup_cashout():
        return 0.0
    return (pup_value_pp() - av_pp_at(t, "AFT_INT")) * pols_if(t + 1)


# ----------------------------------------
# Decrements and the in-force recursion


def pols_if(t):
    """l(t): the number of policies in force at the **start** of policy year t.

    ``pols_if_init()`` at the frame's start — ``t = 1`` for new business and
    ``t = duration_init + 1`` for an in-force point — then
    ``l(t+1) = l(t) - deaths - surrenders - commutations``.  This is the weight on every
    accumulation-phase cash flow of the same :func:`result_cf` row; the annuity is weighted by
    :func:`pols_annuity` instead, which differs inside the *Rentengarantiezeit*.

    ``pols_if(proj_len() + 1)`` is defined and is **zero**, because ``mort_rate`` is 1 at
    attained age ``omega_age() - 1``.  It is read by :func:`check_decrement_closure` and by
    nothing else, and :func:`result_cf` stops at ``proj_len()``.
    """
    t0 = int(model_point()["duration_init"]) + 1
    if t < t0 or t > proj_len() + 1:
        return 0.0
    if t == t0:
        return pols_if_init()
    return pols_if_at(t - 1, "AFT_DECR")


def pols_if_at(t, timing):
    """The number of policies in force at a point inside policy year t.

    ``"BEF_DECR"``
        l(t), the start of the year, before any decrement; the same number as
        :func:`pols_if` and the weight on that year's cash flows.

    ``"BEF_LAPSE"``
        after deaths, before surrenders — the processing order takes deaths at the end of the
        year and surrenders after them **[std order]**, so this is the population surrenders
        are taken from.

    ``"AFT_DECR"``
        l(t+1), the end-of-year state, after deaths, surrenders and — at ``t = n`` — the
        commutation split.
    """
    if timing == "BEF_DECR":
        return pols_if(t)
    if timing == "BEF_LAPSE":
        return pols_if(t) - pols_death(t)
    if timing == "AFT_DECR":
        return (pols_if(t) - pols_death(t) - pols_lapse(t)
                - pols_commutation(t))
    raise ValueError("invalid timing")


def pols_death(t):
    """l(t) q(t): expected deaths in policy year t, at the end of the year.

    On the **second-order** basis.  The claimant has already paid the year's premium, which
    fell due in advance at the start of it, so :func:`premiums` is not further multiplied by a
    survival factor.  Deaths continue through the payout phase and move :func:`pols_if`, but
    pay nothing: ``db_pp`` is zero after the *Rentenbeginn*.
    """
    return pols_if(t) * mort_rate(t)


def pols_lapse(t):
    """Surrenders at the end of policy year t, taken from the survivors of the year's deaths.

    Zero in the payout phase, where :func:`lapse_rate` is zero.  A *Beitragsfreistellung* is
    **not** counted here: it is an election that keeps the contract alive, not a decrement.
    The one place the two meet is the § 165 cash-out branch, where the whole surviving cohort
    leaves through this decrement at the surrender value.
    """
    return pols_if_at(t, "BEF_LAPSE") * lapse_rate(t)


def pols_surv_rb():
    """The policies surviving to the *Rentenbeginn*: ``l(n) - deaths(n) - surrenders(n)``.

    The population the *Kapitalwahlrecht* splits.  Struck at the end of policy year ``n``,
    after that year's decrements and before the commutation.
    """
    n = int(model_point()["aufschub_y"])
    return pols_if(n) - pols_death(n) - pols_lapse(n)


def pols_commutation(t):
    """The policies taking the *Kapitalabfindung* at the *Rentenbeginn*.

    ``kapitalwahl_rate x pols_surv_rb()`` at ``t = n`` and zero at every other t.  The rate is
    a **model-point attribute, not a behavioural formula**: the annuitise-or-commute decision
    is a tax comparison — the *Ertragsanteil* on each instalment against half the
    *Unterschiedsbetrag* taxed once — and this model computes no tax, so the rate stands in
    for a calculation it does not perform.
    """
    n = int(model_point()["aufschub_y"])
    if t != n:
        return 0.0
    return float(model_point()["kapitalwahl_rate"]) * pols_surv_rb()


def pols_annuitization(t):
    """The policies converting to the annuity at the *Rentenbeginn*.

    ``(1 - kapitalwahl_rate) x pols_surv_rb()`` at ``t = n`` and zero elsewhere.  It is
    ``pols_if(n + 1)`` by construction, and it is the count the *Rentengarantiezeit*
    instalments are paid on however many annuitants are still alive.
    """
    n = int(model_point()["aufschub_y"])
    if t != n:
        return 0.0
    return (1.0 - float(model_point()["kapitalwahl_rate"])) * pols_surv_rb()


def pols_annuity(t):
    """a(t): the count the annuity instalment is **paid on** in policy year t.

    Zero before the *Rentenbeginn*; the **annuitised** count inside the *Rentengarantiezeit*,
    ``n < t <= n + m``, because there the instalment is due whether or not the annuitant is
    alive; the survivors after it.  Weighting the guaranteed years by survivors is a listed
    pitfall, and on the anchor cell the two differ over ``t = 18 ... 27`` and coincide from
    ``t = 28``.
    """
    mp = model_point()
    n = int(mp["aufschub_y"])
    if t <= n:
        return 0.0
    if t <= n + int(mp["rgz_years"]):
        return pols_annuitization(n)
    return pols_if(t)


# ----------------------------------------
# The Rentenbeginn and the annuity in payment


def capital_gross_pp():
    """The accumulated value per policy at the *Rentenbeginn*, before the *Bewertungsreserven*.

    ``av_pp_at(n, "AFT_INT") + av_sur_pp_at(n, "AFT_INT")``: both accounts, at the end of
    policy year ``n``, after that year's crediting.  The contract value used for
    annuitisation includes the *Überschussbeteiligung*.
    """
    n = int(model_point()["aufschub_y"])
    return av_pp_at(n, "AFT_INT") + av_sur_pp_at(n, "AFT_INT")


def val_reserve_pp():
    """The *Bewertungsreserven* crystallised at the *Rentenbeginn*, per policy.

    ``val_reserve_rate x capital_gross_pp()``, 1,5 % **[std]**.  The mechanic is cited twice
    over — participation in the *Bewertungsreserven* is *hälftig* under § 153 Abs. 3 VVG and
    the transition to annuity payment is a key point for it — and **no amount, ratio or
    reserve level was established anywhere**, so the rate is a placeholder sized to be visible
    without dominating.  Policyholders also participate during the payout phase; that
    continuing participation is not modelled.
    """
    return (float(data.param_table().at["val_reserve_rate", "value"])  # noqa: F821
            * capital_gross_pp())


def capital_conv_pp():
    """K: the conversion capital per policy, ``max(guar_capital_pp, capital_gross + val_reserve)``.

    The contract value used for annuitisation, including *Überschussbeteiligung* and
    *Bewertungsreserven*, **subject to a minimum guaranteed contract value** stated in the
    general contract data.  The floor is inoperative on the anchor cell, whose
    ``guar_capital_pp`` is nil, and binds on point 13.

    The commuting policyholders receive this same amount: the corpus gives no basis for paying
    them less than the annuitants convert, and inventing one would be a charge no source
    supports.
    """
    return max(float(model_point()["guar_capital_pp"]),
               capital_gross_pp() + val_reserve_pp())


def annuity_rate_guar():
    """f_g: the *garantierter Rentenfaktor*, in euro a month per 10 000 € of capital.

    Fixed **at inception** on the tariff bases — a recognised mortality table (DAV 2004 R) and
    an interest basis the carrier chooses, in the one document that states it below the
    then-current *Höchstrechnungszins*.  A model-point attribute, because it is a property of
    the contract's vintage and not of the projection.  It is a floor, not the applied factor.
    """
    return float(model_point()["annuity_rate_guar"])


def annuity_rate_curr():
    """f_c: the *aktueller Rentenfaktor* at the annuitant's attained age at *Rentenbeginn*.

    Read from *rentenfaktor_table.csv* at ``(rf_scenario_id, issue_age + aufschub_y)``.
    German insurers derive the current factor of a deferred contract from the tariff they are
    then writing for **immediately beginning annuities**, which is why the immediate-annuity
    document is the direct evidence for the deferred contract's conversion basis.  Every level
    here is **[std]**: no market factor was established for any carrier in any year.
    """
    mp = model_point()
    return float(data.rentenfaktor_table().at[                       # noqa: F821
        (mp["rf_scenario_id"], int(mp["issue_age"]) + int(mp["aufschub_y"])),
        "annuity_rate_curr"])


def annuity_rate_appl():
    """f: the applied *Rentenfaktor*, ``max(annuity_rate_guar(), annuity_rate_curr())``.

    At the start of annuity payments a second *Rentenfaktor* is compared with the guaranteed
    one and **the higher of the two is guaranteed for the annuity payment period**.  That
    ``max`` is a written option on the insurer's own future annuity tariff, and the
    deterministic path does not price it.

    Both branches ship: 32,00 € on the anchor cell, where the current factor wins over a
    guaranteed 28,00 €, and the guarantee binding on point 13.  A model applying the
    guaranteed factor alone understates the anchor cell's annuity by 12,5 %.
    """
    return max(annuity_rate_guar(), annuity_rate_curr())


def annuity_guar_mth_pp():
    """G: the *garantierte Rente*, monthly, per policy.

    ``capital_conv_pp() / 10 000 x annuity_rate_appl()`` — the conversion rule in one line.
    Struck once, at the *Rentenbeginn*, and level for life thereafter; only this part is
    guaranteed, the *Überschussrente* beside it is not.
    """
    return capital_conv_pp() / 10000.0 * annuity_rate_appl()


def annuity_sur_mth_pp(t):
    """U(t): the *Überschussrente*, monthly, per policy, by *Überschussverwendung*.

    ``konstant``
        ``sur_ann_rate x G``, level.  Set from a whole-period projection at outset and
        falling if the insurer earns less.

    ``volldynamisch``
        ``G x ((1 + sur_ann_growth)^k - 1)`` with ``k = t - n - 1``: nil in the first payout
        year and rising with actual surplus development thereafter.

    ``teildynamisch``
        ``theta sur_ann_rate G + G ((1 + theta sur_ann_growth)^k - 1)``: a stated combination
        of the two, half of each at ``theta = 0.5``.

    The three systems and their *directions* are established; **no level, rate or split was
    established for any of them**, so all three parameters are **[std]**.
    """
    mp = model_point()
    n = int(mp["aufschub_y"])
    if t <= n:
        return 0.0
    par = data.param_table()                                         # noqa: F821
    rate = float(par.at["sur_ann_rate", "value"])
    growth = float(par.at["sur_ann_growth", "value"])
    theta = float(par.at["sur_ann_theta", "value"])
    k = t - n - 1
    system = mp["payout_system"]
    guar = annuity_guar_mth_pp()
    if system == "konstant":
        return rate * guar
    if system == "volldynamisch":
        return guar * ((1.0 + growth) ** k - 1.0)
    if system == "teildynamisch":
        return (theta * rate * guar
                + guar * ((1.0 + theta * growth) ** k - 1.0))
    raise ValueError("invalid payout_system")


def annuity_pp(t):
    """The annual annuity per policy: ``12 x (G + U(t))``, zero before the *Rentenbeginn*.

    The twelve is the **compression of a monthly-in-advance annuity onto the annual grid**
    **[std]**: neither the payment timing nor the in-advance / in-arrears basis was
    established, and paying the year's twelve instalments at the start of the year is generous
    to the payout phase by roughly half a year's interest on one year's annuity, every year.

    No administration charge is deducted.  ``annuity_admin_rate`` ships in the charge table at
    1,5 % and is **not applied**: the *Rentenfaktor* is exogenous here and already carries the
    tariff's payout loading, so deducting again would charge it twice.
    """
    if t <= int(model_point()["aufschub_y"]):
        return 0.0
    return 12.0 * (annuity_guar_mth_pp() + annuity_sur_mth_pp(t))


def annuity_payments(t):
    """The annuity outgo in policy year t: ``annuity_pp(t) x pols_annuity(t)``.

    Weighted by the count the instalment is *paid on*, which inside the *Rentengarantiezeit*
    is the annuitised count and not the survivors.
    """
    return annuity_pp(t) * pols_annuity(t)


def annuity_due_factor():
    """A **diagnostic**: the annuity-due factor on the shipped proxy at the guarantee basis.

    ``sum over the payout years of v^k x kp_x`` with ``v = 1 / (1 + int_rate_guar())`` and
    survivorship from :func:`mort_rate`, evaluated at the annuitant's attained age at
    *Rentenbeginn*.  **No cash flow reads it.**

    It exists because this model publishes a **[std]** *Rentenfaktor* and a **[std]** annuity
    table, and those two are **not calibrated to each other**.  The *Rentenfaktor* is
    authoritative: it fixes the benefit amount, while the mortality proxy fixes only how long
    that amount is paid.  Publishing the factor the proxy would imply — ``10 000 / (12 x
    annuity_due_factor())`` — makes the gap visible rather than hidden.  Anyone substituting a
    real DAV 2004 R must re-strike the *Rentenfaktoren* with it or accept an inconsistency the
    model will not flag.
    """
    n = int(model_point()["aufschub_y"])
    disc = 1.0 / (1.0 + int_rate_guar())
    surv = 1.0
    total = 0.0
    for s in range(n + 1, proj_len() + 1):
        total = total + surv * disc ** (s - n - 1)
        surv = surv * (1.0 - mort_rate(s))
    return total


# ----------------------------------------
# Claims, expenses and the cash flow statement


def claims(t, kind=None):
    """Benefit outgo in policy year t, by kind; the total when kind is omitted.

    ``"DEATH"``
        ``db_pp(t) x pols_death(t)``, paid at the end of the year of death.  **Zero after the
        *Rentenbeginn***, where ``db_pp`` is zero.

    ``"LAPSE"``
        ``cv_pp(t) x pols_lapse(t)``, the surrender value on the survivors of the year's
        deaths.  Zero in the payout phase, where there is no surrender.

    ``"COMMUTATION"``
        ``capital_conv_pp() x pols_commutation(t)``, the *Kapitalabfindung* under the
        *Kapitalwahlrecht*, paid in row ``n`` and in no other row.  The commuters receive the
        same capital the annuitants convert, *Bewertungsreserven* included.

    The annuity itself is **not** a claim kind: it is a recurring benefit with its own
    weighting rule and is published as :func:`annuity_payments`.
    """
    if kind is None:
        return sum(claims(t, k) for k in ("DEATH", "LAPSE", "COMMUTATION"))
    if kind == "DEATH":
        return db_pp(t) * pols_death(t)
    if kind == "LAPSE":
        return cv_pp(t) * pols_lapse(t)
    if kind == "COMMUTATION":
        return capital_conv_pp() * pols_commutation(t)
    raise ValueError("invalid kind")


def expense_acq_pp():
    """The acquisition expense per policy at issue, from *param_table.csv*: 400,00 € **[std]**."""
    return float(data.param_table().at["expense_acq_pp", "value"])   # noqa: F821


def expense_maint_pp():
    """The maintenance expense per policy per year in the accumulation phase: 45,00 € **[std]**."""
    return float(data.param_table().at["expense_maint_pp", "value"])  # noqa: F821


def expense_annuity_pp():
    """The administration expense per policy per year in the payout phase: 30,00 € **[std]**."""
    return float(data.param_table().at["expense_annuity_pp", "value"])  # noqa: F821


def expense_claim_pp():
    """The settlement expense per death, surrender or commutation event: 120,00 € **[std]**."""
    return float(data.param_table().at["expense_claim_pp", "value"])  # noqa: F821


def expense_infl():
    """The annual expense inflation rate: 2,0 % p.a. **[std]**."""
    return float(data.param_table().at["expense_infl", "value"])     # noqa: F821


def expenses_pp(t):
    """The per-policy administration expense in policy year t, inflated.

    ``expense_maint_pp()`` in the accumulation phase and ``expense_annuity_pp()`` in the
    payout phase, each times ``(1 + expense_infl())^(t - 1)`` so inflation compounds from
    inception rather than from the start of the frame — which matters for the in-force points,
    whose frames open partway through the contract.
    """
    level = (expense_maint_pp() if t <= int(model_point()["aufschub_y"])
             else expense_annuity_pp())
    return level * (1.0 + expense_infl()) ** (t - 1)


def expenses(t):
    """The insurer's own outgo in policy year t: acquisition, administration and settlement.

    Acquisition falls once, in the frame's first year and only for new business — an in-force
    model point's acquisition cost was incurred before the valuation date.  Administration is
    per policy on the exposed count, which is ``pols_if(t)`` while premiums accumulate and
    ``pols_annuity(t)`` once the annuity is in payment.  Settlement falls on every death,
    surrender and commutation.

    **These are expenses, not charges.**  The *Kostenbeiträge* the tariff deducts —
    ``charge_acq_pp``, ``charge_prem_pp``, ``charge_admin_pp``, ``charge_risk_pp`` — move
    money inside the contract and are not here: ``expenses(t)`` is invariant to ``beta_rate``
    and ``gamma_rate`` while ``av_pp(t+1)`` is not.  Booking the charges as expenses inflates
    outgo by the whole charge load and is the commonest way to make a German model look
    conservative.
    """
    mp = model_point()
    n = int(mp["aufschub_y"])
    t0 = int(mp["duration_init"]) + 1
    out = 0.0
    if t == t0 and int(mp["duration_init"]) == 0:
        out = out + expense_acq_pp() * pols_if(t)
    out = out + expenses_pp(t) * (pols_if(t) if t <= n else pols_annuity(t))
    out = out + expense_claim_pp() * (pols_death(t) + pols_lapse(t)
                                      + pols_commutation(t))
    return out


def net_cf(t):
    """The net liability cash flow of policy year t, **income positive**.

    ``premiums - claims_death - claims_lapse - claims_commutation - annuity_payments -
    expenses``.  The six components are exactly the six that cross the contract boundary; the
    account movements beside them in :func:`result_cf` — ``prem_to_av``, ``int_credited``,
    ``bonus_credited`` — are internal and are reported, not summed.

    The shape to expect on the anchor cell is strongly positive through the accumulation
    phase, a large negative spike in year 17 where the *Kapitalabfindung* falls, and a long
    negative annuity tail thereafter.
    """
    return (premiums(t) - claims(t, "DEATH") - claims(t, "LAPSE")
            - claims(t, "COMMUTATION") - annuity_payments(t) - expenses(t))


def liability_cf(t):
    """The same stream as :func:`net_cf`, outgo positive: ``-net_cf(t)`` exactly.

    The orientation a valuation layer consumes: a Solvency II best estimate is
    ``sum v(t) liability_cf(t)`` over the relevant risk-free term structure, plus a risk
    margin.  Published as a column beside :func:`net_cf` so the sign convention is verifiable
    in the frame rather than only in prose.
    """
    return -net_cf(t)


# ----------------------------------------
# The published identities


def check_net_cf_resid(t):
    """The cash-flow-statement residual in policy year t; zero everywhere.

    ``net_cf`` as published in :func:`result_cf`, less the same frame's own
    ``premiums - claims_death - claims_lapse - claims_commutation - annuity_payments -
    expenses``.  It is rebuilt **from the frame** rather than from the cells, so it fails if a
    published column and the headline number ever stop being the same arithmetic — which is
    the failure the identity exists to catch.
    """
    row = result_cf().loc[t]
    rebuilt = (row["premiums"] - row["claims_death"] - row["claims_lapse"]
               - row["claims_commutation"] - row["annuity_payments"]
               - row["expenses"])
    return float(row["net_cf"]) - float(rebuilt)


def check_net_cf():
    """True when the published cash flow statement reconciles in every projected year.

    delib's first ruling: every model in this library publishes the identity that
    reconstructs its headline number from the statement's own parts, so that ``net_cf`` is not
    the one quantity nothing checks.  It also asserts ``liability_cf(t) == -net_cf(t)``
    exactly, which is the library-wide sign convention.
    """
    for t in result_cf().index:
        scale = max(1.0, abs(premiums(t)) + abs(claims(t))
                    + abs(annuity_payments(t)) + abs(expenses(t)))
        if abs(check_net_cf_resid(t)) > roll_fwd_tol() * scale:
            return False
        if abs(liability_cf(t) + net_cf(t)) > roll_fwd_tol() * scale:
            return False
    return True


def check_pols_roll_fwd_resid(t):
    """The in-force roll-forward residual in policy year t; zero everywhere.

    ``pols_if(t) - pols_if(t+1) - pols_death(t) - pols_lapse(t) - pols_commutation(t)``.  The
    recursion and the three exits are formed separately, so they agree by algebra when — and
    only when — every one of them is read at the same ``t``.  What it catches is a misindexed
    recursion: rolling forward with ``w(t-1)``, or dropping the commutation from the recursion
    while still paying the *Kapitalabfindung*, both leave a residual here.
    """
    return (pols_if(t) - pols_if(t + 1) - pols_death(t)
            - pols_lapse(t) - pols_commutation(t))


def check_pols_roll_fwd():
    """True when the in-force roll-forward closes and ``pols_if`` stays non-negative."""
    tol = roll_fwd_tol() * max(pols_if_init(), 1.0)
    for t in result_cf().index:
        if abs(check_pols_roll_fwd_resid(t)) > tol:
            return False
        if pols_if(t) < -tol:
            return False
    return True


def check_decrement_closure_resid(t):
    """The cumulative decrement-closure residual at the end of policy year t; zero.

    The deaths, surrenders and commutations up to and including ``t``, plus ``pols_if(t+1)``,
    less the original cohort.  Built by **direct summation over the exit cells**, with no
    reference to the recursion that produced ``pols_if``, which is what makes it more than the
    telescope of :func:`check_pols_roll_fwd`: it catches a wrong starting cohort, an exit
    counted in two places, and a policy that commutes at the *Rentenbeginn* and reappears in
    the annuity — the arithmetic form of paying the capital twice.

    At ``t = proj_len()`` it closes on ``pols_if_init()`` exactly with ``pols_if(N+1) = 0``,
    because ``mort_rate`` is 1 at attained age ``omega_age() - 1``.  A projection truncated
    before then would fail here rather than silently drop the annuity tail.
    """
    exits = sum(pols_death(s) + pols_lapse(s) + pols_commutation(s)
                for s in range(int(model_point()["duration_init"]) + 1, t + 1))
    return exits + pols_if(t + 1) - pols_if_init()


def check_decrement_closure():
    """True when exits and survivors account for the whole cohort at every projected t."""
    tol = roll_fwd_tol() * max(pols_if_init(), 1.0)
    return all(abs(check_decrement_closure_resid(t)) <= tol
               for t in result_cf().index)


def check_av_roll_fwd_resid(t):
    """The *Deckungskapital* roll-forward residual in policy year t; zero everywhere.

    ``av(t) + prem_to_av(t) - charge_from_av(t) + int_credited(t) + pup_uplift(t) -
    av_release(t) - av(t+1)``, at fund level.

    It ties the account to the cash flow statement: the *Sparbeitrag* that left the premium
    must arrive here, the charge the premium could not meet must leave here, and the balance
    the leavers took with them must equal what the death and surrender claims paid out.  It
    closes across the *Beitragsfreistellung* reset only because :func:`pup_uplift` is
    published, and across the *Rentenbeginn* only because the whole balance is released there.
    """
    return (av(t) + prem_to_av(t) - charge_from_av_pp(t) * pols_if(t)
            + int_credited(t) + pup_uplift(t) - av_release(t) - av(t + 1))


def check_av_roll_fwd():
    """True when the *Deckungskapital* rolls forward exactly in every projected year."""
    for t in result_cf().index:
        scale = max(1.0, abs(av(t)), abs(av(t + 1)), abs(premiums(t)))
        if abs(check_av_roll_fwd_resid(t)) > roll_fwd_tol() * scale:
            return False
    return True


def check_av_sur_roll_fwd_resid(t):
    """The *Ansammlungsguthaben* roll-forward residual in policy year t; zero everywhere.

    ``av_sur(t) + bonus_credited(t) - av_sur_release(t) - av_sur(t+1)``.  Nothing else touches
    the side account: no premium is credited to it, no charge is taken from it, and it is
    untouched by a *Beitragsfreistellung*.  A model that credited the declared rate to the
    *Deckungskapital* as well as here would leave a residual at every t.
    """
    return (av_sur(t) + bonus_credited(t) - av_sur_release(t)
            - av_sur(t + 1))


def check_av_sur_roll_fwd():
    """True when the *Ansammlungsguthaben* rolls forward exactly in every projected year."""
    for t in result_cf().index:
        scale = max(1.0, abs(av_sur(t)), abs(av_sur(t + 1)), abs(av(t)))
        if abs(check_av_sur_roll_fwd_resid(t)) > roll_fwd_tol() * scale:
            return False
    return True


def check_prem_split_resid(t):
    """The premium-decomposition residual in policy year t; zero everywhere.

    Two identities in one number, the larger in absolute value being returned:
    ``prem_pp = prem_to_av_pp + charge_from_prem_pp`` — every euro of premium is either saved
    or spent on a charge — and ``charge_due_pp = charge_from_prem_pp + charge_from_av_pp`` —
    every euro of charge is met either from the premium or from the account.  Together they
    are what stops a charge from being taken twice or from vanishing.
    """
    a = prem_pp(t) - prem_to_av_pp(t) - charge_from_prem_pp(t)
    b = charge_due_pp(t) - charge_from_prem_pp(t) - charge_from_av_pp(t)
    return a if abs(a) >= abs(b) else b


def check_prem_split():
    """True when the premium and the charge both decompose exactly in every projected year."""
    for t in result_cf().index:
        scale = max(1.0, abs(prem_pp(t)), abs(charge_due_pp(t)))
        if abs(check_prem_split_resid(t)) > roll_fwd_tol() * scale:
            return False
    return True


def check_cv_floor_resid(t):
    """The surrender-value residual in policy year t: ``cv_pp - max(cv_tariff_pp, cv_floor_pp)``.

    Zero everywhere by construction; what the companion :func:`check_cv_floor` adds is the
    one-sided assertion that the value never falls below the § 169 Abs. 3 floor however large
    the *Stornoabzug* is set — which is the statutory content, since a deduction in respect of
    unamortised acquisition costs is void.
    """
    return cv_pp(t) - max(cv_tariff_pp(t), cv_floor_pp(t))


def check_cv_floor():
    """True when the surrender value is the floored tariff value in every projected year."""
    for t in result_cf().index:
        scale = max(1.0, abs(cv_pp(t)))
        if abs(check_cv_floor_resid(t)) > roll_fwd_tol() * scale:
            return False
        if cv_pp(t) < cv_floor_pp(t) - roll_fwd_tol() * scale:
            return False
    return True


def check_annuity_conv_resid(t):
    """The conversion residual: ``annuity_guar_mth_pp x 10 000 - capital_conv_pp x f``.

    A scalar identity — the conversion is struck once, at the *Rentenbeginn* — evaluated at
    every ``t`` so that it has the same shape as the other checks.  ``f`` is rebuilt here as
    ``max(annuity_rate_guar(), annuity_rate_curr())`` rather than read from
    :func:`annuity_rate_appl`, so the check is independent of the cells it is checking.
    """
    return (annuity_guar_mth_pp() * 10000.0
            - capital_conv_pp() * max(annuity_rate_guar(), annuity_rate_curr()))


def check_annuity_conv():
    """True when the *Rentenbeginn* conversion obeys all three of its rules.

    The conversion arithmetic itself; that the applied *Rentenfaktor* is never below the
    guaranteed one, which is the whole content of ``max(garantierter, aktueller)``; and that
    the conversion capital is never below the minimum guaranteed contract value stated in the
    general contract data.
    """
    scale = max(1.0, abs(capital_conv_pp()))
    tol = roll_fwd_tol() * scale * 10000.0
    if abs(check_annuity_conv_resid(result_cf().index[0])) > tol:
        return False
    if annuity_rate_appl() < annuity_rate_guar() - roll_fwd_tol():
        return False
    if capital_conv_pp() < float(model_point()["guar_capital_pp"]) - roll_fwd_tol() * scale:
        return False
    return True


def check_annuity_guarantee_resid(t):
    """The *Rentengarantiezeit* weighting residual in policy year t; zero everywhere.

    ``pols_annuity(t)`` less ``max(pols_if(t), 1{n < t <= n+m} x pols_annuitization(n))``,
    which is zero before the *Rentenbeginn*.  Stating the identity with the ``max`` is what
    makes it independent of the definition it checks: it holds because
    ``pols_if(t) <= pols_annuitization(n)`` throughout the payout phase, so a model that
    weighted the guaranteed years by survivors would fail here at every ``t`` inside the
    window where a death has occurred.
    """
    mp = model_point()
    n = int(mp["aufschub_y"])
    if t <= n:
        return pols_annuity(t)
    guaranteed = (pols_annuitization(n)
                  if t <= n + int(mp["rgz_years"]) else 0.0)
    return pols_annuity(t) - max(pols_if(t), guaranteed)


def check_annuity_guarantee():
    """True when the annuity is weighted by the annuitised count inside the guarantee period."""
    tol = roll_fwd_tol() * max(pols_if_init(), 1.0)
    return all(abs(check_annuity_guarantee_resid(t)) <= tol
               for t in result_cf().index)


# ----------------------------------------
# Output


def result_cf():
    """Result table of cash flows and account balances, indexed by policy year t.

    The frame runs from the model point's first projected year — ``t = 1`` for new business,
    ``t = duration_init + 1`` for an in-force point — to ``proj_len()``, contiguously.

    ``pols_if`` is the start-of-year count and the weight on the accumulation-phase cash flows
    of the same row; ``pols_annuity`` is the count the annuity instalment is paid on, which
    differs inside the *Rentengarantiezeit*.  ``av``, ``av_sur``, ``prem_to_av``,
    ``int_credited`` and ``bonus_credited`` are **state movements reported, not cash flows
    summed**: they move money inside the contract and never cross the boundary.  The six that
    do are ``premiums``, the three ``claims_*``, ``annuity_payments`` and ``expenses``, and
    those six are exactly what :func:`check_net_cf` reconciles.  ``liability_cf`` is ``net_cf``
    outgo-positive.
    """
    ts = list(range(int(model_point()["duration_init"]) + 1, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_annuity": [pols_annuity(t) for t in ts],
            "av": [av(t) for t in ts],
            "av_sur": [av_sur(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "prem_to_av": [prem_to_av(t) for t in ts],
            "int_credited": [int_credited(t) for t in ts],
            "bonus_credited": [bonus_credited(t) for t in ts],
            "claims_death": [claims(t, "DEATH") for t in ts],
            "claims_lapse": [claims(t, "LAPSE") for t in ts],
            "claims_commutation": [claims(t, "COMMUTATION") for t in ts],
            "annuity_payments": [annuity_payments(t) for t in ts],
            "expenses": [expenses(t) for t in ts],
            "liability_cf": [liability_cf(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_pols():
    """Result table of decrement rates, per-policy amounts and account values, indexed by t.

    The per-policy view behind :func:`result_cf`: the two mortality bases side by side, the
    surrender rate, the premium and its decomposition, the three account balances and the
    surrender value with its two branches.  Nothing here is a cash flow.
    """
    ts = list(range(int(model_point()["duration_init"]) + 1, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "mort_rate_guar": [mort_rate_guar(t) for t in ts],
            "mort_rate": [mort_rate(t) for t in ts],
            "lapse_rate": [lapse_rate(t) for t in ts],
            "prem_pp": [prem_pp(t) for t in ts],
            "charge_due_pp": [charge_due_pp(t) for t in ts],
            "prem_to_av_pp": [prem_to_av_pp(t) for t in ts],
            "av_pp": [av_pp(t) for t in ts],
            "av_sur_pp": [av_sur_pp(t) for t in ts],
            "av_spread_pp": [av_spread_pp(t) for t in ts],
            "cv_tariff_pp": [cv_tariff_pp(t) for t in ts],
            "cv_floor_pp": [cv_floor_pp(t) for t in ts],
            "cv_pp": [cv_pp(t) for t in ts],
            "db_pp": [db_pp(t) for t in ts],
            "annuity_pp": [annuity_pp(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

pd = ("Module", "pandas")
