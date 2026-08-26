# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The five input CSVs are read here, **once per model**, and referenced from
:mod:`~.EC_FR_A.Projection` as ``data``. :mod:`~.EC_FR_A.Projection` is parameterized by
``point_id``, so each ``Projection[N]`` is a separate ItemSpace with its own cells
cache; if the readers lived there, every model point would re-read every file. Holding
them in an unparameterized Space reads each file once no matter how many policies are
projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/eurocroissance/``, rather than data stored inside the model. The model folder
therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded values — so
a diff of the model shows logic changes only. This follows ``annuallife.TradLife_A``;
contrast ``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model through
modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``EC_FR_A`` folder without its parent's CSVs produces a model that reads and then fails
on first evaluation.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so
the model works wherever the repository is checked out. Each table has a filename
Reference and a reader Cells:

======================  ==========================  ==============================
Reference               Cells                       File
======================  ==========================  ==============================
model_point_file        model_point_table()         model_point_table.csv
mort_table_file         mort_table()                mort_table.csv
lapse_table_file        lapse_table()               lapse_table.csv
scenario_table_file     scenario_table()            scenario_table.csv
tec_curve_file          tec_curve()                 tec_curve.csv
======================  ==========================  ==============================

Two of these are **scenario** files rather than assumption files, and that is a product
statement. The A. 134-1 discount rate is 90% of the *taux de l'échéance constante* at the
remaining maturity, so the level *and the slope* of the TEC curve drive the *provision
mathématique* directly: in the notes' worked example a 150 bp fall in the TEC adds 587.44
to ``pm(6)``, more than twice the year's time effect. A model that carried a flat TEC
assumption in a Reference would not be modelling this product's dominant risk, so the
curve is a table with a maturity dimension and ``Projection.tec_rate`` interpolates
across it exactly as the article requires.

Every decrement table shipped here is a **[std]** proxy and says so in its own
``provenance`` column. The regulatory tables the code points to — TH 00-02 / TF 00-02 for
non-annuity contracts, TGH05 / TGF05 for annuities, applied under art. A. 335-1 with the
annexed *décalages d'âge* — are cited by name and arrêté in ``sources.md`` and **never
shipped**; art. A. 132-18 also permits an insurer's own table certified by an independent
approved actuary, so no single market basis exists to ship.
"""

from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def input_dir():
    """The directory holding the input CSVs: the model folder's parent.

    Inputs are *external* files, not data stored inside the model, so the model
    folder is pure formulas.  The path is resolved at run time from where the model
    was read, following ``annuallife.TradLife_A``.
    """
    return _model.path.parent                                        # noqa: F821


def model_point_table():
    """The model point table, read from *model_point_table.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / model_point_file, index_col="point_id")        # noqa: F821


def mort_table():
    """The base annual mortality rates by sex and *âge atteint*, from *mort_table.csv*.

    A **[std]** Makeham proxy shaped like the INSEE *quotients de mortalité*, which are
    the only freely redistributable French mortality series.  The homologated tables
    TH 00-02 / TF 00-02 are cited by arrêté and never shipped, and A. 132-18 permits an
    insurer's own certified table besides, so there is no single market basis to
    reproduce.  Anchored so that ``Projection.mort_be_factor`` applied to the male age-57
    rate — the worked example's entry age — gives exactly 0.5000% p.a.  Sorted on read,
    because ``Projection.mort_rate`` indexes into it.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file,                               # noqa: F821
        index_col=["sex", "age"]).sort_index()


def lapse_table():
    """The base annual *rachat* rates by policy year, from *lapse_table.csv*.

    Two columns: ``lapse_rate``, the full surrender (*rachat total*), level at 2.5% p.a.;
    and ``wd_rate``, the partial surrender (*rachat partiel*), 6% of the provision in
    years 1-2 and 3% thereafter.  Both are **[std]** — the published *mémoire* observes
    2%-3% and 6% then 2%-4%, and no eurocroissance lapse experience exists beyond it,
    because the product is too small and too young to have any.  The dynamic overlays
    layered on the full-surrender rate in ``Projection.lapse_rate`` matter more than the
    level does: a saver who surrenders a 2° engagement while its guarantee is in the money
    gives up the entire guarantee, which is the strongest exit deterrent in the product.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / lapse_table_file, index_col="policy_year").sort_index()


def scenario_table():
    """The gross asset return by scenario and projection year, from *scenario_table.csv*.

    Net of asset management fees (0.20% equities, 0.10% bonds), which is the basis the
    notes quote ``r(t)`` on.  Five paths: ``shock`` is the worked example's — 4.00% to
    ``t`` = 5, **-25.00%** at ``t`` = 6 and 6.00% after — and the others are the flat and
    stressed paths the remaining model points run on.  A **scenario** rather than a best
    estimate: the maturity guarantee is a put on the auxiliary account and its cost is
    convex in the asset shock, so a deterministic run understates it and the *mémoire*
    duly runs 1 000 risk-neutral scenarios.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / scenario_table_file,                           # noqa: F821
        index_col=["scenario", "year"]).sort_index()


def tec_curve():
    """The TEC term structure by scenario, projection year and maturity, from *tec_curve.csv*.

    The *taux de l'échéance constante* at maturities 1, 2, 5, 10, 20 and 30 years.
    ``Projection.i_pm`` takes 90% of the rate at the *remaining* maturity, interpolating
    linearly between the bracketing maturities and holding the longest rate beyond the
    curve, with a floor at zero.  The haircut, the interpolation and the floor are
    art. A. 134-1; reading the index maturity as the remaining term is **[std]**, and
    ``Projection.tec_rate`` says why.  Levels are **[std]** too: the
    ACPR's revaluation study records the 10-year OAT averaging 3.0% in 2023 and 2024, and
    nothing more precise was retrieved.  Sorted on read, because the interpolation walks
    the maturity index in order.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / tec_curve_file,                                # noqa: F821
        index_col=["scenario", "year", "maturity"]).sort_index()


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

mort_table_file = "mort_table.csv"

lapse_table_file = "lapse_table.csv"

scenario_table_file = "scenario_table.csv"

tec_curve_file = "tec_curve.csv"

pd = ("Module", "pandas")
