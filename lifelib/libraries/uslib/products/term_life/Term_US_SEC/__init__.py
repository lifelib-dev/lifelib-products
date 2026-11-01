# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""In-force reference liability cash flow model for U.S. level premium term life insurance.

:mod:`~.Term_US_SEC` projects the policy :mod:`~.Term_US_S` projects — a single-life,
fully underwritten level premium term policy: level premiums for the level period, then
Jump-to-ART renewal at unchanged face amount to expiry at attained age 95, convertible to
permanent cover before ``min(end of level period, attained age 70)``, with no cash value —
from a **valuation date** rather than from issue. A model point may be a policy already
in force at that date, one issued at it, or one to be issued in the ten years after it,
as in lifelib's ``basiclife/BasicTerm_SE``, which extends ``basiclife/BasicTerm_S`` the
same way. Its formulas are the executable counterpart of
``products/term_life/technical-notes.md``, and ``products/term_life/model-sec.md``
explains what running in force changes.

**Spaces.** The model contains two:

:mod:`~.Term_US_SEC.Data`
    Reads the four assumption CSVs it shares with :mod:`~.Term_US_S` and its own model
    point table, and holds their filename References. It takes no parameters, so each
    file is read **once per model**.

:mod:`~.Term_US_SEC.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its
    ``data`` Reference, which resolves to the single :mod:`~.Term_US_SEC.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized,
every ``Projection[N]`` is a separate ItemSpace with its own cells cache; readers
placed there would re-read every file for every policy. In ``Data`` they are evaluated
once, however many policies are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run
time rather than stored inside the model. The model folder itself holds no data, so
the model and its inputs must travel together.

**Projection basis.** Monthly steps on two clocks. ``t`` counts months from the
valuation date, 0-based, as ``basiclife/BasicTerm_SE`` counts them: ``t = 0`` is the
valuation month for every model point, however old the policy, and the frame runs
``t = 0, 1, ..., proj_len() - 1``, where ``proj_len()`` counts the months from the
valuation date to expiry at attained age 95. ``duration_mth(t)`` counts the months the
policy has been in force, ``duration_mth_init() + t`` from the model point's
``duration_mth`` at ``t = 0``, and the contract runs on it: the completed policy years
are ``duration(t) = duration_mth(t) // 12``, the contractual 1-based label is
``policy_year(t) = duration(t) + 1``, and the attained age is
``age_at_entry() + duration(t)``. Everything contractual about the product is annual —
the guaranteed premium schedule, the ART renewals, the shock lapse — so the policy year
is the lookup key. Expense inflation alone runs on ``t``, so the maintenance charge is in
valuation-date dollars; acquisition, a flat amount per policy issued, is not inflated,
as in ``basiclife/BasicTerm_SE``. On a point issued at ``t = 0`` the two clocks
coincide, and the model computes what :mod:`~.Term_US_S` computes, except that
acquisition is charged per policy issued rather than once per model point, and that
``pols_if_init()`` is the count already in force at the valuation date, 0 for such a
point, whose policies enter as new business at ``t = 0``.

Decrements follow suit in two speeds. ``mort_rate(t)`` and ``lapse_rate(t)`` are the
**annual** rates of the policy year containing month ``t`` — the vectors the technical
notes tabulate — and ``mort_rate_mth(t)`` and ``lapse_rate_mth(t)`` are the monthly
rates actually applied, ``1 - (1 - q)^(1/12)``. The shock lapse is the documented
exception: it is not spread but falls in full at the end of the final level-period
month, the policy's month ``12n - 1``, immediately before the first ART premium is due.

Because the ordinary rates compound back to the annual ones and the shock sits on a
year boundary, the in-force **at every policy anniversary** is exactly what an
annual-step model would carry. The cash flows are not, and are not meant to be:
claims fall at the end of the month of death, maintenance expense accrues monthly, and
a modal premium is collected when it is contractually due — which is what the finer
grid is for. ``result_cf_annual()`` sums the frame into policy years so the two can be
read side by side, and ``result_pols()`` sets out the counts: in force, new business
and each decrement, month by month.

**What is sourced and what is not.** The contractual elements are taken from a
specimen policy: the guaranteed premium schedule, the $65 policy fee inside it, the
modal factors and expiry at attained age 95. Everything behavioural and
expense-related — mortality, lapse, the shock lapse, post-level-term mortality
deterioration, conversion, commission, expenses and premium tax — is a standardization
introduced for the reference implementation, because no public source carries it.
**This model is a mechanics demonstration, not a pricing or reserving result.**
Replace the assumption tables with company data before drawing any conclusion from the
output.

**Model points.** ``model_point_table_sec.csv`` is generated from :mod:`~.Term_US_S`
and its model point table, and the tests regenerate it and compare, so no row is typed
by hand. Points 1 and 2 are the twins of :mod:`~.Term_US_S`'s two points, issued at the
valuation date. Points 3 to 5 are S points restated in force at S months 12, 126 and
719 — on an anniversary in the level period, midway through the first ART year, and in
the last month of cover — each opened with the count S carries into that month. Point 6
is the anchor cell issued three months after the valuation date. All six use the anchor
configuration T10 / M / StdNT / band 1 / annual mode, because the specimen gives a
guaranteed premium scale for that cell alone. A model point on any other plan, sex,
class or band requires ``premium_rates.csv`` to be extended first.

**Verification.** On the two twins every cell this model shares with
:mod:`~.Term_US_S` agrees with it at every argument the S model evaluates in its sweep,
``pols_if_init`` and ``model_point`` excepted, so the worked example
``tests/test_term_life_us.py`` asserts — money to the cent, in-force to six decimals —
holds here too, with no number restated. ``tests/test_term_life_us_sec.py`` splices: an
S point restated in force at month ``d`` continues the S projection from ``d`` on, cell
by cell, at months around the shock, the first ART premium and the last month of
cover. It splices S's two points, and three variants of them in a copy of S's table,
never committed, that reach what S's own points cannot: a conversion window closed by
attained age 70, the other three premium modes, a 20-year level period, and cover that
ends with the level period. And a point issued ``k`` months late is the S projection
``k`` months on.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/term_life/Term_US_SEC")
    >>> model.Projection[4].result_cf()
    >>> model.Projection[4].result_pols()
"""

from modelx.serialize.jsonvalues import *

_name = "Term_US_SEC"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]
