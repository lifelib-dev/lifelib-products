# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for the French euro support (fonds en euros).

:mod:`~.Euro_FR_A` is the executable counterpart of
``products/assurance_vie_euro/technical-notes.md`` in the lifelib-products library. It
projects gross best-estimate liability cash flows for single model points on the euro
support of a `contrat d'assurance vie` — the standardized composite specified in
``product-spec.md``, not any single insurer's fund — together with the two state
variables that make the product what it is: the `épargne acquise` and the `provision
pour participation aux bénéfices` (PPB).

**The rate is an allocation, not an assumption.** That sentence is the model. Every
year the insurer builds the `compte de participation aux résultats` that art. A132-11
of the Code des assurances prescribes — 85% of the `compte financier`, plus the
`compte technique` less the greater of 10% of it and 4.5% of premiums — and the whole
of that balance must reach policyholders. What the insurer chooses is only *when*: what
it does not credit this year is carried to the PPB, and what it carried in an earlier
year it may credit now. The credited rate `taux servi` is therefore the statutory floor
moved up or down by the PPB lever, floored again by the `taux minimum garanti`, and
never by an assumption typed into a table.

**The eight-year clock is a deadline, not an average.** A dotation carried to the PPB in
financial year ``v`` must be applied to mathematical provisions or paid to policyholders
within the eight financial years that follow. The model therefore carries a **per-vintage
ledger**, ``ppb_vintage_pp(t, v)``, released oldest-first, so that the clock is a real
date on a real balance. Modelling the PPB as a single pot with an average age would meet
the eight-year rule on average and breach it on every vintage.

**The `effet cliquet` is asserted, not assumed.** Credited `participation aux bénéfices`
is definitively acquired and cannot be called back, so ``check_cliquet()`` asserts that
the credited interest is never negative and that the cumulative-PB ledger never falls.
What the ratchet does *not* say is that the account never falls: under the `garantie
nette` the `frais de gestion sur encours` keeps biting in a nil-PB year, and both
statements are true at once.

**Spaces.** The model contains two:

:mod:`~.Euro_FR_A.Data`
    Reads the four input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.Euro_FR_A.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1, the notes' worked example. It reaches the input
    tables through its ``data`` Reference, which resolves to the single
    :mod:`~.Euro_FR_A.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized,
every ``Projection[N]`` is a separate ItemSpace with its own cells cache; readers placed
there would re-read every file for every policy. In ``Data`` they are evaluated once,
however many policies are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run
time rather than stored inside the model. The model folder itself holds no data, so
the model and its inputs must travel together.

**Projection basis.** Annual steps, because the `participation aux bénéfices` is fixed
for the closing financial year and credited at 31 December value date, and because the
art. A132-16 clock counts financial years. `Versements` and `rachats partiels` are spread
evenly through the year and enter the crediting base at weight 0.5; the revalorisation
and the management charge land at 31 December; decrements act at 31 December **after**
crediting, so an exiting policy takes the full year's `taux servi`. Age is age last
birthday. ``t`` counts policy years from the valuation date, 1-based.

**`Prélèvements sociaux` are inside the account and outside ``net_cf``.** The 17.2% levy
is withheld as the interest is credited, every year, because the rights are expressed in
euros — this is the euro fund's signature mechanic and the commonest foreign-model
error. It sits inside the account roll-forward, because it is money that genuinely
leaves the contract; it sits outside ``net_cf``, because it is a policyholder tax the
insurer remits to the State rather than a benefit or an insurer expense. It has its own
``soc_levy`` column so a fund-level asset projection can add it back in one step.

**What is sourced and what is not.** The mechanics are sourced: the A132-11 split and
which limb attaches to which account, the A132-12 minimum benefit, the eight-year PPB
release horizon, the `effet cliquet`, the `garantie nette` capital floor and its
measurement before levies, the death benefit being the account value and nothing more,
the absence of a surrender charge, and the annual timing of the social levies. Every
*rate* is a standardization: no insurer publishes its dotation or release policy, no
French euro-fund lapse experience is public, no contract in the source set publishes a
TMG, and the statutory mortality tables are cited but not redistributable — the shipped
table is an INSEE-shaped proxy. **This model is a mechanics demonstration, not a pricing
or reserving result.**

**Verification.** ``tests/test_assurance_vie_euro_fr.py`` asserts the notes' worked
example row by row to the cent — the `taux servi` and PPB table, the `épargne acquise`
roll-forward, the year-6 trace at full precision, the twelve-year levy and account
identities, and the PPB clock closing exactly at its last date — and then one test per
modelling pitfall the notes list.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/assurance_vie_euro/Euro_FR_A")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "Euro_FR_A"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]
