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
# The name is CamelCase of the product folder slug plus "US" — term-life -> TermLifeUS —
# and test_model_conventions.py asserts that rule, so the two columns cannot drift apart.
MODELS = {
    # Life
    "TermLifeUS": ("us/models/term-life/TermLifeUS", ANNUAL),
    "WholeLifeUS": ("us/models/whole-life/WholeLifeUS", ANNUAL),
    "UniversalLifeUS": ("us/models/universal-life/UniversalLifeUS", MONTHLY),
    "IndexedULUS": ("us/models/indexed-ul/IndexedULUS", MONTHLY),
    "VariableULUS": ("us/models/variable-ul/VariableULUS", MONTHLY),
    "GuaranteedULUS": ("us/models/guaranteed-ul/GuaranteedULUS", MONTHLY),
    # Annuity — deferred
    "FixedDeferredAnnuityUS": (
        "us/models/fixed-deferred-annuity/FixedDeferredAnnuityUS", MONTHLY),
    "FixedIndexedAnnuityUS": (
        "us/models/fixed-indexed-annuity/FixedIndexedAnnuityUS", MONTHLY),
    "VariableAnnuityUS": ("us/models/variable-annuity/VariableAnnuityUS", MONTHLY),
    "RegisteredIndexLinkedAnnuityUS": (
        "us/models/registered-index-linked-annuity/RegisteredIndexLinkedAnnuityUS",
        MONTHLY),
    # Annuity — payout
    "ImmediateAnnuityUS": ("us/models/immediate-annuity/ImmediateAnnuityUS", MONTHLY),
    "DeferredIncomeAnnuityUS": (
        "us/models/deferred-income-annuity/DeferredIncomeAnnuityUS", MONTHLY),
}


def model_path(name):
    """Absolute path to a model folder, from its entry in :data:`MODELS`."""
    return REPO / MODELS[name][0]


@pytest.fixture(scope="module")
def term_life():
    """The TermLifeUS model, closed after the module finishes."""
    model = mx.read_model(model_path("TermLifeUS"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def anchor(term_life):
    """Model point 1 — the worked-example anchor cell."""
    return term_life.Projection[1]
