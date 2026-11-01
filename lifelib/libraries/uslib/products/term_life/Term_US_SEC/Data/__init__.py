# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The five input CSVs are read here, **once per model**, and referenced from
:mod:`~.Term_US_SEC.Projection` as ``data``. :mod:`~.Term_US_SEC.Projection` is
parameterized by ``point_id``, so each ``Projection[N]`` is a separate ItemSpace with
its own cells cache; if the readers lived there, every model point would re-read every
file. Holding them in an unparameterized Space reads each file once no matter how many
policies are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/term_life/``, rather than data stored inside the model. The model folder
therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded values —
so a diff of the model shows logic changes only. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``Term_US_SEC`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

**Four of the tables are Term_US_S's.** The premium schedule, the mortality table, the
class factors and the shock-lapse buckets are the files :mod:`~.Term_US_S` reads, read
here in place: one copy of each table serves both models, so an edit to one reaches
both. The model point table is this model's own, ``model_point_table_sec.csv``; it sits
beside ``Term_US_S``'s ``model_point_table.csv``, which this model never opens.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so
the model works wherever the repository is checked out. Each table has a filename
Reference and a reader Cells:

======================  ==========================  ==============================
Reference               Cells                       File
======================  ==========================  ==============================
model_point_file        model_point_table()         model_point_table_sec.csv
premium_rates_file      premium_rates()             premium_rates.csv
mort_table_file         mort_table()                mort_table.csv
class_factor_file       class_factor_table()        class_factor_table.csv
shock_lapse_file        shock_lapse_table()         shock_lapse_table.csv
======================  ==========================  ==============================

**The model point table is checked as it is read.** Two of its columns are the
in-force interface, ``policy_count`` and ``duration_mth``, and :func:`model_point_table`
refuses a table that lacks either, repeats a ``point_id``, or holds a count or a
duration no policy can have. The checks run in turn, and the first that fails raises,
naming the missing column or every point that fails it. It also refuses a policy to be
issued more than ``future_horizon_mth`` months after the valuation date, 120 months as
shipped: future new business is written over a stated horizon, so that no frame runs
longer than cover from issue plus that horizon. Set to 0, the Reference refuses future
new business altogether. Whether a point is still in cover at the valuation date is a
rule of the product rather than of the table, and ``Projection.proj_len`` checks it.

To swap in a licensed mortality basis, replace ``mort_table.csv`` with a same-schema
file, or point ``mort_table_file`` at a different name, then clear the cache. No
formula changes.
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
    """The model point table, read from *model_point_table_sec.csv* and checked.

    Indexed by ``point_id``. Two columns are the in-force interface, as in
    ``basiclife.BasicTerm_SE``: ``policy_count``, and ``duration_mth``, the completed
    policy months at the valuation date. The rest are ``Term_US_S``'s, except
    ``row_kind``, ``source_policy_id`` and ``source_mth``, which record where the
    generator took each shipped row from and which no formula reads.

    The checks run over the whole table at once, and the first that fails raises
    ``ValueError``, naming the missing column or every point it fails on:

    * both in-force columns are present;
    * no ``point_id`` appears twice;
    * ``policy_count`` is a number, zero or more;
    * ``duration_mth`` is a whole number of months: positive for a policy in force, 0
      for one issued at the valuation date, negative for one issued later;
    * no policy is issued more than ``future_horizon_mth`` months after the valuation
      date, so ``duration_mth`` is ``-future_horizon_mth`` or more. At 0 the model takes
      no future new business, and the message says so; a negative horizon is itself
      refused.
    """
    name = model_point_file                                          # noqa: F821
    table = pd.read_csv(input_dir() / name, index_col="point_id")    # noqa: F821
    for column in ("policy_count", "duration_mth"):
        if column not in table.columns:
            raise ValueError(f"{name} has no {column} column")
    repeated = table.index[table.index.duplicated()].unique().tolist()
    if repeated:
        raise ValueError(f"{name}: point_id {repeated} appears more than once")
    count = pd.to_numeric(table["policy_count"], errors="coerce")    # noqa: F821
    bad = table.index[~((count >= 0) & (count < float("inf")))].tolist()
    if bad:
        raise ValueError(f"{name}: policy_count must be a number, zero or more; it is "
                         f"not at point_id {bad}")
    months = pd.to_numeric(table["duration_mth"], errors="coerce")   # noqa: F821
    bad = table.index[~(months % 1 == 0)].tolist()
    if bad:
        raise ValueError(f"{name}: duration_mth must be a whole number of months; it "
                         f"is not at point_id {bad}")
    horizon = future_horizon_mth                                     # noqa: F821
    if horizon < 0:
        raise ValueError(f"future_horizon_mth must be 0 months or more, not {horizon}")
    bad = table.index[months < -horizon].tolist()
    if bad and horizon == 0:
        raise ValueError(f"{name}: duration_mth must be 0 or more: this model takes no "
                         f"future new business; it is not at point_id {bad}")
    if bad:
        raise ValueError(f"{name}: duration_mth must be -{horizon} or more, a policy "
                         f"issued at most {horizon} months after the valuation date; it "
                         f"is not at point_id {bad}")
    return table


def premium_rates():
    """The guaranteed premium schedule, read from *premium_rates.csv*.

    Keyed by the contractual, 1-based ``policy_year`` (1 = the issue year), not by the
    0-based projection index; ``Projection.premium_pp_ann_py(y)`` looks it up at policy
    year ``y``: ``premium_pp_ann(t)`` at ``policy_year(t) = duration(t) + 1``, the policy
    year containing month ``t``, and ``jump_ratio()`` at years ``n`` and ``n + 1``.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / premium_rates_file,                            # noqa: F821
        index_col=["plan", "sex", "rate_class", "band", "policy_year"])


def mort_table():
    """The base mortality table by age, read from *mort_table.csv*."""
    return pd.read_csv(input_dir() / mort_table_file, index_col="age")  # noqa: F821


def class_factor_table():
    """The underwriting-class factors, read from *class_factor_table.csv*."""
    return pd.read_csv(input_dir() / class_factor_file, index_col="rate_class")  # noqa: F821


def shock_lapse_table():
    """The shock-lapse buckets by jump ratio, read from *shock_lapse_table.csv*."""
    return pd.read_csv(input_dir() / shock_lapse_file)               # noqa: F821


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table_sec.csv"

premium_rates_file = "premium_rates.csv"

mort_table_file = "mort_table.csv"

class_factor_file = "class_factor_table.csv"

shock_lapse_file = "shock_lapse_table.csv"

future_horizon_mth = 120

pd = ("Module", "pandas")