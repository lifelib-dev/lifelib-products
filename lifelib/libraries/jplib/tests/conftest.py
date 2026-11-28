"""Shared fixtures for the reference-model tests.

The registry these fixtures read — :data:`MODELS`, :data:`LIB` and :func:`model_path` —
lives in :mod:`jp_registry` rather than here, and the test modules import it from there.
``conftest.py`` is a name pytest fixes, so with three in-library suites in one run the
files collide in ``sys.modules`` and a suite can end up locating another library's models.
See :mod:`jp_registry` for the full account.

Each model gets two fixtures: the model itself, read once per test module and closed
afterwards, and its **anchor cell** — ``Projection[1]``, which is by library convention the
model point the technical notes' worked example projects. A test module needing a second
model point takes it from the model fixture inside its own module
(``term_life.Projection[4]``) rather than adding a fixture here, so that the fixture list
stays one line of thought per model.
"""
import pathlib
import shutil

import modelx as mx
import pytest

from jp_registry import LIB, ANNUAL, MONTHLY, MODELS, model_path  # noqa: F401


# ---------------------------------------------------------------------------
# Protection


@pytest.fixture(scope="module")
def term_life():
    """The Term_JP_S model, closed after the module finishes."""
    model = mx.read_model(model_path("Term_JP_S"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def jp_term_anchor(term_life):
    """Model point 1 — the 定期保険 worked-example anchor cell."""
    return term_life.Projection[1]


@pytest.fixture(scope="module")
def income_guarantee():
    """The IncomeTerm_JP_S model, closed after the module finishes."""
    model = mx.read_model(model_path("IncomeTerm_JP_S"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def jp_income_anchor(income_guarantee):
    """Model point 1 — the 収入保障保険 worked-example anchor cell."""
    return income_guarantee.Projection[1]


# ---------------------------------------------------------------------------
# Savings


@pytest.fixture(scope="module")
def whole_life():
    """The WholeLife_JP_S model, closed after the module finishes."""
    model = mx.read_model(model_path("WholeLife_JP_S"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def jp_wl_anchor(whole_life):
    """Model point 1 — the 終身保険 worked-example anchor cell."""
    return whole_life.Projection[1]


@pytest.fixture(scope="module")
def endowment():
    """The Endowment_JP_S model, closed after the module finishes."""
    model = mx.read_model(model_path("Endowment_JP_S"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def jp_endowment_anchor(endowment):
    """Model point 1 — the 養老保険 worked-example anchor cell."""
    return endowment.Projection[1]


@pytest.fixture(scope="module")
def fx_whole_life():
    """The FXWholeLife_JP_S model, closed after the module finishes."""
    model = mx.read_model(model_path("FXWholeLife_JP_S"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def jp_fxwl_anchor(fx_whole_life):
    """Model point 1 — the 外貨建終身保険 worked-example anchor cell."""
    return fx_whole_life.Projection[1]


# ---------------------------------------------------------------------------
# Third sector (第三分野)


@pytest.fixture(scope="module")
def medical():
    """The Medical_JP_S model, closed after the module finishes."""
    model = mx.read_model(model_path("Medical_JP_S"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def jp_medical_anchor(medical):
    """Model point 1 — the 医療保険 worked-example anchor cell."""
    return medical.Projection[1]


@pytest.fixture(scope="module")
def cancer():
    """The Cancer_JP_S model, closed after the module finishes."""
    model = mx.read_model(model_path("Cancer_JP_S"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def jp_cancer_anchor(cancer):
    """Model point 1 — the がん保険 worked-example anchor cell."""
    return cancer.Projection[1]


@pytest.fixture(scope="module")
def nursing_care():
    """The LTC_JP_S model, closed after the module finishes."""
    model = mx.read_model(model_path("LTC_JP_S"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def jp_ltc_anchor(nursing_care):
    """Model point 1 — the 介護保険 worked-example anchor cell."""
    return nursing_care.Projection[1]


# ---------------------------------------------------------------------------
# Annuity


@pytest.fixture(scope="module")
def individual_annuity():
    """The Annuity_JP_S model, closed after the module finishes."""
    model = mx.read_model(model_path("Annuity_JP_S"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def jp_annuity_anchor(individual_annuity):
    """Model point 1 — the 個人年金保険 worked-example anchor cell."""
    return individual_annuity.Projection[1]


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
