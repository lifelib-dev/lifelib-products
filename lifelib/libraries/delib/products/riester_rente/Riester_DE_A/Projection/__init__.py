# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.Riester_DE_A` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the worked example's anchor cell
    >>> Projection.point_id = 11           # or switch the default

``t`` counts **policy years**, 1-based: ``t = 1`` is the policy year that opens at the
1 January 2027 valuation date and ``t = proj_len() = omega_age - age(1) + 1`` the last.
The frame is contiguous and uniform on every model point, including a point that commutes
at *Rentenbeginn* and therefore carries zeros to the end — a uniform frame is what lets
two model points be read side by side, and truncating a commuted point is a listed
pitfall.

**Two phases in one projection.** ``t_conv() = rentenbeginn_age - age(1) + 1`` is the
conversion year. ``is_accum(t)`` holds for ``t < t_conv()`` and ``is_payout(t)`` for
``t >= t_conv()``. The accumulation recursions stop at ``t_conv()``; the lifelong annuity
runs from ``t_conv()`` to ``proj_len()``. A model that stops at *Rentenbeginn* has not
modelled the benefit the AltZertG requires.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent directory,
``products/riester_rente/``, read at run time rather than stored inside the model. The
model folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded
values — so a diff of the model shows logic changes only, and an input can be edited or
swapped without rewriting the model. This follows ``annuallife.TradLife_A``; contrast
``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``Riester_DE_A`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

Each table has a filename Reference and a reader Cells, both on
:mod:`~.Riester_DE_A.Data`, reached here through the ``data`` Reference:

=========================  =====================================  ==========================
Reference                  Cells                                  File
=========================  =====================================  ==========================
model_point_file           data.model_point_table()               model_point_table.csv
mort_accum_file            data.mort_table_accum()                mort_table_accum.csv
annuity_mort_file          data.annuity_mort_table()              annuity_mort_table.csv
lapse_file                 data.lapse_table()                     lapse_table.csv
zulage_file                data.zulage_schedule()                 zulage_schedule.csv
income_file                data.income_schedule()                 income_schedule.csv
surplus_file               data.surplus_scenario()                surplus_scenario.csv
freq_loading_file          data.freq_loading()                    freq_loading.csv
=========================  =====================================  ==========================

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` and ``savings.CashValue_SE``
wherever those models have an analogue — ``pols_*`` for policy counts, plural nouns for
cash flows, ``*_rate`` for rates, ``*_pp`` for per-policy amounts, ``claims(t, kind)``
with an uppercase ``kind`` string, ``pols_if_at(t, timing)`` and ``av_pp_at(t, timing)``
for the within-year reads, ``prem_to_av_pp`` for the part of the contribution credited to
the account. The technical notes use compact actuarial symbols instead. The mapping is:

=========================  ==============================  ==========================
Notes symbol               Cells                           Meaning
=========================  ==============================  ==========================
(none)                     model_point()                   The selected model point row
n = omega - x(1) + 1       proj_len()                      Last projected period index
T                          t_conv()                        The conversion year
x(t)                       age(t)                          Attained age in year t
d(t)                       duration(t)                     Completed contract years + t
tau(t)                     calendar_year(t)                Calendar year of period t
(phase)                    is_accum(t), is_payout(t)       Accumulation / payout flag
l(t)                       pols_if(t)                      In force at the START of year t
l(1)                       pols_if_init()                  Opening policy count
l(t)(1-q), l(t+1)          pols_if_at(t, timing)           BEF_DECR / AFT_DECR
q(t)                       mort_rate(t)                    Death rate applied in year t
(table)                    mort_rate_at_age(x)             Accumulation table rate at x
q(x, tau)                  annuity_mort_rate(x, tau)       Generational annuitant rate
w(t)                       lapse_rate(t)                   Surrender rate in year t
theta(t)                   transfer_rate(t)                Anbieterwechsel rate in year t
(none)                     pols_death(t)                   Expected deaths in year t
(none)                     pols_lapse(t)                   Expected surrenders in year t
(none)                     pols_transfer(t)                Expected transfers out in year t
l(T)                       pols_conv()                     Policies reaching Rentenbeginn
(none)                     pols_annuity_pay(t)             Policies paid an instalment
Y(t)                       income_ref(t)                   Previous year's earnings
Z*(t)                      zulage_entitlement_pp(t)        Full Sec. 84/85 entitlement
Zhat(t)                    zulage_granted_pp(t)            After the Sec. 86 Kuerzung
Z(t)                       zulage_pp(t)                    Zulage CREDITED in year t
(none)                     zulage_cum_pp(t)                Cumulative Zulagen credited
M(t)                       mindesteigenbeitrag_pp(t)       The Sec. 86 minimum
E(t)                       eigenbeitrag_pp(t)              Own contribution, before phi
E(t) phi                   eigenbeitrag_paid_pp(t)         Own contribution, as paid
phi                        prem_freq_load()                Ratenzuschlag multiplier
C(t)                       contrib_total_pp(t)             Total contribution received
K_a(t)                     acq_charge_pp(t)                Acquisition charge
K_v(t)                     admin_charge_pp(t)              Administration charge
S(t)                       prem_to_av_pp(t)                Sparbeitrag; MAY BE NEGATIVE
D(t)                       dk_pp(t)                        Deckungskapital
U(t)                       surplus_acct_pp(t)              Ueberschussguthaben
A(t) = D(t) + U(t)         av_pp(t)                        Account value per policy
A(t), A(t)+S(t), A(t+1)    av_pp_at(t, timing)             BEF_PREM / AFT_PREM / AFT_INT
A(t) l(t)                  av_at(t, timing)                The same, aggregated
i                          rechnungszins()                 Guaranteed rate
j(t)                       laufende_verz(t)                Declared rate; INCLUDES i
i (D+S)                    int_guar_pp(t)                  Guaranteed interest
(j-i)(D+S) + j U           int_surplus_pp(t)               Declared surplus above it
(none)                     int_credited_pp(t)              Their sum
G(t)                       guar_pp(t)                      Beitragsgarantie accumulator
kappa(t)                   guar_carve_out_pp(t)            Biometric carve-out, 20 % cap
(none)                     garantieluecke_pp(t)            Running shortfall; DIAGNOSTIC
(none)                     pool_gefoerdert_pp(t)           Cumulative subsidised contribs
(none)                     pool_ungefoerdert_pp(t)         Cumulative unsubsidised ones
(none)                     slueb_pp()                      Schlussueberschussanteil
(none)                     bewres_pp()                     Bewertungsreserven share
(none)                     account_conv_pp()               Account at Rentenbeginn
V                          capital_conv_pp()               Conversion capital
Lambda                     garantieluecke_conv_pp()        Garantieluecke the insurer funds
a-double-dot               ann_factor()                    First-order annuity-due factor
R_c                        rentenfaktor_curr()             Current Rentenfaktor
R_g                        rentenfaktor_guar()             Guaranteed Rentenfaktor
R                          rentenfaktor_applied()          max(R_g, R_c)
(none)                     annuity_month_pp()              Monthly instalment per policy
(none)                     is_kleinbetrag()                The commutation test
(none)                     teilkapital_pp()                Teilkapitalauszahlung
(none)                     annuity_capital_pp()            Capital left to annuitise
(none)                     commutation_pp()                Kleinbetragsrenten-Abfindung
a(t)                       annuity_pp(t)                   Annual annuity, 12 instalments
(none)                     db_pp(t)                        Death benefit, gross
(none)                     cv_pp(t)                        Rueckkaufswert, gross
(none)                     transfer_value_pp(t)            Anbieterwechsel transfer value
(none)                     exit_charge_pp(t)               Stornoabzug + transfer charge
(none)                     premiums(t)                     Eigenbeitrag income
(none)                     zulagen(t)                      Zulage income, SEPARATE column
(none)                     int_credited(t)                 Interest credited, REPORTED
(none)                     claims(t, kind)                 Benefit outgo by kind
(none)                     expenses(t)                     Expense outgo
(none)                     commissions(t)                  Commission outgo
net_cf(t)                  net_cf(t)                       Net cash flow, income positive
liability_cf(t)            liability_cf(t)                 The same stream, outgo positive
=========================  ==============================  ==========================

Six names needed care.

``Z*(t)``, ``Zhat(t)`` and ``Z(t)`` are three different quantities and the product turns
on the difference. :func:`zulage_entitlement_pp` is the full § 84/85 entitlement of
contribution year ``t``; :func:`zulage_granted_pp` is that entitlement after the § 86
**proportional** Kürzung, which reduces the subsidy in the ratio of the contribution paid
to the *Mindesteigenbeitrag* rather than withdrawing it; and :func:`zulage_pp` is the cash
**credited** in year ``t``, which the ZfA pays one year in arrear, so it is
``zulage_granted_pp(t - 1)``. Those are **two different lags** — the entitlement looks
back one *calendar* year for income, the cash one *projection* year — and collapsing them
into one is the first listed pitfall. Note also that ``zulage_pp(t_conv())`` is **not**
zero: the final contribution year's Zulage lands in the conversion year and must be
credited, guaranteed and converted before the guarantee is tested.

``C(t)`` in the notes is the contribution *credited*; :func:`contrib_total_pp` here is the
cash actually **received**, ``eigenbeitrag_paid_pp(t) + zulage_pp(t) + contrib_extra_pp``,
and the *Ratenzuschlag* it carries is deducted back out inside :func:`admin_charge_pp`,
whose percentage base is the **unloaded** ``E + Z + extra``. The notes write ``S = C - K_a
- K_v`` with an unloaded ``C`` and a ``K_v`` that already carries ``E(phi - 1)``, which
deducts the loading twice. The arrangement here deducts it exactly once, which is what
makes :func:`prem_to_av_pp`, :func:`guar_pp` and every benefit **invariant to the payment
frequency** while :func:`premiums` rises by ``E(t)(phi - 1)`` — the property the notes'
pitfall 11 asserts.

``S(t)`` **may be negative**, and that is the point of model point 10. The acquisition
charge runs for its five contract years whether or not contributions are paid, so on a
*beitragsfrei* contract the *Sparbeitrag* is negative and the *Deckungskapital* falls.

``D`` and ``U`` are **guarantee accounting, not two investment strategies.** The whole
account grows at the declared ``j(t)``; ``D`` is carved out of it as the part the
*Rechnungszins* guarantees, and ``U`` is the *verzinsliche Ansammlung* of the excess. The
German arithmetic error this prevents is adding the declared *laufende Verzinsung* **to**
the *Rechnungszins*: ``j`` already includes ``i``.

``G(t)`` is an accumulator of **contributions**, never of interest, and it is compared
with the account **exactly once**, at ``t_conv()``. :func:`garantieluecke_pp` is published
at every ``t`` because it is positive in the early durations of any charged contract and a
reader should see that, but it is a **diagnostic**: :func:`db_pp`, :func:`cv_pp` and
:func:`transfer_value_pp` are *not* floored at it, and flooring them is a listed pitfall.

``pols_annuity_pay(t)`` is the whole of the *Rentengarantiezeit*. During the guarantee
period the instalment is paid on ``pols_conv()`` rather than on ``pols_if(t)``, because
payments continue to beneficiaries; afterwards it is paid on the survivors. The guarantee
period changes **who is paid**, never **how much**, so :func:`annuity_pp` does not read
``rentengarantie_years`` at all.

.. rubric:: The Zulage is a contribution, not a benefit

It is paid by the *Zentrale Zulagenstelle für Altersvermögen* to the **provider**, credited
to the contract, counted in the *Beitragsgarantie*, invested, and taxed at the end like
any other contribution. It never reaches the saver's bank account. So :func:`zulagen` is a
positive income column of :func:`result_cf`, published **beside** :func:`premiums` and
never folded into it: the separation is the single most important reporting decision in
this model, because a statement that folds the two cannot answer the one question the
product is about. The § 10a *Sonderausgabenabzug* and the *Günstigerprüfung* top-up are
**not** modelled and have no cells, because they are a personal tax matter between the
saver and the tax office and never touch the contract.

.. rubric:: Benefits are gross of the Rückzahlungsbetrag

On a *Kündigung* the provider withholds every Zulage credited and every § 10a relief
granted and remits them to the ZfA. That is a **tax collection, not a reduction in the
insurer's obligation**, so :func:`cv_pp` and :func:`db_pp` are published gross and netting
the *Rückzahlungsbetrag* out of them would understate the outgo. :func:`zulage_cum_pp`
publishes the reclaimable Zulage limb as a diagnostic; the § 10a limb depends on the
saver's marginal rate and cannot be computed from contract data at all, so no cells
attempts it.

.. rubric:: Sign convention

:func:`net_cf` is **income positive** — contributions and Zulagen in, benefits, expenses
and commission out — which is the notes' own orientation and the library-wide sign.
:func:`liability_cf` publishes the same stream outgo-positive, ``liability_cf(t) =
-net_cf(t)`` exactly, so a Solvency II best estimate is ``sum v(t) liability_cf(t)`` over
whatever discount curve the valuation layer supplies. Both are columns of
:func:`result_cf`, so the identity is verifiable in the frame rather than only in prose.

``int_credited`` is a column of :func:`result_cf` and is **reported, not summed into**
``net_cf``: it is money moving inside the account, not across the insurer's boundary.

.. rubric:: What is deliberately not here

No unit-linked fund and no rebalancing algorithm — that chassis is
``products/fondsgebundene_rentenversicherung/``. No *Auszahlungsplan mit Restverrentung*.
No Wohn-Riester in either limb: no *Eigenheimbetrag* withdrawal decrement, no certified
*Darlehen*, no *Wohnförderkonto*, the last because it is a notional tax-bookkeeping account
carrying no cash flow at all. No *Berufsunfähigkeits-Zusatzversicherung* liability — only
the guarantee carve-out its premium creates. No *Versorgungsausgleich*, no surplus in
payment, no policyholder tax of any kind, and no apportionment of investment return between
the subsidised and unsubsidised contribution pools, which a real *Leistungsmitteilung*
must perform. And no *Beitragsfreistellung* **decrement**: it is the dominant exit in the
real German book and it is represented here as a per-model-point switch (``bfs_year``),
because a paid-up policy and a premium-paying one have different account values and
different guarantee accumulators from the moment they diverge, and a scalar
single-model-point projection cannot carry two of each without doubling every recursion.
Model point 10 shows the mechanic on one policy; a book projection needs the cohort split.
"""

from modelx.serialize.jsonvalues import *

_formula = lambda point_id: None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells
#
# === the model point


def model_point():
    """The selected model point as a Series, indexed by ``point_id``."""
    return data.model_point_table().loc[point_id]                    # noqa: F821


def sex():
    """The saver's sex, M or F.  **Reporting only — it must not enter any rate.**

    Riester tariffs have been **unisex** since a 2006 vintage, six years before the
    general unisex rule, so neither the contribution, the decrements nor the
    *Rentenfaktor* may read this cells.  It is carried because the administration records
    it and because its *absence* from every formula is the assertion worth making.
    """
    v = model_point()["sex"]
    if v not in ("M", "F"):
        raise ValueError("invalid sex")
    return v


def issue_age():
    """The attained age at which the contract was concluded, age last birthday.

    With :func:`duration_init` it fixes ``age(1) = issue_age() + duration_init()``, the
    attained age at the valuation date.  It does not otherwise enter the projection: no
    rate in this model is struck at issue.
    """
    return int(model_point()["issue_age"])


def duration_init():
    """Completed contract years at the valuation date; 0 for a point projected from issue.

    It drives three things and each of them matters.  ``duration(t) = duration_init() +
    t`` selects the *Stornoabzug* band and the acquisition-charge window, so an in-force
    point picks up the charge only for the contract years it has left; the expense
    inflation factor runs on contract duration rather than projection year; and the
    acquisition expense and initial commission fall only where ``duration_init() == 0``,
    because on an in-force point they are in the past.
    """
    return int(model_point()["duration_init"])


def pols_if_init():
    """The number of policies the model point represents at the start of year 1.

    ``result_cf()``'s first ``pols_if`` value equals this exactly, because no decrement has
    been applied when the first period opens.
    """
    return float(model_point()["pols_if_init"])


def rentenbeginn_age():
    """The attained age at which the payout phase begins.

    Bounded below by the completed 62nd year for a contract concluded from 1 January 2012
    (the completed 60th before that), which is a certification condition of the AltZertG
    rather than a tariff term.  Model point 13 sits at the floor.
    """
    return int(model_point()["rentenbeginn_age"])


def rechnungszins():
    """i: the tariff's guaranteed rate of interest.

    At or below the *Höchstrechnungszins* of the contract's vintage — 0,25 % for the
    2024-vintage anchor, 0,90 % on the older model point 3.  It caps the *reserving* rate
    rather than the rate a policy may guarantee, so a tariff may guarantee less; using the
    cap of the vintage is the highest defensible value and therefore makes the
    *Beitragsgarantie* cheapest.  It is a **model point** attribute rather than a library
    constant because the *Zinszusatzreserve* on the older Riester vintages turns on it.
    """
    return float(model_point()["rechnungszins"])


def beitragssumme():
    """The *Beitragssumme* fixed at conclusion, in euros.

    The base of the acquisition charge and of the initial commission, and nothing else.
    On the ``mindest`` contribution form it is a contractual figure rather than the sum
    the projection actually collects, because the § 86 minimum moves with income.
    """
    return float(model_point()["beitragssumme"])


def contrib_form():
    """The contribution form: ``mindest`` or ``fixed``.

    ``mindest`` recomputes the § 86 *Mindesteigenbeitrag* every year from the previous
    calendar year's earnings, so the contribution rises with income and steps down when a
    *Kinderzulage* stops.  ``fixed`` is a level contractual contribution, which is what a
    *mittelbar* eligible spouse paying the 60 € *Sockelbeitrag* has, and what a saver
    contributing at the § 10a ceiling has.
    """
    v = model_point()["contrib_form"]
    if v not in ("mindest", "fixed"):
        raise ValueError("invalid contrib_form")
    return v


def contrib_fixed_pp():
    """The level own contribution under the ``fixed`` form, per policy per year; 0 otherwise."""
    return float(model_point()["contrib_fixed_pp"])


def contrib_ratio():
    """The fraction of the *Mindesteigenbeitrag* actually paid, on the ``mindest`` form.

    1.00 pays the minimum in full and draws the full Zulagen.  Below 1.00 the § 86 Kürzung
    reduces the **subsidy** in the same proportion — it is not a lapse, not a premium
    holiday and not a cliff edge.  Model point 7 sits at 0.50 and draws exactly half.
    """
    return float(model_point()["contrib_ratio"])


def contrib_extra_pp():
    """Unsubsidised contribution above the § 10a ceiling, per policy per year.

    It enters the account **and** the *Beitragsgarantie*, because the guarantee is on the
    *Altersvorsorgebeiträge* paid in and does not distinguish the pools, but it draws no
    Zulage and it does not enlarge the entitlement.  A single Riester contract can
    therefore carry two tax regimes at once, which is why
    :func:`pool_gefoerdert_pp` and :func:`pool_ungefoerdert_pp` are tracked separately.
    """
    return float(model_point()["contrib_extra_pp"])


def rider_prem_pp():
    """Contribution applied to a biometric rider, per policy per year.

    **Not a cash flow of this model.**  The rider's own liability lives in
    ``products/berufsunfaehigkeit/``; what it does here is create the guarantee carve-out
    of :func:`guar_carve_out_pp`, capped at 20 % of total contributions, which is the
    reason a Riester contract can carry a *Berufsunfähigkeits-Zusatzversicherung* without
    the *Beitragsgarantie* having to reproduce its premiums.
    """
    return float(model_point()["rider_prem_pp"])


def income_id():
    """The key into *income_schedule.csv* naming this policy's earnings path."""
    return model_point()["income_id"]


def income_init():
    """Contribution-liable earnings in the calendar year **before** the projection starts.

    The reference income for ``t = 1``, because the § 86 base is the *previous* year's
    earnings.  Zero for a *mittelbar zulageberechtigt* spouse, whose *Mindesteigenbeitrag*
    is then the 60 € *Sockelbeitrag* floor.
    """
    return float(model_point()["income_init"])


def zulage_id():
    """The key into *zulage_schedule.csv* naming this policy's entitlement drivers."""
    return model_point()["zulage_id"]


def zulage_init_pp():
    """The Zulage credited in projection year 1, earned in the contribution year before it.

    This column exists **only** because the ZfA pays in arrear, so an in-force point opens
    owing one Zulage.  On model point 6 it carries the once-in-a-lifetime 200 €
    *Berufseinsteiger-Bonus* alongside the *Grundzulage*; on a point projected from its own
    inception it is zero, because there is no earlier contribution year.
    """
    return float(model_point()["zulage_init_pp"])


def prem_freq():
    """The payment frequency: annual, half_yearly, quarterly or monthly."""
    v = model_point()["prem_freq"]
    if v not in ("annual", "half_yearly", "quarterly", "monthly"):
        raise ValueError("invalid prem_freq")
    return v


def prem_freq_load():
    """phi: the *Ratenzuschlag* multiplier for this policy's payment frequency.

    Read from *freq_loading.csv*.  A **charge**: the saver pays ``E(t) x phi`` and only
    ``E(t)`` reaches the *Sparbeitrag* base and the *Beitragsgarantie*, so the loading
    enlarges :func:`premiums` and leaves :func:`prem_to_av_pp`, :func:`guar_pp` and every
    benefit untouched.
    """
    return float(data.freq_loading().at[prem_freq(), "load"])        # noqa: F821


def bfs_year():
    """The projection year from which contributions stop (*Beitragsfreistellung*); 0 = never.

    A **state change, not a termination**: ``pols_if`` is continuous across it, the account
    keeps rolling, the guarantee accumulator freezes once the last Zulage has landed, and
    the acquisition charge keeps biting for its five contract years — which is what drives
    :func:`prem_to_av_pp` negative on model point 10.
    """
    return int(model_point()["bfs_year"])


def dk_pp_init():
    """D(1): the *Deckungskapital* per policy at the valuation date, in euros."""
    return float(model_point()["dk_pp_init"])


def surplus_pp_init():
    """U(1): the *Überschussguthaben* per policy at the valuation date, in euros."""
    return float(model_point()["surplus_pp_init"])


def guar_pp_init():
    """G(1): the *Beitragsgarantie* accumulator per policy at the valuation date.

    The *Altersvorsorgebeiträge* credited before the projection opens — the saver's own
    contributions and the Zulagen actually credited, not the entitlements earned.  On the
    anchor it is **above** the account, so the cell opens with a positive
    :func:`garantieluecke_pp`, which is the normal state of a charged contract in its early
    durations and affects no benefit.
    """
    return float(model_point()["guar_pp_init"])


def teilkapital_share():
    """The elected *Teilkapitalauszahlung*, as a share of the conversion capital.

    Zero to the statutory 0.30.  A lump sum above the cap would be *schädliche Verwendung*
    of the excess; the model does not police the cap, it takes the elected share as a
    contract term and the model point table stays inside it.  There is **no** lump sum on a
    commuted contract: a *Kleinbetragsrenten-Abfindung* is the whole capital in one payment.
    """
    return float(model_point()["teilkapital_share"])


def rentenfaktor_guar():
    """R_g: the guaranteed *Rentenfaktor*, euros of monthly annuity per 10 000 € of capital.

    Struck at inception and contractual thereafter.  It is an **independent contract term**
    rather than a function of the model's own annuity basis, so it and
    :func:`rentenfaktor_curr` can disagree; :func:`rentenfaktor_applied` says which wins.
    """
    return float(model_point()["rentenfaktor_guar"])


def rentengarantie_years():
    """The *Rentengarantiezeit* in years from *Rentenbeginn*; 0 for a pure lifelong annuity.

    It changes **who is paid** — payments continue to beneficiaries — and never **how
    much**.  :func:`annuity_pp` does not read it.
    """
    return int(model_point()["rentengarantie_years"])


def scenario_id():
    """The key into *surplus_scenario.csv* naming this policy's declared-rate path."""
    return model_point()["scenario_id"]


# === the time axis and the two phases


def proj_len():
    """n: the **last projected period index**, ``omega_age - age(1) + 1``.

    The library's reading of ``proj_len()``, asserted in the conventions suite:
    ``result_cf().index[-1] == proj_len()``, not a row count.  The projection runs to the
    end of the mortality table so that the lifelong annuity is projected to exhaustion and
    the decrement closure identity is exact.
    """
    return omega_age - age(1) + 1                                    # noqa: F821


def t_conv():
    """T: the conversion year, ``rentenbeginn_age - age(1) + 1``.

    The boundary between the two phases and the single moment at which the
    *Beitragsgarantie* is tested.  ``is_accum(t)`` holds strictly before it; the conversion
    year itself is the first payout year, because the first annuity instalment falls at
    *Rentenbeginn* and the account is extinguished there.
    """
    return rentenbeginn_age() - age(1) + 1


def age(t):
    """x(t): attained age last birthday in period t.

    ``issue_age() + duration_init() + t - 1``, so ``age(1)`` is the attained age at the
    valuation date.  Every rate in the model is indexed by this and never by sex.
    """
    return issue_age() + duration_init() + t - 1


def duration(t):
    """d(t): completed contract years at the end of period t, ``duration_init() + t``.

    The **contract** clock rather than the projection clock.  It selects the surrender and
    transfer bands, gates the five-year acquisition charge, and drives the expense
    inflation factor, so an in-force point inherits the charge window its contract has
    actually used up.
    """
    return duration_init() + t


def calendar_year(t):
    """tau(t): the calendar year of period t, ``2026 + t``.

    The projection opens at the **1 January 2027** valuation date on every model point, so
    the calendar axis is common across the table.  It enters only the generational annuity
    basis, where ``annuity_mort_rate(x, tau)`` needs both arguments.
    """
    return valuation_year + t - 1                                    # noqa: F821


def is_accum(t):
    """True while the contract is accumulating: ``t < t_conv()``.

    Contributions, the Zulage credit, the charges, the interest credit and the surrender
    and transfer decrements all live here.  The Zulage credit is the one item that also
    runs **at** ``t_conv()``: the final contribution year's subsidy lands in the conversion
    year, and dropping it silently removes a full year's subsidy from both the account and
    the guarantee.
    """
    return t < t_conv()


def is_payout(t):
    """True from *Rentenbeginn* onward: ``t >= t_conv()``.

    The conversion year is a payout year: the lump sum, the commutation and the first
    annuity instalment are all paid at the start of it.
    """
    return t >= t_conv()


# === decrement rates


def mort_rate_at_age(x):
    """The accumulation-phase table death rate at attained age x.

    A **[std]** proxy for DAV 2008 T, read from *mort_table_accum.csv* and carrying no
    improvement dimension.  Forced to 1 at ``omega_age`` so the closure identity is exact
    there whatever the table says.
    """
    if x >= omega_age:                                               # noqa: F821
        return 1.0
    return float(data.mort_table_accum().at[x, "qx"])                # noqa: F821


def annuity_mort_rate(x, tau):
    """q(x, tau): the **generational** annuitant death rate at age x in calendar year tau.

    ``qx_base(x) x (1 - improvement(x))^(tau - annuity_base_year)`` from
    *annuity_mort_table.csv*, a **[std]** proxy for DAV 2004 R.  It depends on **both**
    arguments, and that is the property a replacement may not drop: a twenty-year-deferred
    annuitisation happens on the mortality of its own conversion year, and a period-table
    proxy understates it by a margin that dwarfs every other assumption here.  Strictly
    decreasing in ``tau`` below ``omega_age``, where it is forced to 1.
    """
    if x >= omega_age:                                               # noqa: F821
        return 1.0
    tab = data.annuity_mort_table()                                  # noqa: F821
    qb = float(tab.at[x, "qx_base"])
    im = float(tab.at[x, "improvement"])
    return qb * (1.0 - im) ** (tau - annuity_base_year)              # noqa: F821


def mort_rate(t):
    """q(t): the death rate actually applied in period t, on a **best-estimate** basis.

    The basis **switches at ``t_conv()``**, and the two adjustments run in opposite
    directions because the direction of prudence forks by product.  In accumulation the
    rate is ``mort_rate_at_age(x(t)) x mort_be_factor`` with the factor at 0.80: a
    first-order *death* table assumes mortality higher than expected, so the best estimate
    sits below it.  In payout it is ``annuity_mort_rate(x(t), tau(t)) x
    annuity_mort_be_factor`` with the factor at 1.15: a first-order *annuity* table assumes
    mortality lower than expected, so the best estimate sits above it.  Using one table for
    both phases, or one factor in both directions, is a listed pitfall.
    """
    if age(t) >= omega_age:                                          # noqa: F821
        return 1.0
    if is_accum(t):
        return min(1.0, mort_rate_at_age(age(t)) * mort_be_factor)   # noqa: F821
    return min(1.0, annuity_mort_rate(age(t), calendar_year(t))
               * annuity_mort_be_factor)                             # noqa: F821


def lapse_rate(t):
    """w(t): the annual surrender rate in period t, from *lapse_table.csv* by duration.

    Zero from ``t_conv()``: a contract in payment cannot be surrendered.  The level is
    deliberately small — a *Kündigung* is *schädliche Verwendung*, repaying every Zulage
    and every § 10a relief and taxing the accumulated growth, against a surrender value
    already below the contributions paid in the early years — so the German market's
    description of a Riester contract as economically unsurrenderable is stated
    numerically rather than only in prose.
    """
    if not is_accum(t):
        return 0.0
    return float(data.lapse_table().at[duration(t), "lapse_rate"])   # noqa: F821


def transfer_rate(t):
    """theta(t): the annual *Anbieterwechsel* rate in period t, from *lapse_table.csv*.

    Set **above** :func:`lapse_rate` at every duration.  The statutory *Wechselrecht* moves
    the capital to another certified contract with no subsidy consequence at all, so it
    dominates surrender for any saver who wants out of the provider but not out of the
    system.  Zero from ``t_conv()``.
    """
    if not is_accum(t):
        return 0.0
    return float(data.lapse_table().at[duration(t), "transfer_rate"])  # noqa: F821


# === the in-force recursion


def pols_if(t):
    """l(t): policies in force at the **START** of period t.

    ``pols_if_init()`` in year 1, then the decrements of the previous year.  This is the
    weight on every cash flow of the same :func:`result_cf` row; end-of-period state is
    reached through :func:`pols_if_at`.  ``pols_if(proj_len() + 1)`` is defined and is
    zero, because ``mort_rate`` is 1 at ``omega_age``; it is read by
    :func:`check_pols_roll_fwd` and by nothing else.
    """
    if t < 1 or t > proj_len() + 1:
        return 0.0
    if t == 1:
        return pols_if_init()
    return pols_if_at(t - 1, "AFT_DECR")


def pols_if_at(t, timing):
    """Policies in force at a point inside period t.

    ``"BEF_DECR"``
        l(t), the start of the period, before any decrement — the same number as
        :func:`pols_if` and the weight on that period's cash flows.

    ``"AFT_DECR"``
        l(t+1), the end-of-period state.  In accumulation that is mortality first, then
        surrender on the survivors of mortality, then transfer on the survivors of both, a
        stated **[std]** ordering.  In the conversion year of a **commuted** contract it is
        zero: the *Kleinbetragsrenten-Abfindung* discharges the contract outright.
    """
    if timing == "BEF_DECR":
        return pols_if(t)
    if timing == "AFT_DECR":
        if t < 1 or t > proj_len():
            return 0.0
        if t == t_conv() and is_kleinbetrag():
            return 0.0
        return (pols_if(t) - pols_death(t) - pols_lapse(t)
                - pols_transfer(t))
    raise ValueError("invalid timing")


def pols_death(t):
    """l(t) q(t): expected deaths in period t, at the end of the period.

    In accumulation the claim is the account value; in payout the account is already
    extinguished, so a death moves :func:`pols_if` and pays nothing except through the
    *Rentengarantiezeit*, which pays the **survivors' beneficiaries** rather than the
    estate.  Zero in the conversion year of a commuted contract, where the whole population
    leaves through the *Abfindung* instead.
    """
    if t < 1 or t > proj_len():
        return 0.0
    if t == t_conv() and is_kleinbetrag():
        return 0.0
    return pols_if(t) * mort_rate(t)


def pols_lapse(t):
    """Expected surrenders in period t, on the survivors of mortality.

    A *Kündigung*: *schädliche Verwendung*, paying :func:`cv_pp` gross of the
    *Rückzahlungsbetrag* the provider withholds and remits.  Zero from ``t_conv()``.
    """
    if not is_accum(t) or t < 1:
        return 0.0
    return pols_if(t) * (1.0 - mort_rate(t)) * lapse_rate(t)


def pols_transfer(t):
    """Expected *Anbieterwechsel* exits in period t, on the survivors of both prior decrements.

    A **separate decrement from surrender**, not a variant of it: the transfer moves the
    capital to another certified contract at full value less a flat charge, with no
    *Stornoabzug* and no subsidy consequence.  Collapsing the two is a listed pitfall.
    """
    if not is_accum(t) or t < 1:
        return 0.0
    return (pols_if(t) * (1.0 - mort_rate(t)) * (1.0 - lapse_rate(t))
            * transfer_rate(t))


def pols_conv():
    """l(T): the policies that reach *Rentenbeginn* and convert.

    Struck once.  It is the count the lump sum, the commutation and — during the
    *Rentengarantiezeit* — the annuity instalment are paid on.
    """
    return pols_if(t_conv())


def pols_annuity_pay(t):
    """The policies an annuity instalment is actually paid on in period t.

    ``pols_conv()`` while ``0 <= t - t_conv() < rentengarantie_years``, because during the
    *Rentengarantiezeit* the instalment continues to a deceased annuitant's beneficiaries;
    ``pols_if(t)`` afterwards.  Zero before *Rentenbeginn* and zero on a commuted contract,
    which pays no annuity at all.
    """
    if not is_payout(t) or t > proj_len() or is_kleinbetrag():
        return 0.0
    if t - t_conv() < rentengarantie_years():
        return pols_conv()
    return pols_if(t)


# === the subsidy chain


def income_ref(t):
    """Y(t): the contribution-liable earnings the § 86 minimum of period t is struck on.

    The **previous calendar year's** earnings — ``income_init()`` at ``t = 1``, otherwise
    ``income(t - 1)`` from *income_schedule.csv*.  This is the first of the model's two
    lags and it is a **calendar** lag; the second, the ZfA payment lag in
    :func:`zulage_pp`, is a **projection** lag.  They are different lags and collapsing
    them into one is the first listed pitfall.  Zero once contributions have ceased.
    """
    if not is_accum(t):
        return 0.0
    if t == 1:
        return income_init()
    return float(data.income_schedule().at[(income_id(), t - 1), "income"])  # noqa: F821


def zulage_entitlement_pp(t):
    """Z*(t): the full § 84/85 *Altersvorsorgezulage* entitlement of contribution year t.

    ``grundzulage x unmittelbar + kinderzulage_pre2008 x n_pre + kinderzulage_post2008 x
    n_post + bonus x berufseinsteiger_bonus``, with the drivers read from
    *zulage_schedule.csv*.  The two *Kinderzulage* rates are a permanent **birth-cohort**
    split rather than a transitional rule, so a contract can draw both at once — model
    point 3 draws 175 + 185 + 300 = 660,00 € — and using a single rate is a listed pitfall.
    Zero once contributions have ceased.
    """
    if not is_accum(t):
        return 0.0
    row = data.zulage_schedule().loc[(zulage_id(), t)]               # noqa: F821
    return (grundzulage * float(row["unmittelbar"])                  # noqa: F821
            + kinderzulage_pre2008 * float(row["n_kinder_pre2008"])  # noqa: F821
            + kinderzulage_post2008 * float(row["n_kinder_post2008"])  # noqa: F821
            + berufseinsteiger_bonus * float(row["bonus"]))          # noqa: F821


def mindesteigenbeitrag_pp(t):
    """M(t): the § 86 *Mindesteigenbeitrag* of contribution year t.

    ``max(sockelbeitrag, min(mindest_rate x Y(t), foerder_ceiling) - Z*(t))``: 4 % of the
    previous calendar year's contribution-liable earnings, capped at the 2 100 €
    *Sonderausgaben* ceiling, **less** the full entitlement, and floored at the 60 €
    *Sockelbeitrag*.  The floor is what makes the product's economics extraordinary at low
    incomes: on model point 4, 60,00 € of own money draws 775,00 € of Zulagen.  Zero once
    contributions have ceased, which is also the guard that keeps
    :func:`zulage_granted_pp` from dividing by zero.
    """
    if not is_accum(t):
        return 0.0
    return max(sockelbeitrag,                                        # noqa: F821
               min(mindest_rate * income_ref(t), foerder_ceiling)    # noqa: F821
               - zulage_entitlement_pp(t))


def eigenbeitrag_pp(t):
    """E(t): the saver's own contribution in period t, **before** the *Ratenzuschlag*.

    ``contrib_ratio() x M(t)`` on the ``mindest`` form and ``contrib_fixed_pp()`` on the
    ``fixed`` one.  Zero from ``bfs_year()`` where that is set, and zero from ``t_conv()``:
    the last contribution year is ``t_conv() - 1``.  This is the amount that reaches the
    *Sparbeitrag* base and the *Beitragsgarantie*; :func:`eigenbeitrag_paid_pp` is what the
    saver actually hands over.
    """
    if not is_accum(t):
        return 0.0
    if bfs_year() > 0 and t >= bfs_year():
        return 0.0
    if contrib_form() == "fixed":
        return contrib_fixed_pp()
    return contrib_ratio() * mindesteigenbeitrag_pp(t)


def eigenbeitrag_paid_pp(t):
    """E(t) phi: the own contribution the saver actually pays, after the *Ratenzuschlag*.

    The loading is a charge, so this is larger than :func:`eigenbeitrag_pp` on any
    non-annual frequency while nothing that touches the account or the guarantee changes.
    """
    return eigenbeitrag_pp(t) * prem_freq_load()


def zulage_granted_pp(t):
    """Zhat(t): the entitlement of contribution year t after the § 86 Kürzung.

    ``Z*(t) x min(1, E(t) / M(t))``.  The sanction for underpaying is **proportional, not a
    cliff edge**: a saver paying half the *Mindesteigenbeitrag* draws half the Zulagen
    rather than none.  Model point 7 sits at exactly that.  Zero where the minimum is zero,
    which is the case once contributions have ceased.
    """
    m = mindesteigenbeitrag_pp(t)
    if m <= 0.0:
        return 0.0
    return zulage_entitlement_pp(t) * min(1.0, eigenbeitrag_pp(t) / m)


def zulage_pp(t):
    """Z(t): the Zulage actually **credited** to the contract in period t.

    ``zulage_init_pp()`` in year 1 and ``zulage_granted_pp(t - 1)`` thereafter, because the
    ZfA determines the entitlement of a contribution year and pays the provider in the
    following one.  This is the **second** of the model's two lags and it is a *projection*
    lag, not the calendar lag of :func:`income_ref`.

    ``zulage_pp(t_conv())`` is **non-zero**: contributions stop at ``t_conv() - 1`` and the
    Zulage they earned lands in the conversion year, where it must be credited, guaranteed
    and converted before the *Beitragsgarantie* is tested.  It is zero only after that.
    """
    if t < 1 or t > t_conv():
        return 0.0
    if t == 1:
        return zulage_init_pp()
    return zulage_granted_pp(t - zulage_lag)             # noqa: F821


def zulage_cum_pp(t):
    """Cumulative Zulagen credited up to and including period t.

    The ZfA-reclaimable limb of the *Rückzahlungsbetrag* that a *Kündigung* triggers, and a
    **diagnostic only**: it is never netted from a benefit, because the withholding is a
    tax collection the provider performs on the state's behalf and not a reduction in the
    insurer's obligation.  The § 10a limb of the same *Rückzahlungsbetrag* depends on the
    saver's marginal rate and cannot be computed from contract data at all, so no cells
    attempts it.
    """
    if t < 1:
        return 0.0
    if t == 1:
        return zulage_pp(1)
    return zulage_cum_pp(t - 1) + zulage_pp(t)


# === contributions, charges and the Sparbeitrag


def contrib_total_pp(t):
    """C(t): the total contribution **received** in period t, per policy.

    ``eigenbeitrag_paid_pp(t) + zulage_pp(t) + contrib_extra_pp()`` while contributions
    run.  It carries the *Ratenzuschlag*, which :func:`admin_charge_pp` deducts straight
    back out, so the loading is taken exactly once and :func:`prem_to_av_pp` is invariant
    to the payment frequency.  The unsubsidised limb stops with the subsidised one, at
    ``bfs_year()`` or at ``t_conv()``.
    """
    return (eigenbeitrag_paid_pp(t) + zulage_pp(t)
            + (contrib_extra_pp() if (is_accum(t) and not
                                      (bfs_year() > 0 and t >= bfs_year()))
               else 0.0))


def acq_charge_pp(t):
    """K_a(t): the acquisition charge deducted in period t, per policy.

    ``acq_charge_rate x beitragssumme() / acq_charge_years`` in contract years 1 to 5 and
    zero afterwards.  The AltZertG requires acquisition and distribution costs to be spread
    over **at least five years**, which is a materially tighter constraint on *Zillmerung*
    than anything the VVG imposes on a Schicht-3 contract.  The charge runs for its five
    contract years **whether or not contributions are paid**, so on a *beitragsfrei*
    contract it drives :func:`prem_to_av_pp` negative; stopping it at *Beitragsfreistellung*
    is a listed pitfall.
    """
    if t > t_conv() or duration(t) > acq_charge_years:               # noqa: F821
        return 0.0
    return acq_charge_rate * beitragssumme() / acq_charge_years      # noqa: F821


def admin_charge_pp(t):
    """K_v(t): the administration charge deducted in period t, per policy.

    ``admin_charge_prem_rate`` of the contribution credited — **Zulagen included**, which
    is a standardization the German corpus does not settle and which matters most on
    exactly the low-income cells the product was designed for — plus a fixed
    ``admin_charge_fixed`` a year, plus the *Ratenzuschlag* ``E(t)(phi - 1)`` that
    :func:`contrib_total_pp` collected.  The percentage base is the **unloaded**
    contribution, so the loading is neither charged twice nor credited.
    """
    if t > t_conv():
        return 0.0
    base = (eigenbeitrag_pp(t) + zulage_pp(t)
            + (contrib_extra_pp() if (is_accum(t) and not
                                      (bfs_year() > 0 and t >= bfs_year()))
               else 0.0))
    return (admin_charge_prem_rate * base + admin_charge_fixed       # noqa: F821
            + eigenbeitrag_pp(t) * (prem_freq_load() - 1.0))


def prem_to_av_pp(t):
    """S(t): the *Sparbeitrag* — the part of the contribution credited to the account.

    ``contrib_total_pp(t) - acq_charge_pp(t) - admin_charge_pp(t)``.  **It may be
    negative**: the fixed administration charge and the five-year acquisition charge
    continue on a *beitragsfrei* contract with no contribution to meet them, so the
    *Deckungskapital* falls.  That is the mechanic model point 10 exists to show, and it is
    a property of the German cost-spreading rule rather than a modelling artefact.
    """
    if t > t_conv():
        return 0.0
    return contrib_total_pp(t) - acq_charge_pp(t) - admin_charge_pp(t)


# === the account: two balances, one credited rate


def laufende_verz(t):
    """j(t): the declared *laufende Verzinsung* of period t, from *surplus_scenario.csv*.

    It **includes** the *Rechnungszins*: ``j - i`` is the *laufende
    Zinsüberschussbeteiligung* and adding the two together is the German arithmetic error
    this model is built to make visible.  Zero from ``t_conv()``, where the account is
    extinguished.  The largest single lever in the model and the least supported — no
    declared rate at any carrier was established, so ``base`` is a round number and ``low``
    is a stress rather than a forecast.
    """
    if not is_accum(t):
        return 0.0
    return float(data.surplus_scenario().at[(scenario_id(), t),      # noqa: F821
                                            "laufende_verz"])


def int_guar_pp(t):
    """The guaranteed interest credited at the end of period t, ``i x (D(t) + S(t))``.

    Credited on the *Deckungskapital* **plus the year's Sparbeitrag**, so a contribution
    earns a full year's interest in the year it is paid: contributions fall at the start of
    the year and interest at the end of it.
    """
    if not is_accum(t):
        return 0.0
    return rechnungszins() * (dk_pp(t) + prem_to_av_pp(t))


def int_surplus_pp(t):
    """The declared surplus above the guaranteed rate, credited at the end of period t.

    ``(j(t) - i) x (D(t) + S(t)) + j(t) x U(t)``.  The *Überschussguthaben* bears the
    **whole** declared rate, because it carries no guarantee to carve out of it; the
    *Deckungskapital* bears only the excess here, having already been credited ``i`` in
    :func:`int_guar_pp`.  Setting ``j = i`` makes the first term vanish, which is the
    check that the two rates are not being added.
    """
    if not is_accum(t):
        return 0.0
    return ((laufende_verz(t) - rechnungszins())
            * (dk_pp(t) + prem_to_av_pp(t))
            + laufende_verz(t) * surplus_acct_pp(t))


def int_credited_pp(t):
    """The total interest credited to the account in period t, per policy.

    ``int_guar_pp(t) + int_surplus_pp(t)``, which equals ``j(t) x (D(t) + S(t) + U(t))``
    exactly — the whole account grows at the declared rate and the split between the two
    legs is guarantee accounting rather than two investment strategies.
    """
    return int_guar_pp(t) + int_surplus_pp(t)


def dk_pp(t):
    """D(t): the *Deckungskapital* per policy at the **start** of period t.

    ``(D(t-1) + S(t-1)) x (1 + i)``: the part of the account the *Rechnungszins*
    guarantees.  Extinguished from ``t_conv() + 1``, where the capital has become an
    annuity.
    """
    if t < 1 or t > t_conv():
        return 0.0
    if t == 1:
        return dk_pp_init()
    return (dk_pp(t - 1) + prem_to_av_pp(t - 1)) * (1.0 + rechnungszins())


def surplus_acct_pp(t):
    """U(t): the *Überschussguthaben* per policy at the start of period t.

    *Verzinsliche Ansammlung*: the declared surplus accrues in a second account beside the
    *Deckungskapital* and bears the declared rate.  Extinguished from ``t_conv() + 1``.
    """
    if t < 1 or t > t_conv():
        return 0.0
    if t == 1:
        return surplus_pp_init()
    return surplus_acct_pp(t - 1) + int_surplus_pp(t - 1)


def av_pp(t):
    """A(t) = D(t) + U(t): the account value per policy at the start of period t.

    The death benefit, the base of the *Rückkaufswert* and of the transfer value, and the
    quantity the *Beitragsgarantie* is compared with at *Rentenbeginn*.  **Zero for
    ``t > t_conv()``**: the account is extinguished at conversion, which is why a death in
    the payout phase pays nothing outside the *Rentengarantiezeit*.
    """
    return dk_pp(t) + surplus_acct_pp(t)


def av_pp_at(t, timing):
    """The account value per policy at a point inside period t.

    ``"BEF_PREM"``
        A(t), before the year's contribution is credited.

    ``"AFT_PREM"``
        A(t) + S(t), after the *Sparbeitrag* and before interest — the base the year's
        interest is credited on.

    ``"AFT_INT"``
        A(t+1), after interest and before the decrements act.  This is what a death,
        surrender or transfer benefit of period t is struck on, because the decrements act
        at the end of the year after crediting and an exiting policy takes the full year's
        interest.
    """
    if timing == "BEF_PREM":
        return av_pp(t)
    if timing == "AFT_PREM":
        return av_pp(t) + prem_to_av_pp(t)
    if timing == "AFT_INT":
        return av_pp(t + 1)
    raise ValueError("invalid timing")


def av_at(t, timing):
    """The aggregate account value at a point inside period t: ``av_pp_at(t, timing) x l(t)``.

    Weighted on the **start-of-period** count, which is the weight on that
    :func:`result_cf` row's cash flows; the roll-forward in :func:`check_av_roll_fwd`
    compares this with the next period's opening aggregate and the exits in between.
    """
    return av_pp_at(t, timing) * pols_if(t)


# === the Beitragsgarantie accumulator and the two pools


def guar_carve_out_pp(t):
    """kappa(t): the biometric-rider carve-out from the guarantee in period t.

    ``min(rider_prem_pp(), 0.20 x (E + Z + extra + rider))``.  Contributions used to insure
    reduced earning capacity or a survivor's benefit are excluded from the
    *Beitragserhaltungszusage*, but only up to a share of total contributions, so raising
    ``rider_prem_pp`` past the cap does **not** shrink the guarantee any further.  Model
    point 9 sits exactly at the cap: 400,00 € of rider premium on a 1 200,00 € contribution
    carves out 240,00 € and no more.
    """
    if not is_accum(t):
        return 0.0
    extra = (contrib_extra_pp()
             if not (bfs_year() > 0 and t >= bfs_year()) else 0.0)
    total = eigenbeitrag_pp(t) + zulage_pp(t) + extra + rider_prem_pp()
    return min(rider_prem_pp(), guar_carve_out_cap * total)          # noqa: F821


def guar_pp(t):
    """G(t): the *Beitragsgarantie* accumulator per policy at the start of period t.

    ``G(t+1) = G(t) + E(t) + Z(t) + contrib_extra_pp - kappa(t)`` while ``t <= t_conv()``,
    frozen thereafter.  Three things this encodes.  It counts **Zulagen credited**, in the
    year they are credited, not entitlements in the year they are earned.  It counts
    **unsubsidised** contributions too, because the undertaking is on the
    *Altersvorsorgebeiträge* paid in and does not distinguish the pools.  And it never
    counts interest: the guarantee is nominal.
    """
    if t < 1:
        return 0.0
    if t == 1:
        return guar_pp_init()
    if t - 1 > t_conv():
        return guar_pp(t - 1)
    extra = (contrib_extra_pp() if (is_accum(t - 1) and not
                                    (bfs_year() > 0 and t - 1 >= bfs_year()))
             else 0.0)
    return (guar_pp(t - 1) + eigenbeitrag_pp(t - 1) + zulage_pp(t - 1)
            + extra - guar_carve_out_pp(t - 1))


def garantieluecke_pp(t):
    """The running *Garantielücke*, ``max(0, G(t) - A(t))``.  **A diagnostic.**

    Positive in the early durations of any charged contract — the anchor opens at
    358,94 € — and normally closing later as interest accrues.  The *Beitragsgarantie* is
    tested **once**, at *Rentenbeginn*, so this number affects **no** benefit: flooring
    :func:`db_pp`, :func:`cv_pp` or :func:`transfer_value_pp` at the guarantee is a listed
    pitfall and would misstate every early-duration exit.  It is published so that a reader
    sees the fact rather than infers it.
    """
    return max(0.0, guar_pp(t) - av_pp(t))


def pool_gefoerdert_pp(t):
    """Cumulative **subsidised** contributions credited up to period t, per policy.

    The saver's own contribution plus the Zulagen — the money whose benefit is taxed in
    full under § 22 Nr. 5 with no *Ertragsanteil*.  **Contributions only**: the model does
    not apportion investment return between the two pools, which a real
    *Leistungsmitteilung* must do, and says so rather than pretending otherwise.
    """
    if t < 1:
        return 0.0
    add = eigenbeitrag_pp(t) + zulage_pp(t)
    return add if t == 1 else pool_gefoerdert_pp(t - 1) + add


def pool_ungefoerdert_pp(t):
    """Cumulative **unsubsidised** contributions credited up to period t, per policy.

    Money paid into the same contract above the § 10a ceiling.  It enters the account and
    the *Beitragsgarantie* but draws no Zulage, and its benefit falls under the ordinary
    private-annuity rules rather than § 22 Nr. 5 — so a single Riester contract can carry
    two tax regimes at once and the provider must track the pools for the life of the
    contract.  Model point 8 is the cell that exercises it.
    """
    if t < 1:
        return 0.0
    add = (contrib_extra_pp() if (is_accum(t) and not
                                  (bfs_year() > 0 and t >= bfs_year())) else 0.0)
    return add if t == 1 else pool_ungefoerdert_pp(t - 1) + add


# === conversion at Rentenbeginn


def slueb_pp():
    """The *Schlussüberschussanteil* declared at *Rentenbeginn*, per policy.

    ``slueb_rate`` of the contributions credited over the life of the contract, which is
    ``guar_pp(t_conv() + 1)`` where no rider carve-out ran before the valuation date — the
    guarantee accumulator is exactly that sum, opening balance included.  It is **counted
    toward the guarantee**, which is the provider-favourable reading of a question the
    German corpus does not settle; excluding it, and the *Bewertungsreserven* share with
    it, raises the projected guarantee cost by their whole amount.
    """
    return slueb_rate * guar_pp(t_conv() + 1)                        # noqa: F821


def bewres_pp():
    """The *Bewertungsreserven* share allocated at *Rentenbeginn*, per policy.

    ``bewres_rate`` of the account at conversion — the individual entitlement to the
    *hälftige* participation in unrealised gains that § 153 Abs. 3 VVG gives on
    termination.  Like the *Schlussüberschussanteil* it is counted toward the guarantee
    here, and the level is a standardization.
    """
    T = t_conv()
    return bewres_rate * (dk_pp(T) + prem_to_av_pp(T)                # noqa: F821
                          + surplus_acct_pp(T))


def account_conv_pp():
    """The account available at *Rentenbeginn* before the guarantee is applied, per policy.

    ``D(T) + S(T) + U(T) + slueb_pp() + bewres_pp()``.  ``S(T)`` is there because the final
    contribution year's Zulage is credited **in** the conversion year; no interest is
    credited in the conversion year, because the account is converted at the start of it.
    """
    T = t_conv()
    return (dk_pp(T) + prem_to_av_pp(T) + surplus_acct_pp(T)
            + slueb_pp() + bewres_pp())


def capital_conv_pp():
    """V: the capital actually converted at *Rentenbeginn*, per policy.

    ``max(account_conv_pp(), guar_pp(t_conv() + 1))`` — the *Beitragserhaltungszusage*
    applied, once, at the only moment the AltZertG requires it.  Where the account falls
    short the insurer makes up the difference out of its own funds; that difference is
    :func:`garantieluecke_conv_pp`.
    """
    return max(account_conv_pp(), guar_pp(t_conv() + 1))


def garantieluecke_conv_pp():
    """Lambda: the *Garantielücke* the insurer funds at *Rentenbeginn*, per policy.

    ``max(0, guar_pp(t_conv() + 1) - account_conv_pp())``.  **The product's signature
    output**: it is the realised cost of the 100 % *Beitragsgarantie* on this path, and it
    is a *declared-rate* question rather than a *Rechnungszins* question — model point 11
    is the anchor on a 0,50 % declared rate and exists to make that visible.  The
    deterministic path reports it on one scenario; a time-value-of-options-and-guarantees
    calculation would re-evaluate the crediting rule per stochastic scenario, and the two
    scenarios shipped are a sensitivity rather than a distribution.
    """
    return max(0.0, guar_pp(t_conv() + 1) - account_conv_pp())


def ann_factor():
    """a-double-dot: the annuity-due factor at *Rentenbeginn* on the **first-order** basis.

    ``sum_{k>=0} v^k x kp(x(T), tau(T)) - 11/24`` at ``annuity_rechnungszins``, with
    survivorship on the generational annuitant table at factor **1.00** — the basis the
    market's *Rentenfaktor* is struck on — and the Woolhouse ``-11/24`` correction, which
    converts the annual-due factor to a monthly-due one.  The projection's own
    survivorship, by contrast, runs on the **second-order** basis at
    ``annuity_mort_be_factor``; the wedge between the two is the *Risikoüberschuss* in
    payment, which this model does not distribute.

    On the anchor — age 67 in calendar 2044 — it is 20,87222879, and that is the number a
    substitute annuity table must reproduce for the notes' worked example to close.
    """
    v = 1.0 / (1.0 + annuity_rechnungszins)                          # noqa: F821
    x0, tau0 = age(t_conv()), calendar_year(t_conv())
    total, kp, k = 0.0, 1.0, 0
    while kp > 0.0 and x0 + k <= omega_age:                          # noqa: F821
        total += v ** k * kp
        kp *= 1.0 - annuity_mort_rate(x0 + k, tau0 + k)
        k += 1
    return total - woolhouse                                        # noqa: F821


def rentenfaktor_curr():
    """R_c: the current *Rentenfaktor* implied by the model's own annuity basis.

    ``(1 - rentenfaktor_margin) x 10 000 / (12 x ann_factor())``.  The whole payout-phase
    loading — the *Sicherheitsabschlag* and the administration margin — sits in this one
    deduction rather than being taken partly here and partly out of each instalment, which
    would double-count; the insurer's real payout administration is instead an explicit
    expense cash flow.  On the anchor it is 27,947822, **below** the guaranteed 29,00, so
    the guarantee binds.
    """
    return ((1.0 - rentenfaktor_margin) * 10000.0                    # noqa: F821
            / (12.0 * ann_factor()))


def rentenfaktor_applied():
    """R: the *Rentenfaktor* actually applied, ``max(rentenfaktor_guar(), rentenfaktor_curr())``.

    The German market's own construction: the guaranteed factor is a floor struck at
    inception, and a provider whose current basis has become more generous applies the
    better one.  The two are **independent** — one is a contract term, the other a function
    of the shipped annuity table — so the model states which is authoritative when they
    disagree instead of leaving it to be inferred.
    """
    return max(rentenfaktor_guar(), rentenfaktor_curr())


def annuity_month_pp():
    """The monthly annuity instalment per policy, in euros.

    ``annuity_capital_pp() / 10 000 x rentenfaktor_applied()`` — the *Rentenfaktor* is
    quoted per 10 000 € of capital, which is the German market's convention and the reason
    a factor of 29,00 is a monthly and not an annual amount.  Zero on a commuted contract.
    """
    return annuity_capital_pp() / 10000.0 * rentenfaktor_applied()


def is_kleinbetrag():
    """True where the annuity is small enough to be commuted as a *Kleinbetragsrente*.

    The provider may pay the whole capital as an *Abfindung*, without *schädliche
    Verwendung*, where the monthly annuity would not exceed 1 % of the monthly
    *Bezugsgröße* of § 18 SGB IV.  Two standardizations sit here and both are stated rather
    than buried.  The test is applied to the annuity **actually payable after the elected
    lump sum**, which is the reading that trips *less* often; and the threshold is held
    **flat in nominal terms**, while the *Bezugsgröße* is reset annually — on a
    seventeen-year deferral that **understates** the commutation rate, and the direction of
    the error is said out loud.

    The commutation is **computed, not assumed**: the model tests the annuity it has
    actually produced, so the commutation rate on a book is an output rather than an input.
    Given how much of the German Riester book runs at the *Sockelbeitrag*, that is the right
    way round.
    """
    test = ((1.0 - min(teilkapital_share(), teilkapital_cap))         # noqa: F821
            * capital_conv_pp() / 10000.0
            * rentenfaktor_applied())
    return bool(test <= kleinbetrag_threshold_mth)                   # noqa: F821


def teilkapital_pp():
    """The *Teilkapitalauszahlung* paid at *Rentenbeginn*, per policy.

    ``min(teilkapital_share(), teilkapital_cap) x capital_conv_pp()``: the elected share,
    clamped at the statutory 30 %, taken as a lump sum without losing the subsidy.  A larger
    election would be *schädliche Verwendung* of the excess rather than a bigger lump sum,
    so the model caps it rather than modelling the sanction.  **Zero on a commuted
    contract**: an *Abfindung* is the whole capital in one payment, so there is no lump sum
    beside it.
    """
    if is_kleinbetrag():
        return 0.0
    return min(teilkapital_share(), teilkapital_cap) * capital_conv_pp()  # noqa: F821


def annuity_capital_pp():
    """The capital left to annuitise after the elected lump sum, per policy.

    ``capital_conv_pp() - teilkapital_pp()``, and zero on a commuted contract.  The AltZertG
    requires the remainder after the lump sum to buy a **lifelong** benefit with constant or
    rising payments; a falling annuity is not certifiable and a pure drawdown with no
    lifelong element is not either.
    """
    if is_kleinbetrag():
        return 0.0
    return capital_conv_pp() - teilkapital_pp()


def commutation_pp():
    """The *Kleinbetragsrenten-Abfindung* paid at *Rentenbeginn*, per policy.

    The **whole** conversion capital where :func:`is_kleinbetrag` holds, and zero
    otherwise.  It is *förderunschädlich* — no Zulage is repaid — and since 2018 it is taxed
    under the *Fünftelregelung* of § 34 EStG, which is context rather than a cash flow here
    because this model publishes gross liability flows.
    """
    return capital_conv_pp() if is_kleinbetrag() else 0.0


def annuity_pp(t):
    """a(t): the annual annuity per policy in payout year t — twelve monthly instalments.

    ``12 x annuity_month_pp()``, level, paid at the start of the payout year to whoever
    :func:`pols_annuity_pay` says is paid.  It does **not** read
    :func:`rentengarantie_years`: the guarantee period changes who is paid and never how
    much, and a model point with no guarantee period pays the *same* annuity to a smaller
    count.  Zero before *Rentenbeginn* and zero on a commuted contract.
    """
    if not is_payout(t) or t > proj_len() or is_kleinbetrag():
        return 0.0
    return 12.0 * annuity_month_pp()


# === benefits on exit


def db_pp(t):
    """The death benefit per policy in period t, **gross** of the *Rückzahlungsbetrag*.

    The account value after the year's interest, ``av_pp_at(t, "AFT_INT")``, so there is no
    sum at risk and no *Risikobeitrag* anywhere in the accumulation.  Zero in payout, the
    account having become an annuity.  It is **not** floored at :func:`guar_pp`: the
    *Beitragsgarantie* is tested at *Rentenbeginn* and nowhere else.  On death without a
    transfer to a surviving spouse's own certified contract the provider withholds the
    Zulagen and the § 10a relief and remits them, but that is a tax collection and netting
    it here would understate the insurer's outgo.
    """
    if not is_accum(t):
        return 0.0
    return av_pp_at(t, "AFT_INT")


def cv_pp(t):
    """The *Rückkaufswert* per policy in period t, gross of the *Rückzahlungsbetrag*.

    ``av_pp_at(t, "AFT_INT") x (1 - stornoabzug_rate)``.  The statutory floor is the
    *Deckungskapital* computed on at least five-year cost spreading, which is satisfied by
    construction here because the acquisition charge is spread over exactly five years.
    Not floored at the guarantee.
    """
    if not is_accum(t):
        return 0.0
    return av_pp_at(t, "AFT_INT") * (1.0 - stornoabzug_rate)         # noqa: F821


def transfer_value_pp(t):
    """The *Anbieterwechsel* transfer value per policy in period t.

    ``max(0, av_pp_at(t, "AFT_INT") - transfer_charge)``: the full account less a flat
    charge, with **no** *Stornoabzug*.  That is the whole economic difference between a
    transfer and a surrender, and collapsing the two into one decrement is a listed
    pitfall — it would apply a percentage charge where a flat one belongs and, far worse,
    would attribute the *schädliche Verwendung* consequences of a *Kündigung* to an exit
    that has none.
    """
    if not is_accum(t):
        return 0.0
    return max(0.0, av_pp_at(t, "AFT_INT") - transfer_charge)        # noqa: F821


def exit_charge_pp(t):
    """The charge the insurer retains on the year's exits — an **aggregate**, not per policy.

    ``stornoabzug_rate x A(t+1) x pols_lapse(t) + min(transfer_charge, A(t+1)) x
    pols_transfer(t)``.  It is the residue that keeps the account roll-forward exact: the
    account released by an exiting policy either leaves as a benefit or stays with the
    insurer as this charge, and :func:`check_av_roll_fwd` closes only when both are
    counted.  The name keeps the ``_pp`` suffix of the notes' own symbol table.
    """
    if not is_accum(t):
        return 0.0
    a = av_pp_at(t, "AFT_INT")
    return (stornoabzug_rate * a * pols_lapse(t)                     # noqa: F821
            + min(transfer_charge, a) * pols_transfer(t))            # noqa: F821


# === the cash flow statement


def claims(t, kind=None):
    """Benefit outgo in period t, by kind; the total over all six kinds when kind is omitted.

    ``"DEATH"``
        the account value paid at the end of the year of death, gross of the
        *Rückzahlungsbetrag*.  Zero in payout.

    ``"LAPSE"``
        the *Rückkaufswert* on a *Kündigung*, net of the *Stornoabzug* and gross of the
        *Rückzahlungsbetrag*.

    ``"TRANSFER"``
        the *Anbieterwechsel* transfer value, a **separate** decrement from surrender with
        no *Stornoabzug* and no subsidy consequence.

    ``"LUMPSUM"``
        the *Teilkapitalauszahlung* at *Rentenbeginn*, on ``pols_conv()``, in the
        conversion year only.

    ``"COMMUTATION"``
        the *Kleinbetragsrenten-Abfindung* at *Rentenbeginn*, on ``pols_conv()``, in the
        conversion year only.  A contract pays this **or** a lump sum and an annuity, never
        both.

    ``"ANNUITY"``
        the year's twelve instalments, on ``pols_annuity_pay(t)`` — which is
        ``pols_conv()`` inside the *Rentengarantiezeit* and ``pols_if(t)`` afterwards.
    """
    if kind is None:
        return sum(claims(t, k) for k in ("DEATH", "LAPSE", "TRANSFER",
                                          "LUMPSUM", "COMMUTATION", "ANNUITY"))
    if kind == "DEATH":
        return db_pp(t) * pols_death(t)
    if kind == "LAPSE":
        return cv_pp(t) * pols_lapse(t)
    if kind == "TRANSFER":
        return transfer_value_pp(t) * pols_transfer(t)
    if kind == "LUMPSUM":
        return teilkapital_pp() * pols_conv() if t == t_conv() else 0.0
    if kind == "COMMUTATION":
        return commutation_pp() * pols_conv() if t == t_conv() else 0.0
    if kind == "ANNUITY":
        return annuity_pp(t) * pols_annuity_pay(t)
    raise ValueError("invalid kind")


def premiums(t):
    """The saver's own contribution income in period t, an inflow.

    ``(eigenbeitrag_paid_pp(t) + contrib_extra_pp) x l(t)``: the *Eigenbeitrag* **after**
    the *Ratenzuschlag*, plus any unsubsidised contribution.  It excludes the Zulagen,
    which are :func:`zulagen`, and it excludes ``rider_prem_pp``, which is the biometric
    rider's premium and belongs to the rider's own liability rather than to this one.
    """
    extra = (contrib_extra_pp() if (is_accum(t) and not
                                    (bfs_year() > 0 and t >= bfs_year())) else 0.0)
    return (eigenbeitrag_paid_pp(t) + extra) * pols_if(t)


def zulagen(t):
    """The state *Zulage* income in period t, an inflow: ``zulage_pp(t) x l(t)``.

    **A contribution with a different payer**, published in its own column and never folded
    into :func:`premiums`.  It is paid by the ZfA to the provider, credited to the
    contract, counted in the *Beitragsgarantie* and invested; it never reaches the saver's
    bank account and it never appears with a negative sign.  On the low-income model points
    it is the **majority** of the contribution, which is the whole economics of the product
    and is invisible in a statement that nets it against the premium.
    """
    return zulage_pp(t) * pols_if(t)


def int_credited(t):
    """Interest credited to the account in period t, aggregated: ``int_credited_pp(t) x l(t)``.

    **Reported, not summed into** :func:`net_cf`: it is money moving inside the account,
    not across the insurer's boundary.  It is published because the account roll-forward is
    unreadable without it and because the guarantee's cost is entirely a question of how it
    compares with the contributions the guarantee accumulates.
    """
    return int_credited_pp(t) * pols_if(t)


def expenses(t):
    """Total expense outgo in period t, excluding commission.

    Four components, all **[std]** because no German insurer publishes a unit cost.  The
    acquisition expense ``expense_acq + expense_acq_rate x beitragssumme()`` at issue, only
    on a point with ``duration_init() == 0``.  Per-policy maintenance ``expense_maint``
    inflating at ``expense_infl`` on **contract** duration, on the in-force, in
    accumulation only.  ``expense_annuity`` per annuitant actually paid, in payout.  And
    ``expense_claim`` per death, surrender or transfer.  The maintenance figure carries the
    Zulage administration — the *Dauerzulageantrag*, the annual data exchange with the ZfA
    and the *Leistungsmitteilung* — which is a real and product-specific cost.
    """
    total = 0.0
    if t == 1 and duration_init() == 0:
        total += (expense_acq + expense_acq_rate                     # noqa: F821
                  * beitragssumme()) * pols_if(1)
    if is_accum(t):
        total += (expense_maint                                      # noqa: F821
                  * (1.0 + expense_infl) ** (duration(t) - 1)        # noqa: F821
                  * pols_if(t))
    total += expense_annuity * pols_annuity_pay(t)                   # noqa: F821
    total += expense_claim * (pols_death(t) + pols_lapse(t)          # noqa: F821
                              + pols_transfer(t))
    return total


def commissions(t):
    """Commission outgo in period t **[std]**, published beside :func:`expenses`.

    ``comm_rate_init x beitragssumme()`` at issue on a point written at the valuation date,
    otherwise ``comm_rate_renew`` of the contributions credited — the *Eigenbeitrag* and
    the Zulagen alike, because the provider is remunerated on what it administers.  The
    initial rate sits at the *Höchstzillmersatz*; **the cash leaves at issue while the
    charge is recovered over five years**, and that gap is the new-business strain the
    insurer carries.  Zero from *Rentenbeginn*.  It is a **separate** column from
    :func:`expenses` and :func:`net_cf` subtracts each exactly once.
    """
    if t == 1 and duration_init() == 0:
        return comm_rate_init * beitragssumme() * pols_if(1)         # noqa: F821
    if not is_accum(t):
        return 0.0
    return comm_rate_renew * (eigenbeitrag_pp(t) + zulage_pp(t)) * pols_if(t)  # noqa: F821


def net_cf(t):
    """The net liability cash flow of period t, **income positive**.

    Contributions and Zulagen in, the six kinds of benefit out, expenses and commission
    out.  ``int_credited`` is **not** in it: interest moves money inside the account rather
    than across the insurer's boundary.  The notes' own sign and the library-wide one.

    The shape to expect on an in-force accumulation cell is a modest positive: the
    contribution and the Zulage exceed the expected exit benefits and the expense, and the
    surplus builds the account.  Then a very large negative in the conversion year — the
    *Teilkapitalauszahlung* or the *Abfindung* leaves in one payment — followed by a long
    thin negative tail of annuity instalments.
    """
    return (premiums(t) + zulagen(t)
            - claims(t, "DEATH") - claims(t, "LAPSE") - claims(t, "TRANSFER")
            - claims(t, "LUMPSUM") - claims(t, "COMMUTATION")
            - claims(t, "ANNUITY")
            - expenses(t) - commissions(t))


def liability_cf(t):
    """The same stream as :func:`net_cf`, outgo positive: ``-net_cf(t)`` exactly.

    The orientation a valuation layer consumes: a Solvency II best estimate is
    ``sum v(t) liability_cf(t)`` over the relevant risk-free term structure, plus a risk
    margin.  Published as a column beside :func:`net_cf` so the sign convention is
    verifiable in the frame rather than only in prose.
    """
    return -net_cf(t)


# === the check identities


def check_net_cf_resid(t):
    """The cash flow statement's own reconciliation residual in period t; zero everywhere.

    ``net_cf(t)`` less ``premiums + zulagen`` less the six ``claims_*`` less ``expenses``
    less ``commissions``, each read from the same published cells :func:`result_cf` prints.
    What it catches is a column that is in the frame but not in the total, or in the total
    twice: dropping ``zulagen`` from the sum, folding ``commissions`` into ``expenses`` and
    subtracting both, or summing ``int_credited`` into the net — the last being the most
    tempting, because interest is the largest number on the row.
    """
    return net_cf(t) - (
        premiums(t) + zulagen(t)
        - claims(t, "DEATH") - claims(t, "LAPSE") - claims(t, "TRANSFER")
        - claims(t, "LUMPSUM") - claims(t, "COMMUTATION")
        - claims(t, "ANNUITY")
        - expenses(t) - commissions(t))


def check_net_cf():
    """True when the cash flow statement reconciles in every projected period.

    **delib's first ruling**: every model in this library publishes the identity that
    reconstructs ``net_cf(t)`` from its statement's own published parts, so that the
    headline number of a cash flow model is not the one quantity nothing checks.  No
    argument, one bool over all ``t``; :func:`check_net_cf_resid` gives the signed residual
    of the period that failed.
    """
    return all(abs(check_net_cf_resid(t)) <= roll_fwd_tol            # noqa: F821
               * max(1.0, guar_pp(t_conv() + 1))
               for t in range(1, proj_len() + 1))


def check_av_roll_fwd_resid(t):
    """The aggregate account roll-forward residual in period t; zero everywhere.

    While ``t < t_conv()``: the account at the start of ``t + 1`` less the account at the
    start of ``t``, the year's *Sparbeitrag* and the year's credited interest, plus the
    three exit benefits and the charge the insurer retained on them.  Every euro that
    leaves the account either becomes a benefit or stays with the insurer as
    :func:`exit_charge_pp`, and omitting the second is the way this identity usually fails
    — the *Stornoabzug* and the transfer charge look like income rather than like account
    released.

    From ``t_conv()`` the identity becomes the assertion that the account is **gone**: the
    residual is ``av_pp(t + 1)``, which is zero because conversion extinguishes it.
    """
    if t >= t_conv():
        return av_pp(t + 1)
    return (av_at(t + 1, "BEF_PREM")
            - (av_at(t, "BEF_PREM") + prem_to_av_pp(t) * pols_if(t)
               + int_credited(t)
               - claims(t, "DEATH") - claims(t, "LAPSE")
               - claims(t, "TRANSFER") - exit_charge_pp(t)))


def check_av_roll_fwd():
    """True when the account rolls forward exactly in every projected period."""
    return all(abs(check_av_roll_fwd_resid(t)) <= roll_fwd_tol       # noqa: F821
               * max(1.0, guar_pp(t_conv() + 1))
               for t in range(1, proj_len() + 1))


def check_guar_roll_fwd_resid(t):
    """The *Beitragsgarantie* accumulator's roll-forward residual in period t; zero everywhere.

    ``G(t+1) - G(t) - E(t) - Z(t) - contrib_extra + kappa(t)`` while ``t <= t_conv()``, and
    ``G(t+1) - G(t)`` afterwards, where the accumulator is frozen.  It catches the three
    ways this accumulator is usually built wrong: adding the entitlement of year ``t``
    rather than the Zulage **credited** in it, adding interest to a guarantee that is
    nominal, and dropping the unsubsidised contribution, which the undertaking covers
    because it is on the *Altersvorsorgebeiträge* paid in and does not distinguish the
    pools.
    """
    if t > t_conv():
        return guar_pp(t + 1) - guar_pp(t)
    extra = (contrib_extra_pp() if (is_accum(t) and not
                                    (bfs_year() > 0 and t >= bfs_year())) else 0.0)
    return (guar_pp(t + 1) - guar_pp(t) - eigenbeitrag_pp(t)
            - zulage_pp(t) - extra + guar_carve_out_pp(t))


def check_guar_roll_fwd():
    """True when the guarantee accumulator rolls forward and the 20 % carve-out cap holds.

    Two conditions, because the second is the one a rider premium breaks silently:
    ``guar_carve_out_pp(t)`` must never exceed ``guar_carve_out_cap`` times the total
    contribution including the rider premium, so raising ``rider_prem_pp`` past the cap
    cannot shrink the guarantee further.
    """
    ok = all(abs(check_guar_roll_fwd_resid(t)) <= roll_fwd_tol       # noqa: F821
             * max(1.0, guar_pp(t_conv() + 1))
             for t in range(1, proj_len() + 1))
    cap = all(guar_carve_out_pp(t) <= guar_carve_out_cap             # noqa: F821
              * (eigenbeitrag_pp(t) + zulage_pp(t) + contrib_extra_pp()
                 + rider_prem_pp()) + roll_fwd_tol                   # noqa: F821
              for t in range(1, t_conv()))
    return bool(ok and cap)


def check_pols_roll_fwd_resid(t):
    """The in-force roll-forward residual in period t; zero everywhere.

    ``l(t) - l(t+1) - pols_death(t) - pols_lapse(t) - pols_transfer(t)``, less the whole
    converting cohort in the conversion year of a **commuted** contract, where the
    *Kleinbetragsrenten-Abfindung* discharges the contract outright and the population
    leaves through an exit that is not a decrement.  What it catches is a misindexed
    recursion — rolling forward with ``w(t-1)`` or ``q(t+1)`` — and a transfer decrement
    that moves ``pols_if`` without being counted, which is how collapsing transfer into
    surrender usually shows up.
    """
    commuted = (pols_conv() if (t == t_conv() and is_kleinbetrag()) else 0.0)
    return (pols_if(t) - pols_if(t + 1) - pols_death(t) - pols_lapse(t)
            - pols_transfer(t) - commuted)


def check_pols_roll_fwd():
    """True when the in-force roll-forward closes and the whole cohort is accounted for.

    Two conditions.  The per-period recursion above, and the **closure identity**: the
    deaths, surrenders, transfers and any commuted cohort summed over the whole projection,
    plus ``pols_if(proj_len() + 1)``, equal ``pols_if_init()``.  The second is built by
    direct summation over the exit cells with no reference to the recursion that produced
    ``pols_if``, so it catches a wrong starting cohort and an exit counted in two places,
    which the telescoping first condition cannot.  ``mort_rate`` is 1 at ``omega_age``, so
    the survivor term is exactly zero and the identity is exact rather than approximate.
    """
    n = proj_len()
    step = all(abs(check_pols_roll_fwd_resid(t)) <= roll_fwd_tol     # noqa: F821
               * max(pols_if_init(), 1.0)
               for t in range(1, n + 1))
    exits = sum(pols_death(s) + pols_lapse(s) + pols_transfer(s)
                for s in range(1, n + 1))
    if is_kleinbetrag():
        exits += pols_conv()
    closure = abs(exits + pols_if(n + 1) - pols_if_init()) <= (
        roll_fwd_tol * max(pols_if_init(), 1.0))                     # noqa: F821
    return bool(step and closure)


def check_conversion_resid(t):
    """The total absolute conversion residual, reported at ``t = t_conv()`` and zero elsewhere.

    Three identities are summed, all of them at the conversion year, because conversion is
    a single event rather than a recursion.  First, the guarantee is applied:
    ``capital_conv_pp() = max(account_conv_pp(), guar_pp(t_conv() + 1))``.  Second, the
    capital is fully disposed of: ``capital_conv_pp() = teilkapital_pp() +
    annuity_capital_pp() + commutation_pp()``, so a commuted contract pays no lump sum
    beside the *Abfindung* and an annuitised one pays no *Abfindung* beside the annuity.
    Third, the current *Rentenfaktor* and the annuity factor are consistent by
    construction: ``rentenfaktor_curr() x 12 x ann_factor() = (1 - rentenfaktor_margin) x
    10 000``, which is the identity that catches a Woolhouse correction applied twice, a
    factor struck on the second-order basis, or a margin taken both in the factor and in the
    instalment.

    Unlike the other residuals this one is an absolute total rather than a signed
    difference, because the three components have different units and there is nothing a
    signed sum of them would mean.
    """
    if t != t_conv():
        return 0.0
    r1 = capital_conv_pp() - max(account_conv_pp(), guar_pp(t_conv() + 1))
    r2 = capital_conv_pp() - (teilkapital_pp() + annuity_capital_pp()
                              + commutation_pp())
    r3 = (rentenfaktor_curr() * 12.0 * ann_factor()
          - (1.0 - rentenfaktor_margin) * 10000.0)                   # noqa: F821
    return abs(r1) + abs(r2) + abs(r3)


def check_conversion():
    """True when the conversion at *Rentenbeginn* closes on all three identities."""
    return all(check_conversion_resid(t) <= roll_fwd_tol             # noqa: F821
               * max(1.0, guar_pp(t_conv() + 1))
               for t in range(1, proj_len() + 1))


def check_zulage_lag_resid(t):
    """The Zulage-lag residual in period t; zero everywhere.

    ``zulage_pp(t)`` less what the ZfA lag says it must be: ``zulage_init_pp()`` at
    ``t = 1``, ``zulage_granted_pp(t - 1)`` for ``2 <= t <= t_conv()``, and zero after the
    conversion year.  It is the mechanical form of the first listed pitfall — collapsing
    the calendar lag on income and the payment lag on cash into one offset — and of the
    second, dropping the final contribution year's Zulage, which the ``t = t_conv()`` case
    pins down.
    """
    if t == 1:
        return zulage_pp(1) - zulage_init_pp()
    if t <= t_conv():
        return zulage_pp(t) - zulage_granted_pp(t - 1)
    return zulage_pp(t)


def check_zulage_lag():
    """True when the Zulage is credited one projection year after it is earned, everywhere."""
    return all(abs(check_zulage_lag_resid(t)) <= roll_fwd_tol        # noqa: F821
               * max(1.0, guar_pp(t_conv() + 1))
               for t in range(1, proj_len() + 1))


# === result tables


def result_cf():
    """Result table of cash flows, indexed by period t, ``1 ... proj_len()``.

    ``pols_if`` is the **start**-of-period count, which is the weight applied to every cash
    flow on the same row, and its first value is ``pols_if_init()`` exactly.
    ``pols_annuity_pay`` is beside it because during the *Rentengarantiezeit* the two
    differ and the annuity is paid on the second.  ``premiums`` and ``zulagen`` are
    **separate** income columns — the Zulage is a contribution with a different payer, and
    folding it into the premium destroys the one number this product is about.
    ``int_credited`` is a state movement, **reported and not summed into** ``net_cf``.  The
    six ``claims_*`` columns are the split of ``claims(t, kind)``; there is no bare
    ``claims`` subtotal column, because a statement must not publish a subtotal beside its
    own parts.  ``liability_cf`` is ``net_cf`` outgo-positive.

    The frame is uniform across model points and runs to ``proj_len()`` on every one of
    them, including a contract commuted at *Rentenbeginn*, which then carries zeros to the
    end rather than being truncated.
    """
    ts = list(range(1, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_annuity_pay": [pols_annuity_pay(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "zulagen": [zulagen(t) for t in ts],
            "int_credited": [int_credited(t) for t in ts],
            "claims_death": [claims(t, "DEATH") for t in ts],
            "claims_lapse": [claims(t, "LAPSE") for t in ts],
            "claims_transfer": [claims(t, "TRANSFER") for t in ts],
            "claims_lumpsum": [claims(t, "LUMPSUM") for t in ts],
            "claims_commutation": [claims(t, "COMMUTATION") for t in ts],
            "claims_annuity": [claims(t, "ANNUITY") for t in ts],
            "expenses": [expenses(t) for t in ts],
            "commissions": [commissions(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
            "liability_cf": [liability_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_acct():
    """Result table of the two state variables and the subsidy chain, indexed by t.

    The account and the guarantee side by side with the contribution that drives both, so a
    reader can follow the *Garantielücke* opening and closing.  Not part of the cash flow
    statement and not asserted by the conventions suite; it is the frame the technical
    notes' worked example reads its per-policy columns from.
    """
    ts = list(range(1, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "income_ref": [income_ref(t) for t in ts],
            "zulage_entitlement_pp": [zulage_entitlement_pp(t) for t in ts],
            "zulage_pp": [zulage_pp(t) for t in ts],
            "mindesteigenbeitrag_pp": [mindesteigenbeitrag_pp(t) for t in ts],
            "eigenbeitrag_pp": [eigenbeitrag_pp(t) for t in ts],
            "acq_charge_pp": [acq_charge_pp(t) for t in ts],
            "admin_charge_pp": [admin_charge_pp(t) for t in ts],
            "prem_to_av_pp": [prem_to_av_pp(t) for t in ts],
            "int_credited_pp": [int_credited_pp(t) for t in ts],
            "dk_pp": [dk_pp(t) for t in ts],
            "surplus_acct_pp": [surplus_acct_pp(t) for t in ts],
            "av_pp": [av_pp(t) for t in ts],
            "guar_pp": [guar_pp(t) for t in ts],
            "garantieluecke_pp": [garantieluecke_pp(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

valuation_year = 2027

omega_age = 110

grundzulage = 175.0

kinderzulage_pre2008 = 185.0

kinderzulage_post2008 = 300.0

berufseinsteiger_bonus = 200.0

mindest_rate = 0.04

foerder_ceiling = 2100.0

sockelbeitrag = 60.0

zulage_lag = 1

acq_charge_rate = 0.025

acq_charge_years = 5

admin_charge_prem_rate = 0.04

admin_charge_fixed = 12.0

guar_carve_out_cap = 0.2

slueb_rate = 0.02

bewres_rate = 0.01

teilkapital_cap = 0.3

kleinbetrag_threshold_mth = 39.55

rentenfaktor_margin = 0.3

annuity_rechnungszins = 0.01

woolhouse = 0.4583333333333333

mort_be_factor = 0.8

annuity_mort_be_factor = 1.15

annuity_base_year = 2027

stornoabzug_rate = 0.02

transfer_charge = 50.0

expense_maint = 30.0

expense_infl = 0.02

expense_annuity = 24.0

expense_claim = 80.0

expense_acq = 150.0

expense_acq_rate = 0.02

comm_rate_init = 0.025

comm_rate_renew = 0.015

roll_fwd_tol = 1e-09

pd = ("Module", "pandas")
