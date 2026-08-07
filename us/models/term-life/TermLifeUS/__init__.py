# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for U.S. level premium term life insurance.

:mod:`~TermLifeUS` is the executable counterpart of
``us/products/term-life/technical-notes.md`` in the lifelib-products library. It
projects gross liability cash flows for a single-life, fully underwritten level
premium term policy: level premiums for the level period, then Jump-to-ART renewal at
unchanged face amount to expiry at attained age 95, convertible to permanent cover
before ``min(end of level period, attained age 70)``, with no cash value.

The model contains one Space, :mod:`~TermLifeUS.Projection`, which holds all the
formulas and data.

**Projection basis.** Annual steps. Policy year ``t`` runs 1, 2, ..., ``proj_len()``,
where ``proj_len() = 95 - age_at_entry()``. Premiums, commission, premium tax and
expenses fall at the beginning of the year; death claims and the conversion credit at
the end; lapses and conversions act on end-of-year survivors. Note the contrast with
lifelib's ``BasicTerm_S``, where ``t`` counts **months** — here it counts **years**,
because every decrement in this product is on an annual cycle and there is no account
value requiring monthiversary processing. The technical notes describe an optional
monthly mode; it is not implemented.

**What is sourced and what is not.** The contractual elements are taken from a
specimen policy: the guaranteed premium schedule, the $65 policy fee inside it, and
expiry at attained age 95. Everything behavioural and expense-related — mortality,
lapse, the shock lapse, post-level-term mortality deterioration, conversion,
commission, expenses and premium tax — is a standardization introduced for the
reference implementation, because no public source carries it. **This model is a
mechanics demonstration, not a pricing or reserving result.** Replace the assumption
tables with company data before drawing any conclusion from the output.

**Verification.** Model point 1 is the anchor cell of the worked example in the
technical notes, and ``tests/test_term_life_us.py`` asserts all twelve of its rows —
money to the cent, in-force to six decimals.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("us/models/term-life/TermLifeUS")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "TermLifeUS"

_allow_none = False

_spaces = [
    "Projection"
]

