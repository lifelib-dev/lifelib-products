# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for the German klassische Riester-Rentenversicherung.

:mod:`~.Riester_DE_A` is the executable counterpart of
``products/riester_rente/technical-notes.md`` in the lifelib-products delib library. It
projects gross best-estimate liability cash flows, undiscounted, for a single-policy
model point of a **certified Altersvorsorgevertrag under the AltZertG** — Schicht 2 of
the German pension system — on an **annual** grid, through both phases of the contract:
the accumulation of a *Deckungskapital* with *Überschussbeteiligung*, and the lifelong
*Leibrente* the capital is converted into at *Rentenbeginn*.

Three things make this the Riester model rather than a translated Schicht-3 one.

**The state pays part of the premium, and it is a cash flow.** The *Zulage* is a
contribution paid by the *Zentrale Zulagenstelle für Altersvermögen* to the provider and
credited to the contract; it is not a benefit and it is not a tax refund. It is published
in its own ``zulagen`` column beside ``premiums``, never folded into it, because a
statement that folds the two cannot answer the one question this product is about. The
entitlement is driven by two **different** lags — the *Mindesteigenbeitrag* looks back one
*calendar* year for income, the cash arrives one *projection* year late — and collapsing
them into one is the first listed modeling pitfall.

**There is a 100 % Beitragsgarantie, and it is tested exactly once.** ``guar_pp(t)``
accumulates every *Altersvorsorgebeitrag* credited — the saver's own contribution, the
Zulagen, and any unsubsidised contribution above the § 10a ceiling — less the biometric
carve-out capped at 20 % of total contributions. It is compared with the account **only**
at *Rentenbeginn*, where ``garantieluecke_conv_pp()`` is the shortfall the insurer funds.
``garantieluecke_pp(t)`` is published for every ``t`` as a **diagnostic**: it is normally
positive in the early durations of any charged contract, and flooring a death, surrender
or transfer benefit at it is a modeling error, not prudence.

**The payout phase is part of the liability.** Conversion at ``t_conv()`` strikes the
capital, the *Schlussüberschussanteil*, the *Bewertungsreserven* share and the applied
*Rentenfaktor*, elects the *Teilkapitalauszahlung* of up to 30 %, and applies the
*Kleinbetragsrente* test — which is **computed rather than assumed**, so the commutation
rate on a book is an output. The annuity then runs on a **generational** second-order
annuitant basis to ``omega_age``, with the *Rentengarantiezeit* changing who is paid and
never how much.

**Spaces.** The model contains two:

:mod:`~.Riester_DE_A.Data`
    Reads the eight input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.Riester_DE_A.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1, the worked example's anchor cell. It reaches the
    input tables through its ``data`` Reference, which resolves to the single
    :mod:`~.Riester_DE_A.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized, every
``Projection[N]`` is a separate ItemSpace with its own cells cache; readers placed there
would re-read every file for every policy. In ``Data`` they are evaluated once, however
many policies are projected.

Input data is **external**: plain CSVs in the model folder's parent directory, read at
run time rather than stored inside the model. The model folder itself holds no data — no
``_data/``, no IOSpec, no embedded values — so a diff of the model shows logic changes
only, and the model and its inputs must travel together.

**Projection basis.** Annual steps, 1-based, which is the contract's own grid in every
respect that matters: the Zulage is an annual entitlement determined on a calendar year,
the *Überschuss* is declared annually, and the *Beitragsgarantie* is tested once. Policy
year ``t`` runs ``1 ... proj_len()``, with ``proj_len() = omega_age - age(1) + 1`` and
``t = 1`` opening at the 1 January 2027 valuation date. The one genuinely sub-annual
element, the monthly *Leibrente*, is compressed to one annual payment at the start of the
payout year; the *level* of the annuity is still right, because the conversion factor
carries the Woolhouse ``-11/24`` correction. ``products/sofortrente/`` runs monthly for
exactly that reason.

**What is sourced and what is not.** The statutory mechanics are cited: who is
*zulageberechtigt*, the *Grundzulage* / *Kinderzulage* / *Berufseinsteiger-Bonus*
structure, the § 86 *Mindesteigenbeitrag* with its 4 % rate, its 2 100 € ceiling, its
60 € *Sockelbeitrag* floor and its **proportional** Kürzung, the ZfA payment lag, the
*Beitragserhaltungszusage*, the 30 % *Teilkapitalauszahlung* cap, the five-year floor on
acquisition-cost spreading, the *Wechselrecht*, the *Kleinbetragsrenten-Abfindung* and
the *schädliche Verwendung* consequences of a *Kündigung*. **No carrier-specific
parameter was established for any German Riester product, at any house, for any year**,
so every charge, every declared rate, every *Rentenfaktor*, every behavioural rate and
both decrement tables are standardizations marked ``[std]`` in the shipped CSVs and in
the notes. The DAV tables (DAV 2008 T, DAV 2004 R) are the property of the Deutsche
Aktuarvereinigung, are not public and are **not redistributed here**: they are cited by
name and stood in for by anchored proxies, and :mod:`~.Riester_DE_A.Data` says what a
replacement must preserve. **This model is a mechanics demonstration, not a pricing or
reserving result.** Replace the decrement, charge and surplus tables with company data
before drawing any conclusion from the output.

**Model points.** Thirteen, covering both contribution forms, all four payment
frequencies, an at-inception point beside the in-force ones, both *Kinderzulage* rates
running at once, the *Sockelbeitrag* floor, the *Berufseinsteiger-Bonus*, the § 86
proportional Kürzung, an unsubsidised second contribution pool, the 20 % biometric
carve-out cap, a *Beitragsfreistellung*, a stressed declared rate on which the
*Garantielücke* binds, a pure lifelong annuity with no lump sum and no guarantee period,
and a late entrant at the statutory earliest *Rentenbeginn* of 62. Model point 1 is the
anchor cell of the worked example in the technical notes.

**Verification.** ``tests/test_riester_rente_de.py`` asserts the notes' worked example to
the cent and ``pols_if`` to six decimals, and one test per listed modeling pitfall. The
model publishes six ``check_*`` identities — ``check_net_cf``, ``check_av_roll_fwd``,
``check_guar_roll_fwd``, ``check_pols_roll_fwd``, ``check_conversion`` and
``check_zulage_lag`` — and the library's conventions suite calls all six on every model
point.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/riester_rente/Riester_DE_A")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "Riester_DE_A"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]
