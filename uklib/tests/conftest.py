"""Shared fixtures for the reference-model tests.

Models are located relative to **this library directory**, so the suite runs from a clean
clone with no installation step, and keeps running from a copy made by
``lifelib.create()`` — where it tests *that copy's* models, which is the whole point of
shipping the tests inside the library.

That is why the path here is relative and not :data:`lifelib._dirs.TEMPLATES`: the
canonical locator resolves to the *installed* library, so a copy would silently test
lifelib's pristine models instead of the user's edited ones, and pass while proving
nothing.

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

LIB = pathlib.Path(__file__).resolve().parents[1]

ANNUAL = {"grid": "annual", "age_basis": "ANB", "discounted": False}
MONTHLY = {"grid": "monthly", "age_basis": "ANB", "discounted": False}

# name -> (path relative to the library root, metadata)
#
# The name is <market short name>_<country>_<grid>: the name the product is actually known
# by (CI, IP, WOL, ULB, WP, PA — the same short names the taxonomy table in the library's
# README uses), then UK, then _A for an annual step or _S for a monthly one.  The grid
# letters follow lifelib, where annuallife/TradLife_A is the annual-step model and
# basiclife/BasicTerm_S and savings/CashValue_SE are the monthly ones.
#
# This pairing is not derivable from the folder slug — "unit_linked_bond" spelled out is
# unusable in a model name — so it lives here, and test_model_conventions.py asserts name,
# folder and the model's own _name all agree.
MODELS = {
    # Protection
    "Term_UK_A": ("products/term_assurance/Term_UK_A", ANNUAL),
}


def model_path(name):
    """Absolute path to a model folder, from its entry in :data:`MODELS`."""
    return LIB / MODELS[name][0]


@pytest.fixture(scope="module")
def term_assurance():
    """The Term_UK_A model, closed after the module finishes."""
    model = mx.read_model(model_path("Term_UK_A"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def uk_term_anchor(term_assurance):
    """Model point 1 — the UK term worked-example anchor cell."""
    return term_assurance.Projection[1]
