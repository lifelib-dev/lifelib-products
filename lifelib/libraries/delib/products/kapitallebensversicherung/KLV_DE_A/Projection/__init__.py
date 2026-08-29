# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.KLV_DE_A` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the worked example's anchor cell
    >>> Projection.point_id = 8            # or switch the default

``t`` counts **policy years, 1-based and measured from issue**: policy year ``t`` runs from
the (``t``-1)-th policy anniversary to the ``t``-th, ``age(t) = issue_age() + t - 1`` is the
attained age at the start of it and ``duration(t) = t - 1`` the completed policy years.
Counting from issue rather than from the valuation date makes every duration-keyed lookup —
the *Stornoabzug*, the surrender table, the § 169 Abs. 3 five-year spreading — direct. The
frame runs ``t = t_start() ... proj_len()`` contiguously, with
``t_start() = duration_init() + 1`` and ``proj_len() = policy_term()``, the **last projected
period index** and the policy year in which the *Ablauf* falls. **There is no
``t = proj_len() + 1`` row.**

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent directory,
``products/kapitallebensversicherung/``, read at run time rather than stored inside the
model. The model folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no
embedded values — so a diff of the model shows logic changes only, and an input can be
edited or swapped without rewriting the model. This follows ``annuallife.TradLife_A``;
contrast ``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model through
modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``KLV_DE_A`` folder without its parent's CSVs produces a model that reads and then fails on
first evaluation.

Each table has a filename Reference and a reader Cells, both on :mod:`~.KLV_DE_A.Data`,
reached here through the ``data`` Reference:

========================  =================================  ==========================
Reference                 Cells                              File
========================  =================================  ==========================
model_point_file          data.model_point_table()           model_point_table.csv
mort_table_file           data.mort_table()                  mort_table.csv
lapse_file                data.lapse_table()                 lapse_table.csv
surplus_rate_file         data.surplus_rate_table()          surplus_rate_table.csv
cost_file                 data.cost_table()                  cost_table.csv
freq_loading_file         data.freq_loading_table()          freq_loading_table.csv
deckrv_file               data.deckrv_table()                deckrv_table.csv
========================  =================================  ==========================

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` and ``savings.CashValue_SE``
wherever those models have an analogue — ``pols_*`` for policy counts, plural nouns for
cash flows, ``*_rate`` for rates, ``*_pp`` for per-policy amounts, ``claims(t, kind)`` with
an uppercase ``kind`` string, ``*_at(t, timing)`` for the within-year reads. The technical
notes use compact actuarial symbols instead. The mapping is:

=========================  ==============================  ==========================
Notes symbol               Cells                           Meaning
=========================  ==============================  ==========================
(none)                     model_point()                   The selected model point row
n                          proj_len()                      Last policy year = policy_term
(none)                     t_start()                       First projected policy year
m                          prem_term()                     Beitragszahlungsdauer
x(t)                       age(t)                          Attained age in year t
k = t - 1                  duration(t)                     Completed policy years
SE                         sum_assured()                   Guaranteed Erlebensfallleistung
SD                         sum_death()                     Guaranteed Todesfallleistung
i1                         rechnungszins()                 First-order interest rate
v1^k                       disc_factor_1st(k)              First-order discount factor
kpx                        tpx_1st(k)                      First-order survival from issue
q1(t)                      mort_rate_base(t)               First-order mortality in year t
(table)                    mort_rate_at_age(x)             First-order rate at age x
q(t)                       mort_rate(t)                    Best-estimate mortality
f                          rating_factor()                 Risikozuschlag on the death leg
alpha, beta, gamma         alpha_rate(), beta_rate(),      Zillmersatz; premium loading;
                           gamma_rate()                    sum-insured loading
phi                        prem_freq_load()                Ratenzahlungszuschlag
(none)                     instalments()                   Payments a year
(pricing)                  pv_death_1st(), pv_maturity_1st(),  The equivalence's parts
                           pv_benefit_1st(), ann_due_prem_1st(),
                           ann_due_term_1st()
B                          prem_gross_pp()                 Annual Bruttobeitrag before phi
BS                         beitragssumme()                 Beitragssumme = B x m
A                          alpha_cost()                    Zillmered acquisition cost
P^n                        prem_net_level_pp()             Net level premium
P^Z                        prem_zill_pp()                  Zillmer premium
(prospective)              pv_benefit_fut(t),              The reserve's parts
                           ann_due_prem_fut(t)
V^n, V^Z, V^min            res_net_pp(t), res_zill_pp(t),  The three constructions
                           res_min_pp(t)
V(t)                       res_pp(t)                       Deckungskapital at start of t
(within year)              res_pp_at(t, timing)            BEF_PREM / AFT_PREM / AFT_INT
G(t)                       res_guar_pp(t)                  Section 169 value at end of t
RK(t)                      surr_value_pp(t)                Rueckkaufswert payable
(unit paid-up)             pu_single_prem(t)               Single premium for one unit
(none)                     bfz_si_pp()                     Beitragsfreie Versicherungssumme
(none)                     bfz_uplift_pp(t)                Section 169 uplift on election
(none)                     is_paid_up(t)                   Whether the contract is beitragsfrei
d(t)                       decl_rate(t)                    Declared laufende Verzinsung
z(t)                       zins_ueberschuss_rate(t)        Interest surplus rate
s(t)                       term_rate(t)                    Schlussueberschussanteilsatz
a(t)                       ans_rate(t)                     Ansammlungszinssatz
(base)                     surplus_base_pp(t)              Deckungskapital at allocation
C(t)                       surplus_credit_pp(t)            Surplus allocated for year t
S(t)                       term_bonus_pp(t)                Accrued Schlussueberschussanteil
U(t)                       av_pp(t)                        Ueberschussguthaben per policy
(within year)              av_pp_at(t, timing)             BEF_INT / AFT_INT / AFT_CREDIT
(aggregate)                av(t), av_at(t, timing)         The same, times pols_if(t)
Z(t)                       bonus_si_pp(t)                  Bonus sum insured
(offset)                   prem_offset_pp(t)               Beitragsverrechnung offset
B phi                      prem_charged_pp(t)              Zahlbeitrag before the offset
(none)                     prem_paid_pp(t)                 Zahlbeitrag actually paid
(none)                     premiums(t)                     Premium income
w(t)                       lapse_rate(t)                   Surrender rate
sigma(t)                   storno_rate(t)                  Stornoabzug rate
l(t)                       pols_if(t)                      In force at the start of year t
(within year)              pols_if_at(t, timing)           BEF_DECR / AFT_MORT / AFT_LAPSE
(exits)                    pols_death(t), pols_lapse(t),   Expected exits in year t
                           pols_maturity(t)
(none)                     benefit_full_pp(t)              Full death benefit before 161
(none)                     benefit_death_pp(t)             What a death claim pays
(none)                     benefit_maturity_pp(t)          What the Ablauf pays
claims_*                   claims(t, kind)                 DEATH / MATURITY / LAPSE
(none)                     inflation_factor(t)             Expense inflation factor
(none)                     claim_expenses(t)               Claim handling expense
(none)                     expenses_pp(t)                  Per-policy expense
E(t)                       expenses(t)                     Expense outgo, no commission
(none)                     commissions(t)                  Commission outgo
net_cf(t)                  net_cf(t)                       Net cash flow, income positive
liability_cf(t)            liability_cf(t)                 The same stream, outgo positive
=========================  ==============================  ==========================

.. rubric:: The declared rate is a total, not an add-on

The single most common way to get this product wrong. The *laufende Verzinsung* **is** the
*Garantieverzinsung* plus the *laufende Zinsüberschussbeteiligung*, so

    zins_ueberschuss_rate(t) = max(0, decl_rate(t) - rechnungszins())

is 1,70 pp on the anchor cell's 2,70 % declaration against a 1,00 % guarantee, and never
2,70 pp on top of 1,00 pp. The interest-surplus rate is **derived and never an input**. The
outer ``max`` is what keeps the ``nil`` scenario honest: the declared rate is then below the
guarantee, which the reserve roll-forward still meets in full, so the surplus is zero rather
than negative.

The base it multiplies is the ***Deckungskapital* at the allocation date** —
``max(res_pp_at(t, "AFT_INT"), 0)`` — not the sum insured and not the premium. That inner
``max`` is equally load-bearing: a *gezillmerte Deckungskapital* is **negative** for the
first several years, and a positive rate on a negative base credits a negative surplus. It
follows that a *gezillmert* contract earns **no** interest surplus in its early years even
though the § 153 VVG entitlement runs from inception — economically right, because there is
no fund to earn on, and worth saying because it looks like a bug.

.. rubric:: Three reserves, and the one the customer gets

:func:`res_zill_pp` is the *gezillmerte Deckungskapital*: it is exactly ``-alpha_cost()`` at
issue and stays negative for several years. :func:`res_min_pp` is the § 169 Abs. 3 VVG floor,
the same net reserve with the acquisition cost amortised **straight-line over the first five
contract years** rather than over the whole premium term. Because
``ann_due_prem_fut(t) / ann_due_prem_1st()`` falls roughly linearly over ``m`` years while
``max(0, 1 - k/5)`` reaches zero after five, the floor **normally binds** on a long
*gezillmert* contract, with equality only at durations 0 and ``m``. :func:`res_guar_pp` is
their maximum, floored at zero, struck at the **end** of policy year ``t`` because that is
what "zum Schluss der laufenden Versicherungsperiode" requires — so it reads the reserves at
``t + 1``.

With ``zillmer_on = 0`` (model point 13) ``alpha_cost()`` is zero, all three coincide and the
floor is slack — a useful invariance test. With ``prem_term = 1`` (model point 2) the 25 ‰
*Zillmersatz* buys almost nothing and the floor is slack from the first anniversary. Both are
the correct answer rather than a degenerate case.

Note that the acquisition cost is in the **premium** whether or not the contract is
zillmered: ``zillmer_on`` enters :func:`alpha_cost`, which is a *reserving* quantity, and not
the pricing equation, which always charges ``alpha_rate() * beitragssumme()``. That is why one
insurer can publish a *gezillmerte* and a non-*gezillmerte* edition of the same tariff at the
same price.

.. rubric:: Paid-up is not lapse, and it can fail

§ 165 VVG lets the policyholder demand conversion to a *prämienfreie Versicherung* at the end
of the current *Versicherungsperiode*, **provided the agreed *Mindestversicherungsleistung* is
reached**. The paid-up sum is bought with the § 169 value, so
``bfz_si_pp() = res_guar_pp(bfz_year()) / pu_single_prem(bfz_year() + 1)``, and the contract
stays in ``pols_if`` with that reduced sum in place of ``sum_assured()``. Where the sum falls
short of ``bfz_min_si``, the statute obliges the insurer to pay the § 169 value instead and
**the election becomes a surrender**: :func:`lapse_rate` returns 1.0 in that year, the whole
cohort leaves as ``claims(t, "LAPSE")`` and every later row is zero. Model point 11 takes the
first branch and model point 12 the second.

Because the § 169 floor generally exceeds the Zillmer reserve, the paid-up sum bought is worth
more than the Zillmer reserve released. :func:`bfz_uplift_pp` is that difference, discounted
to the start of the election year, and it enters :func:`res_pp_at` so that
:func:`check_res_roll_fwd` still closes in the election year rather than being switched off
there.

.. rubric:: What surrender pays, and what it does not

    surr_value_pp(t) = res_guar_pp(t) * (1 - storno_rate(t))
                       + av_pp_at(t, "AFT_CREDIT")
                       + term_surr_share * term_bonus_pp(t + 1)

Three rules ride on that line. The ***Stornoabzug* bites on the guaranteed value only** — the
published deduction is a percentage of the *Deckungskapital* — so the accumulated
*Überschussguthaben* passes through undeducted. ``term_surr_share = 0`` in the base run: the
accrued *Schlussüberschussanteil* is paid at the *Ablauf* and on death and **not** on
surrender, which is the choice that does not invent an entitlement the sources do not
describe; the parameter is exposed rather than hard-coded. And the surrender value is what a
suicide inside three years is paid: § 161 VVG makes the insurer *leistungsfrei* **and**
obliges it to pay the *Rückkaufswert* including *Überschussanteile*, so the German rule is a
benefit **substitution** and not a forfeiture.

.. rubric:: The two mortality bases must not be crossed

:func:`mort_rate_base` is the first-order table rate: it prices and it reserves.
:func:`mort_rate` is ``mort_rate_base(t) * mort_be_factor`` with ``mort_be_factor = 0.75``:
it projects. The 33 % wedge is the *Sicherheitszuschlag*, whose systematic release **is** the
*Risikoüberschuss* — which this model does not compute, and which a model that reserves on
the best estimate has thrown away. ``rating_factor`` is a third thing again: it is the
*Risikozuschlag*, and it multiplies the first-order rate **in the death leg of the pricing and
the prospective reserve only** — never the survivorship factors, never the benefit, and never
a best-estimate rate. ``sex`` drives the decrement lookup and **must not enter the premium**:
German new business has been unisex since 21 December 2012, and the pricing basis here is a
fixed portfolio blend.

.. rubric:: The three Überschussverwendung systems

``ansammlung`` accumulates the credit at ``ans_rate`` in :func:`av_pp` and raises the maturity
benefit; ``bonus`` buys paid-up sum insured at first-order rates in :func:`bonus_si_pp`,
raising the **death** benefit immediately by the full bonus sum but accumulating only at
``rechnungszins``; ``beitragsverrechnung`` carries last year's credit forward as this year's
premium offset in :func:`prem_offset_pp` and neither balance grows. Because
``ans_rate > rechnungszins`` the first gives a higher maturity benefit and the second a higher
death benefit — exactly the asymmetry the sources record, and the test that distinguishes
them. A model that sets the two rates equal destroys it.

Under ``beitragsverrechnung`` the **renewal commission is charged on
:func:`prem_charged_pp`, not on :func:`prem_paid_pp`**: the intermediary is paid on the tariff
premium, the surplus offset being a policyholder rebate.

.. rubric:: Modules that are off in the base run

Two dynamic lapse constructions ship switched off, so the base run reproduces the worked
example while the machinery stays visible. **Premium-shock lapse**, ``beta_shock = 0``:
``1 + beta_shock * max(0, prem_paid_pp(t)/prem_paid_pp(t-1) - 1 - 0.05)``, inert on a level
*Bruttobeitrag* but live under *Beitragsverrechnung*, where a fall in the declared rate raises
the *Zahlbeitrag*. **Rate-gap lapse**, ``lapse_gap_a = 0``:
``lapse_gap_a * max(0, ref_rate - decl_rate(t) - 0.005)``, keyed on the gap between the
declared rate and what is available elsewhere. **No German calibration of any of these numbers
exists**, which is why both ship off. ``bwr_rate = 0`` likewise switches off the
*Beteiligung an den Bewertungsreserven*, on the reasoning that the *Sicherungsbedarf* has
routinely exhausted the half share.

.. rubric:: Sign convention

:func:`net_cf` is **income positive** — *Beiträge* in, claims, expenses and commission out —
which is the notes' own orientation and the library-wide sign. :func:`liability_cf` publishes
the same stream outgo-positive, ``liability_cf(t) = -net_cf(t)`` exactly. Both are columns of
:func:`result_cf`, so the identity is verifiable in the frame rather than only in prose.
:func:`expenses` **excludes** commission — the deliberate difference from the frlib chassis,
where commission sits inside the expense column — so the six flow columns of
:func:`result_cf` sum to :func:`net_cf` without a double count. That sum is what
:func:`check_net_cf` asserts, and it is this library's first ruling.

The shape to expect on the anchor cell is a large first-year strain, the *Zillmerung* and the
initial commission together far exceeding the first *Beitrag*, then positive margins that grow
as the *Deckungskapital* and the *Überschussguthaben* build, and a single very large negative
year at the *Ablauf* when the *Erlebensfallleistung* falls due.
"""

from modelx.serialize.jsonvalues import *

_formula = lambda point_id: None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

# --- the model point -------------------------------------------------------

def model_point():
    """The selected model point as a Series, indexed by ``point_id``."""
    return data.model_point_table().loc[point_id]                    # noqa: F821


def policy_id():
    """The policy identifier of the selected model point, e.g. ``DE-KLV-0001``."""
    return model_point()["policy_id"]


def sex():
    """The insured's sex, M or F.  **Decrement lookup only - never a pricing input.**

    § 20 Abs. 2 Satz 1 AGG was repealed and German new business has been unisex since
    21 December 2012, so :func:`prem_gross_pp` must be identical for two model points
    differing only here.  The first-order table is nevertheless sex-specific, because that
    is the raw material a unisex tariff blends; the blend itself is **[std]** and this model
    prices every point on its own ``sex`` row only through the *decrements*, which is what
    model points 1 and 7 exist to make visible.
    """
    v = model_point()["sex"]
    if v not in ("M", "F"):
        raise ValueError("invalid sex")
    return v


def smoker():
    """The insured's smoker status, N or S.

    Carried because the *Gesundheitsprüfung* asks, and because it is what a *Risikozuschlag*
    would be struck on.  It feeds :func:`rating_factor` through the model point rather than
    through a formula: DAV 2008 T R / NR exist for smoker-differentiated pricing but are not
    public, and no German insurer publishes a loading scale.
    """
    v = model_point()["smoker"]
    if v not in ("N", "S"):
        raise ValueError("invalid smoker")
    return v


def issue_year():
    """The calendar year of conclusion: the contract's **cohort identity**.

    It fixes the two DeckRV ceilings through :func:`hrz_max` and :func:`zillmer_max`, both of
    which stay with the contract for its whole term, and it fixes the income-tax cohort.  A
    4,00 % guarantee on a 2026 issue year is not a stress, it is a data error - which is why
    :func:`check_rechnungszins_cap` is a model invariant rather than a build script.
    """
    return int(model_point()["issue_year"])


def issue_age():
    """The age last birthday at issue, stepping at the policy anniversary **[std]**.

    No located German endowment wording states an age basis, so the convention is a
    standardization.  On this annual grid an implementation on real dates carries a
    fractional offset of at most one year.
    """
    return int(model_point()["issue_age"])


def duration_init():
    """The completed policy years at the valuation date; 0 for new business.

    It fixes where the frame opens - ``t_start() = duration_init() + 1`` - and it is what
    suppresses the acquisition expense and the initial commission on an in-force point, which
    incurred both long ago.  Model point 10 carries 14.
    """
    return int(model_point()["duration_init"])


def pols_if_init():
    """The number of policies represented at ``t_start()``: 1.0, a single-policy model point.

    The library's projections are per policy, so this is 1 everywhere; it is named rather than
    written as a literal because it is the scale of the roll-forward tolerances and because
    ``result_cf()``'s first ``pols_if`` must equal it exactly.
    """
    return float(model_point()["pols_if_init"])


def policy_term():
    """n: the *Versicherungsdauer* in years.  Equals :func:`proj_len`.

    The *Ablauf* falls at the end of policy year ``n``, and the *Erlebensfallleistung* is paid
    there to the survivors of that year's mortality.
    """
    return int(model_point()["policy_term"])


def prem_term():
    """m: the *Beitragszahlungsdauer* in years, at most :func:`policy_term`.

    ``m = 1`` is the *Einmalbeitrag* - the other premium form, and the case in which
    ``ann_due_prem_1st()`` collapses to 1, the *Beitragssumme* to the single premium itself
    and the 25 ‰ *Zillmersatz* to almost nothing.  ``m < n`` is the *abgekürzte
    Beitragszahlungsdauer*: premiums stop while cover runs on, and the reserve then rolls
    forward with no premium at all.
    """
    return int(model_point()["prem_term"])


def sum_assured():
    """SE: the guaranteed *Erlebensfallleistung*, in euros - the *Versicherungssumme*.

    Paid at the *Ablauf* to a survivor, plus the accumulated *Überschussguthaben*, any bonus
    sum insured and the accrued *Schlussüberschussanteil*.  It is **not** what a paid-up
    contract receives; see :func:`bfz_si_pp`.
    """
    return float(model_point()["sum_assured"])


def death_ratio():
    """The *Todesfallleistung* as a multiple of the *Erlebensfallleistung*.

    1.00 is the *gemischte Versicherung auf den Todes- und Erlebensfall* proper, where the two
    guaranteed sums are equal.  Below 1 the contract is the same chassis with an unequal death
    sum, subject to the *Mindesttodesfallschutz*: for a contract concluded from 1 April 2009
    the death sum must be at least 50 % of the *Beitragssumme*, which is a **model point
    design constraint** checked when the table is built and not a model formula.
    """
    return float(model_point()["death_ratio"])


def prem_freq():
    """The payment frequency, a key into *freq_loading_table.csv*.

    ``annual``, ``half_yearly``, ``quarterly`` or ``monthly``.  The frequency buys a
    *Ratenzahlungszuschlag* only where :func:`unterjaehrig_form` is ``unecht``.
    """
    v = model_point()["prem_freq"]
    if v not in data.freq_loading_table().index:                     # noqa: F821
        raise ValueError("no frequency loading for prem_freq " + str(v))
    return v


def unterjaehrig_form():
    """Whether a sub-annual premium is ``echt`` or ``unecht``.

    ``unecht`` means the *Versicherungsperiode* remains the year and the sub-annual payment is
    an **instalment** of an annual premium, which is what the *Ratenzahlungszuschlag*
    compensates.  ``echt`` means the period is genuinely sub-annual, and then **no loading
    applies**.  Model points 4 and 5 are the same monthly contract under the two readings, and
    the distinction is entirely lost on a model that treats frequency as a single multiplier.
    """
    v = model_point()["unterjaehrig_form"]
    if v not in ("echt", "unecht"):
        raise ValueError("invalid unterjaehrig_form")
    return v


def rechnungszins():
    """i1: the contract's own guaranteed technical rate, fixed at conclusion.

    A **contract term, not a market rate**: it is set once, at conclusion, and carried for the
    whole term, which is why a German in-force book is a stack of cohorts and why the in-force
    model point carries 1,75 % while new business carries 1,00 %.  It must not exceed the
    cohort's :func:`hrz_max`; :func:`check_rechnungszins_cap` asserts it.
    """
    return float(model_point()["rechnungszins"])


def zillmer_on():
    """1 where the *Deckungskapital* is *gezillmert*, 0 where it is not.

    A **per-tariff design choice a German insurer makes and publishes** - one carrier
    maintains a *gezillmerte* and a non-*gezillmerte* edition of the same tariff - and not an
    invariant of German practice.  It enters :func:`alpha_cost` and therefore the *reserve*;
    it does **not** enter the pricing equation, so the two editions cost the same.
    """
    return int(model_point()["zillmer_on"])


def cost_id():
    """The key into *cost_table.csv* naming this policy's loadings and expense basis."""
    return model_point()["cost_id"]


def surplus_use():
    """The *Überschussverwendung*: ``ansammlung``, ``bonus`` or ``beitragsverrechnung``.

    *Verzinsliche Ansammlung* accumulates the credit in :func:`av_pp` at ``ans_rate``; the
    *Bonussystem* buys paid-up sum insured in :func:`bonus_si_pp` at first-order rates; the
    *Beitragsverrechnung* carries the credit forward as next year's premium offset.  Because
    ``ans_rate > rechnungszins``, the first pays more at maturity and the second more on an
    early death - the asymmetry the corpus records and pitfall 15 asserts.
    """
    v = model_point()["surplus_use"]
    if v not in ("ansammlung", "bonus", "beitragsverrechnung"):
        raise ValueError("invalid surplus_use")
    return v


def scenario_id():
    """The key into *surplus_rate_table.csv* naming this policy's declared-rate path.

    ``base``, ``low`` or ``nil``.  The declared rate is **insurer-discretionary, revisable
    annually and capable of being zero**, so it is a scenario rather than an assumption; the
    ``nil`` path is the sourced statement that the surplus may be zero euros, made runnable.
    """
    return model_point()["scenario_id"]


def rating_factor():
    """f: the *Risikozuschlag* multiplier; 1.00 at standard rates.

    It scales the **first-order mortality in the death leg** of :func:`pv_death_1st` and
    :func:`pv_benefit_fut`, so it raises :func:`prem_gross_pp`.  It must not reach the
    survivorship factors, the benefit or the best-estimate rate: :func:`benefit_death_pp` and
    :func:`mort_rate` are both invariant to it.  No German scale is public; model point 14
    carries 1.50 **[std]**.
    """
    return float(model_point()["rating_factor"])


def av_pp_init():
    """The *Überschussguthaben* per policy carried at ``t_start()``, in euros.

    Zero for new business; model point 10 opens at duration 14 with 6 000 € already
    accumulated.  It is **not** part of the *Deckungsrückstellung*: § 341f HGB forms that
    provision *excluding verzinslich angesammelte Überschussanteile*, and the separation is
    the reason this balance is a cells of its own rather than part of :func:`res_pp`.
    """
    return float(model_point()["av_pp_init"])


def bonus_si_init():
    """The bonus sum insured already bought at ``t_start()``, in euros.

    Zero on every shipped model point: the *Bonussystem* point starts at issue with nothing
    bought.  The column exists so that an in-force contract on that system can be projected
    without a formula change.
    """
    return float(model_point()["bonus_si_init"])


def bfz_year():
    """The policy year at whose end *Beitragsfreistellung* is elected; 0 means never.

    A **deterministic model point column, not a decrement**.  The corpus establishes the § 165
    VVG right in full and gives **no take-up rate at all**, and the one market aggregate that
    would bear on it mixes the paid-up route in with surrenders and cannot be split - so
    modelling the election as a schedule keeps an unsourced number out of the base run.  What
    that costs is stated rather than hidden: a real German book converts a material,
    duration-dependent share to *beitragsfrei*, and this model shows that path only where a
    model point elects it.
    """
    return int(model_point()["bfz_year"])


# --- the projection frame --------------------------------------------------

def proj_len():
    """n: the **last projected period index**, equal to :func:`policy_term`.

    Not a row count.  ``result_cf().index[-1] == proj_len()`` on every model point, and the
    *Ablauf* falls at the end of policy year ``proj_len()``, where the survivors of that
    year's mortality take the *Erlebensfallleistung*.  **There is no ``t = proj_len() + 1``
    row**; ``pols_if(proj_len() + 1)`` and ``res_pp(proj_len() + 1)`` are defined because the
    closure and roll-forward identities need them, and they weight no cash flow.
    """
    return policy_term()


def t_start():
    """The first projected policy year: ``duration_init() + 1``.

    A new-business point opens at ``t = 1`` and an in-force point at the duration it has
    already run.  Where the frame *starts* is a product fact and the conventions suite does
    not assert it; contiguity from here to :func:`proj_len` is what it asserts instead.
    """
    return duration_init() + 1


def age(t):
    """x(t): the attained age at the start of policy year t, ``issue_age() + t - 1``."""
    return issue_age() + t - 1


def duration(t):
    """k = t - 1: the completed policy years at the start of policy year t.

    This, and not ``t``, is what every duration-keyed schedule is indexed on - the § 169
    Abs. 3 five-year spreading in :func:`res_min_pp` above all.
    """
    return t - 1


# --- the bases -------------------------------------------------------------

def mort_rate_at_age(x):
    """The first-order annual death rate at attained age x, on this policy's ``sex`` row.

    A table lookup into *mort_table.csv* and nothing else.  The table is a **[std]**
    Makeham-form proxy anchored at ``mort_rate_1st(M, 37) = 0.001200`` exactly, standing in
    for DAV 2008 T, which is the property of the Deutsche Aktuarvereinigung, is not public and
    is not redistributed here; see the ``Data`` docstring for what a replacement must
    preserve.
    """
    return float(data.mort_table().loc[(sex(), int(x)), "mort_rate_1st"])   # noqa: F821


def mort_rate_base(t):
    """q1(t): the **first-order** annual death rate in policy year t.

    This is the rate that **prices and reserves**: it drives :func:`pv_death_1st`,
    :func:`tpx_1st`, :func:`pv_benefit_fut` and the Fackler roll-forward.  It is *not* the
    rate the projection decrements at; see :func:`mort_rate`.  Crossing the two throws away
    the *Sicherheitszuschlag* whose systematic release is the *Risikoüberschuss*.
    """
    return mort_rate_at_age(age(t))


def mort_rate(t):
    """q(t): the **best-estimate** annual death rate in policy year t.

    ``mort_rate_base(t) * mort_be_factor`` with ``mort_be_factor = 0.75`` **[std]**, so the
    first-order table carries a 33 % safety loading.  Annual, as the library-wide convention
    requires; this model has no monthly rate because its grid is the contract's own annual
    one.  Invariant to :func:`rating_factor`, which is a *first-order* loading and has no
    business in a best estimate.
    """
    return min(1.0, mort_rate_base(t) * mort_be_factor)              # noqa: F821


def disc_factor_1st(k):
    """v1^k: the first-order discount factor over k years, at :func:`rechnungszins`.

    Used **only** by the pricing and reserving formulas.  The published cash flows are
    undiscounted; discounting a liability is a valuation layer's job and this library does not
    do it.
    """
    return (1.0 + rechnungszins()) ** (-k)


def tpx_1st(k):
    """kpx: first-order survival from the issue age to ``issue_age() + k``.

    ``tpx_1st(0) = 1`` and ``tpx_1st(k) = tpx_1st(k-1) * (1 - q1(issue_age + k - 1))``, on the
    **unrated** first-order table: :func:`rating_factor` loads the death *claim* rate, not the
    survivorship, so a *Risikozuschlag* raises the price without shortening the life the
    survival benefit is priced on.
    """
    if k <= 0:
        return 1.0
    return tpx_1st(k - 1) * (1.0 - mort_rate_at_age(issue_age() + k - 1))


def hrz_max():
    """The § 2 DeckRV *Höchstrechnungszins* for this contract's ``issue_year``.

    A **cohort fact**: the ceiling in force at conclusion applies for the whole term.  The
    published history splits 1994 and 2000 mid-year and a year-keyed table cannot, so both
    split years carry the **higher** of the two rates - which makes
    :func:`check_rechnungszins_cap` permissive rather than strict in exactly the two years
    where the model cannot know which half of the year a contract was written in **[std]**.
    """
    tbl = data.deckrv_table()                                        # noqa: F821
    y = min(max(issue_year(), int(tbl.index.min())), int(tbl.index.max()))
    return float(tbl.loc[y, "hoechstrechnungszins"])


def zillmer_max():
    """The § 4 DeckRV *Höchstzillmersatz* for this contract's ``issue_year``.

    40 ‰ of the *Beitragssumme* to 2014 and **25 ‰ from 1 January 2015**, the LVRG cut.  A cap
    on the **charge**, and not to be confused with § 169 Abs. 3 VVG's five-year spreading,
    which is a floor on the **value**: :func:`check_zillmer_cap` and :func:`check_surr_floor`
    assert the two separately for that reason.
    """
    tbl = data.deckrv_table()                                        # noqa: F821
    y = min(max(issue_year(), int(tbl.index.min())), int(tbl.index.max()))
    return float(tbl.loc[y, "hoechstzillmersatz"])


def instalments():
    """The number of premium instalments a year for this policy's :func:`prem_freq`.

    1, 2, 4 or 12.  Reported rather than used: the projection runs on an annual grid and
    collects the year's *Beitrag* in advance, so the instalment count enters only the
    *Ratenzahlungszuschlag* it justifies.
    """
    return int(data.freq_loading_table().loc[                        # noqa: F821
        prem_freq(), "instalments"])


def prem_freq_load():
    """phi: the *Ratenzahlungszuschlag* multiplier on the annual *Bruttobeitrag*.

    The table value where :func:`unterjaehrig_form` is ``unecht`` - 1.000 annual, 1.020
    half-yearly, 1.030 quarterly, 1.050 monthly **[std]** - and **exactly 1.000 where it is
    ``echt``**, because a genuine sub-annual *Versicherungsperiode* is not an instalment of an
    annual one and carries no loading.  Model points 4 and 5 are the same monthly contract
    under the two readings.
    """
    if unterjaehrig_form() == "echt":
        return 1.0
    return float(data.freq_loading_table().loc[                      # noqa: F821
        prem_freq(), "prem_freq_load"])


def alpha_rate():
    """alpha: the *Zillmersatz*, a fraction of the *Beitragssumme*.

    25 ‰, sitting **at** the § 4 DeckRV ceiling for a contract written from 2015 - the ceiling
    is cited, the level is **[std]**, and no German carrier's actual acquisition cost is
    public.  It is charged in the premium whether or not the contract is zillmered; only
    :func:`alpha_cost` carries ``zillmer_on``.
    """
    return float(data.cost_table().loc[cost_id(), "alpha_rate"])     # noqa: F821


def beta_rate():
    """beta: the collection loading, a fraction of the *Bruttobeitrag* over ``prem_term``.

    3,0 % **[std]**.  The *form* - a percentage of the gross premium over the premium-paying
    period - is what the corpus establishes; the level is not.
    """
    return float(data.cost_table().loc[cost_id(), "beta_rate"])      # noqa: F821


def gamma_rate():
    """gamma: the administration loading, a fraction of the *Versicherungssumme* p.a.

    1,5 ‰ over the whole *Versicherungsdauer* **[std]**.  Neither the form nor the level is
    established anywhere in the corpus, which is why the reserve carries no separate
    *Verwaltungskostenrückstellung* for the years after the *Beitragszahlungsdauer*: the
    pricing equation funds the running cost and the classical reserve convention assumes the
    ongoing loadings meet it.
    """
    return float(data.cost_table().loc[cost_id(), "gamma_rate"])     # noqa: F821


# --- pricing on the first-order basis --------------------------------------

def sum_death():
    """SD: the guaranteed *Todesfallleistung*, ``sum_assured() * death_ratio()``.

    The **tariff** death sum, which is what the pricing and the reserve are struck on.  What a
    death claim actually pays is :func:`benefit_death_pp`, which adds the surplus balances and
    substitutes the *Rückkaufswert* on the § 161 VVG suicide share; and a paid-up contract's
    guaranteed death sum is ``bfz_si_pp() * death_ratio()`` instead.
    """
    return sum_assured() * death_ratio()


def pv_death_1st():
    """The first-order present value at issue of the death benefit, per policy.

    ``SD * sum over k of v1^(k+1) * kpx * f * q1(x0 + k)`` over the whole *Versicherungsdauer*,
    with the *Risikozuschlag* ``f`` on the **claim rate in this leg only**.  Claims fall at the
    end of the policy year of death, which is why the discount exponent is ``k + 1``.
    """
    n = policy_term()
    x0 = issue_age()
    return sum_death() * sum(
        disc_factor_1st(k + 1) * tpx_1st(k) * rating_factor()
        * mort_rate_at_age(x0 + k) for k in range(n))


def pv_maturity_1st():
    """The first-order present value at issue of the *Erlebensfallleistung*, per policy.

    ``SE * v1^n * npx``.  No *Risikozuschlag*: an extra-mortality loading may not make the
    survival benefit cheaper, so it stays out of both the discount and the survivorship.
    """
    return sum_assured() * disc_factor_1st(policy_term()) * tpx_1st(policy_term())


def pv_benefit_1st():
    """The first-order present value at issue of both guaranteed benefits, per policy.

    On the *gemischte Versicherung* proper, where ``death_ratio = 1``, this is very nearly the
    endowment factor times the sum insured, and the price is only weakly sensitive to the
    mortality basis - the survival leg dominating a twenty-five-year contract's reserve.
    """
    return pv_death_1st() + pv_maturity_1st()


def ann_due_prem_1st():
    """The first-order annuity-due factor over the *Beitragszahlungsdauer*, per policy.

    ``sum over k = 0 .. m-1 of v1^k * kpx``.  Exactly 1.0 on an *Einmalbeitrag*, which is why
    the single-premium branch needs no special case anywhere.
    """
    return sum(disc_factor_1st(k) * tpx_1st(k) for k in range(prem_term()))


def ann_due_term_1st():
    """The first-order annuity-due factor over the *Versicherungsdauer*, per policy.

    ``sum over k = 0 .. n-1 of v1^k * kpx``.  It is the base of the ``gamma`` administration
    loading, which runs for the whole term rather than for the premium-paying period - the
    asymmetry that makes an *abgekürzte Beitragszahlungsdauer* dearer per premium.
    """
    return sum(disc_factor_1st(k) * tpx_1st(k) for k in range(policy_term()))


def prem_gross_pp():
    """B: the annual *Bruttobeitrag* per policy before the *Ratenzahlungszuschlag*.

    Struck by the first-order equivalence principle, which is linear in ``B`` because the
    *Beitragssumme* is ``B * m``::

        B (1 - beta) a_m - alpha B m = pv_benefit_1st + gamma SE a_n

    so ``B = (pv_benefit_1st + gamma SE a_n) / ((1 - beta) a_m - alpha m)``.
    :func:`check_equivalence` asserts that the identity closes.

    The *Bruttobeitrag* is **not** a model point column: no German endowment premium rate
    table is public for any carrier, so a shipped rate would be an invention.  It is derived,
    reported, and it rises with :func:`rating_factor` while being identical for two points
    differing only in :func:`sex`.
    """
    return ((pv_benefit_1st() + gamma_rate() * sum_assured() * ann_due_term_1st())
            / ((1.0 - beta_rate()) * ann_due_prem_1st()
               - alpha_rate() * prem_term()))


def beitragssumme():
    """BS: the *Beitragssumme*, ``prem_gross_pp() * prem_term()``.

    The total of all premiums payable over the agreed term, **before** the
    *Ratenzahlungszuschlag*, and the reference base for the § 4 DeckRV acquisition-cost cap,
    for the initial commission and for the *Mindesttodesfallschutz* test.
    """
    return prem_gross_pp() * prem_term()


def alpha_cost():
    """A: the zillmered acquisition cost written into the reserve, in euros.

    ``zillmer_on() * alpha_rate() * beitragssumme()``.  **Zero on a non-gezillmert tariff**,
    where the three reserve constructions then coincide - but the cost is charged in the
    premium either way, because ``zillmer_on`` decides where it sits in the *reserve* and not
    whether it is charged.  It is capped by :func:`zillmer_max` times the *Beitragssumme*;
    :func:`check_zillmer_cap` asserts it.
    """
    return zillmer_on() * alpha_rate() * beitragssumme()


def prem_net_level_pp():
    """P^n: the net level premium, ``pv_benefit_1st() / ann_due_prem_1st()``.

    The pure benefit premium with no loading of any kind.  It is a **pricing quantity that
    never becomes a cash flow**: what is collected is :func:`prem_paid_pp`.  It is the premium
    the net reserve :func:`res_net_pp` is struck on.
    """
    return pv_benefit_1st() / ann_due_prem_1st()


def prem_zill_pp():
    """P^Z: the Zillmer premium, ``prem_net_level_pp() + alpha_cost() / ann_due_prem_1st()``.

    The net premium plus the level annual charge that amortises the zillmered acquisition cost
    over the *Beitragszahlungsdauer*.  It is the premium the Zillmer reserve rolls forward on,
    which is why :func:`check_res_roll_fwd` reads it and not :func:`prem_charged_pp`: one is a
    first-order reserving quantity and the other is a cash flow.
    """
    return prem_net_level_pp() + alpha_cost() / ann_due_prem_1st()


# --- the Deckungskapital ---------------------------------------------------

def pv_benefit_fut(t):
    """The first-order present value of the remaining guaranteed benefits at the start of t.

    Prospective, over the remaining term ``n - k`` with ``k = t - 1``, on the attained age
    ``age(t)``, with the *Risikozuschlag* on the death leg only.  At ``t = n + 1`` the
    remaining term is zero and the value is ``SE``, the maturity payment then due; beyond that
    it is zero.
    """
    rem = policy_term() - duration(t)
    if rem < 0:
        return 0.0
    if rem == 0:
        return sum_assured()
    x = age(t)
    death = 0.0
    p = 1.0
    for j in range(rem):
        q = mort_rate_at_age(x + j)
        death += disc_factor_1st(j + 1) * p * rating_factor() * q
        p *= (1.0 - q)
    return sum_death() * death + sum_assured() * disc_factor_1st(rem) * p


def ann_due_prem_fut(t):
    """The first-order annuity-due factor over the **remaining** premium-paying period.

    ``sum over j = 0 .. max(0, m - k) - 1 of v1^j * jp(x(t))``.  Zero once the
    *Beitragszahlungsdauer* has run out, which is what makes the reserve of an *abgekürzte
    Beitragszahlungsdauer* roll forward on interest and mortality alone.
    """
    rem = max(0, prem_term() - duration(t))
    if rem <= 0:
        return 0.0
    x = age(t)
    s = 0.0
    p = 1.0
    for j in range(rem):
        s += disc_factor_1st(j) * p
        p *= (1.0 - mort_rate_at_age(x + j))
    return s


def res_net_pp(t):
    """V^n: the **net** prospective reserve at the start of policy year t, per policy.

    ``pv_benefit_fut(t) - prem_net_level_pp() * ann_due_prem_fut(t)``, and therefore exactly
    zero at ``t = 1`` on a new-business point - which is the equivalence principle stated as a
    reserve.  It carries no acquisition cost at all, so it is neither what the insurer holds
    nor what the customer gets; it is the construction the other two are built from.

    This and the two below are the **premium-paying constructions**, computed on the full
    :func:`sum_assured` for the whole remaining term, whether or not the contract has been
    made paid-up.  What the contract actually holds is :func:`res_pp`.
    """
    return pv_benefit_fut(t) - prem_net_level_pp() * ann_due_prem_fut(t)


def res_zill_pp(t):
    """V^Z: the *gezillmerte Deckungskapital* at the start of policy year t, per policy.

    ``res_net_pp(t) - alpha_cost() * ann_due_prem_fut(t) / ann_due_prem_1st()``: the net
    reserve less the part of the acquisition cost the future premiums have yet to repay.

    **It is exactly ``-alpha_cost()`` at ``t = 1``** and stays negative for several years.
    That is not a defect: it is the arithmetic of *Zillmerung*, and it is the reason § 169
    Abs. 3 VVG needs a floor at all.  With ``zillmer_on = 0`` it coincides with
    :func:`res_net_pp`.
    """
    return (res_net_pp(t)
            - alpha_cost() * ann_due_prem_fut(t) / ann_due_prem_1st())


def res_min_pp(t):
    """V^min: the § 169 Abs. 3 VVG floor reserve at the start of policy year t, per policy.

    ``res_net_pp(t) - alpha_cost() * max(0, 1 - k/5)`` with ``k = t - 1``: the same net
    reserve with the *angesetzte Abschluss- und Vertriebskosten* spread **evenly over the
    first five contract years** rather than over the whole premium term.  The straight-line
    reading is **[std]**; the alternative - a five-year *Zillmerung* - gives a slightly lower
    floor at durations 1 to 4 and the same value from duration 5.

    On a long *gezillmert* contract this floor **normally binds**, with equality to
    :func:`res_zill_pp` only at durations 0 and ``m``.  A model publishing only the Zillmer
    reserve as the surrender value understates it at essentially every duration.
    """
    return res_net_pp(t) - alpha_cost() * max(0.0, 1.0 - duration(t) / 5.0)


def is_paid_up(t):
    """Whether the contract is *beitragsfrei* at the start of policy year t.

    True only where a *Beitragsfreistellung* was elected (``bfz_year > 0``), the year has
    passed (``t > bfz_year``) **and the election succeeded** - that is, the
    *beitragsfreie Versicherungssumme* it bought reached the agreed
    *Mindestversicherungsleistung* ``bfz_min_si``.  Where it did not, § 165 VVG obliges the
    insurer to pay the § 169 value instead and the election **becomes a surrender**; see
    :func:`lapse_rate`.

    The clause order matters and is not cosmetic: testing ``t > bfz_year()`` **before**
    calling :func:`bfz_si_pp` is what keeps the election year itself off the paid-up basis, so
    that :func:`res_guar_pp` can price the purchase without depending on its own result.
    """
    return (bfz_year() > 0 and t > bfz_year()
            and bfz_si_pp() >= bfz_min_si)                           # noqa: F821


def res_pp(t):
    """V(t): the guaranteed *Deckungskapital* per policy at the **start** of policy year t.

    The *gezillmerte* construction :func:`res_zill_pp` while the contract is premium-paying,
    and ``bfz_si_pp() * pu_single_prem(t)`` once it is *beitragsfrei* - the reserve of the
    reduced paid-up endowment the § 169 value bought.

    Defined at ``t = proj_len() + 1``, where it is :func:`sum_assured` (or the paid-up sum):
    the closing reserve of the last policy year is the maturity payment itself.  That value
    weights no cash flow and exists for :func:`check_res_roll_fwd`.

    This is the model's contribution to the § 341f HGB *Deckungsrückstellung* line and is
    **not** floored at zero as the balance sheet would floor it, so the negative early
    *gezillmert* values stay visible.  ``av_pp(t)`` is explicitly not part of it.
    """
    if is_paid_up(t):
        return bfz_si_pp() * pu_single_prem(t)
    return res_zill_pp(t)


def res_pp_at(t, timing):
    """The guaranteed *Deckungskapital* per policy at a point inside policy year t.

    ``"BEF_PREM"``
        ``res_pp(t)``, the opening reserve before the year's *Beitrag*.

    ``"AFT_PREM"``
        after the first-order Zillmer premium has been credited, and after any
        :func:`bfz_uplift_pp`.  The premium credited here is ``prem_zill_pp()`` - a
        **first-order reserving quantity**, not the *Zahlbeitrag* of
        :func:`prem_charged_pp` - and it is credited only while the contract is
        premium-paying.

    ``"AFT_INT"``
        the **closing** guaranteed reserve of policy year t: the Fackler roll-forward of
        ``AFT_PREM`` at :func:`rechnungszins` with the first-order mortality released
        over the survivors,

            (V + P^Z) (1 + i1) = f q1 SD + (1 - q1) V(t+1)

        This is the ***Deckungskapital* at the allocation date** that the declared surplus
        rate multiplies, and it is computed **retrospectively** here while
        :func:`res_pp` computes the same quantity prospectively - which is what gives
        :func:`check_res_roll_fwd` its teeth.
    """
    if timing == "BEF_PREM":
        return res_pp(t)
    if timing == "AFT_PREM":
        prem = (prem_zill_pp()
                if (t <= prem_term() and not is_paid_up(t)) else 0.0)
        return res_pp(t) + prem + bfz_uplift_pp(t)
    if timing == "AFT_INT":
        q = mort_rate_base(t)
        si = bfz_si_pp() if is_paid_up(t) else sum_assured()
        return ((res_pp_at(t, "AFT_PREM") * (1.0 + rechnungszins())
                 - rating_factor() * q * si * death_ratio()) / (1.0 - q))
    raise ValueError("invalid timing")


def pu_single_prem(t):
    """The first-order single premium at the start of year t for **one unit** of paid-up cover.

    ``pv_benefit_fut(t) / sum_assured()``: the present value of one euro of
    *Erlebensfallleistung* with ``death_ratio`` euros of *Todesfallleistung* over the
    remaining term, on the contract's own *Rechnungsgrundlagen der Prämienkalkulation*
    including the *Risikozuschlag*.

    It is the price at which the § 169 value buys the *beitragsfreie Versicherungssumme*
    (:func:`bfz_si_pp`), and the price at which the *Bonussystem* buys bonus sum insured
    (:func:`bonus_si_pp`).  At ``t = proj_len() + 1`` it is exactly 1.
    """
    return pv_benefit_fut(t) / sum_assured()


def bfz_si_pp():
    """The *beitragsfreie Versicherungssumme* the § 169 value buys, in euros; 0 if never.

    ``res_guar_pp(bfz_year()) / pu_single_prem(bfz_year() + 1)`` - exactly what § 165 VVG
    prescribes, the paid-up benefit being calculated by recognised actuarial rules on the
    *Rechnungsgrundlagen der Prämienkalkulation* **on the basis of the *Rückkaufswert* under
    § 169 Abs. 3 bis 5**.  Two structural consequences follow: the paid-up sum inherits the
    five-year spreading floor, and because that floor generally exceeds the Zillmer reserve
    the sum bought is worth more than the reserve released - the difference being
    :func:`bfz_uplift_pp`.

    Where the result falls below ``bfz_min_si`` (2 500 € **[std]**) the election is **not** a
    *Beitragsfreistellung* at all; see :func:`is_paid_up` and :func:`lapse_rate`.
    """
    if bfz_year() <= 0:
        return 0.0
    return res_guar_pp(bfz_year()) / pu_single_prem(bfz_year() + 1)


def bfz_uplift_pp(t):
    """The § 169 uplift credited to the reserve in the *Beitragsfreistellung* year; else 0.

    ``(res_guar_pp(t) - res_zill_pp(t+1)) * (1 - q1(t)) / (1 + i1)`` at ``t = bfz_year()``
    where the election succeeds, and zero everywhere else.  It is the § 169 Abs. 3 floor
    uplift - the amount by which the value the paid-up sum is bought with exceeds the Zillmer
    reserve released - discounted back to the start of the election year so that it can enter
    :func:`res_pp_at` as a credit.

    It exists so that :func:`check_res_roll_fwd` **still closes in the election year** rather
    than being switched off there, and the identity it then asserts is a real one: that
    ``bfz_si_pp() * pu_single_prem(bfz_year() + 1)`` really is ``res_guar_pp(bfz_year())``,
    i.e. that the paid-up purchase was made at the right price.
    """
    if bfz_year() <= 0 or t != bfz_year() or not is_paid_up(t + 1):
        return 0.0
    return ((res_guar_pp(t) - res_zill_pp(t + 1))
            * (1.0 - mort_rate_base(t)) / (1.0 + rechnungszins()))


def res_guar_pp(t):
    """G(t): the § 169 VVG guaranteed value at the **end** of policy year t, per policy.

    ``max(res_zill_pp(t+1), res_min_pp(t+1), 0)`` while the contract is premium-paying, and
    ``max(res_pp(t+1), 0)`` once it is *beitragsfrei*, where the floor is already inside the
    paid-up sum that was bought.

    It reads the reserves at ``t + 1`` because § 169 Abs. 3 VVG strikes the value **zum
    Schluss der laufenden Versicherungsperiode** and not at the cancellation date, and it
    takes the maximum because the *Mindestrückkaufswert* is a **floor on the value**: the
    customer gets whichever construction is higher.  It is the base of the *Stornoabzug*, the
    base of the paid-up purchase and the base of the *Bewertungsreserven* share.
    """
    if is_paid_up(t):
        return max(res_pp(t + 1), 0.0)
    return max(res_zill_pp(t + 1), res_min_pp(t + 1), 0.0)


# --- the Ueberschussbeteiligung --------------------------------------------

def decl_rate(t):
    """d(t): the declared *laufende Verzinsung* in policy year t, from the scenario table.

    The **total** declared rate - the *Garantieverzinsung* plus the *laufende
    Zinsüberschussbeteiligung* - and not an increment over the guarantee.  2,70 % on the
    ``base`` path, one carrier's 2026 rate for its classic endowment book held level for the
    whole projection **[std]**; 1,20 % on ``low``; 0 on ``nil``.  It is
    insurer-discretionary, revisable annually and **may be zero euros**, which is why it is a
    scenario rather than an assumption.
    """
    tbl = data.surplus_rate_table()                                  # noqa: F821
    y = min(t, int(tbl.loc[scenario_id()].index.max()))
    return float(tbl.loc[(scenario_id(), y), "decl_rate"])


def zins_ueberschuss_rate(t):
    """z(t): the interest-surplus rate in policy year t, ``max(0, d(t) - i1)``.

    **Derived and never an input.**  A declared 2,70 % on a 1,00 % guarantee is a 1,70 pp
    credit, not 2,70 pp on top of 1,00 pp - the single most common way to get this product
    wrong.  The ``max`` matters on the ``nil`` scenario, where the declared rate falls below
    the guarantee: the reserve still rolls forward at the full :func:`rechnungszins`, so the
    surplus is zero and never negative.
    """
    return max(0.0, decl_rate(t) - rechnungszins())


def term_rate(t):
    """s(t): the *Schlussüberschussanteilsatz* in policy year t, from the scenario table.

    0,40 % p.a. of the *Deckungskapital* on the ``base`` path **[std]** - **nothing in the
    corpus fixes a terminal-bonus level, for any insurer, in any year**.  It accrues on the
    same base as the interest surplus and is paid at the *Ablauf* and on death, and not on
    surrender unless ``term_surr_share`` is raised.
    """
    tbl = data.surplus_rate_table()                                  # noqa: F821
    y = min(t, int(tbl.loc[scenario_id()].index.max()))
    return float(tbl.loc[(scenario_id(), y), "term_rate"])


def ans_rate(t):
    """a(t): the *Ansammlungszinssatz* in policy year t, from the scenario table.

    2,70 % on the ``base`` path, set equal to the declared rate **[std]**.  That equality
    matters for one reason: because ``ans_rate > rechnungszins``, the *verzinsliche
    Ansammlung* out-accumulates the *Bonussystem* at maturity while the *Bonussystem* pays
    more on an early death.  Setting it equal to the guarantee would destroy that asymmetry.
    """
    tbl = data.surplus_rate_table()                                  # noqa: F821
    y = min(t, int(tbl.loc[scenario_id()].index.max()))
    return float(tbl.loc[(scenario_id(), y), "ans_rate"])


def surplus_base_pp(t):
    """The *Deckungskapital* the year-t surplus rates are applied to, per policy.

    ``max(res_pp_at(t, "AFT_INT"), 0)``: the **closing** guaranteed reserve of the year,
    after that year's interest and mortality and before this year's surplus - the reserve
    "calculated at the allocation date", which the sources put at the *Bilanzstichtag*.

    The ``max`` is load-bearing.  A *gezillmerte Deckungskapital* is negative in the early
    years, and a positive rate on a negative base credits a **negative** surplus.  So a
    *gezillmert* contract earns no interest surplus in its first years even though the § 153
    VVG entitlement runs from inception: economically right, because there is no fund to earn
    on, and worth saying because it looks like a bug.
    """
    return max(res_pp_at(t, "AFT_INT"), 0.0)


def surplus_credit_pp(t):
    """C(t): the surplus allocated to the contract for policy year t, per policy.

    ``zins_ueberschuss_rate(t) * surplus_base_pp(t)``.  Zero before the frame opens, so that
    the *Beitragsverrechnung* offset in the first projected year has a defined predecessor.

    What it is applied *to* is decided by :func:`surplus_use`, not here: this cells is the
    amount declared, and the three systems differ in what they do with it.
    """
    if t < t_start():
        return 0.0
    return zins_ueberschuss_rate(t) * surplus_base_pp(t)


def term_bonus_pp(t):
    """S(t): the accrued *Schlussüberschussanteil* at the start of policy year t, per policy.

    ``S(t+1) = S(t) + term_rate(t) * surplus_base_pp(t)``, opening at zero.  It is paid at the
    *Ablauf* and on death and **not** on surrender in the base run, ``term_surr_share`` being
    zero - the choice that does not invent an entitlement the sources do not describe.  It
    accrues but never compounds: no source describes interest on an accrued terminal share.
    """
    if t <= t_start():
        return 0.0
    return term_bonus_pp(t - 1) + term_rate(t - 1) * surplus_base_pp(t - 1)


def av_pp(t):
    """U(t): the *Überschussguthaben* per policy at the start of policy year t, in euros.

    The *verzinsliche Ansammlung* balance: it receives declared surplus and **never premium**.
    There is no unit fund and no policyholder account fed by contributions in this product, so
    the house vocabulary's ``prem_to_av_pp`` has no counterpart here and is not published.

    It is explicitly **not** part of the *Deckungsrückstellung*: § 341f HGB forms that
    provision *excluding verzinslich angesammelte Überschussanteile*.
    """
    if t <= t_start():
        return av_pp_init()
    return av_pp_at(t - 1, "AFT_CREDIT")


def av_pp_at(t, timing):
    """The *Überschussguthaben* per policy at a point inside policy year t.

    ``"BEF_INT"``
        the opening balance, ``av_pp(t)``.

    ``"AFT_INT"``
        after the year's *Ansammlungszins*, ``av_pp(t) * (1 + ans_rate(t))``.  The
        balance earns its own interest whatever the current *Überschussverwendung* is.

    ``"AFT_CREDIT"``
        after this year's declared surplus has been added, which happens **only** under
        ``ansammlung``.  This is the closing balance ``av_pp(t + 1)``, and it is what a
        death, maturity or surrender at the end of year t is paid on top of the
        guaranteed benefit.
    """
    if timing == "BEF_INT":
        return av_pp(t)
    if timing == "AFT_INT":
        return av_pp(t) * (1.0 + ans_rate(t))
    if timing == "AFT_CREDIT":
        credit = (surplus_credit_pp(t)
                  if surplus_use() == "ansammlung" else 0.0)
        return av_pp_at(t, "AFT_INT") + credit
    raise ValueError("invalid timing")


def av(t):
    """The *Überschussguthaben* of the whole model point at the start of year t, in euros.

    ``av_pp(t) * pols_if(t)``: the per-policy balance weighted by the in-force count, which is
    the quantity a portfolio roll-up consumes.
    """
    return av_pp(t) * pols_if(t)


def av_at(t, timing):
    """The aggregate *Überschussguthaben* at a point inside policy year t.

    ``av_pp_at(t, timing) * pols_if(t)``, on the same start-of-year weight as every cash flow
    of that ``result_cf()`` row.  The timings are :func:`av_pp_at`'s.
    """
    return av_pp_at(t, timing) * pols_if(t)


def bonus_si_pp(t):
    """Z(t): the bonus sum insured bought out of surplus, per policy, at the start of year t.

    ``Z(t+1) = Z(t) + surplus_credit_pp(t) / pu_single_prem(t+1)`` under the *Bonussystem*,
    and frozen at :func:`bonus_si_init` under the other two systems.

    The bonus sum is **paid-up insurance**: it raises the death benefit immediately by its
    full face amount, which is why the *Bonussystem* pays more on an early death - but it
    accumulates only at :func:`rechnungszins`, which is why the *verzinsliche Ansammlung*
    pays more at the *Ablauf*.
    """
    if t <= t_start():
        return bonus_si_init()
    add = (surplus_credit_pp(t - 1) / pu_single_prem(t)
           if surplus_use() == "bonus" else 0.0)
    return bonus_si_pp(t - 1) + add


def prem_offset_pp(t):
    """The *Beitragsverrechnung* offset applied to the year-t *Zahlbeitrag*, per policy.

    ``min(prem_charged_pp(t), surplus_credit_pp(t - 1))`` under ``beitragsverrechnung`` and
    zero otherwise: **last** year's declared surplus reduces **this** year's premium, floored
    at zero so that a surplus larger than the premium never becomes a payment to the
    policyholder.

    What it reduces is a *Zahlbeitrag*, not a *Bruttobeitrag*: the tariff premium is unchanged
    and the offset is a **discretionary** rebate the insurer may withdraw without invoking
    § 163 VVG at all.  That is why the renewal commission is charged on
    :func:`prem_charged_pp` and not on :func:`prem_paid_pp`.
    """
    if surplus_use() != "beitragsverrechnung":
        return 0.0
    return min(prem_charged_pp(t), surplus_credit_pp(t - 1))


# --- premium ---------------------------------------------------------------

def prem_charged_pp(t):
    """The *Zahlbeitrag* charged per policy in year t, before any *Beitragsverrechnung*.

    ``prem_gross_pp() * prem_freq_load()`` while ``t <= prem_term()`` **and** the contract is
    not *beitragsfrei*; zero otherwise.  Premiums are payable **in advance** at the start of
    the policy year and cease on death, on *Beitragsfreistellung* and at the end of the
    *Beitragszahlungsdauer*.
    """
    if t <= prem_term() and not is_paid_up(t):
        return prem_gross_pp() * prem_freq_load()
    return 0.0


def prem_paid_pp(t):
    """The *Zahlbeitrag* actually paid per policy in year t, after the surplus offset.

    ``prem_charged_pp(t) - prem_offset_pp(t)``.  It differs from :func:`prem_charged_pp` only
    under ``beitragsverrechnung``, and the difference is a policyholder rebate rather than a
    price change - which is why the two are separate cells and why the commission reads the
    first of them.
    """
    return prem_charged_pp(t) - prem_offset_pp(t)


def premiums(t):
    """*Beitrag* income at the start of policy year t, an inflow.

    ``prem_paid_pp(t) * pols_if(t)``, annual in advance.  **Not** further multiplied by
    ``(1 - q)``: decrements fall at the end of the year, so a life that dies or surrenders
    later in the year has already paid this year's premium, and applying the
    premium-cessation rule again here understates income by about one year's mortality.
    """
    return prem_paid_pp(t) * pols_if(t)


# --- decrements ------------------------------------------------------------

def lapse_rate(t):
    """w(t): the annual surrender rate applied at the **end** of policy year t.

    From *lapse_table.csv* by policy year, and **[std]** throughout: 5,0 % in years 1-2,
    3,5 % in 3-8, 2,0 % in 9-11, **6,0 % in year 12** and 2,5 % from 13.  The *shape* is the
    one thing the evidence supports - the income-tax half-income rule needs twelve years and
    age 60 or 62, so surrenders are suppressed approaching duration 12 and spike at it.  The
    **levels are not sourced**: the only German data are market aggregates that are neither
    endowment-specific nor by duration, and the headline one counts conversions to
    *beitragsfrei* as well as surrenders, so calibrating a surrender decrement to it
    double-counts.

    Two overrides.  **Zero in the final policy year**: the end of year ``n`` is the *Ablauf*,
    so the survivors leave as a maturity - and unlike a term cover this is a real payment
    decision, a surrender paying the § 169 value while a maturity pays the sum insured plus
    surplus.  **1.0 in the year a *Beitragsfreistellung* election fails the
    *Mindestversicherungsleistung* test**, where § 165 VVG turns the election into a
    surrender and the whole cohort leaves; that override is a statutory consequence and not a
    behavioural rate, and it is the only place the shipped table is departed from.
    """
    if t >= proj_len():
        return 0.0
    if bfz_year() > 0 and t == bfz_year() and not is_paid_up(t + 1):
        return 1.0
    tbl = data.lapse_table()                                         # noqa: F821
    return float(tbl.loc[min(t, int(tbl.index.max())), "lapse_rate"])


def storno_rate(t):
    """sigma(t): the *Stornoabzug* rate on a surrender at the end of policy year t.

    10 % of the guaranteed value in policy years 1-5, 7,5 % in 6-10, 5 % in 11-15 and 2,5 %
    from 16 **[std]**, against an observed range of 5 % to 20 % of the *Deckungskapital* from
    **one carrier**, under collective action and a BGH remittal.

    § 169 Abs. 5 VVG permits a deduction only where it is *vereinbart*, *beziffert* and
    *angemessen*, and a deduction for *noch nicht getilgte Abschluss- und Vertriebskosten* is
    unwirksam - which is what stops an insurer recovering through the deduction what the
    five-year spreading denies it.  It bites on the **guaranteed value only**; see
    :func:`surr_value_pp`.
    """
    tbl = data.lapse_table()                                         # noqa: F821
    return float(tbl.loc[min(t, int(tbl.index.max())), "storno_rate"])


def pols_if(t):
    """l(t): the number of policies in force at the **start** of policy year t.

    ``pols_if_init()`` at ``t_start()``, then ``l(t+1) = l(t) (1 - q(t)) (1 - w(t))`` on the
    **best-estimate** mortality.  This is the weight on every cash flow of the same
    :func:`result_cf` row.

    A contract made *beitragsfrei* stays here: § 165 VVG keeps it in force with a reduced sum
    insured, and only a *Kündigung* removes it.  ``pols_if(proj_len() + 1)`` is defined and is
    the maturing cohort; it is read by :func:`check_pols_roll_fwd` and
    :func:`check_decrement_closure` and weights no cash flow.
    """
    if t < t_start() or t > proj_len() + 1:
        return 0.0
    if t == t_start():
        return pols_if_init()
    return pols_if_at(t - 1, "AFT_LAPSE")


def pols_if_at(t, timing):
    """The number of policies in force at a point inside policy year t.

    ``"BEF_DECR"``
        l(t), the start of the year before any decrement - the same number as
        :func:`pols_if` and the weight on that year's cash flows.

    ``"AFT_MORT"``
        after the mortality decrement, ``l(t) (1 - q(t))``.  This is the population the
        surrender rate is taken from **and** the population that matures at ``t = n``,
        which is why the two exits cannot both be applied to it in the final year.

    ``"AFT_LAPSE"``
        l(t+1), the end-of-year state.  In the final policy year :func:`lapse_rate` is
        zero, so this equals :func:`pols_maturity`.
    """
    if timing == "BEF_DECR":
        return pols_if(t)
    if timing == "AFT_MORT":
        return pols_if(t) * (1.0 - mort_rate(t))
    if timing == "AFT_LAPSE":
        if t < t_start() or t > proj_len():
            return 0.0
        return pols_if_at(t, "AFT_MORT") * (1.0 - lapse_rate(t))
    raise ValueError("invalid timing")


def pols_death(t):
    """l(t) q(t): expected deaths in policy year t, claimed at the **end** of the year.

    On the **best-estimate** mortality, not the first-order one.  The decedent has already
    paid the year's *Beitrag*, which fell due in advance at the start of it - which is what
    "premiums cease on death" means on an annual-in-advance grid.
    """
    return pols_if(t) * mort_rate(t)


def pols_lapse(t):
    """Expected surrenders at the end of policy year t, from the survivors of mortality.

    ``pols_if_at(t, "AFT_MORT") * lapse_rate(t)``.  They are paid :func:`surr_value_pp`, which
    on this product is a real and often large amount - unlike a term cover, where a lapse pays
    nothing.  Zero in the final policy year, where the survivors leave as a maturity instead.
    """
    return pols_if_at(t, "AFT_MORT") * lapse_rate(t)


def pols_maturity(t):
    """Policies reaching the *Ablauf* at the end of policy year ``n``; zero before it.

    ``pols_if(n) * (1 - mort_rate(n))`` - the survivors of the final year's mortality, all of
    them, because :func:`lapse_rate` is zero there.  They take the *Erlebensfallleistung*.
    """
    if t != proj_len():
        return 0.0
    return pols_if_at(t, "AFT_MORT")


# --- benefits --------------------------------------------------------------

def benefit_full_pp(t):
    """The full death benefit per claim in policy year t, before the § 161 VVG substitution.

    The guaranteed *Todesfallleistung* plus **all three surplus balances at the end of the
    year**: the *Überschussguthaben*, the bonus sum insured and the accrued
    *Schlussüberschussanteil*.  The surplus is added to the death benefit whole - the two
    benefits of a *gemischte Versicherung* differ only in their guaranteed leg.

    A *beitragsfrei* contract's guaranteed leg is ``bfz_si_pp() * death_ratio()`` instead of
    ``sum_death()``.
    """
    si = bfz_si_pp() if is_paid_up(t) else sum_assured()
    return (si * death_ratio() + av_pp(t + 1)
            + bonus_si_pp(t + 1) + term_bonus_pp(t + 1))


def benefit_death_pp(t):
    """What a death claim in policy year t actually pays, per claim, in euros.

    :func:`benefit_full_pp` from policy year 4 onwards.  In policy years 1 to 3 the § 161 VVG
    *Selbsttötung* rule applies to a share ``suicide_share`` of deaths: the insurer is
    *leistungsfrei* **and must nevertheless pay the *Rückkaufswert* including
    *Überschussanteile* under § 169**.  The German rule is a benefit **substitution**, not a
    forfeiture - materially unlike art. L. 132-7 of the French code, where the cover is of no
    effect in the first year and there is no surrender value to fall back on.

    ``suicide_share = 0.02`` **[std]** stands for "about one death in fifty inside the window
    is an excluded suicide"; no source gives a suicide share of deaths at any age.  Setting it
    to zero is a defensible variant.  Paying **nil** on the excluded share is not.
    """
    if t <= 3:
        return ((1.0 - suicide_share) * benefit_full_pp(t)            # noqa: F821
                + suicide_share * surr_value_pp(t))                   # noqa: F821
    return benefit_full_pp(t)


def benefit_maturity_pp(t):
    """What the *Ablauf* pays per surviving policy at the end of year ``n``; zero before it.

    The guaranteed *Erlebensfallleistung* plus the three surplus balances, plus the
    *Beteiligung an den Bewertungsreserven* at ``bwr_rate`` on the guaranteed value.

    ``bwr_rate = 0`` in the base run **[std]**: § 153 Abs. 3 VVG allocates half the
    *Bewertungsreserven* determined on termination, but § 139 VAG permits participation only
    to the extent they exceed the *Sicherungsbedarf* arising from contracts with an interest
    guarantee, and that need has routinely exhausted them.  The parameter exists so the
    reasoning is visible and reversible.

    A *beitragsfrei* contract matures on ``bfz_si_pp()`` in place of :func:`sum_assured`.
    """
    if t != proj_len():
        return 0.0
    si = bfz_si_pp() if is_paid_up(t) else sum_assured()
    return (si + av_pp(t + 1) + bonus_si_pp(t + 1) + term_bonus_pp(t + 1)
            + bwr_rate * res_guar_pp(t))                              # noqa: F821


def surr_value_pp(t):
    """RK(t): the *Rückkaufswert* payable per policy on a surrender at the end of year t.

    ``res_guar_pp(t) * (1 - storno_rate(t)) + av_pp_at(t, "AFT_CREDIT")
    + term_surr_share * term_bonus_pp(t + 1)``.

    The ***Stornoabzug* bites on the guaranteed value alone**: the published deduction is a
    percentage of the *Deckungskapital*, so the accumulated *Überschussguthaben* passes
    through undeducted.  ``term_surr_share = 0`` in the base run, the accrued
    *Schlussüberschussanteil* being payable at the *Ablauf* and on death and not on surrender;
    the parameter is exposed rather than hard-coded because that choice would move surrender
    values most.

    This is also what a § 161 VVG suicide inside three years is paid, and what a failed
    *Beitragsfreistellung* election is paid under § 165 VVG.
    """
    return (res_guar_pp(t) * (1.0 - storno_rate(t))
            + av_pp_at(t, "AFT_CREDIT")
            + term_surr_share * term_bonus_pp(t + 1))                 # noqa: F821


def claims(t, kind=None):
    """Benefit outgo in policy year t, by kind; the total when kind is omitted.

    ``"DEATH"``
        ``pols_death(t) * benefit_death_pp(t)``: the guaranteed *Todesfallleistung*
        plus the surplus balances, with the § 161 VVG substitution of the
        *Rückkaufswert* on the suicide share in policy years 1 to 3.

    ``"MATURITY"``
        ``pols_maturity(t) * benefit_maturity_pp(t)``, nil except at ``t = n``: the
        *Erlebensfallleistung* plus the surplus balances.

    ``"LAPSE"``
        ``pols_lapse(t) * surr_value_pp(t)``: the *Rückkaufswert*.  Unlike a
        *Risikolebensversicherung*, where a lapse pays nothing, this is a real and
        often large outflow, and in the final policy year the distinction between it
        and a maturity decides a payment rather than only a label.
    """
    if kind is None:
        return sum(claims(t, k) for k in ("DEATH", "MATURITY", "LAPSE"))
    if kind == "DEATH":
        return pols_death(t) * benefit_death_pp(t)
    if kind == "MATURITY":
        return pols_maturity(t) * benefit_maturity_pp(t)
    if kind == "LAPSE":
        return pols_lapse(t) * surr_value_pp(t)
    raise ValueError("invalid kind")


# --- expenses and commission -----------------------------------------------

def inflation_factor(t):
    """The expense inflation factor in policy year t: ``(1 + expense_infl)^(t-1)`` **[std]**.

    Measured from **issue**, not from the valuation date, so an in-force model point opens on
    the inflation its duration has already accumulated.  1,8 % p.a. is a placeholder.
    """
    infl = float(data.cost_table().loc[cost_id(), "expense_infl"])   # noqa: F821
    return (1.0 + infl) ** (t - 1)


def claim_expenses(t):
    """The claim handling expense on the year's exits **[std]**.

    120 € per death, maturity or surrender claim, uninflated.  Named separately because it is
    the only expense line that scales with **claims** rather than with policies, and it is
    inside :func:`expenses`.
    """
    ce = float(data.cost_table().loc[cost_id(), "claim_expense"])    # noqa: F821
    return ce * (pols_death(t) + pols_lapse(t) + pols_maturity(t))


def expenses_pp(t):
    """The per-policy expense in policy year t, in euros, excluding claim handling **[std]**.

    The 300 € acquisition expense at issue - **only** at ``t_start()`` and **only** for a
    new-business point, an in-force point having incurred it long ago - plus the 45 €
    maintenance expense inflated to year t.  All levels are placeholders: **no charge level of
    any kind was established for any German carrier**, and the levels shipped are sized so
    that the first-year acquisition outgo modestly exceeds what the *Zillmerung* recovers, so
    that the anchor cell carries the new-business strain a real German endowment carries.
    """
    cost = data.cost_table().loc[cost_id()]                          # noqa: F821
    acq = (float(cost["acq_expense"])
           if (t == t_start() and duration_init() == 0) else 0.0)
    return acq + float(cost["maint_expense"]) * inflation_factor(t)


def expenses(t):
    """Total insurer expense outgo in policy year t, **excluding commission** **[std]**.

    ``expenses_pp(t) * pols_if(t) + claim_expenses(t)``.

    The deliberate difference from the frlib chassis, where commission sits *inside* the
    expense column and is published beside it: here :func:`commissions` is a separate line, so
    the six flow columns of :func:`result_cf` sum to :func:`net_cf` rather than double-counting
    the commission.  Whichever convention a model takes, taking both at once is the error.
    """
    return expenses_pp(t) * pols_if(t) + claim_expenses(t)


def commissions(t):
    """Commission outgo in policy year t **[std]**, excluded from :func:`expenses`.

    2,5 % of the *Beitragssumme* at conclusion - anchored to the 25 ‰ § 4 DeckRV ceiling and
    to one carrier's reported 25 ‰ - plus a 1,5 % *Bestandsprovision* on the *Bruttobeitrag*
    from the second projected year.  Neither the initial nor the renewal term applies at
    ``t_start()`` on an in-force point: it was paid at conclusion, long before the frame
    opens.

    The renewal commission is charged on :func:`prem_charged_pp` and **not** on
    :func:`prem_paid_pp`: under *Beitragsverrechnung* the intermediary is paid on the tariff
    premium, the surplus offset being a policyholder rebate rather than a price reduction.
    """
    cost = data.cost_table().loc[cost_id()]                          # noqa: F821
    init = (float(cost["comm_init_rate"]) * beitragssumme() * pols_if(t)
            if (t == t_start() and duration_init() == 0) else 0.0)
    renew = (float(cost["comm_renew_rate"]) * prem_charged_pp(t) * pols_if(t)
             if t > t_start() else 0.0)
    return init + renew


# --- output ----------------------------------------------------------------

def net_cf(t):
    """The net liability cash flow of policy year t, **income positive**.

    *Beiträge* less death, maturity and surrender claims, less expenses, less commission -
    each subtracted exactly once, :func:`expenses` excluding commission by construction.  The
    notes' own sign and the library-wide one.

    The shape to expect on the anchor cell is a large first-year strain, then positive margins
    that grow as the *Deckungskapital* and the *Überschussguthaben* build, then a single very
    large negative year at the *Ablauf*.
    """
    return (premiums(t) - claims(t, "DEATH") - claims(t, "MATURITY")
            - claims(t, "LAPSE") - expenses(t) - commissions(t))


def liability_cf(t):
    """The same stream as :func:`net_cf`, outgo positive: ``-net_cf(t)`` exactly.

    The orientation a valuation layer consumes: a Solvency II best estimate is
    ``sum v(t) * liability_cf(t)`` over the relevant risk-free term structure, plus a risk
    margin.  Published as a column of :func:`result_cf` so the sign convention is verifiable
    in the frame rather than only in prose.
    """
    return -net_cf(t)


def check_net_cf_resid(t):
    """The cash flow statement residual in policy year t; zero everywhere.

    ``net_cf - (premiums - claims_death - claims_maturity - claims_lapse - expenses
    - commissions)``, rebuilt **from :func:`result_cf`'s own published columns** rather than
    from the cells behind them.  Reading the frame is the point: the identity then holds of
    what the model actually publishes, so a column dropped, renamed or mis-signed on the way
    into the frame fails here.

    The commission is subtracted **once**: :func:`expenses` excludes it.  A model on the frlib
    convention, where the expense column carries the commission, must not subtract both.
    """
    row = result_cf().loc[t]
    rebuilt = (row["premiums"] - row["claims_death"] - row["claims_maturity"]
               - row["claims_lapse"] - row["expenses"] - row["commissions"])
    return float(row["net_cf"] - rebuilt)


def check_net_cf():
    """True when the cash flow statement reconciles in every projected policy year.

    **This library's first ruling**: every model publishes the identity that reconstructs
    ``net_cf(t)`` from its own cash flow statement's published parts, so that the headline
    number of a cash flow model is not the one quantity nothing checks.  No argument, one bool
    over all ``t``; :func:`check_net_cf_resid` gives the signed residual of the year that
    failed.
    """
    tol = roll_fwd_tol * max(sum_assured(), 1.0)                     # noqa: F821
    return all(abs(check_net_cf_resid(t)) <= tol
               for t in range(t_start(), proj_len() + 1))


def check_pols_roll_fwd_resid(t):
    """The in-force roll-forward residual in policy year t; zero everywhere.

    ``pols_if(t) - pols_if(t+1) - pols_death(t) - pols_lapse(t)``, plus in the final policy
    year the difference between :func:`pols_maturity` and the survivors of that year's
    mortality.  The recursion multiplies ``(1 - q)(1 - w)`` while the exits are formed
    separately, so the two agree by algebra when - and only when - every one of them is read
    at the same ``t``.  What it catches is a **misindexed recursion**, and in the last year a
    maturity count that is not exactly the cohort that survived to it.
    """
    r = (pols_if(t) - pols_if(t + 1) - pols_death(t) - pols_lapse(t))
    if t == proj_len():
        r += pols_maturity(t) - pols_if_at(t, "AFT_MORT")
    return r


def check_pols_roll_fwd():
    """True when the in-force roll-forward closes in every projected policy year.

    No argument, one bool over all ``t``; :func:`check_pols_roll_fwd_resid` gives the signed
    residual of the year that failed.
    """
    tol = roll_fwd_tol * max(pols_if_init(), 1.0)                    # noqa: F821
    return all(abs(check_pols_roll_fwd_resid(t)) <= tol
               for t in range(t_start(), proj_len() + 1))


def check_decrement_closure_resid(t):
    """The cumulative decrement-closure residual at the end of policy year t; zero.

    Deaths plus surrenders plus maturities up to ``t``, plus the survivors carried into
    ``t + 1`` before the *Ablauf*, less the original cohort.  It is built by **direct
    summation over the exit cells**, with no reference to the recursion that produced
    :func:`pols_if`, which is what makes it more than the telescope of
    :func:`check_pols_roll_fwd`: it catches a wrong starting cohort, an exit counted in two
    places, and a maturity that double-counts the final year's surrenders.
    """
    exits = sum(pols_death(s) + pols_lapse(s) + pols_maturity(s)
                for s in range(t_start(), t + 1))
    carried = pols_if(t + 1) if t < proj_len() else 0.0
    return exits + carried - pols_if_init()


def check_decrement_closure():
    """True when deaths, surrenders, maturities and survivors account for the whole cohort.

    No argument, one bool over all ``t``; :func:`check_decrement_closure_resid` gives the
    signed residual of the year that failed.  At ``t = proj_len()`` it is the notes' closure
    identity: the three exit streams sum to :func:`pols_if_init` exactly.
    """
    tol = roll_fwd_tol * max(pols_if_init(), 1.0)                    # noqa: F821
    return all(abs(check_decrement_closure_resid(t)) <= tol
               for t in range(t_start(), proj_len() + 1))


def check_res_roll_fwd_resid(t):
    """The *Deckungskapital* roll-forward residual in policy year t; zero everywhere.

    ``res_pp_at(t, "AFT_INT") - res_pp(t + 1)``: the Fackler recursion

        (V(t) + P^Z + uplift) (1 + i1) = f q1(t) SD + (1 - q1(t)) V(t+1)

    computed **retrospectively** on the left and **prospectively** on the right.  This is the
    strongest single check in the model: it proves that the premium, the first-order
    mortality, the interest rate and the prospective reserve formula are mutually consistent,
    and it fails on a *Risikozuschlag* applied to the survivorship, a Zillmer premium
    amortised over the wrong annuity, a reserve read at the wrong duration, and an
    *abgekürzte Beitragszahlungsdauer* that keeps crediting a premium after it has stopped.

    In the *Beitragsfreistellung* year the identity it asserts is a different one -
    :func:`bfz_uplift_pp` is defined to close it - and there it says that the paid-up sum was
    bought at exactly the § 169 value.
    """
    return res_pp_at(t, "AFT_INT") - res_pp(t + 1)


def check_res_roll_fwd():
    """True when the guaranteed reserve rolls forward in every projected policy year.

    No argument, one bool over all ``t``; :func:`check_res_roll_fwd_resid` gives the signed
    residual of the year that failed.
    """
    tol = roll_fwd_tol * max(sum_assured(), 1.0)                     # noqa: F821
    return all(abs(check_res_roll_fwd_resid(t)) <= tol
               for t in range(t_start(), proj_len() + 1))


def check_surplus_roll_fwd_resid(t):
    """The active *Überschussverwendung* ledger's residual in policy year t; zero everywhere.

    Under ``ansammlung``, ``av_pp(t+1) - [av_pp(t) (1 + a(t)) + C(t)]``; under ``bonus``,
    ``bonus_si_pp(t+1) - [bonus_si_pp(t) + C(t) / pu_single_prem(t+1)]``; under
    ``beitragsverrechnung``, ``prem_offset_pp(t) - min(prem_charged_pp(t), C(t-1))``.

    One check for three ledgers, because exactly one of them is live on any model point - and
    a model that credits the same surplus to two of them fails here rather than quietly
    paying it twice.
    """
    if surplus_use() == "ansammlung":
        return (av_pp(t + 1)
                - (av_pp(t) * (1.0 + ans_rate(t)) + surplus_credit_pp(t)))
    if surplus_use() == "bonus":
        return (bonus_si_pp(t + 1)
                - (bonus_si_pp(t)
                   + surplus_credit_pp(t) / pu_single_prem(t + 1)))
    return prem_offset_pp(t) - min(prem_charged_pp(t), surplus_credit_pp(t - 1))


def check_surplus_roll_fwd():
    """True when the live surplus ledger closes in every projected policy year.

    No argument, one bool over all ``t``; :func:`check_surplus_roll_fwd_resid` gives the
    signed residual of the year that failed.
    """
    tol = roll_fwd_tol * max(sum_assured(), 1.0)                     # noqa: F821
    return all(abs(check_surplus_roll_fwd_resid(t)) <= tol
               for t in range(t_start(), proj_len() + 1))


def check_surr_floor_resid(t):
    """The § 169 Abs. 3 VVG surrender-floor residual in policy year t; zero everywhere.

    The sum of four one-sided violations, each of which can only be negative:
    ``res_guar_pp(t)`` below :func:`res_zill_pp` at ``t + 1``, below :func:`res_min_pp` at
    ``t + 1``, below zero, and :func:`surr_value_pp` below zero.  The two reserve comparisons
    are made only while the contract is premium-paying: once it is *beitragsfrei* the
    premium-paying constructions describe a contract that no longer exists, and the floor is
    already inside the paid-up sum that was bought.

    Near-trivial by construction, since :func:`res_guar_pp` is that maximum - and published
    for the same reason frlib publishes its gate checks: the rule is written twice, so the two
    disagree if either is edited.  What it guards against is the specific and tempting error
    of publishing the Zillmer reserve alone as the surrender value, which understates it at
    essentially every duration on a *gezillmert* contract.
    """
    r = min(0.0, res_guar_pp(t)) + min(0.0, surr_value_pp(t))
    if not is_paid_up(t):
        r += min(0.0, res_guar_pp(t) - res_zill_pp(t + 1))
        r += min(0.0, res_guar_pp(t) - res_min_pp(t + 1))
    return r


def check_surr_floor():
    """True when the § 169 Abs. 3 floor holds in every projected policy year.

    No argument, one bool over all ``t``; :func:`check_surr_floor_resid` gives the signed
    residual of the year that failed.
    """
    tol = roll_fwd_tol * max(sum_assured(), 1.0)                     # noqa: F821
    return all(abs(check_surr_floor_resid(t)) <= tol
               for t in range(t_start(), proj_len() + 1))


def check_equivalence_resid(t):
    """The first-order pricing equivalence residual; the same value at every t.

    ``B (1 - beta) a_m - alpha BS - pv_benefit_1st - gamma SE a_n``.  It does not depend on
    ``t`` - the equivalence is struck once, at issue - and it carries the argument only so
    that every ``check_*`` in this library has the same shape.

    Note that it charges ``alpha_rate() * beitragssumme()`` and **not** :func:`alpha_cost`:
    the acquisition cost is in the premium whether or not the contract is zillmered, which is
    why a *gezillmerte* and a non-*gezillmerte* edition of one tariff cost the same.
    """
    return (prem_gross_pp() * (1.0 - beta_rate()) * ann_due_prem_1st()
            - alpha_rate() * beitragssumme()
            - pv_benefit_1st()
            - gamma_rate() * sum_assured() * ann_due_term_1st())


def check_equivalence():
    """True when the first-order pricing equivalence closes.

    No argument, one bool; :func:`check_equivalence_resid` gives the signed residual.  It is
    what makes :func:`prem_gross_pp` a derived quantity rather than an asserted one, and it is
    the only check that would fail if the *Beitragssumme* were formed on the loaded
    *Zahlbeitrag* instead of on the *Bruttobeitrag*.
    """
    tol = roll_fwd_tol * max(sum_assured(), 1.0)                     # noqa: F821
    return all(abs(check_equivalence_resid(t)) <= tol
               for t in range(t_start(), proj_len() + 1))


def check_rechnungszins_cap_resid(t):
    """The § 2 DeckRV ceiling residual; zero unless the guarantee exceeds the cohort's cap.

    ``min(0, hrz_max() - rechnungszins())``, the same value at every ``t``.  A **parameter
    invariant rather than a roll-forward identity**, and it lives in the model rather than in
    a build script because a German model point's cohort *is* an assumption: a 4,00 %
    guarantee on a 2026 issue year is not a stress, it is a data error.
    """
    return min(0.0, hrz_max() - rechnungszins())


def check_rechnungszins_cap():
    """True when the contract's *Rechnungszins* is within its cohort's *Höchstrechnungszins*.

    No argument, one bool; :func:`check_rechnungszins_cap_resid` gives the signed shortfall.
    """
    return all(abs(check_rechnungszins_cap_resid(t)) <= roll_fwd_tol  # noqa: F821
               for t in range(t_start(), proj_len() + 1))


def check_zillmer_cap_resid(t):
    """The § 4 DeckRV ceiling residual; zero unless the *Zillmersatz* exceeds the cohort's cap.

    ``min(0, zillmer_max() - alpha_rate()) + min(0, zillmer_max() * beitragssumme()
    - alpha_cost())``, the same value at every ``t``: the rate against the ceiling and the
    zillmered amount against the ceiling applied to the *Beitragssumme*.

    It is asserted **separately** from :func:`check_surr_floor` on purpose.  § 4 DeckRV caps
    **how much** may be zillmered at all - a cap on the *charge* - while § 169 Abs. 3 VVG
    fixes **how** the acquisition cost is spread for the surrender floor - a floor on the
    *value*.  Conflating the two is a documented failure mode, and one search summary in the
    research corpus does exactly that.
    """
    return (min(0.0, zillmer_max() - alpha_rate())
            + min(0.0, zillmer_max() * beitragssumme() - alpha_cost()))


def check_zillmer_cap():
    """True when the *Zillmersatz* is within its cohort's *Höchstzillmersatz*.

    No argument, one bool; :func:`check_zillmer_cap_resid` gives the signed shortfall.
    """
    tol = roll_fwd_tol * max(sum_assured(), 1.0)                     # noqa: F821
    return all(abs(check_zillmer_cap_resid(t)) <= tol
               for t in range(t_start(), proj_len() + 1))


def result_cf():
    """Result table of cash flows, indexed by policy year t.

    ``pols_if`` is the **start-of-year** count, which is the weight applied to every cash flow
    on the same row, and its first value is :func:`pols_if_init` exactly.  ``expenses``
    **excludes** commission, so the six flow columns

        premiums, claims_death, claims_maturity, claims_lapse, expenses, commissions

    sum to ``net_cf`` with no double count - which is what :func:`check_net_cf` asserts.
    ``liability_cf`` is ``net_cf`` outgo-positive and is published as the last column so that
    the sign convention is verifiable in the frame.

    The frame runs ``t = t_start() ... proj_len()`` contiguously and stops: the *Ablauf* falls
    at the end of policy year ``proj_len()`` and **there is no ``t = proj_len() + 1`` row**.
    """
    ts = list(range(t_start(), proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "claims_death": [claims(t, "DEATH") for t in ts],
            "claims_maturity": [claims(t, "MATURITY") for t in ts],
            "claims_lapse": [claims(t, "LAPSE") for t in ts],
            "expenses": [expenses(t) for t in ts],
            "commissions": [commissions(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
            "liability_cf": [liability_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_surplus():
    """Result table of the surplus machinery and the reserves, indexed by policy year t.

    ``decl_rate``, ``zins_ueberschuss_rate``, ``surplus_base_pp``, ``surplus_credit_pp``,
    ``res_pp``, ``av_pp``, ``term_bonus_pp`` and ``surr_value_pp`` are **state**, not cash
    flow, which is why they are published here rather than in :func:`result_cf`: a cash flow
    statement whose columns do not all sum to its bottom line is a statement a reader has to
    know which columns to skip.

    Read the first rows of this frame beside the first rows of :func:`result_cf` and the
    product is visible in two numbers: ``res_pp`` is negative while the *Zillmerung* is
    unrecovered, and ``surplus_credit_pp`` is therefore exactly zero over the same years.
    """
    ts = list(range(t_start(), proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "decl_rate": [decl_rate(t) for t in ts],
            "zins_ueberschuss_rate": [zins_ueberschuss_rate(t) for t in ts],
            "surplus_base_pp": [surplus_base_pp(t) for t in ts],
            "surplus_credit_pp": [surplus_credit_pp(t) for t in ts],
            "res_pp": [res_pp(t) for t in ts],
            "av_pp": [av_pp(t) for t in ts],
            "term_bonus_pp": [term_bonus_pp(t) for t in ts],
            "surr_value_pp": [surr_value_pp(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

mort_be_factor = 0.75

suicide_share = 0.02

bfz_min_si = 2500.0

term_surr_share = 0.0

bwr_rate = 0.0

beta_shock = 0.0

lapse_gap_a = 0.0

ref_rate = 0.03

roll_fwd_tol = 1e-10

pd = ("Module", "pandas")
