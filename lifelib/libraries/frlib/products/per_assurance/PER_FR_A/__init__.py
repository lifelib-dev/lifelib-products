# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for the French PER individuel assurantiel.

:mod:`~.PER_FR_A` is the executable counterpart of
``products/per_assurance/technical-notes.md`` in the lifelib-products library. It
projects gross best-estimate liability cash flows for single-policy model points on the
composite *plan d'épargne retraite* those notes specify: a compartment-1 PER assurantiel
with a *fonds en euros* support and a *unités de compte* bucket, run on the *gestion
pilotée par horizon* glide path, with an entry loading, separate euro and UC management
charges, an arbitrage charge on the annual rebalancing, a *garantie plancher* death
floor, and a settlement at the declared horizon split between *capital* and *rente
viagère*.

**Accumulation with a two-way exit.** That sentence is the product. The plan is
**blocked** until the L. 224-1 maturity, so there is no surrender right and no
``lapse_rate`` anywhere in this model. What leaves the book instead are two distinct
statutory exits, and they are not the same thing: a *déblocage anticipé* under one of the
seven L. 224-4 cases, which pays the **whole** account value and bears no charge, and a
**transfer out** to another PER, which pays a transfer value net of a 1% indemnity for
the first five years from the first *versement*. Modelling either as a lapse, or both
with one decrement, attaches the wrong payment formula to half the exits.

**Spaces.** The model contains two:

:mod:`~.PER_FR_A.Data`
    Reads the five input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.PER_FR_A.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its ``data``
    Reference, which resolves to the single :mod:`~.PER_FR_A.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized, every
``Projection[N]`` is a separate ItemSpace with its own cells cache; readers placed there
would re-read every file for every policy. In ``Data`` they are evaluated once, however
many policies are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run time
rather than stored inside the model. The model folder itself holds no data, so the model
and its inputs must travel together.

**The glide path is an input table, not a formula.** ``allocation_grid.csv`` is keyed by
(*allocation_profile*, *years_to_horizon*) and gives the target euro share, so the four
regulatory profiles, and any insurer ladder finer than the four regulatory bands, are a
table edit rather than a code change. That is the product's dominant financial lever and
it is the one thing a reader of this model will want to change first.

**Projection basis.** Annual steps, because the governing cycles are annual: euro-fund
crediting at 31 December and the annual statement. ``t`` counts **plan years** from the
valuation date, 1-based, and ``proj_len()`` is the declared horizon,
``retirement_age - age(0)``. Within a year the *versement* arrives and the balance is
rebalanced to the glide-path target at the start; investment return accrues over the
year; the management charge is taken on the post-crediting balance; the decrements
death, early release and transfer out fall at the end, in that order; and at
``t = proj_len()`` the survivors settle.

**What is sourced and what is not.** The mechanics are sourced: the *blocage* and the
seven early-release cases, the 1%/five-year transfer indemnity, the 0% maximum technical
rate, the regulatory de-risking grid, the euro capital floor stated net of loading and
net of charges, death closing the plan, the exit menu and the compartment-3 annuity-only
rule, and the €110 monthly commutation threshold. Every **rate** is a standardization:
the charge levels are contractual *maxima* rather than levels, no insurer publishes an
annuity rate card, TH 00-02 / TF 00-02 and TGH05 / TGF05 are cited but not shipped, and
no public French experience exists for PER early-release, transfer or annuitisation
behaviour. **This model is a mechanics demonstration, not a pricing or reserving
result.**

**Where the annuity goes.** A liquidating plan that does not commute hands
``annuity_conversion`` to ``Rente_FR_S``, and the annuity's own reserve, its 0.80% p.a.
charge, reversion, *annuités garanties* and revaluation are specified in
``products/rente_viagere/technical-notes.md``. This model commutes to a stated amount and
records what it hands over; it does not re-implement the payout chassis.

**Verification.** ``tests/test_per_assurance_fr.py`` asserts the notes' worked example
row by row to the cent — the glide-path band crossings, the arbitrage charge and which
support pays it, the two supports' crediting and charging, the *garantie plancher* base,
the three decrements, and the settlement with its commutation identity.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/per_assurance/PER_FR_A")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "PER_FR_A"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]
