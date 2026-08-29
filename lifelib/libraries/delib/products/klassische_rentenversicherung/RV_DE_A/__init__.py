# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for the klassische aufgeschobene private Rentenversicherung.

:mod:`~.RV_DE_A` is the executable counterpart of
``products/klassische_rentenversicherung/technical-notes.md`` in the lifelib-products
library. It projects gross best-estimate liability cash flows, undiscounted, for a
single-policy model point of the German Schicht-3 deferred annuity written on the general
account — premiums accumulate in the *Deckungskapital* at the contract's own
*Rechnungszins* with a declared *Überschussbeteiligung* beside it, and at the
*Rentenbeginn* the accumulated capital converts at a *Rentenfaktor* into a lifelong
monthly *Leibrente* or is taken as a lump sum under the *Kapitalwahlrecht*. The grid is
**annual**, which is the contract's own period: the *Rechnungszins* is credited per
*Versicherungsjahr*, the surplus is declared per calendar year, and both *Kündigung* and
*Beitragsfreistellung* take effect "for the end of the current insurance period".

Four things make this the German deferred-annuity model rather than a translated
endowment.

**The declared rate contains the guarantee; it does not sit on top of it.** The *laufende
Verzinsung* is the *Garantieverzinsung* plus the *laufende Zinsüberschussbeteiligung*, so
``bonus_rate(t) = max(0, decl_rate(t) - int_rate_guar())`` and the two credits together
deliver the declared rate and never more. On the anchor cell that is 1,00 % guaranteed
plus 1,55 % surplus against a 2,55 % declaration. On model point 6, a 2,75 % legacy
vintage against the same declaration, ``bonus_rate`` is **zero at every t** while interest
is still credited at 2,75 % — a real German result and the first listed modeling pitfall,
not an artefact. ``check_av_roll_fwd()`` and ``check_av_sur_roll_fwd()`` keep the two
accounts honest about which credit went where.

**The *Rechnungszins* is a model-point attribute, not a global assumption.** A German life
book is a layered stack of guarantee vintages: the rate a contract was written on stays
with it for its whole life, so points 1, 6 and 14 credit 1,00 %, 2,75 % and 0,90 % in the
same run, from the same tables. Anything that reads a single interest rate off the model
has misunderstood the product.

**The conversion is an option the insurer wrote.** At the *Rentenbeginn* the applied
*Rentenfaktor* is ``max(garantierter, aktueller)`` — the factor fixed at inception against
the one the carrier is applying to immediate annuities at that date — and the higher of
the two is then guaranteed for the whole payment period. On the anchor cell the current
factor wins at 32,00 € against a guaranteed 28,00 €; on point 13 the guarantee binds over
a *low* scenario. A model applying the guaranteed factor alone understates the anchor's
annuity by 12,5 %. ``check_annuity_conv()`` asserts the rule and the guaranteed-contract-
value floor beside it.

**The *Rentengarantiezeit* is paid to the dead.** Inside the guarantee window the
instalment is due whether or not the annuitant is alive, so the annuity is weighted by the
**annuitised** count and not by survivors: ``pols_annuity(t) = max(pols_if(t),
1{n < t <= n+m} pols_annuitization(n))``, asserted by ``check_annuity_guarantee()`` on
every model point.

**Spaces.** The model contains two:

:mod:`~.RV_DE_A.Data`
    Reads the eight input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.RV_DE_A.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its ``data``
    Reference, which resolves to the single :mod:`~.RV_DE_A.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized, every
``Projection[N]`` is a separate ItemSpace with its own cells cache; readers placed there
would re-read every file for every policy. In ``Data`` they are evaluated once, however
many policies are projected.

Input data is **external**: plain CSVs in the model folder's parent directory, read at run
time rather than stored inside the model. The model folder itself holds no data — no
``_data/``, no IOSpec, no embedded values — so the model and its inputs must travel
together. This follows ``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``,
which keeps its inputs inside the model.

**Projection basis.** Annual steps. ``t`` counts **policy years** from inception, 1-based:
policy year ``t`` runs from the anniversary at attained age ``issue_age + t - 1`` to the
next, and the calendar year of the row is ``issue_year + t - 1`` for every point in the
table, which is what lets one generational mortality surface and one declared-rate path
serve a book of mixed vintages. A new-business point opens at ``t = 1``; an in-force point
that has already run ``duration_init`` complete policy years opens at
``t = duration_init + 1`` carrying its balances on the model point. ``proj_len() =
omega_age() - issue_age`` is the **last** projected policy year, so a life annuity is
projected to exhaustion rather than truncated at a fixed horizon — on the anchor cell,
``t = 1 ... 71``. The *Rentenbeginn* falls at the end of policy year ``n = aufschub_y``:
accumulation rows are ``t <= n``, payout rows ``t > n``, the *Kapitalabfindung* is paid in
row ``n`` and the first annuity instalment in row ``n + 1``.

**What is sourced and what is not.** The contractual mechanics are sourced: the
*Deckungskapital* as the premium net of risk and expense cover accumulated at the
*Rechnungszins*; the *Höchstzillmersatz* of 25 ‰ from 2015 and 40 ‰ before; the § 169
Abs. 3 surrender floor that spreads acquisition costs over five years; the § 169 Abs. 5
*Stornoabzug* conditions; the § 165 paid-up rule and its minimum-benefit branch; the three
death-benefit designs; the conversion rule and the ``max(guaranteed, current)``
*Rentenfaktor*; the *Bewertungsreserven* crystallisation at the transition to annuity
payment; and the *Rentengarantiezeit*. **Every level is a standardization.** No
*Rentenfaktor*, no declared surplus rate, no charge parameter, no expense and no
behavioural rate was established for this product at any German carrier for any year, and
the DAV tables (DAV 2004 R here) are the property of the Deutsche Aktuarvereinigung, are
not public and are cited by name rather than redistributed. **This model is a mechanics
demonstration, not a pricing or reserving result.** Replace the decrement, charge and rate
tables with company data before drawing any conclusion from the output.

**Model points.** Fourteen, covering both premium forms, all four payment frequencies, two
in-force cells on two legacy guarantee vintages, both charge sets, all three death-benefit
forms with and without the surplus account, all three payout systems, five
*Rentengarantiezeit* durations including zero, *Kapitalwahlrecht* take-ups of 0 %, 20 %,
30 % and 100 %, the *Dynamik*, both statutory *Beitragsfreistellung* branches, and the
boundary cases: the paid-up conversion that fails the *Mindestversicherungsleistung* and
is cashed out (8), full commutation at *Rentenbeginn* (9), and the guaranteed
*Rentenfaktor* binding over a lower current one together with a binding
``guar_capital_pp`` (13). Model point 1 is the anchor cell of the worked example in the
technical notes.

**Verification.** ``tests/test_klassische_rentenversicherung_de.py`` asserts the notes'
worked example to the cent and ``pols_if`` to six decimals, and one test per listed
modeling pitfall. Nine ``check_*`` identities travel with the model itself and are called
on every model point by ``tests/test_model_conventions_de.py``.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/klassische_rentenversicherung/RV_DE_A")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "RV_DE_A"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]
