# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.Basis_DE_A` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the worked example's anchor cell
    >>> Projection.point_id = 5            # or switch the default

``t`` counts **projection years from the valuation date**, 1-based: ``t = 1`` is the
first projected year and ``t = proj_len() = omega_age() - age(1) + 1`` the last. Policy
duration at the start of year ``t`` is ``duration(t) = duration_init + t - 1`` **completed**
policy years, so a new-business point opens at ``duration(1) = 0``; an in-force point
opens at whatever duration it has already run and **the frame still starts at ``t = 1``**.
The annuity is lifelong, so the projection runs to the end of the mortality table; at
``t = proj_len()`` the last survivor dies and ``pols_if(proj_len() + 1)`` is zero.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent directory,
``products/basisrente/``, read at run time rather than stored inside the model. The model
folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded
values. This follows ``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which
keeps its inputs *inside* the model.

Each table has a filename Reference and a reader Cells, both on
:mod:`~.Basis_DE_A.Data`, reached here through the ``data`` Reference:

=========================  ===================================  ==========================
Reference                  Cells                                File
=========================  ===================================  ==========================
model_point_file           data.model_point_table()             model_point_table.csv
mort_table_file            data.mort_table()                    mort_table.csv
surplus_file               data.surplus_table()                 surplus_table.csv
rentenfaktor_file          data.rentenfaktor_table()            rentenfaktor_table.csv
charge_file                data.charge_table()                  charge_table.csv
behaviour_file             data.behaviour_table()               behaviour_table.csv
option_file                data.option_table()                  option_table.csv
=========================  ===================================  ==========================

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` and ``savings.CashValue_SE``
wherever those models have an analogue — ``pols_*`` for policy counts, plural nouns for
cash flows, ``*_rate`` for rates, ``*_pp`` for per-policy amounts, ``claims(t, kind)``
with an uppercase ``kind`` string, ``av_pp_at(t, timing)`` and ``pols_if_at(t, timing)``
for the within-year reads. The technical notes use compact actuarial symbols instead.
The mapping is:

=========================  ==============================  ==============================
Notes symbol               Cells                           Meaning
=========================  ==============================  ==============================
(none)                     model_point()                   The selected model point row
n = omega - x(1) + 1       proj_len()                      Last projected year
x(t)                       age(t)                          Attained age in year t
d(t)                       duration(t)                     Completed policy years in year t
y(t)                       cal_year(t)                     Calendar year in year t
omega                      omega_age()                     Terminal age of the table
T                          ret_t()                          Projection year of Rentenbeginn
(none)                     gtd_end_t()                     Last year of the Rentengarantiezeit
S                          beitragssumme_pp()              Beitragssumme at inception
P0 (1 + delta)^d(t)        prem_base_pp(t)                 Contractual Beitrag before phi
phi                        prem_freq_load()                Ratenzahlungszuschlag
P(t)                       prem_pp(t)                      Beitrag charged per paying policy
Z(t)                       zuz_pp(t)                       Zuzahlung per paying policy
(take-up)                  zuz_take_up(t)                  Zuzahlung utilisation rate
(none)                     prem_total_pp(t)                Total contribution incl. BUZ
zill_rate x S              alpha_total_pp()                Zillmerised acquisition charge
alpha(t)                   alpha_amort_pp(t)               Its annual instalment
alpha_z(t)                 alpha_zuz_pp(t)                 Acquisition charge on a Zuzahlung
u(t)                       unit_cost_pp(t)                 Stueckkosten, inflating
N(t)                       prem_to_av_pp(t)                Premium credited after charges
premiums(t)                premiums(t)                     Laufende Beitraege, fund level
zuzahlungen(t)             zuzahlungen(t)                  Zuzahlungen, fund level
A^p(t, .)                  av_pp_at(t, timing)             Deckungskapital per paying policy
A^p(t)                     av_pp(t)                        Its start-of-year value
A^f(t, .)                  av_pu_at(t, timing)             Premium-free block, fund level
A(t, .)                    av_at(t, timing)                Whole Deckungskapital, fund level
A(t)                       av(t)                           Its start-of-year value
(declared)                 decl_rate(t)                    Declared laufende Verzinsung
i(t)                       cred_rate(t)                    max(gtd_rate, decl_rate(t))
q^t(x, y)                  mort_rate_at_age(x, y)          First-order table rate
(table)                    mort_rate_base(t)               Table rate in year t
q(t)                       mort_rate(t)                    Best-estimate death rate
f(t)                       bf_rate(t)                      Beitragsfreistellung rate
l(t)                       pols_if(t)                      In force at the start of year t
l^p(t)                     pols_paying(t)                  Premium-paying subset
l^f(t)                     pols_paidup(t)                  Premium-free subset
l(t)(1-q)                  pols_if_at(t, timing)           BEF_DECR / AFT_DEATH / AFT_FREEZE
(none)                     pols_death(t)                   Expected deaths in year t
(none)                     pols_death_paying(t)            of which premium-paying
(none)                     pols_death_paidup(t)            of which premium-free
(none)                     pols_freeze(t)                  Beitragsfreistellung transfers
g(t)                       pols_gtd(t)                     Rentengarantiezeit continuations
(current)                  rentenfaktor_curr()             Aktueller Rentenfaktor at ret_age
(options)                  rf_option_factor()              Option reduction on the factor
R                          rentenfaktor_applied()          The factor actually applied
F                          fund_at_conv()                  Fund converted at Rentenbeginn
b(t)                       ann_bonus_rate(t)               Ueberschussrente uplift
a(t)                       ann_pp(t)                       Annual annuity per annuitant
(none)                     db_pp(t)                        Reserve released per paying death
(none)                     db_pu_pp(t)                     Reserve released per paid-up death
claims_death, _annuity,    claims(t, kind)                 Benefit outgo by kind
claims_survivor
E(t)                       expenses(t)                     Insurer expense outgo
C(t)                       commissions(t)                  Commission outgo
net_cf(t)                  net_cf(t)                       Net cash flow, income positive
liability_cf(t)            liability_cf(t)                 The same stream, outgo positive
=========================  ==============================  ==============================

Four names needed care.

``av_pp_at`` is **per premium-paying policy** and ``av_pu_at`` is the premium-free block
**at fund level**. They are not two spellings of one quantity and they must not be
averaged into a single per-policy figure: a policy that froze at duration 5 and one that
froze at duration 15 hold different reserves, only the aggregate of the second kind is
meaningful, and collapsing the two is the third listed modeling pitfall.
:func:`av_at` is the fund-level total, ``av_pp_at(t, .) x pols_paying(t) + av_pu_at(t, .)``,
and it is the only one of the three that rolls forward on mortality alone.

``bf_rate`` is the *Beitragsfreistellung* rate and is emphatically **not** ``lapse_rate``.
There is no lapse decrement on this product and no cells of that name anywhere in the
model. A freeze is a transfer between two ledgers, not an exit: it appears in
:func:`pols_paying` and :func:`pols_paidup` and **not** in :func:`pols_if`, which
decrements on mortality alone.

``prem_total_pp`` reconstructs the contribution the policyholder actually pays,
``(P(t) + Z(t)) / (1 - buz_prem_share)``, and is a **reporting cells that enters no cash
flow**. The BUZ premium buys a cover this model does not project — the disability
mechanics belong to ``BU_DE_S`` — so it appears in no :func:`result_cf` column and in
:func:`net_cf` at no ``t``. Modelling it as premium income with no benefit is the
seventeenth pitfall.

``claims(t, "DEATH")`` is not a lump sum to a beneficiary. § 10 EStG requires everything
paid to a survivor to be paid **as an annuity**, so what is booked at the moment of death
is the *Deckungskapital* leaving this contract as the **single premium of a survivor's
annuity** — itself a new liability, an immediate annuity, that this model does not
project. Reading it as a payable capital sum misreads the product, which is the tenth
pitfall.

.. rubric:: The product is defined by prohibitions

The entitlement under a *Basisrentenvertrag* is *nicht vererblich*, *nicht übertragbar*,
*nicht beleihbar*, *nicht veräußerbar* and *nicht kapitalisierbar*. Arithmetically that
means there is **no surrender value at any duration**, no *Kapitalwahlrecht*, no
*Teilkapitalauszahlung*, no commutation of a *Kleinbetragsrente*, and no lump sum of any
kind at any date. § 169 VVG — the *Rückkaufswert*, the *Mindestrückkaufswert*, the
*Stornoabzug* — is inoperative on this contract.

So this model has **no ``lapse_rate``, no ``surr_rate``, no ``cv_pp``, no ``loan_pp``,
no ``withdrawals`` and no ``claims_lapse`` column**. Those are structural absences, not
switched-off options, and :func:`check_no_capital` asserts the consequence at every
``t``: the only payments the model can make are an annuity instalment, a
*Rentengarantiezeit* continuation and a survivor's single premium.

The mirror error is subtler than importing a surrender column, and it is worth naming:
computing a *Rückkaufswert* internally "for reference" and then flooring the
*Deckungskapital* at it. :func:`prem_to_av_pp` is negative in the first years of a
heavily zillmerised contract and the account is **not** floored, because there is no
*Rückkaufswert* for a floor to protect. That is why a German *Deckungskapital* starts
near zero.

.. rubric:: Two ledgers, one model point

A *Beitragsfreistellung* under § 165 VVG survives intact on this contract and is its only
behavioural exit. It stops the premium and moves the policy to the premium-free cohort,
where its *Deckungskapital* is still credited, still pays the *Stückkosten* and the
reserve charge, stops paying the premium charge and the *Zillmerung* instalment, and
still converts at *Rentenbeginn*. It does not end the contract, release any value, change
the *Rentenbeginn* or release any of the § 10 constraints.

The model therefore carries :func:`pols_paying` and :func:`pols_paidup` and their two
account blocks, and

    ``pols_if(t + 1) = pols_if(t) x (1 - mort_rate(t))``

with ``bf_rate`` absent from the identity. :func:`check_pols_roll_fwd` asserts both that
the two ledgers sum to :func:`pols_if` and that :func:`pols_if` decrements on mortality
alone. A model point opens either **entirely** premium-paying or **entirely**
premium-free (``paidup_at_init``); a part-paid-up book is two model points, because
averaging the two cohorts' reserves is the third pitfall.

No *Wiederinkraftsetzung* is modelled: the premium-free block is absorbing, which is
conservative on premium income and is a standardization rather than a contract fact.

.. rubric:: The declared rate is the total credited rate

``cred_rate(t) = max(gtd_rate, decl_rate(t))``, a maximum and not a sum. A German
*laufende Verzinsung* is quoted as the **total** rate credited to the *Deckungskapital*,
already including the contract's *Rechnungszins*; adding the declared rate on top of the
guarantee is the sixth pitfall. The guarantee is a cohort fact fixed at conclusion and
carried on the model point as ``gtd_rate``, so a book spanning the 2,75 % vintage of 2006
and the 1,00 % vintage of 2025 has both branches of the ``max`` live at once — model
point 8 credits its guarantee at every ``t`` while the anchor credits the declared path
at every ``t``.

The reserve charge γ is netted inside the same step, ``(1 + cred_rate(t) - gamma_av)``,
and the *Stückkosten* are taken before it. γ, β, the *Stückkosten* and the *Zillmerung*
instalment are **deductions from the policyholder's account** — insurer income — and the
insurer's own outgo is the acquisition expense, the commission, the maintenance expense
and the annuity administration. Booking a charge as both is the fourth pitfall, and it is
why :func:`expenses` is invariant to ``beta_prem``, ``gamma_av`` and ``zill_rate``: those
three move :func:`net_cf` only through the smaller annuity the smaller fund buys at
*Rentenbeginn*.

.. rubric:: The conversion at Rentenbeginn

At the start of projection year ``T = ret_t()`` the whole fund carried out of year
``T - 1``, grossed up by the *Schlussüberschussanteil*, converts::

    fund_at_conv()  = av_at(T, "BEF_PREM") x (1 + terminal_bonus_rate)

    ann_pp(T)       = fund_at_conv() / pols_if(T) / rf_unit
                      x rentenfaktor_applied() x ann_freq

There is no lump sum, no election and no notice period — this is the one date in the
contract's life at which anything happens, and nothing happens at it that the
policyholder chooses. ``av(t)`` is zero for every ``t > T``; at ``t = T`` itself the
published ``av`` column is the pre-conversion fund, which is the number the annuity is
struck on and the one a reader of the worked example needs. :func:`check_conversion`
inverts the identity and is zero at every other ``t``; :func:`check_av_roll_fwd` asserts
that the account is emptied at ``T`` and stays empty.

``rentenfaktor_applied() = max(rentenfaktor_gtd, rentenfaktor_curr()) x
rf_option_factor()``. The ``max`` is the contract's own rule, and it means the projection
is sensitive to whichever of the two factors is higher and completely insensitive to the
other: the anchor converts at the current 31,50 € and model point 13 at its guaranteed
34,00 €. Taking the guaranteed factor when the current one is higher, or the reverse, is
the thirteenth pitfall.

**The conversion basis is not the projection basis, and that is deliberate.**
``rentenfaktor_gtd`` was struck at inception on first-order DAV 2004 R with a prudential
margin and a conservative interest basis; the projection runs on the best estimate,
``mort_rate(t) = mort_be_factor x mort_rate_base(t)``. The wedge between the two is the
payout phase's *Risikoüberschuss*, and ``ann_bonus_rate`` — a *teildynamische Rente* —
is the mechanism that gives it back to the annuitant. :func:`ann_pp` at ``ret_t()`` is
therefore invariant to ``mort_be_factor`` while ``claims_annuity`` is not. A model that
converted on its own best-estimate mortality would abolish the wedge and with it the
whole German payout-phase surplus mechanic, which is the eleventh pitfall.

.. rubric:: Death before Rentenbeginn pays nothing in the base design

With the survivor rider off — ``surv_annuity_rate = 0``, which is the base design and the
anchor's setting — a death in the *Aufschubphase* pays **nothing**: the reserve is
released as a mortality profit, because the entitlement is *nicht vererblich*. With the
rider on, the released reserve is payable **only where an eligible survivor exists**, and
:func:`claims` weights it by ``elig_surv_prob``.

Either way the reserve leaves the fund, which is why

    ``av_at(t + 1, "BEF_PREM") = av_at(t, "AFT_INT") x (1 - mort_rate(t))``

holds whether or not the rider is on. That single identity is the arithmetic content of
*nicht vererblich*, and :func:`check_av_roll_fwd` asserts it. The survivor's annuity
fraction is paid for through :func:`rf_option_factor` — a reduction in the
*Rentenfaktor* — rather than by scaling the death benefit, which is how a German tariff
prices the cover.

.. rubric:: The Rentengarantiezeit is a stream, never a lump sum

A *Rentengarantiezeit* runs ``guarantee_period_y`` years **from *Rentenbeginn***, not from
each death, so every continuation ends on the same date and :func:`pols_gtd` is a
one-line recursion ending at :func:`gtd_end_t`. The instalments continue **only to a
permitted survivor**, so each death contributes ``elig_surv_prob`` of a continuation and
where no eligible survivor exists the payments simply cease. They are **never
commutable**: no cash flow anywhere in this model discounts a continuation into a capital
sum. Getting either limb wrong is the fourteenth pitfall.

.. rubric:: Modules that are off in the base run

Three constructions are implemented and are inert on the anchor, so the base run
reproduces the worked example while the machinery stays visible and testable:

- **The survivor's annuity**, ``surv_annuity_rate = 0`` on the anchor, which makes
  ``claims_death`` structurally zero at every ``t``. Model points 3 and 12 switch it on.
  With it off, ``elig_surv_prob`` has no effect on any cash flow.
- **The *Rentengarantiezeit***, ``guarantee_period_y = 0`` on the anchor, which makes
  ``claims_survivor`` structurally zero and ``pols_gtd`` zero at every ``t``. Model points
  4 and 12 switch it on at 10 and 20 years.
- **The BUZ**, ``buz_prem_share = 0`` on the anchor. It is carried as a premium share and
  nothing else; model point 11 sets it to 0.49, the statutory boundary, and
  ``prem_total_pp`` is the only cells that reads it.

Both zero columns are **published rather than dropped**, because a column of zeros states
the product fact where a missing column would only hide it.

.. rubric:: Sign convention

:func:`net_cf` is **income positive** — *laufende Beiträge* and *Zuzahlungen* in, death
benefits, annuity instalments, survivor continuations, expenses and commission out —
which is the library-wide sign. :func:`liability_cf` publishes the same stream
outgo-positive, ``liability_cf(t) = -net_cf(t)`` exactly, so a Solvency II best estimate
is ``sum v(t) x liability_cf(t)`` over whatever discount curve the valuation layer
supplies. Both are columns of :func:`result_cf`, so the identity is verifiable in the
frame rather than only in prose. Unlike ``TD_FR_A``, :func:`expenses` here does **not**
include the commission: the two are separate lines of the notes' own cash flow statement
and :func:`net_cf` subtracts each once.

The shape to expect is a large new-business strain in year 1 — the *Zillmerung*
instalment is an account deduction and costs the insurer nothing, but the initial
commission at 2,5 % of the *Beitragssumme* and the acquisition expense both fall at
inception against a single year's contribution — then two decades of positive
accumulation-phase margin, a single very large negative year at *Rentenbeginn* only in
the sense that the fund converts (no cash moves), and a long negative payout tail.
"""

from modelx.serialize.jsonvalues import *

_formula = lambda point_id: None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def model_point():
    """The selected model point as a Series, from *model_point_table.csv*."""
    return data.model_point_table().loc[point_id]                    # noqa: F821


def pols_if_init():
    """The number of policies the model point represents at the valuation date.

    The opening value of :func:`pols_if`, and therefore the first ``pols_if`` value of
    :func:`result_cf`.  It opens entirely in :func:`pols_paying` or entirely in
    :func:`pols_paidup` according to ``paidup_at_init``.
    """
    return float(model_point()["pols_if_init"])


def omega_age():
    """The terminal age of the mortality table: the last ``age`` in *mort_table.csv*.

    121 on the shipped **[std]** table, the age German annuity tables are conventionally
    carried to.  The projection runs to it because the annuity is lifelong, and
    :func:`mort_rate` returns 1.0 there, so the last survivor dies at ``t = proj_len()``
    and there is no tail state of any kind.
    """
    return int(data.mort_table().index.max())                        # noqa: F821


def proj_len():
    """n: the **last projected year index**, ``omega_age() - age(1) + 1``.

    Not a row count: :func:`result_cf` is 1-based and ends at ``t = proj_len()``, which is
    this library's reading of ``proj_len()`` and is asserted by the conventions suite.
    77 on the anchor cell — twenty-two years of *Aufschubphase* at attained ages 45 to 66
    and fifty-five years of *Rentenphase* at ages 67 to 121.
    """
    return omega_age() - age(1) + 1


def age(t):
    """x(t): attained age at the start of projection year t.

    ``entry_age + duration_init + t - 1``.  Age last birthday at conclusion
    (*Eintrittsalter*), stepping on the policy anniversary **[std]**: no German convention
    was established, and here mortality drives the annuity's duration rather than any
    benefit amount, so a half-year offset is second order.
    """
    return int(model_point()["entry_age"]) + int(model_point()["duration_init"]) + t - 1


def duration(t):
    """d(t): **completed** policy years at the start of projection year t.

    ``duration_init + t - 1``, so a new-business point opens at ``duration(1) = 0``.  The
    *Beitragsdynamik*, the *Zillmerung* amortisation window and the *Zuzahlung* end date
    are all keyed to this rather than to ``t``, which is what makes an in-force model
    point work: model point 6 opens at ``duration(1) = 17`` and its premium at
    ``prem_base_pp x 1.02^17``.  Keying any of the three to ``t`` is the seventh pitfall.

    The ``dur`` index of *behaviour_table.csv* is the **policy year**, ``duration(t) + 1``.
    """
    return int(model_point()["duration_init"]) + t - 1


def cal_year(t):
    """y(t): calendar year at the start of projection year t.

    ``conclusion_year + duration_init + t - 1``.  Carried because the mortality basis is
    **generational**: DAV 2004 R is a *Generationentafel* with the improvement inside the
    table, so :func:`mort_rate_at_age` needs a calendar year as well as an age.  Two model
    points that reach the same attained age in different calendar years see different
    rates, and treating the basis as a period table is the fifteenth pitfall.
    """
    return int(model_point()["conclusion_year"]) + int(model_point()["duration_init"]) + t - 1


def ret_t():
    """T: the projection year in which *Rentenbeginn* falls, ``ret_age - age(1) + 1``.

    23 on the anchor cell.  **``T <= 0`` for a model point that opens in the
    *Rentenphase***, in which case the conversion never occurs inside the projection,
    ``ann_pp(1) = ann_pp_init`` and :func:`check_conversion` is vacuously true.  Model
    point 8 has ``ret_t() = -2``.

    The earliest permitted *Rentenbeginn* is the completion of the 62nd year of life for
    contracts concluded after 31 December 2011 and the 60th for earlier ones; the model
    reads ``ret_age`` from the model point and does not enforce the floor, which is a
    contract-writing rule rather than a projection rule.
    """
    return int(model_point()["ret_age"]) - age(1) + 1


def gtd_end_t():
    """The last projection year in which a *Rentengarantiezeit* continuation is payable.

    ``max(1, ret_t()) + guarantee_period_y - 1``.  The guarantee runs from *Rentenbeginn*,
    **not** from each death, so every continuation ends on the same date and
    :func:`pols_gtd` is zero from ``gtd_end_t() + 1`` onwards however late the death that
    started it.  Zero-length where ``guarantee_period_y = 0``, in which case
    :func:`pols_gtd` is zero everywhere.
    """
    return max(1, ret_t()) + int(model_point()["guarantee_period_y"]) - 1


def beitragssumme_pp():
    """S: the contract's *Beitragssumme* at inception, per policy.

    The sum of the contractual *laufende Beiträge* over the whole premium term
    **including** the *Beitragsdynamik* and **excluding** *Zuzahlungen* and the
    *Ratenzahlungszuschlag*::

        S = sum_{u=0}^{m-1} prem_base_pp x (1 + prem_dyn_rate)^u,   m = ret_age - entry_age

    and simply ``prem_base_pp`` for a single premium.  Excluding *Zuzahlungen* is the
    conservative reading of a question no retrieved source settles, and it matters twice:
    S is the base of the 25 ‰ *Höchstzillmersatz* cap on the acquisition charge written
    into the account, and it is the base of the initial commission.  On a long-dated
    contract with a *Dynamik* the cap binds in euro terms far above what the same
    percentage would allow on a short one.

    Struck once, at inception, from the *contract's* own terms — not from the projection —
    so an in-force model point carries the same S it was written with.
    """
    dyn = float(model_point()["prem_dyn_rate"])
    base = float(model_point()["prem_base_pp"])
    if model_point()["prem_form"] == "single":
        return base
    m = int(model_point()["ret_age"]) - int(model_point()["entry_age"])
    return sum(base * (1.0 + dyn) ** u for u in range(max(m, 0)))


def prem_freq_load():
    """phi: the *Ratenzahlungszuschlag* for the model point's payment frequency.

    Read from *option_table.csv* under ``option_id = "prem_mode"``: 1.000 annual, 1.020
    half-yearly, 1.030 quarterly, 1.050 monthly **[std]**.  It multiplies the *laufender
    Beitrag* and **nothing else** — not the *Zuzahlung*, which carries no frequency
    loading because it is a single payment, and not a single premium, which is why
    :func:`prem_freq_load` returns 1.0 for ``prem_form = "single"``.  Applying it twice, or
    to the *Zuzahlung*, is the eighth pitfall.
    """
    if model_point()["prem_form"] == "single":
        return 1.0
    return float(data.option_table().loc[                            # noqa: F821
        ("prem_mode", model_point()["prem_mode"]), "factor"])


def prem_base_pp(t):
    """The contractual *laufender Beitrag* in year t, before the *Ratenzahlungszuschlag*.

    ``prem_base_pp x (1 + prem_dyn_rate)^duration(t)`` on the ``regular`` form: the
    *Beitragsdynamik* compounds on the base premium from **inception**, so it is keyed to
    the policy duration and not to the projection year.  For ``prem_form = "single"`` the
    *Einmalbeitrag* is paid once, at ``t = 1`` and only where ``duration_init = 0``, and is
    zero at every other ``t``.

    This is the contractual amount.  What is actually charged is :func:`prem_pp`, which
    applies phi and stops at *Rentenbeginn*.
    """
    if model_point()["prem_form"] == "single":
        if t == 1 and int(model_point()["duration_init"]) == 0:
            return float(model_point()["prem_base_pp"])
        return 0.0
    return (float(model_point()["prem_base_pp"])
            * (1.0 + float(model_point()["prem_dyn_rate"])) ** duration(t))


def prem_pp(t):
    """P(t): the *laufender Beitrag* charged per premium-paying policy in year t.

    ``prem_base_pp(t) x prem_freq_load()``, taken at the **start** of the year (annual in
    advance; a fractionated mode changes the amount through the *Ratenzahlungszuschlag*,
    not the grid).  Zero from ``t = ret_t()`` — premiums stop at *Rentenbeginn* — and zero
    on a model point that opens *beitragsfrei*, whose whole cohort is in
    :func:`pols_paidup` anyway.  Letting premiums run past *Rentenbeginn* is the seventh
    pitfall.

    A dying policy has already paid the year's premium, because deaths fall at the end of
    the year: :func:`premiums` is weighted by the **opening** :func:`pols_paying` and is
    not further multiplied by ``(1 - mort_rate)``.
    """
    if t < 1 or t >= ret_t() or t > proj_len():
        return 0.0
    if int(model_point()["paidup_at_init"]) == 1:
        return 0.0
    return prem_base_pp(t) * prem_freq_load()


def zuz_take_up(t):
    """The *Zuzahlung* utilisation rate in year t, from *behaviour_table.csv*.

    Looked up at ``dur = duration(t) + 1``, the policy year: 0.70 at policy years 1–5,
    0.85 at 6–15, 0.90 at 16+ **[std]**, clamped to the last row beyond the table.

    A *utilisation rate*, not a contract term.  The contribution the *Höchstbetrag* makes
    possible is paid out of a profit not known until the year end, so whether it is paid
    at all is behavioural; a model that treats the *Zuzahlung* as contractual has quietly
    set this to 1.0.  Nothing in the delib corpus supports any level.
    """
    tab = data.behaviour_table()                                     # noqa: F821
    key = model_point()["beh_table_id"]
    d = min(duration(t) + 1, int(tab.loc[key].index.max()))
    return float(tab.loc[(key, max(d, 1)), "zuz_take_up"])


def zuz_pp(t):
    """Z(t): the *Zuzahlung* paid per premium-paying policy in year t.

    ``zuzahlung_pp x zuz_take_up(t)``, taken at the start of the year alongside the
    *laufender Beitrag* and carrying **no** *Ratenzahlungszuschlag*.  Zero from
    ``t = ret_t()``, zero once ``duration(t) >= zuzahlung_end_dur``, and zero on a
    model point that opens *beitragsfrei*.

    The *Zuzahlung* is the product's signature premium form — a self-employed buyer tops
    the contract up out of a good year — and it is the reason ``zuzahlungen`` is published
    as a column of its own rather than folded into ``premiums``: it is a distinct premium
    form on a distinct charge basis, carrying ``alpha_zuz_rate`` instead of a share of the
    *Zillmerung*.
    """
    if t < 1 or t >= ret_t() or t > proj_len():
        return 0.0
    if int(model_point()["paidup_at_init"]) == 1:
        return 0.0
    if duration(t) >= int(model_point()["zuzahlung_end_dur"]):
        return 0.0
    return float(model_point()["zuzahlung_pp"]) * zuz_take_up(t)


def prem_total_pp(t):
    """The **total** contribution the policyholder pays in year t, including the BUZ.

    ``(prem_pp(t) + zuz_pp(t)) / (1 - buz_prem_share)``.  A **reporting cells that enters
    no cash flow**: it appears in no :func:`result_cf` column and in :func:`net_cf` at no
    ``t``.  ``prem_base_pp`` is the *old-age* contribution; the BUZ premium buys a cover
    this model does not project, and its disability mechanics belong to ``BU_DE_S``.

    ``buz_prem_share < 0.50`` is the statutory invariant — the supplementary covers
    together must stay strictly below half the total contribution or the whole
    contribution loses its *Sonderausgabenabzug* — and model point 11 sits at 0.49, the
    boundary.  Modelling the BUZ as premium income with no benefit is the seventeenth
    pitfall.
    """
    return (prem_pp(t) + zuz_pp(t)) / (1.0 - float(model_point()["buz_prem_share"]))


def alpha_total_pp():
    """The zillmerised acquisition charge written into the account, per policy.

    ``zill_rate x beitragssumme_pp()``.  The *Höchstzillmersatz* caps it at **25 ‰ of the
    *Beitragssumme*** for business written from 1 January 2015, reduced from 40 ‰ by the
    LVRG; the shipped tariffs carry the two rates and the in-force pre-2015 model points
    take the older one.

    This is a **deduction from the policyholder's *Deckungskapital***, hence insurer
    income — not an expense.  The insurer's own acquisition outgo is ``acq_expense_pp``
    plus the initial commission, and the German design is precisely that what the insurer
    pays out is sized to what it may write into the reserve.
    """
    return (float(data.charge_table().loc[                           # noqa: F821
        model_point()["tariff_id"], "zill_rate"]) * beitragssumme_pp())


def alpha_amort_pp(t):
    """alpha(t): the *Zillmerung* instalment struck against the account in year t.

    ``alpha_total_pp() / zill_spread_y`` in equal instalments over the contract's first
    ``zill_spread_y = 5`` years of *Aufschubphase* — **of the contract**, not of the
    projection — and zero thereafter.  An in-force model point past duration 5 therefore
    sees none of it at any ``t``: model point 6, at ``duration_init = 17``, sees zero
    throughout.  A single-premium contract runs the same five instalments, so the total
    written into its account is the same 25 ‰ of the *Beitragssumme* and the debit simply
    outlives the one premium that paid for it.

    Charging the whole *Zillmerung* in year one is the fifth pitfall.  On the anchor cell
    the instalment is equal at ``t = 1 ... 5``, zero from ``t = 6``, and the five sum to
    ``zill_rate x beitragssumme_pp()`` exactly.

    Whether the AltZertG's five-year spreading of acquisition and distribution costs
    reaches *Basisrentenverträge* at all was not established; the five years here are the
    LVRG-era German market shape and are **[std]**.
    """
    if t < 1 or t >= ret_t() or t > proj_len():
        return 0.0
    if int(model_point()["paidup_at_init"]) == 1:
        return 0.0
    if duration(t) >= zill_spread_y:                                 # noqa: F821
        return 0.0
    return alpha_total_pp() / zill_spread_y                          # noqa: F821


def alpha_zuz_pp(t):
    """alpha_z(t): the acquisition charge on the year's *Zuzahlung*, per paying policy.

    ``alpha_zuz_rate x zuz_pp(t)``, charged in the year the *Zuzahlung* is paid **[std]**.
    A *Zuzahlung* is not part of the *Beitragssumme* and so carries no share of the
    *Zillmerung*; it carries its own single charge instead, which is the normal German
    treatment of a top-up.  Zero where no *Zuzahlung* is paid.
    """
    return (float(data.charge_table().loc[                           # noqa: F821
        model_point()["tariff_id"], "alpha_zuz_rate"]) * zuz_pp(t))


def unit_cost_pp(t):
    """u(t): the *Stückkosten* charged to the account in year t, per policy.

    ``unit_cost_pp x (1 + expense_infl)^(t - 1)`` **[std]** — 36,00 € inflating at 1,5 %
    a year.  Charged to **both** blocks: a premium-free policy keeps paying the
    *Stückkosten* and the reserve charge and stops paying beta and the *Zillmerung*
    instalment, which is the whole economic content of a *Beitragsfreistellung*.

    An account deduction, not an expense.  The insurer's own maintenance outgo is
    ``maint_expense_pp`` and is a separate line of :func:`expenses`.
    """
    return (float(data.charge_table().loc[                           # noqa: F821
        model_point()["tariff_id"], "unit_cost_pp"])
        * (1.0 + float(data.charge_table().loc[                      # noqa: F821
            model_point()["tariff_id"], "expense_infl"])) ** (t - 1))


def prem_to_av_pp(t):
    """N(t): the premium credited to the account in year t, after all four charges.

    ``(P(t) + Z(t)) x (1 - beta_prem) - alpha_amort_pp(t) - alpha_zuz_pp(t) -
    unit_cost_pp(t)``.

    **N(t) may be negative** in the first years of a heavily zillmerised contract, and it
    is **not floored**: there is no *Rückkaufswert* on this product for a floor to protect,
    and flooring the account at an internally computed surrender value would change the
    early years even though nothing is ever paid.  That a German *Deckungskapital* starts
    near zero is a consequence of this line and not a modelling artefact.

    Zero from ``t = ret_t()``: there is no account in the *Rentenphase*.
    """
    if t < 1 or t >= ret_t() or t > proj_len():
        return 0.0
    beta = float(data.charge_table().loc[                            # noqa: F821
        model_point()["tariff_id"], "beta_prem"])
    return ((prem_pp(t) + zuz_pp(t)) * (1.0 - beta)
            - alpha_amort_pp(t) - alpha_zuz_pp(t) - unit_cost_pp(t))


def premiums(t):
    """*Laufende Beiträge* collected in year t at fund level, an inflow.

    ``prem_pp(t) x pols_paying(t)``, weighted by the **premium-paying** ledger and by the
    **opening** count: premiums fall at the start of the year and deaths at the end, so a
    policy that dies during year t has already paid for it.  Multiplying by
    ``(1 - mort_rate(t))`` here applies the death rule twice.
    """
    return prem_pp(t) * pols_paying(t)


def zuzahlungen(t):
    """*Zuzahlungen* collected in year t at fund level, an inflow.

    ``zuz_pp(t) x pols_paying(t)``.  Published as a column of its own rather than folded
    into :func:`premiums` because it is a distinct premium form on a distinct charge
    basis, and because setting ``zuz_take_up`` to zero — which removes about two fifths of
    the anchor's contribution stream — is a legitimate variant a reader should be able to
    see the size of.
    """
    return zuz_pp(t) * pols_paying(t)


def mort_rate_at_age(x, y):
    """q^t(x, y): the **first-order** table death rate at age x in calendar year y.

    ``qx(x) x (1 - trend(x))^(y - mort_base_year)``, clipped to ``[0, 1]``.  The
    generational form: the improvement lives **inside** the basis, which is what makes
    DAV 2004 R a *Generationentafel* and what a replacement table must preserve.  Two
    model points at the same attained age in different calendar years see different rates,
    and the shipped table is anchored at ``mort_rate_at_age(67, 2005) = 0.014000``.

    First order, so it carries the DAV's prudential margins.  The guaranteed
    *Rentenfaktor* is struck on this basis; the projection runs on :func:`mort_rate`.
    """
    row = data.mort_table().loc[x]                                   # noqa: F821
    rate = (float(row["qx"])
            * (1.0 - float(row["trend"])) ** (y - mort_base_year))   # noqa: F821
    return min(max(rate, 0.0), 1.0)


def mort_rate_base(t):
    """The first-order table rate applying in projection year t.

    ``mort_rate_at_age(age(t), cal_year(t))``.  Split from :func:`mort_rate` so that the
    table rate and the best-estimate rate have separate names and the step between them is
    a single visible factor.
    """
    return mort_rate_at_age(age(t), cal_year(t))


def mort_rate(t):
    """q(t): the best-estimate annual death rate applied in projection year t.

    ``mort_be_factor x mort_rate_base(t)``, the step from the shipped first-order table to
    a best estimate.  ``mort_be_factor = 0.85`` is **[std]** and is the single largest
    unanchored number in the payout phase.

    **The terminal age is absorbing**: ``mort_rate(t) = 1.0`` where
    ``age(t) >= omega_age()``, whatever ``mort_be_factor`` says, so the last survivor dies
    at ``t = proj_len()``, ``pols_if(proj_len() + 1) = 0`` exactly and the decrement
    closure identity holds to the last euro.  Without it the generational trend would
    carry the table's own terminal rate below 1 and leave a residue in force after the end
    of the table.

    Deaths fall at the **end** of the year, after interest is credited, so a dying policy
    carries a full year's interest and has paid a full year's premium.
    """
    if age(t) >= omega_age():
        return 1.0
    return min(1.0, mort_be_factor * mort_rate_base(t))              # noqa: F821


def bf_rate(t):
    """f(t): the *Beitragsfreistellung* rate applied in projection year t.

    Read from *behaviour_table.csv* at ``dur = duration(t) + 1``: 4,0 % at policy years
    1–5, 3,0 % at 6–10, 2,0 % at 11+ **[std]**, clamped to the last row beyond the table.

    **This is not a lapse rate and there is no lapse decrement on this product.** § 165 VVG
    survives and is the contract's only behavioural exit, but it removes the premium, not
    the policy: the rate moves policies from :func:`pols_paying` to :func:`pols_paidup` and
    appears nowhere in :func:`pols_if`.  Treating it as a lapse is the second pitfall.

    Zero from ``t = ret_t()`` — there is no premium left to stop — and zero on a
    single-premium contract for the same reason.  Applied to the **survivors** of the
    year's death decrement.
    """
    if t < 1 or t >= ret_t() or t > proj_len():
        return 0.0
    if model_point()["prem_form"] == "single":
        return 0.0
    tab = data.behaviour_table()                                     # noqa: F821
    key = model_point()["beh_table_id"]
    d = min(duration(t) + 1, int(tab.loc[key].index.max()))
    return float(tab.loc[(key, max(d, 1)), "bf_rate"])


def pols_paying(t):
    """l^p(t): premium-paying policies at the **start** of projection year t.

    ``pols_if_init()`` at ``t = 1`` unless the model point opens *beitragsfrei*, then
    ``l^p(t + 1) = l^p(t) x (1 - q(t)) x (1 - f(t))``: the death decrement first, the
    *Beitragsfreistellung* on its survivors.  The weight on :func:`premiums` and
    :func:`zuzahlungen`.

    A model point opens **entirely** paying or **entirely** premium-free.  A part-paid-up
    book is two model points; averaging the two cohorts is the third pitfall.
    """
    if t < 1 or t > proj_len() + 1:
        return 0.0
    if t == 1:
        return 0.0 if int(model_point()["paidup_at_init"]) == 1 else pols_if_init()
    return pols_paying(t - 1) * (1.0 - mort_rate(t - 1)) * (1.0 - bf_rate(t - 1))


def pols_paidup(t):
    """l^f(t): premium-free (*beitragsfreie*) policies at the start of projection year t.

    ``l^f(t + 1) = l^f(t) x (1 - q(t)) + pols_freeze(t)``.  The block is **absorbing**: no
    *Wiederinkraftsetzung* is modelled, because none was established, which is conservative
    on premium income and is a standardization rather than a contract fact.

    A premium-free policy is still in force, still certified, still protected and still
    converts at *Rentenbeginn*.  It keeps paying the *Stückkosten* and the reserve charge
    out of its own *Deckungskapital* and stops paying beta and the *Zillmerung* instalment.
    """
    if t < 1 or t > proj_len() + 1:
        return 0.0
    if t == 1:
        return pols_if_init() if int(model_point()["paidup_at_init"]) == 1 else 0.0
    return pols_paidup(t - 1) * (1.0 - mort_rate(t - 1)) + pols_freeze(t - 1)


def pols_if(t):
    """l(t): policies in force at the **start** of projection year t, both cohorts.

    ``pols_paying(t) + pols_paidup(t)``, and the weight on every cash flow of the same
    :func:`result_cf` row.  It obeys

        ``pols_if(t + 1) = pols_if(t) x (1 - mort_rate(t))``

    with ``bf_rate`` **absent from the identity**, because a *Beitragsfreistellung* is a
    transfer between the two ledgers and not an exit.  That is the whole of what
    distinguishes this product's decrement structure from a Schicht-3 annuity's, and
    :func:`check_pols_roll_fwd` asserts it.

    ``pols_if(proj_len() + 1)`` is defined and is **zero**, because :func:`mort_rate` is 1
    at the terminal age.  It is read by :func:`check_pols_roll_fwd` and by nothing else;
    :func:`result_cf` stops at ``t = proj_len()``.
    """
    return pols_paying(t) + pols_paidup(t)


def pols_if_at(t, timing):
    """The number of policies in force at a point inside projection year t.

    ``"BEF_DECR"``
        l(t), the start of the year, before any decrement; the same number as
        :func:`pols_if` and the weight on that year's cash flows.

    ``"AFT_DEATH"``
        ``l(t) x (1 - q(t))``, after the death decrement, which falls at the end of the
        year after interest has been credited.  This is the population the
        *Beitragsfreistellung* is taken from.

    ``"AFT_FREEZE"``
        l(t + 1).  **Numerically identical to** ``"AFT_DEATH"``, and deliberately so: the
        freeze moves policies between :func:`pols_paying` and :func:`pols_paidup` without
        removing any, so the total is unchanged.  The two timings exist so that the
        processing order is readable in the code and so that the equality is a statement
        the model makes rather than one a reader has to reconstruct.
    """
    if timing == "BEF_DECR":
        return pols_if(t)
    if timing == "AFT_DEATH":
        return pols_if(t) * (1.0 - mort_rate(t))
    if timing == "AFT_FREEZE":
        return pols_if_at(t, "AFT_DEATH")
    raise ValueError("invalid timing")


def pols_death_paying(t):
    """Expected deaths among premium-paying policies in year t: ``l^p(t) x q(t)``.

    Split from :func:`pols_death_paidup` because the two cohorts release **different**
    reserves — :func:`db_pp` per policy against :func:`db_pu_pp` — and only the split
    figure can be multiplied by the right one.
    """
    return pols_paying(t) * mort_rate(t)


def pols_death_paidup(t):
    """Expected deaths among premium-free policies in year t: ``l^f(t) x q(t)``."""
    return pols_paidup(t) * mort_rate(t)


def pols_death(t):
    """Expected deaths in projection year t, both cohorts.

    ``pols_death_paying(t) + pols_death_paidup(t)``, equivalently ``l(t) x q(t)``.  In the
    *Aufschubphase* a death pays **nothing** in the base design — the reserve is released
    as a mortality profit, because the entitlement is *nicht vererblich* — and with the
    survivor rider on it pays only where an eligible survivor exists.  In the
    *Rentenphase* the annuity simply ends, and each death contributes ``elig_surv_prob`` of
    a *Rentengarantiezeit* continuation where one is running.
    """
    return pols_death_paying(t) + pols_death_paidup(t)


def pols_freeze(t):
    """Policies going *beitragsfrei* during projection year t.

    ``l^p(t) x (1 - q(t)) x f(t)``: the *Beitragsfreistellung* is taken on the **survivors**
    of the year's death decrement, which is the processing order the notes set out
    **[std]**.  Zero in the *Rentenphase* and zero on a single-premium contract.

    Each frozen policy carries ``av_pp_at(t, "AFT_INT")`` of *Deckungskapital* with it from
    the paying block into the premium-free block, which is the term
    ``pols_freeze(t) x av_pp_at(t, "AFT_INT")`` in :func:`av_pu_at`.  Nothing leaves the
    fund, which is why :func:`check_av_roll_fwd` closes across a freeze.
    """
    if t < 1 or t >= ret_t() or t > proj_len():
        return 0.0
    return pols_paying(t) * (1.0 - mort_rate(t)) * bf_rate(t)


def pols_gtd(t):
    """g(t): *Rentengarantiezeit* continuations running at the start of year t.

    The guarantee runs ``guarantee_period_y`` years **from *Rentenbeginn***, so every
    continuation ends on the same date::

        g(t) = 0                                     for t < max(1, ret_t()) or t > gtd_end_t()
        g(t) = g(t - 1) + pols_death(t - 1) x elig_surv_prob    inside the window

    ``elig_surv_prob`` is what makes this a Schicht-1 guarantee rather than a Schicht-3
    one: the instalments continue **only to a permitted survivor** — a spouse, a registered
    partner, or a child while *Kindergeld* runs — and where none exists the payments simply
    cease.  They are also **never commutable**: :func:`claims` pays ``ann_pp(t) x g(t)`` as
    a stream and nothing anywhere discounts a continuation into a capital sum.

    Monotone non-decreasing inside the window, and exactly zero outside it.  Zero at every
    ``t`` where ``guarantee_period_y = 0``, which is the base design and the anchor's
    setting.
    """
    if int(model_point()["guarantee_period_y"]) == 0:
        return 0.0
    start = max(1, ret_t())
    if t < start or t > gtd_end_t() or t > proj_len():
        return 0.0
    if t == start:
        return 0.0
    return pols_gtd(t - 1) + pols_death(t - 1) * elig_surv_prob      # noqa: F821


def decl_rate(t):
    """The declared *laufende Verzinsung* in projection year t, from *surplus_table.csv*.

    2,60 % for ``t = 1 ... 10``, 2,40 % for ``t = 11 ... 20``, 2,20 % thereafter in the
    ``base`` scenario **[std]**, clamped to the last row beyond the table.

    **It is the total credited rate, not a spread over the *Rechnungszins*.**  German
    declared rates are quoted that way, which is why :func:`cred_rate` is a maximum and not
    a sum.  A scenario rather than a forecast: no declared rate specific to a Basisrente
    was established anywhere in the delib corpus, and the path is set above the 1,00 %
    *Höchstrechnungszins* by a plausible surplus margin and graded down.
    """
    tab = data.surplus_table()                                       # noqa: F821
    key = model_point()["surplus_scenario_id"]
    tt = min(max(t, 1), int(tab.loc[key].index.max()))
    return float(tab.loc[(key, tt), "decl_rate"])


def cred_rate(t):
    """i(t): the rate credited to the *Deckungskapital* in projection year t.

    ``max(gtd_rate, decl_rate(t))`` — a **maximum**, not a sum.  ``gtd_rate`` is the
    contract's *Rechnungszins*, capped at the *Höchstrechnungszins* in force at conclusion
    and fixed for the whole term, so a book carries a stack of guarantee vintages and the
    ``max`` picks a different branch on each.  On the anchor (1,00 %) the declared path
    binds at every ``t``; on model point 8 (2,75 %, above the whole declared path) the
    guarantee binds at every ``t``.

    Stacking the declared rate on top of the guarantee is the sixth pitfall and is worth a
    great deal over a twenty-two-year deferment.  The reserve charge gamma is netted
    inside the same crediting step, in :func:`av_pp_at` and :func:`av_pu_at`.
    """
    return max(float(model_point()["gtd_rate"]), decl_rate(t))


def av_pp(t):
    """A^p(t): the *Deckungskapital* **per premium-paying policy** at the start of year t.

    ``av_pp_init`` at ``t = 1`` for a point that opens premium-paying, zero for one that
    opens *beitragsfrei* (whose whole reserve is in :func:`av_pu_at`), then
    ``av_pp_at(t - 1, "AFT_INT")``.

    Per **policy**, against :func:`av_pu_at`, which is the premium-free block at **fund**
    level.  The two diverge from the first freeze and must not be averaged into one
    per-policy figure: that is the third pitfall.  Zero from ``t = ret_t() + 1``, the fund
    having become an annuity obligation.
    """
    if t < 1 or t > ret_t() or t > proj_len() + 1:
        return 0.0
    if t == 1:
        if int(model_point()["paidup_at_init"]) == 1:
            return 0.0
        return float(model_point()["av_pp_init"])
    return av_pp_at(t - 1, "AFT_INT")


def av_pp_at(t, timing):
    """A^p(t, .): the *Deckungskapital* per premium-paying policy inside year t.

    ``"BEF_PREM"``
        :func:`av_pp`, the start of the year before the premium is taken.

    ``"AFT_PREM"``
        after the year's premium, *Zuzahlung* and all four charges:
        ``av_pp_at(t, "BEF_PREM") + prem_to_av_pp(t)``.

    ``"AFT_INT"``
        after interest, credited at the **end** of the year net of the reserve charge:
        ``av_pp_at(t, "AFT_PREM") x (1 + cred_rate(t) - gamma_av)``.  A policy that dies
        during the year has been credited a full year's interest, because deaths fall
        after crediting.

    All three are zero from ``t = ret_t()`` except ``"BEF_PREM"`` at ``t = ret_t()``
    itself, which is the fund the annuity is struck on.
    """
    if t < 1 or t > proj_len():
        return 0.0
    if timing == "BEF_PREM":
        return av_pp(t)
    if t >= ret_t():
        if timing in ("AFT_PREM", "AFT_INT"):
            return 0.0
        raise ValueError("invalid timing")
    if timing == "AFT_PREM":
        return av_pp_at(t, "BEF_PREM") + prem_to_av_pp(t)
    if timing == "AFT_INT":
        gamma = float(data.charge_table().loc[                       # noqa: F821
            model_point()["tariff_id"], "gamma_av"])
        return av_pp_at(t, "AFT_PREM") * (1.0 + cred_rate(t) - gamma)
    raise ValueError("invalid timing")


def av_pu_at(t, timing):
    """A^f(t, .): the premium-free block's *Deckungskapital*, at **fund** level.

    Carried at fund level rather than per policy because a policy that froze at duration 5
    and one that froze at duration 15 hold different reserves and only the aggregate is
    meaningful.

    ``"BEF_PREM"``
        ``av_pp_init x pols_if_init()`` at ``t = 1`` for a model point that opens
        *beitragsfrei*, zero otherwise; then
        ``av_pu_at(t - 1, "AFT_INT") x (1 - q(t - 1)) + pols_freeze(t - 1) x
        av_pp_at(t - 1, "AFT_INT")`` — the survivors of the block, plus the reserves the
        year's freezes carried across from the paying block.

    ``"AFT_PREM"``
        ``av_pu_at(t, "BEF_PREM") - unit_cost_pp(t) x pols_paidup(t)``.  The block pays the
        *Stückkosten* and nothing else: no premium, so no beta and no *Zillmerung*
        instalment.  That asymmetry is the whole economic content of a
        *Beitragsfreistellung*.

    ``"AFT_INT"``
        as for the paying block, ``x (1 + cred_rate(t) - gamma_av)``.
    """
    if t < 1 or t > proj_len():
        return 0.0
    if timing == "BEF_PREM":
        if t > ret_t():
            return 0.0
        if t == 1:
            if int(model_point()["paidup_at_init"]) == 1:
                return float(model_point()["av_pp_init"]) * pols_if_init()
            return 0.0
        return (av_pu_at(t - 1, "AFT_INT") * (1.0 - mort_rate(t - 1))
                + pols_freeze(t - 1) * av_pp_at(t - 1, "AFT_INT"))
    if t >= ret_t():
        if timing in ("AFT_PREM", "AFT_INT"):
            return 0.0
        raise ValueError("invalid timing")
    if timing == "AFT_PREM":
        return av_pu_at(t, "BEF_PREM") - unit_cost_pp(t) * pols_paidup(t)
    if timing == "AFT_INT":
        gamma = float(data.charge_table().loc[                       # noqa: F821
            model_point()["tariff_id"], "gamma_av"])
        return av_pu_at(t, "AFT_PREM") * (1.0 + cred_rate(t) - gamma)
    raise ValueError("invalid timing")


def av_at(t, timing):
    """A(t, .): the whole *Deckungskapital* at fund level inside year t.

    ``av_pp_at(t, timing) x pols_paying(t) + av_pu_at(t, timing)``, with the **opening**
    paying count as the weight at every timing, because deaths fall after interest.

    This is the only one of the three account cells that rolls forward on mortality alone::

        av_at(t + 1, "BEF_PREM") = av_at(t, "AFT_INT") x (1 - mort_rate(t))

    and that identity — :func:`check_av_roll_fwd` — holds **whether or not** the survivor
    rider is on, because the reserve of a policy terminated by death leaves the fund either
    way: as a claim where an eligible survivor exists, as a mortality profit where none
    does.  It is the arithmetic content of *nicht vererblich*.  It also holds across a
    *Beitragsfreistellung*, because a freeze moves reserve between the two blocks without
    removing any.
    """
    return av_pp_at(t, timing) * pols_paying(t) + av_pu_at(t, timing)


def av(t):
    """A(t): the *Deckungskapital* at the start of year t, fund level.

    ``av_at(t, "BEF_PREM")``.  A **state variable, reported and not summed** — the third
    column of :func:`result_cf` is a balance, not a cash flow, and adding it to anything
    is a category error.

    Zero for every ``t > ret_t()``.  At ``t = ret_t()`` itself it is the **pre-conversion
    fund**, which is the number the annuity is struck on and the one a reader following the
    worked example needs; :func:`fund_at_conv` grosses it up by the *Schlussüberschussanteil*
    and the account is empty from the next year onwards.
    """
    return av_at(t, "BEF_PREM")


def rentenfaktor_curr():
    """The insurer's *aktueller Rentenfaktor* at the conversion age.

    Read from *rentenfaktor_table.csv* at ``(rf_scenario_id, ret_age)``: euro of monthly
    annuity per 10 000 € of capital.  31,50 € at age 67 in the ``base`` scenario **[std]**;
    the ``low`` scenario runs about 12 % below it.

    Entirely **[std]**: no *Rentenfaktor* level, range or time series exists anywhere in
    the delib corpus, for this or any product.  It is the single largest lever in the
    model, because it converts the entire accumulated fund into the entire payout-phase
    liability.  Zero where the model point opens in the *Rentenphase* and no conversion
    occurs.
    """
    if ret_t() < 1:
        return 0.0
    return float(data.rentenfaktor_table().loc[                      # noqa: F821
        (model_point()["rf_scenario_id"], int(model_point()["ret_age"])), "rf_curr"])


def rf_option_factor():
    """The multiplicative reduction in the *Rentenfaktor* bought by the two options.

    ``factor("guarantee_period", guarantee_period_y) x factor("survivor",
    surv_annuity_rate)`` from *option_table.csv*: 1,000 for no *Rentengarantiezeit*, 0,995
    for ten years and 0,974 for twenty; 1,000 for no survivor's annuity and 0,930 for one
    at 60 % of the main annuity.  All **[std]**.

    A German tariff pays for both covers **out of the annuity** rather than by scaling the
    death benefit, which is why they appear here and not in :func:`claims`.  1,000 on the
    anchor cell, where both options are off.
    """
    tab = data.option_table()                                        # noqa: F821
    g = "%d" % int(model_point()["guarantee_period_y"])
    s = "%.2f" % float(model_point()["surv_annuity_rate"])
    return (float(tab.loc[("guarantee_period", g), "factor"])
            * float(tab.loc[("survivor", s), "factor"]))


def rentenfaktor_applied():
    """R: the *Rentenfaktor* actually applied at *Rentenbeginn*.

    ``max(rentenfaktor_gtd, rentenfaktor_curr()) x rf_option_factor()``.

    The ``max`` is the contract's own rule and it is a genuine discontinuity: the
    projection is sensitive to whichever factor is higher and completely insensitive to the
    other.  The anchor cell converts at the current 31,50 € against a guaranteed 28,00 €;
    model point 13 converts at its guaranteed 34,00 € against a ``low``-scenario current
    27,72 €, which is why that point exists.  Taking one when the other is higher is the
    thirteenth pitfall.  Monotone non-decreasing in both inputs.

    ``rentenfaktor_gtd`` was struck at inception on **first-order** DAV 2004 R with a
    prudential margin and a conservative interest basis; it is not, and must not be, the
    projection's own best-estimate basis.
    """
    return max(float(model_point()["rentenfaktor_gtd"]),
               rentenfaktor_curr()) * rf_option_factor()


def fund_at_conv():
    """F: the fund converted at *Rentenbeginn*, including the *Schlussüberschussanteil*.

    ``av_at(ret_t(), "BEF_PREM") x (1 + terminal_bonus_rate)``, at fund level.

    The *Schlussüberschussanteil* is allocated at this **single date** and at no other,
    which is a contract fact rather than a standardization: the contract has no earlier
    exit — no surrender, no capital option — so there is no earlier trigger for a terminal
    bonus to attach to.  The 4,0 % level is **[std]** with nothing behind it.

    Zero for a model point that opens in the *Rentenphase*, where no conversion occurs
    inside the projection.
    """
    if ret_t() < 1:
        return 0.0
    sigma = float(data.charge_table().loc[                           # noqa: F821
        model_point()["tariff_id"], "terminal_bonus_rate"])
    return av_at(ret_t(), "BEF_PREM") * (1.0 + sigma)


def ann_bonus_rate(t):
    """b(t): the *Überschussrente* uplift applied at the end of payout year t.

    1,0 % p.a. compounding in the ``base`` scenario **[std]**, read from
    *surplus_table.csv*.  A *teildynamische Rente*: a *volldynamische* one would consume
    the whole first-order margin released in the payout phase and a *konstante* one none,
    and 1,0 % is deliberately in between.

    It is the mechanism that gives the conversion-basis wedge back to the annuitant — the
    fund is converted on first-order mortality and run off on the best estimate — so this
    lever and ``mort_be_factor`` between them decide the payout phase's whole economics.
    Both are **[std]** independently.
    """
    tab = data.surplus_table()                                       # noqa: F821
    key = model_point()["surplus_scenario_id"]
    tt = min(max(t, 1), int(tab.loc[key].index.max()))
    return float(tab.loc[(key, tt), "ann_bonus_rate"])


def ann_pp(t):
    """a(t): the annual annuity per surviving annuitant in projection year t.

    Zero before *Rentenbeginn*; at ``t = ret_t()`` the conversion::

        ann_pp(T) = fund_at_conv() / pols_if(T) / rf_unit
                    x rentenfaktor_applied() x ann_freq

    which is the **cohort-average** annual annuity per annuitant — exact at fund level even
    though the paying and premium-free cohorts arrive with different per-policy reserves —
    and thereafter ``ann_pp(t) = ann_pp(t - 1) x (1 + ann_bonus_rate(t - 1))``.

    For a model point that opens in the *Rentenphase* (``ret_t() <= 0``) the conversion
    never occurs inside the projection and ``ann_pp(1) = ann_pp_init``.

    ``ann_freq = 12`` because the annuity is **monthly**; the twelve instalments are booked
    together at the **start** of the payout year on the opening in-force count, so a life
    that dies during the year has been paid for the whole of it.  That is a stated
    approximation of a monthly grid on an annual one — the twelfth pitfall names it — and
    it is generous to the year of death by up to a full year's annuity, concentrated in the
    high-mortality tail.
    """
    if t < 1 or t > proj_len():
        return 0.0
    start = max(1, ret_t())
    if t < start:
        return 0.0
    if t == start:
        if ret_t() < 1:
            return float(model_point()["ann_pp_init"])
        if pols_if(t) <= 0.0:
            return 0.0
        return (fund_at_conv() / pols_if(t) / rf_unit                # noqa: F821
                * rentenfaktor_applied() * ann_freq)                 # noqa: F821
    return ann_pp(t - 1) * (1.0 + ann_bonus_rate(t - 1))


def db_pp(t):
    """The *Deckungskapital* released per dying **premium-paying** policy in year t.

    ``av_pp_at(t, "AFT_INT")``: deaths fall after interest is credited, so the reserve
    released is the end-of-year one.  What is *paid* is this amount only where the survivor
    rider is on **and** an eligible survivor exists; otherwise the whole of it is a
    mortality profit and nothing is paid.  See :func:`claims`.
    """
    return av_pp_at(t, "AFT_INT")


def db_pu_pp(t):
    """The *Deckungskapital* released per dying **premium-free** policy in year t.

    ``av_pu_at(t, "AFT_INT") / pols_paidup(t)``: the premium-free block is carried at fund
    level, so the per-policy figure is an average over policies that froze at different
    durations.  That average is exact for this purpose — the deaths are a uniform share of
    the block — and it is the only per-policy figure the block admits.  Zero where the
    block is empty.
    """
    if pols_paidup(t) <= 0.0:
        return 0.0
    return av_pu_at(t, "AFT_INT") / pols_paidup(t)


def claims(t, kind=None):
    """Benefit outgo in projection year t, by kind; the total when kind is omitted.

    ``"DEATH"``
        the *Deckungskapital* released by deaths in the *Aufschubphase*, weighted by
        ``elig_surv_prob``.  **Structurally zero where ``surv_annuity_rate = 0``**, which
        is the base design and the anchor's setting: the entitlement is *nicht vererblich*,
        so a death before *Rentenbeginn* pays nothing and the reserve is released as a
        mortality profit.  Zero from ``t = ret_t()`` in every case.

        Where the rider is on this is **not a lump sum to a beneficiary**.  Everything paid
        to a survivor must be paid as an annuity, so what is booked is the reserve leaving
        this contract as the **single premium of a survivor's annuity** — a new liability,
        an immediate annuity, that this model does not project.

    ``"ANNUITY"``
        ``ann_pp(t) x pols_if(t)``: twelve monthly instalments booked at the start of the
        payout year on the opening in-force count.

    ``"SURVIVOR"``
        ``ann_pp(t) x pols_gtd(t)``: the *Rentengarantiezeit* stream, payable only to a
        permitted survivor and **never commutable**.  Structurally zero where
        ``guarantee_period_y = 0``.

    There is no fourth kind, and there can be none: no surrender value, no capital option,
    no partial capital payment and no commutation exist on this product.
    :func:`check_no_capital` asserts that the total is exactly the sum of these three.
    """
    if kind is None:
        return sum(claims(t, k) for k in ("DEATH", "ANNUITY", "SURVIVOR"))
    if kind == "DEATH":
        if float(model_point()["surv_annuity_rate"]) <= 0.0:
            return 0.0
        if t < 1 or t >= ret_t() or t > proj_len():
            return 0.0
        return elig_surv_prob * (                                    # noqa: F821
            db_pp(t) * pols_death_paying(t) + db_pu_pp(t) * pols_death_paidup(t))
    if kind == "ANNUITY":
        if t < max(1, ret_t()) or t > proj_len():
            return 0.0
        return ann_pp(t) * pols_if(t)
    if kind == "SURVIVOR":
        if t < 1 or t > proj_len():
            return 0.0
        return ann_pp(t) * pols_gtd(t)
    raise ValueError("invalid kind")


def expenses(t):
    """E(t): the insurer's own expense outgo in projection year t, fund level.

    Acquisition expense at inception (``t = 1`` and ``duration_init = 0`` only), then the
    maintenance expense per in-force policy in the *Aufschubphase* and the annuity
    administration per annuitant **and per *Rentengarantiezeit* continuation** in the
    *Rentenphase*, both inflating at ``expense_infl`` from the valuation date.  The payout
    phase is administratively cheaper than the accumulation phase, which is why the two
    rates differ.

    **The commission is not in here.**  It is a separate line of the notes' cash flow
    statement and a separate column of :func:`result_cf`, and :func:`net_cf` subtracts each
    once.

    Nor are the *charges*: beta, gamma, the *Stückkosten* and the *Zillmerung* amortisation
    are deductions from the policyholder's account and hence insurer **income**.  This
    cells is therefore invariant to ``beta_prem``, ``gamma_av`` and ``zill_rate``, and
    those three move :func:`net_cf` only through the smaller annuity that a smaller fund
    buys at *Rentenbeginn*.  Booking a charge as an expense as well is the fourth pitfall.
    """
    if t < 1 or t > proj_len():
        return 0.0
    row = data.charge_table().loc[model_point()["tariff_id"]]        # noqa: F821
    infl = (1.0 + float(row["expense_infl"])) ** (t - 1)
    out = 0.0
    if t == 1 and int(model_point()["duration_init"]) == 0:
        out += float(row["acq_expense_pp"]) * pols_if_init()
    if t < ret_t():
        out += float(row["maint_expense_pp"]) * infl * pols_if(t)
    else:
        out += float(row["annuity_admin_pp"]) * infl * (pols_if(t) + pols_gtd(t))
    return out


def commissions(t):
    """C(t): commission outgo in projection year t, fund level.

    ``comm_init_rate x beitragssumme_pp() x pols_if_init()`` at inception — the
    *Abschlussprovision*, sized to the *Zillmerung* cap, which is the German design in
    which what the insurer pays out is what it may write into the reserve — plus
    ``comm_renew_rate x (premiums(t) + zuzahlungen(t))`` from ``t = 2``, the
    *Bestandsprovision*.  Both **[std]**: the corpus's only datum is a 1 575 €
    *Abschlussprovision* on one specimen quotation, and it is [unverified].

    Paid **only** where the model point is new business (``duration_init = 0``): an
    in-force point's acquisition commission was paid before the valuation date and is not a
    projected cash flow.
    """
    if t < 1 or t > proj_len():
        return 0.0
    row = data.charge_table().loc[model_point()["tariff_id"]]        # noqa: F821
    out = 0.0
    if t == 1 and int(model_point()["duration_init"]) == 0:
        out += float(row["comm_init_rate"]) * beitragssumme_pp() * pols_if_init()
    if t >= 2:
        out += float(row["comm_renew_rate"]) * (premiums(t) + zuzahlungen(t))
    return out


def net_cf(t):
    """The net liability cash flow of projection year t, **income positive**.

    ``premiums + zuzahlungen - claims_death - claims_annuity - claims_survivor - expenses
    - commissions``.  The library-wide sign; :func:`liability_cf` publishes the same stream
    outgo-positive.

    ``expenses`` here does **not** include the commission — the two are separate lines and
    each is subtracted once — and ``av`` is a balance rather than a cash flow and enters
    nothing.  ``prem_total_pp`` enters nothing either: the BUZ premium buys a cover this
    model does not project.

    :func:`check_net_cf` reconstructs this from :func:`result_cf`'s own published columns,
    which is delib's first ruling — the headline number of a cash flow model must not be
    the one quantity nothing checks.
    """
    return (premiums(t) + zuzahlungen(t)
            - claims(t, "DEATH") - claims(t, "ANNUITY") - claims(t, "SURVIVOR")
            - expenses(t) - commissions(t))


def liability_cf(t):
    """The same stream as :func:`net_cf`, outgo positive: ``-net_cf(t)`` exactly.

    The orientation the technical notes print and the one a valuation layer consumes: a
    Solvency II best estimate is ``sum v(t) x liability_cf(t)`` over the relevant risk-free
    term structure, plus a risk margin.  Published as a column beside :func:`net_cf` so
    the sign convention is verifiable in the frame rather than only in prose.  This library
    discounts nothing and computes no reserve.
    """
    return -net_cf(t)


def check_net_cf_resid(t):
    """The cash flow statement's residual in projection year t; zero everywhere.

    Reconstructs ``net_cf(t)`` from :func:`result_cf`'s **own published columns** —

        ``premiums + zuzahlungen - claims_death - claims_annuity - claims_survivor
        - expenses - commissions - net_cf``

    — rather than from the cells that produced them, so a column added to the frame but not
    to :func:`net_cf`, a mis-signed column, or a column whose cells and frame entry have
    drifted apart all leave a residual here.  ``pols_if``, ``pols_paying`` and ``av`` are
    counts and a balance and are excluded from the identity by construction.
    """
    row = result_cf().loc[t]
    return float(row["premiums"] + row["zuzahlungen"]
                 - row["claims_death"] - row["claims_annuity"] - row["claims_survivor"]
                 - row["expenses"] - row["commissions"] - row["net_cf"])


def check_net_cf():
    """True when the published cash flow statement reconciles in every projected year.

    **delib's first ruling**, required of every model in this library: the identity that
    reconstructs ``net_cf(t)`` from the statement's own parts, in code rather than in prose.
    :func:`check_net_cf_resid` gives the signed residual of the year that failed.

    The tolerance is ``roll_fwd_tol`` relative to the largest ``|net_cf|`` in the run, so
    it means the same thing on a 300 € contribution and on a 30 826 € one.
    """
    scale = max([1.0] + [abs(net_cf(t)) for t in range(1, proj_len() + 1)])
    return all(abs(check_net_cf_resid(t)) <= roll_fwd_tol * scale     # noqa: F821
               for t in range(1, proj_len() + 1))


def check_pols_roll_fwd_resid(t):
    """The policy-ledger residual in projection year t; zero everywhere.

    A **non-negative** residual, because it closes two identities at once and a signed sum
    could let them cancel.  The first term says the two ledgers exhaust the in-force
    count; the second and third say the in-force count decrements on **mortality alone**,
    the last of them saying in code that the *Beitragsfreistellung* leaves the total
    untouched::

        |pols_paying(t) + pols_paidup(t) - pols_if(t)|
        |pols_if(t + 1) - pols_if_at(t, "AFT_FREEZE")|
        |pols_if_at(t, "AFT_FREEZE") - pols_if(t) x (1 - mort_rate(t))|

    The second is the one to stare at: ``bf_rate`` does not appear in it.  A
    *Beitragsfreistellung* is a transfer between the ledgers and not an exit, so a model
    that subtracts it from :func:`pols_if` — the second pitfall — fails here, and so does a
    misindexed recursion that rolls forward with ``mort_rate(t + 1)``.
    """
    return (abs(pols_paying(t) + pols_paidup(t) - pols_if(t))
            + abs(pols_if(t + 1) - pols_if_at(t, "AFT_FREEZE"))
            + abs(pols_if_at(t, "AFT_FREEZE") - pols_if(t) * (1.0 - mort_rate(t))))


def check_pols_roll_fwd():
    """True when both policy-ledger identities close in every projected year."""
    scale = max(pols_if_init(), 1.0)
    return all(check_pols_roll_fwd_resid(t) <= roll_fwd_tol * scale  # noqa: F821
               for t in range(1, proj_len() + 1))


def check_av_roll_fwd_resid(t):
    """The *Deckungskapital* residual in projection year t; zero everywhere.

    Before *Rentenbeginn*::

        av_at(t + 1, "BEF_PREM") - av_at(t, "AFT_INT") x (1 - mort_rate(t))

    the fund-level roll-forward on **mortality alone**.  It holds across a
    *Beitragsfreistellung*, because a freeze moves reserve between the two blocks without
    removing any, and it holds whether or not the survivor rider is on, because the reserve
    of a policy terminated by death leaves the fund either way — as a claim where an
    eligible survivor exists, as a mortality profit where none does.  That is the
    arithmetic content of *nicht vererblich*.

    At ``t = ret_t()`` the residual is ``av_at(t, "AFT_INT")``: the conversion empties the
    account, so nothing is credited into it in the conversion year.  After it the residual
    adds ``av(t)`` as well, so a *Deckungskapital* surviving into the *Rentenphase* fails
    here.  A model that collapsed the paying and premium-free blocks into one average
    per-policy reserve fails at the first freeze.
    """
    if t < ret_t():
        return av_at(t + 1, "BEF_PREM") - av_at(t, "AFT_INT") * (1.0 - mort_rate(t))
    if t == ret_t():
        return av_at(t, "AFT_INT")
    return av_at(t, "AFT_INT") + av(t)


def check_av_roll_fwd():
    """True when the *Deckungskapital* rolls forward and is emptied at *Rentenbeginn*."""
    return all(abs(check_av_roll_fwd_resid(t))
               <= roll_fwd_tol * max(1.0, abs(av_at(t, "AFT_INT")),   # noqa: F821
                                     abs(av(t)))
               for t in range(1, proj_len() + 1))


def check_conversion_resid(t):
    """The conversion residual; zero at every t, and non-trivial only at ``ret_t()``.

    Inverts the conversion identity at ``T = ret_t()``::

        ann_pp(T) x pols_if(T) x rf_unit / (rentenfaktor_applied() x ann_freq)
        - fund_at_conv()

    so it catches a factor applied per policy instead of per fund, an ``ann_freq`` of 1
    where the annuity is monthly, and a ``rf_unit`` of 1 000 instead of 10 000.  Zero at
    every other ``t``, which is the second thing it asserts: the fund converts **exactly
    once**, at ``ret_t()``, and there is no second conversion, no partial commutation and
    no re-quotation.

    Vacuously zero for a model point that opens in the *Rentenphase*, where the conversion
    happened before the valuation date.
    """
    if ret_t() < 1 or t != ret_t():
        return 0.0
    if rentenfaktor_applied() <= 0.0:
        return 0.0
    return (ann_pp(t) * pols_if(t) * rf_unit                         # noqa: F821
            / (rentenfaktor_applied() * ann_freq)                    # noqa: F821
            - fund_at_conv())


def check_conversion():
    """True when the whole fund converts exactly once, at *Rentenbeginn*."""
    scale = max(1.0, abs(fund_at_conv()))
    return all(abs(check_conversion_resid(t)) <= roll_fwd_tol * scale  # noqa: F821
               for t in range(1, proj_len() + 1))


def check_no_capital_resid(t):
    """The *nicht kapitalisierbar* residual in projection year t; zero everywhere.

    A **non-negative** residual with two limbs:

    * ``|claims(t, "DEATH")|`` wherever the survivor rider is off (``surv_annuity_rate =
      0``) or ``t >= ret_t()``.  A death before *Rentenbeginn* pays **nothing** in the base
      design, and after *Rentenbeginn* the annuity simply ends; paying anything there is
      the ninth pitfall.
    * ``|claims(t) - claims(t, "DEATH") - claims(t, "ANNUITY") - claims(t, "SURVIVOR")|``,
      which asserts that there is **no fourth kind of payment**.  No surrender value, no
      *Rückkaufswert*, no *Kapitalwahlrecht*, no *Teilkapitalauszahlung*, no
      *Kleinbetragsrenten-Abfindung* and no commutation of a *Rentengarantiezeit* exist on
      this product, so the only things this model can pay are an annuity instalment, a
      guarantee continuation and a survivor's single premium.

    The absence of a ``claims_lapse`` column, a ``cv_pp`` cells and a ``lapse_rate`` cells
    is asserted in the product's own test module, because it is an absence and cannot be
    computed here.
    """
    resid = abs(claims(t) - claims(t, "DEATH") - claims(t, "ANNUITY")
                - claims(t, "SURVIVOR"))
    if float(model_point()["surv_annuity_rate"]) <= 0.0 or t >= ret_t():
        resid += abs(claims(t, "DEATH"))
    return resid


def check_no_capital():
    """True when no payment other than a permitted annuity or survivor benefit is made."""
    scale = max([1.0] + [abs(claims(t)) for t in range(1, proj_len() + 1)])
    return all(check_no_capital_resid(t) <= roll_fwd_tol * scale      # noqa: F821
               for t in range(1, proj_len() + 1))


def check_annuity_roll_fwd_resid(t):
    """The annuity and *Rentengarantiezeit* residual in year t; zero everywhere.

    A **non-negative** residual with three limbs:

    * inside the payout phase, ``|ann_pp(t) - ann_pp(t - 1) x (1 + ann_bonus_rate(t - 1))|``
      — the *Überschussrente* compounds and nothing else touches the annuity once it is
      struck;
    * before it, ``|ann_pp(t)| + |pols_gtd(t)|`` — nothing is in payment before
      *Rentenbeginn*;
    * after ``gtd_end_t()``, ``|pols_gtd(t)|`` — the *Rentengarantiezeit* runs from
      *Rentenbeginn*, not from each death, so every continuation ends on the same date.
    """
    start = max(1, ret_t())
    resid = 0.0
    if t < start:
        resid += abs(ann_pp(t)) + abs(pols_gtd(t))
    elif t > start:
        resid += abs(ann_pp(t) - ann_pp(t - 1) * (1.0 + ann_bonus_rate(t - 1)))
    if t > gtd_end_t():
        resid += abs(pols_gtd(t))
    return resid


def check_annuity_roll_fwd():
    """True when the annuity compounds and the guarantee window closes on time."""
    scale = max(1.0, abs(ann_pp(max(1, ret_t()))))
    return all(check_annuity_roll_fwd_resid(t) <= roll_fwd_tol * scale  # noqa: F821
               for t in range(1, proj_len() + 1))


def result_cf():
    """Result table of cash flows, indexed by projection year t.

    ``pols_if`` is the start-of-year count and the weight applied to every cash flow on the
    same row; ``pols_paying`` is the premium-paying subset and the weight on the two
    premium columns; ``av`` is the *Deckungskapital* at the start of the year, a **balance
    that is reported and not summed**.  Columns 4 and 5 enter ``net_cf`` positively and
    columns 6 to 10 negatively.  ``liability_cf`` is ``net_cf`` outgo-positive.

    ``claims_death`` is structurally zero wherever ``surv_annuity_rate = 0`` and
    ``claims_survivor`` wherever ``guarantee_period_y = 0``; both are published rather than
    dropped, because a column of zeros states the product fact where a missing column
    would only hide it.  There is **no ``claims_lapse`` column and no surrender column of
    any name**: the entitlement is *nicht kapitalisierbar*.

    The frame runs ``t = 1 ... proj_len()`` and stops.  At ``t = proj_len()`` the last
    survivor dies, and there is no tail state, no maturity payment and nothing left to pay.
    """
    ts = list(range(1, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_paying": [pols_paying(t) for t in ts],
            "av": [av(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "zuzahlungen": [zuzahlungen(t) for t in ts],
            "claims_death": [claims(t, "DEATH") for t in ts],
            "claims_annuity": [claims(t, "ANNUITY") for t in ts],
            "claims_survivor": [claims(t, "SURVIVOR") for t in ts],
            "expenses": [expenses(t) for t in ts],
            "commissions": [commissions(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
            "liability_cf": [liability_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_pols():
    """Result table of policy counts, rates and per-policy amounts, indexed by t.

    The companion to :func:`result_cf`: the two policy ledgers and the transfers between
    them, the decrement and crediting rates, the per-policy premium and *Zuzahlung*, the
    *Deckungskapital* of the premium-paying cohort, and the annuity in payment.  It is what
    a reader needs to follow the worked example's independent checks, and it holds nothing
    that :func:`result_cf` also publishes except ``pols_if``.
    """
    ts = list(range(1, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_paidup": [pols_paidup(t) for t in ts],
            "pols_death": [pols_death(t) for t in ts],
            "pols_freeze": [pols_freeze(t) for t in ts],
            "pols_gtd": [pols_gtd(t) for t in ts],
            "mort_rate": [mort_rate(t) for t in ts],
            "bf_rate": [bf_rate(t) for t in ts],
            "cred_rate": [cred_rate(t) for t in ts],
            "prem_pp": [prem_pp(t) for t in ts],
            "zuz_pp": [zuz_pp(t) for t in ts],
            "prem_to_av_pp": [prem_to_av_pp(t) for t in ts],
            "av_pp": [av_pp(t) for t in ts],
            "ann_pp": [ann_pp(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

mort_be_factor = 0.85

elig_surv_prob = 0.55

mort_base_year = 2005

zill_spread_y = 5

rf_unit = 10000.0

ann_freq = 12

roll_fwd_tol = 1e-9

pd = ("Module", "pandas")
