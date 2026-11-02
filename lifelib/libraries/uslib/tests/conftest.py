"""Shared fixtures for the reference-model tests, and the suite's two pytest markers.

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

The ``sec_full`` marker is registered here for the same reason.  It marks the cases of an
SEC model's full splice grid beyond the core that runs by default, which skip, with the
reason shown, unless ``USLIB_SEC_FULL=1`` is set (USLIB-SEC-PLAN.md K6), and
``pytest -m sec_full`` selects them.  One leg of the CI matrix sets it, so they run in
every CI run, on that leg.
"""
import modelx as mx
import pytest

from us_registry import LIB, ANNUAL, MONTHLY, MODELS, model_path  # noqa: F401


def pytest_configure(config):
    """Register the ``cython`` marker the compile tests carry, and ``sec_full``."""
    config.addinivalue_line(
        "markers",
        "cython: compiles a model with modelx-cython; skips without modelx-cython or a C "
        "compiler")
    config.addinivalue_line(
        "markers",
        "sec_full: a case of an SEC model's full splice grid; skips unless "
        "USLIB_SEC_FULL=1")


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


@pytest.fixture(scope="session")
def sec_build(tmp_path_factory):
    """The SEC models compiled in this session: ``sec_build(name)`` is ``name``'s build.

    Each model is compiled once per session, into a temporary directory, never into the
    tree (USLIB-SEC-PLAN.md D12), and only when a compile test asks for it, so a session
    that selects none compiles nothing.  Without modelx-cython or a compiler the asking
    test skips, or fails under ``USLIB_REQUIRE_CYTHON=1`` (``sec_support.require_cython``).
    """
    from sec_support import SecBuilds
    return SecBuilds(tmp_path_factory)


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item, call):
    """Under ``USLIB_REQUIRE_CYTHON=1``, report a ``cython`` test that skips as failed.

    ``sec_support.require_cython`` fails a compile test that finds the toolchain missing,
    but a test can skip before its body runs: one parametrized over the SEC models at
    stage ``"EC"`` skips, "got empty parameter set", when the registry holds none.  In the
    ``cython`` CI job any such skip is a green run that compiled nothing (D13), so it is
    turned into a failure here, whatever skipped it.
    """
    import os
    report = yield
    if (report.skipped and not hasattr(report, "wasxfail")
            and item.get_closest_marker("cython") is not None
            and os.environ.get("USLIB_REQUIRE_CYTHON") == "1"):
        given = report.longrepr
        reason = given[-1] if isinstance(given, tuple) else given
        report.outcome = "failed"
        report.longrepr = f"USLIB_REQUIRE_CYTHON=1 forbids a skip, and it skipped: {reason}"
    return report
