# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for French eurocroissance business.

:mod:`~.EC_FR_A` is the executable counterpart of
``products/eurocroissance/technical-notes.md`` in the lifelib-products library. It
projects gross best-estimate liability cash flows for single-policy model points on the
two composite chassis those notes specify — **Chassis A**, the 1° engagement carrying a
*provision mathématique* alongside *parts de provision de diversification*, and
**Chassis B**, the 2° engagement carrying parts only with a capital guarantee that bites
at the *échéance* and nowhere before it.

**Two provisions, two state variables, and one rebalancing a year.** That sentence is
the model. The *provision mathématique* is the guaranteed amount discounted at the
A. 134-1 rate; the *provision de diversification* takes whatever the account's assets
leave over, floored at the parts' minimum value. Neither is a cash flow. The policy's
cash flows are *versements* in and surrender, death and maturity claims out; the two
provisions reach them only through the R. 134-5 surrender and R. 134-6 maturity
formulas.

**The provision mathématique is re-struck, never accumulated.** ``pm(t)`` is ``mg(t)``
discounted at the *current* ``i_pm(t)``, so it lands on the guarantee exactly at the
*échéance* whatever the path of rates: ``pm(n) = mg(n)`` identically. That is what makes
the Chassis A guarantee pre-funded by construction, and it is why an in-force model point
carries no accumulated PM — the model re-derives it, and
``Projection.check_pm_restruck`` asserts the shipped extract agrees.

**The Chassis B surrender value is not guaranteed.** Before the *échéance* a 2°
engagement pays ``parts × part value`` and nothing else. On the notes' year-6 shock that
is 9,899.22 against a guarantee of 11,760.00 — 84.18% of net *versements*. A model that
floors it is modelling a contract that does not exist, and that is this product's central
error.

**The insurer's own funds never reach a policyholder before the term.** The L. 134-3
contribution completing the representation and the *provision pour garantie à terme* are
computed, reported and kept out of every benefit column;
``Projection.check_own_funds_not_paid`` asserts it.

**Spaces.** The model contains two:

:mod:`~.EC_FR_A.Data`
    Reads the five input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.EC_FR_A.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its
    ``data`` Reference, which resolves to the single :mod:`~.EC_FR_A.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized,
every ``Projection[N]`` is a separate ItemSpace with its own cells cache; readers
placed there would re-read every file for every policy. In ``Data`` they are evaluated
once, however many policies are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run
time rather than stored inside the model. The model folder itself holds no data, so
the model and its inputs must travel together.

**Projection basis.** Annual steps, because the governing discretion cycle — the
striking of the *compte de participation aux résultats* and the allocation of its
balance — is annual under R. 134-4. ``t`` counts policy years from issue and starts at
``t = 0``, the issue point, where the initial *versement* creates the rights. Charges in
number of parts and scheduled *versements* fall at the start of the year; the asset
return accrues over it; the performance levy, the re-striking of both provisions, the
insurer's asset affectations and any free *versement* fall at the end, in that order;
decrements and claims follow. Age is *âge atteint*.

**What the annual grid cannot say.** A. 134-5 requires the diversification provision to
be re-struck at an intermediate value **at least monthly** and prices an exit on a
*forward* part value — the next striking after the request. An annual grid compresses
that to one striking a year and prices exits on the year-end value. That is a documented
simplification, not an equivalence.

**What is sourced and what is not.** The mechanics are sourced, and unusually completely
so: eurocroissance is a statutory construct, and arts. L. 134-1 to L. 134-5,
R. 134-1 to R. 134-12 and A. 134-1 to A. 134-7 of the Code des assurances fix the
provision definitions, the six permitted charge bases, the surrender and maturity values,
the minimum part value, the 90%-of-TEC discount ceiling and the PGT. Every *rate* is a
standardization: no *notice d'information*, *conditions générales* or PRIIPs *document
d'information clé* for any eurocroissance support was retrieved, the regulatory mortality
tables are cited but never shipped, and no eurocroissance lapse experience is public.
**This model is a mechanics demonstration, not a pricing or reserving result.**

**Verification.** ``tests/test_eurocroissance_fr.py`` asserts both chassis of the notes'
worked example row by row to the cent — the asset roll, the parts levy and its base, the
performance levy, the re-strike of the PM and its rate/time decomposition, the minimum
part value, the insurer's contribution, the PGT, the year-3 *versement* split, and every
exit value the two chassis pay.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/eurocroissance/EC_FR_A")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "EC_FR_A"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]
