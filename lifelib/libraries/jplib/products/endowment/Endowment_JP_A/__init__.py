# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for Japanese endowment and education assurance.

:mod:`~.Endowment_JP_A` is the executable counterpart of
``products/endowment/technical-notes.md`` in the lifelib-products library. It projects
gross best-estimate liability cash flows for a single-policy model point of the
standardized composite in its two cells:

**endowment** (養老保険, *yōrō hoken*)
    a finite term with a maturity benefit 満期保険金 (*manki hokenkin*) equal to the death
    benefit, so the policy value converges on the sum assured by construction.

**education** (学資保険, *gakushi hoken*)
    a staged 学資金 (*gakushikin*, education money) schedule read from a table, a death
    payment that is a return of premiums rather than a sum assured, and 保険料払込免除
    (*hokenryō haraikomi menjo*, waiver of premium) on the 契約者 (*keiyakusha*,
    policyholder) — **a second decrement on a second life who is not the insured**. That
    last has no analogue in the U.S. or UK reference models.

The structural difference from a whole life chassis is that there is **no tail and no
terminal age**: the projection length is exactly the term, every state closes at the end
of the last period, and the closing cash flow is a certain payment of the sum assured to
the survivors rather than a decrement. Importing a terminal age here would project a
contract that has already matured.

**Spaces.** The model contains two:

:mod:`~.Endowment_JP_A.Data`
    Reads the four input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.Endowment_JP_A.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its ``data``
    Reference, which resolves to the single :mod:`~.Endowment_JP_A.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized, every
``Projection[N]`` is a separate ItemSpace with its own cells cache; readers placed there
would re-read every file for every policy. In ``Data`` they are evaluated once, however
many policies are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run
time rather than stored inside the model. The model folder itself holds no data, so the
model and its inputs must travel together.

**Projection basis.** Annual steps on policy years running anniversary to anniversary.
The period index ``t`` is **0-based**: ``t = 0`` is the first policy year and
``t = proj_len() - 1`` the last, where ``proj_len() = policy_term()`` is the number of
projected years, so the frame is ``range(proj_len())`` and the contractual policy year is
the 1-based label ``t + 1``. A second index, ``k``, counts anniversaries with ``k = 0`` at
issue: period ``t`` runs from anniversary ``t`` to anniversary ``t + 1``, and the
per-policy value construction (``pol_val_pp``, ``cv_pp``, ``surr_charge_pp``,
``benefit_pct``, ``prem_cum_pp``) is indexed by ``k``, so the flows of period ``t`` read
it at ``t + 1``.
Premium, maintenance expense and renewal commission fall at the start of the period;
acquisition expense and initial commission at issue; death claims and claim expense at
the end of the period of death; the staged benefit and the maturity benefit at the
end of the period, to policies surviving that period's mortality; surrenders at the
end of the period, after deaths and after any staged benefit due at that anniversary,
valued on the surrender value net of that benefit.

**What is sourced and what is not.** Both annual premiums on the two anchor cells are
12 times a published monthly premium for exactly those cells [S9][S11], and the 予定利率
(assumed interest rate) of 1.00% that the cash-value construction runs on is published
by product group before and after a dated revision [S9]. Everything else quantitative is
a standardization introduced for the reference implementation: no carrier publishes a
surrender-value formula or a numeric surrender-value table for either cell, no carrier
publishes an expense basis, and no carrier publishes a lapse curve by duration. The
mortality tables shipped in ``mort_table.csv`` are a **[std] construction** anchored so
that the model reproduces the rates the technical notes quote; the 日本アクチュアリー会
(Institute of Actuaries of Japan) tables they point at are cited by URL and never
reproduced, because the publisher's site terms prohibit it. **This model is a mechanics
demonstration, not a pricing or reserving result.** Replace the assumption tables and
the cash-value basis with a company 算出方法書 before drawing any conclusion from the
output.

**Model points.** Nine, covering both cells, both staged-schedule shapes, the waiver in
both positions of its carve-out switch, a suppressed lapse rate on the waived state, a
loaded mortality basis, a shortened premium term, the automatic premium loan module and
a drawn policy loan. Model point 1 is the anchor cell of the worked example in the
technical notes; model point 2 is the education cell of the same worked example.

**Verification.** ``tests/test_endowment_jp.py`` asserts the notes' worked example to
the yen and the in-force columns to six decimals on both anchor cells, together with the
roll-forward identities exposed as ``check_*()`` cells.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/endowment/Endowment_JP_A")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "Endowment_JP_A"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]
