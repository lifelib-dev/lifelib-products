"""Shared fixtures for the reference-model tests.

Models are located relative to the repository root so the suite runs from a clean
clone with no installation step.

:data:`MODELS` is the registry ``test_model_conventions.py`` is parametrized over, so
registering a model here subjects it to the whole house style: it then either conforms or
fails.  The metadata records the projection basis, which is not uniform across the
library — some products run on an annual grid and some on a monthly one — and records
that none of them discount.  That last entry is a property of the library, not an
omission: every ``technical-notes.md`` specifies *gross liability cash flows* and leaves
discounting and reserves to a separate layer that consumes them.
"""
import pathlib

import modelx as mx
import pytest

REPO = pathlib.Path(__file__).resolve().parents[1]

ANNUAL = {"grid": "annual", "age_basis": "ANB", "discounted": False}
MONTHLY = {"grid": "monthly", "age_basis": "ANB", "discounted": False}

# name -> (path relative to the repo root, metadata)
#
# The name is <market short name>_<country>_<grid>: the name the product is actually known
# by (MYGA, RILA, SPIA, ULSG — the same short names us/README.md's taxonomy tables use),
# then US, then _A for an annual step or _S for a monthly one.  The grid letters follow
# lifelib, where annuallife/TradLife_A is the annual-step model and basiclife/BasicTerm_S
# and savings/CashValue_SE are the monthly ones.
#
# This pairing is not derivable from the folder slug — "registered-index-linked-annuity"
# spelled out is unusable and the industry says RILA — so it lives here, and
# test_model_conventions.py asserts name, folder and the model's own _name all agree.
MODELS = {
    # Life
    "Term_US_A": ("us/models/term-life/Term_US_A", ANNUAL),
    "WholeLife_US_A": ("us/models/whole-life/WholeLife_US_A", ANNUAL),
    "UL_US_S": ("us/models/universal-life/UL_US_S", MONTHLY),
    "IUL_US_S": ("us/models/indexed-ul/IUL_US_S", MONTHLY),
    "VUL_US_S": ("us/models/variable-ul/VUL_US_S", MONTHLY),
    "ULSG_US_S": ("us/models/guaranteed-ul/ULSG_US_S", MONTHLY),
    # Annuity — deferred
    "MYGA_US_S": (
        "us/models/fixed-deferred-annuity/MYGA_US_S", MONTHLY),
    "FIA_US_S": (
        "us/models/fixed-indexed-annuity/FIA_US_S", MONTHLY),
    "VA_US_S": ("us/models/variable-annuity/VA_US_S", MONTHLY),
    "RILA_US_S": (
        "us/models/registered-index-linked-annuity/RILA_US_S",
        MONTHLY),
    # Annuity — payout
    "SPIA_US_S": ("us/models/immediate-annuity/SPIA_US_S", MONTHLY),
    "DIA_US_S": (
        "us/models/deferred-income-annuity/DIA_US_S", MONTHLY),
}


def model_path(name):
    """Absolute path to a model folder, from its entry in :data:`MODELS`."""
    return REPO / MODELS[name][0]


@pytest.fixture(scope="module")
def term_life():
    """The Term_US_A model, closed after the module finishes."""
    model = mx.read_model(model_path("Term_US_A"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def anchor(term_life):
    """Model point 1 — the worked-example anchor cell."""
    return term_life.Projection[1]
