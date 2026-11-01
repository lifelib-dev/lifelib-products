"""Shared fixtures for the reference-model tests, and the suite's one pytest marker.

The registry these fixtures read — :data:`MODELS`, :data:`LIB` and :func:`model_path` —
lives in :mod:`us_registry` rather than here, and the test modules import it from there.
``conftest.py`` is a name pytest fixes, so with two in-library suites in one run the two
files collide in ``sys.modules`` and each suite can end up locating the *other* library's
models.  See :mod:`us_registry` for the full account.

The ``cython`` marker is registered here rather than in a root ``pytest.ini`` because the
suite ships inside the library, and a copy made by ``lifelib.create()`` carries this file
but no configuration from above it.  The marker is what ``pytest -m cython`` selects the
compile tests by (USLIB-SEC-PLAN.md D13), and registering it keeps them free of pytest's
unknown-mark warning.  The tests themselves skip when modelx-cython or a C compiler is
absent, so a bare ``pytest`` stays green on a machine that has neither.  The ``cython`` CI
job, which installs both, sets ``USLIB_REQUIRE_CYTHON=1``, and there such a skip fails.
"""
import modelx as mx
import pytest

from us_registry import LIB, ANNUAL, MONTHLY, MODELS, model_path  # noqa: F401


def pytest_configure(config):
    """Register the ``cython`` marker the compile tests carry."""
    config.addinivalue_line(
        "markers",
        "cython: compiles a model with modelx-cython; skips without modelx-cython or a C "
        "compiler")


@pytest.fixture(scope="module")
def term_life():
    """The Term_US_S model, closed after the module finishes."""
    model = mx.read_model(model_path("Term_US_S"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def anchor(term_life):
    """Model point 1 — the worked-example anchor cell."""
    return term_life.Projection[1]
