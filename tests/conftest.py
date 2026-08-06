"""Shared fixtures for the reference-model tests.

Models are located relative to the repository root so the suite runs from a clean
clone with no installation step.
"""
import pathlib

import modelx as mx
import pytest

REPO = pathlib.Path(__file__).resolve().parents[1]

# name -> (path relative to the repo root, metadata)
MODELS = {
    "TermLifeUS": (
        "us/models/term-life/TermLifeUS",
        {"grid": "annual", "age_basis": "ANB", "discounted": False},
    ),
}


@pytest.fixture(scope="module")
def term_life():
    """The TermLifeUS model, closed after the module finishes."""
    model = mx.read_model(REPO / MODELS["TermLifeUS"][0])
    yield model
    model.close()


@pytest.fixture(scope="module")
def anchor(term_life):
    """Model point 1 — the worked-example anchor cell."""
    return term_life.Projection[1]
