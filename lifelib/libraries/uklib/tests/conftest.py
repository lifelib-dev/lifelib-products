"""Shared fixtures for the reference-model tests, and the suite's three pytest markers.

The registry these fixtures read — :data:`MODELS`, :data:`LIB` and :func:`model_path` —
lives in :mod:`uk_registry` rather than here, and the test modules import it from there.
``conftest.py`` is a name pytest fixes, so with two in-library suites in one run the two
files collide in ``sys.modules`` and each suite can end up locating the *other* library's
models.  See :mod:`uk_registry` for the full account.

The markers, the ``sec_build`` fixture and the two hooks below are uslib's
(``uslib/tests/conftest.py``), read for this library: its ``UKLIB_*`` variables, its
harness :mod:`uk_sec_support`, and its CI jobs ``cython_uk`` and ``sec_uk``
(UKLIB-SEC-PLAN.md U3, U7, §3 item 5).

The ``cython`` marker is registered here rather than in a root ``pytest.ini`` because the
suite ships inside the library, and a copy made by ``lifelib.create()`` carries this file
but no configuration from above it.  The marker is what ``pytest -m cython`` selects the
compile tests by (USLIB-SEC-PLAN.md D13), and registering it keeps them free of pytest's
unknown-mark warning.  The tests themselves skip when modelx-cython or a C compiler is
absent, so a bare ``pytest`` stays green on a machine that has neither.  The ``cython_uk``
CI job, which installs both, sets ``UKLIB_REQUIRE_CYTHON=1``, and there such a skip fails.
That job runs one shard of the compile tests to a leg, named by ``UKLIB_CYTHON_SHARD``:
``toolchain``, or the product directory of an SEC model at stage ``"EC"``, whose shard
holds its product module's compile tests and its cases of
``test_compiled_conventions_uk.py``, so that the model compiles once a leg (D13).
:func:`pytest_collection_modifyitems` deselects the compile tests outside the shard, by
``uk_sec_support.cython_shard``, and fails a shard that selects none under
``UKLIB_REQUIRE_CYTHON=1``.  Unset, it deselects nothing.

The ``sec_full`` marker is registered here for the same reason.  It marks the cases of an
SEC model's full splice grid beyond the core that runs by default, which skip, with the
reason shown, unless ``UKLIB_SEC_FULL=1`` is set (UKLIB-SEC-PLAN.md U6), and
``pytest -m sec_full`` selects them.  CI's ``sec_uk`` job sets it on its Linux legs, one
module to a leg, so they run in every CI run, and the ``cython_uk`` job on its Linux leg,
where the compiled grids run at full size.

The ``docutils`` marker is registered here for the same reason.  It marks the tests that
read a model's docstrings through docutils as the docs build does, which skip where
docutils is absent: it is not a requirement of the models, and lifelib's CI does not
install it.  The CI legs that run the full grids install it and set
``UKLIB_REQUIRE_DOCUTILS=1``, under which such a skip fails, as ``UKLIB_REQUIRE_CYTHON=1``
fails a compile test's (USLIB-SEC-PLAN.md §5.4).

**Two libraries in one process.**  uslib's ``conftest.py`` registers the same three markers
and defines the same two hooks, and CI's ``test`` job collects both suites in one run, as
lifelib's own CI will.  Each library's variables govern its own tests alone.  pytest hands
:func:`pytest_runtest_makereport` to the ``conftest.py`` files above a test's own file, so
this one never sees uslib's tests, nor uslib's these.  But every
:func:`pytest_collection_modifyitems` is handed every item collected, so this one
deselects only the compile tests of this directory, and asks only of those whether the
shard kept any: a shard of uklib's that selects none is an error even where uslib's
compile tests are collected beside it.
"""
import os
import pathlib
import shutil

import modelx as mx
import pytest

from uk_registry import LIB, ANNUAL, MONTHLY, MODELS, model_path  # noqa: F401

# This suite's directory, whose compile tests alone pytest_collection_modifyitems shards.
HERE = pathlib.Path(__file__).resolve().parent


def pytest_configure(config):
    """Register the ``cython`` marker the compile tests carry, ``sec_full`` and
    ``docutils``."""
    config.addinivalue_line(
        "markers",
        "cython: compiles a model with modelx-cython; skips without modelx-cython or a C "
        "compiler")
    config.addinivalue_line(
        "markers",
        "sec_full: a case of an SEC model's full splice grid; skips unless "
        "UKLIB_SEC_FULL=1")
    config.addinivalue_line(
        "markers",
        "docutils: parses docstrings with docutils; skips where docutils is absent")


@pytest.fixture(scope="module")
def term_assurance():
    """The Term_UK_S model, closed after the module finishes."""
    model = mx.read_model(model_path("Term_UK_S"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def uk_term_anchor(term_assurance):
    """Model point 1 — the UK term worked-example anchor cell."""
    return term_assurance.Projection[1]


@pytest.fixture(scope="module")
def critical_illness():
    """The CI_UK_S model, closed after the module finishes."""
    model = mx.read_model(model_path("CI_UK_S"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def uk_ci_anchor(critical_illness):
    """Model point 1 — the UK critical illness worked-example anchor cell."""
    return critical_illness.Projection[1]


@pytest.fixture(scope="module")
def income_protection():
    """The IP_UK_S model, closed after the module finishes."""
    model = mx.read_model(model_path("IP_UK_S"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def uk_ip_claim(income_protection):
    """Model point 2 — the claims-in-payment cell the worked example computes."""
    return income_protection.Projection[2]


@pytest.fixture(scope="module")
def whole_of_life():
    """The WOL_UK_S model, closed after the module finishes."""
    model = mx.read_model(model_path("WOL_UK_S"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def uk_o50_anchor(whole_of_life):
    """Model point 1 — the over-50s worked-example anchor cell."""
    return whole_of_life.Projection[1]


@pytest.fixture(scope="module")
def unit_linked_bond():
    """The ULB_UK_S model, closed after the module finishes."""
    model = mx.read_model(model_path("ULB_UK_S"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def uk_bond_anchor(unit_linked_bond):
    """Model point 1 — the unit-linked bond worked-example anchor cell."""
    return unit_linked_bond.Projection[1]


@pytest.fixture(scope="module")
def with_profits():
    """The WP_UK_S model, closed after the module finishes."""
    model = mx.read_model(model_path("WP_UK_S"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def uk_wp_up(with_profits):
    """Model point 1 — the worked example's scenario A, the up market."""
    return with_profits.Projection[1]


@pytest.fixture(scope="module")
def uk_wp_down(with_profits):
    """Model point 2 — the worked example's scenario B, the down market."""
    return with_profits.Projection[2]


@pytest.fixture(scope="module")
def pension_annuity():
    """The PA_UK_S model, closed after the module finishes."""
    model = mx.read_model(model_path("PA_UK_S"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def uk_pa_scenario(pension_annuity):
    """Model point 1 — the worked example's scenario configuration."""
    return pension_annuity.Projection[1]


@pytest.fixture(scope="session")
def sec_build(tmp_path_factory):
    """The SEC models compiled in this session: ``sec_build(name)`` is ``name``'s build.

    Each model is compiled once per session, into a temporary directory, never into the
    tree (USLIB-SEC-PLAN.md D12), and only when a compile test asks for it, so a session
    that selects none compiles nothing.  Without modelx-cython or a compiler the asking
    test skips, or fails under ``UKLIB_REQUIRE_CYTHON=1``
    (``uk_sec_support.require_cython``).  uslib's ``conftest.py`` defines a fixture of the
    same name over its own harness; pytest gives each suite the one above its files.
    """
    from uk_sec_support import SecBuilds
    return SecBuilds(tmp_path_factory)


def _ours(item):
    """Whether ``item`` is one of this directory's compile tests: marked ``cython``, and
    collected from a file here, not from another library's suite."""
    return (item.get_closest_marker("cython") is not None
            and item.path.resolve().parent == HERE)


@pytest.hookimpl(trylast=True)
def pytest_collection_modifyitems(config, items):
    """Under ``UKLIB_CYTHON_SHARD``, deselect this suite's ``cython`` tests outside that
    shard.

    The shards are ``uk_sec_support.cython_shards``, read from the registry, and a test's
    is ``uk_sec_support.cython_shard``; a name that is no shard is a usage error, which
    lists them.  Run last, after ``-m`` has deselected, so that what is left is what the
    session runs: under ``UKLIB_REQUIRE_CYTHON=1``, a shard left with no compile test of
    this suite is an error too, as a run that selects no test is (D13), and not a green leg
    that compiled nothing.  Tests without the marker are left to ``-m``, and other suites'
    tests are not touched, nor counted: uslib's compile tests, collected beside these, are
    neither deselected here nor taken for a compile test of uklib's shard.
    """
    shard = os.environ.get("UKLIB_CYTHON_SHARD", "")
    if not shard:
        return
    from uk_sec_support import cython_shard, cython_shards
    shards = cython_shards()
    if shard not in shards:
        raise pytest.UsageError(f"UKLIB_CYTHON_SHARD={shard!r} is no shard; the shards are "
                                f"{', '.join(shards)}")
    kept, dropped = [], []
    for item in items:
        (dropped if _ours(item) and cython_shard(item, shards) != shard
         else kept).append(item)
    if dropped:
        config.hook.pytest_deselected(items=dropped)
        items[:] = kept
    if (os.environ.get("UKLIB_REQUIRE_CYTHON") == "1"
            and not any(_ours(item) for item in kept)):
        raise pytest.UsageError(f"UKLIB_REQUIRE_CYTHON=1, and UKLIB_CYTHON_SHARD={shard!r} "
                                f"selects no compile test")


# Each marker whose skip a CI job forbids, with the variable that forbids it.
REQUIRED = (("cython", "UKLIB_REQUIRE_CYTHON"), ("docutils", "UKLIB_REQUIRE_DOCUTILS"))


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item, call):
    """Under ``UKLIB_REQUIRE_CYTHON=1``, report a ``cython`` test that skips as failed, and
    under ``UKLIB_REQUIRE_DOCUTILS=1`` a ``docutils`` test.

    ``uk_sec_support.require_cython`` fails a compile test that finds the toolchain
    missing, but a test can skip before its body runs: one parametrized over the SEC models
    at stage ``"EC"`` skips, "got empty parameter set", when the registry holds none.  In
    the ``cython_uk`` CI job any such skip is a green run that compiled nothing (D13), so
    it is turned into a failure here, whatever skipped it.  A docstring parse test skips
    where docutils is absent, and on the CI leg that installs docutils such a skip is a
    green run that parsed nothing, so it fails there the same way.  pytest calls this hook
    for the tests below this file alone, so uslib's variables never fail a test of
    uklib's, nor these one of uslib's.
    """
    report = yield
    if report.skipped and not hasattr(report, "wasxfail"):
        for marker, variable in REQUIRED:
            if (item.get_closest_marker(marker) is not None
                    and os.environ.get(variable) == "1"):
                given = report.longrepr
                reason = given[-1] if isinstance(given, tuple) else given
                report.outcome = "failed"
                report.longrepr = f"{variable}=1 forbids a skip, and it skipped: {reason}"
                break
    return report


# ---------------------------------------------------------------------------
# Throwaway product copy for input-swap and mutation tests


@pytest.fixture
def product_copy(tmp_path):
    """A throwaway copy of the product directory, model and input CSVs together.

    The inputs are **external files** in the model folder's parent, so a test that wants
    to move an assumption has to move a file, and moving one inside the repository would
    leave an orphan CSV that convention tests fail on. Copying the directory instead
    keeps every such test off the shipped tree entirely; ``input_dir()`` resolves to
    ``_model.path.parent`` at run time, so the copy reads its own CSVs with no formula changed.
    """
    models = []

    def _copy(model_dir, name):
        model_dir = pathlib.Path(model_dir)
        dest = tmp_path / name
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(model_dir.parent, dest,
                        ignore=shutil.ignore_patterns("__pycache__"))
        model = mx.read_model(dest / model_dir.name, name=name)
        models.append(model)
        return model

    yield _copy

    for model in models:
        try:
            if model.name in mx.get_models():
                model.close()
        except Exception:
            pass
