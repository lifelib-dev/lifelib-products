# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The six input CSVs are read here, **once per model**, and referenced from
:mod:`~.WholeLife_US_SEC.Projection` as ``data``. :mod:`~.WholeLife_US_SEC.Projection` is
parameterized by ``point_id``, so each ``Projection[N]`` is a separate ItemSpace with
its own cells cache; if the readers lived there, every model point would re-read every
file. Holding them in an unparameterized Space reads each file once no matter how many
policies are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/whole_life/``, rather than data stored inside the model. The model folder
therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded values —
so a diff of the model shows logic changes only. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``WholeLife_US_SEC`` folder without its parent's CSVs produces a model that reads and
then fails on first evaluation.

**Five of the tables are WholeLife_US_S's.** The guaranteed cash value schedule, the net
single premiums, the nonforfeiture net level premiums, the guaranteed mortality and the
final-expense premium rates are the files :mod:`~.WholeLife_US_S` reads, read here in
place: one copy of each table serves both models, so an edit to one reaches both. The
model point table is this model's own, ``model_point_table_sec.csv``; it sits beside
``WholeLife_US_S``'s ``model_point_table.csv``, which this model never opens.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so
the model works wherever the repository is checked out. Each table has a filename
Reference and a reader Cells:

======================  ==========================  ==============================
Reference               Cells                       File
======================  ==========================  ==============================
model_point_file        model_point_table()         model_point_table_sec.csv
cv_file                 cv_table()                  cv_table.csv
nsp_file                nsp_table()                 nsp_table.csv
np_guar_file            np_guar_table()             np_guar_table.csv
mort_table_file         mort_table()                mort_table.csv
premium_rates_file      premium_rates()             premium_rates.csv
======================  ==========================  ==============================

**The model point table is checked as it is read.** Nine of its columns are the
in-force interface: ``policy_count`` and ``duration_mth``, as in
``basiclife.BasicTerm_SE``, and the seven columns of an in-force policy's opening
state. :func:`model_point_table` refuses a table that lacks any of them, repeats a
``point_id``, holds a count or a duration no policy can have, or holds an opening state
no policy can be in. The checks run in turn, and the first that fails raises, naming the
missing column or every point that fails it. It also refuses a policy to be issued more
than ``future_horizon_mth`` months after the valuation date, 120 months as shipped:
future new business is written over a stated horizon, so that no frame runs longer than
cover from issue plus that horizon. Set to 0, the Reference refuses future new business
altogether. Whether a point is still in cover at the valuation date is a rule of the
product rather than of the table, and ``Projection.proj_len`` checks it.

The four guarantee-basis tables belong together. ``mort_table.csv`` holds the
guaranteed mortality ``q^g``, ``nsp_table.csv`` the endowment-at-100 net single
premiums that price paid-up additions, ``np_guar_table.csv`` the nonforfeiture net
level premium that the dividend's interest margin is credited on, and ``cv_table.csv``
the guaranteed cash value schedule. The technical notes' first "known modeling
pitfall" is exactly a mismatch between them, and it prescribes regenerating all four
from one 2017 CSO / 4% source.

**The shipped four are not one construction, and no set carrying the worked example's
anchors could be.** On a single mortality basis at 4% the notes' own definition
collapses to ``NNLP = 1000 d NSP_45 / (1 - NSP_45)``, so the worked example's
``NNLP = 13.00`` forces ``NSP_45 = 0.252616`` and hence ``NSP_55 <= 0.252616 x 1.04^10
= 0.373933`` — short of the worked example's ``NSP_55 = 0.42``, whatever mortality is
assumed. Each shipped table is therefore pinned to its own worked-example anchor
independently: ``q^g_54 = 0.00320``, ``NSP_55 = 0.42``, ``NP_g = 13.00``, and 95.00 and
112.00 per $1,000 on the policy-year 9 and 10 rows of the cash value schedule — the
worked example's ``CV_107`` and ``CV_119``. The anchor cell, in force 108 months at the
valuation date, reaches them as ``cv_pp_anniv(9)``, the value entering its ``t = 0``,
which ``WholeLife_US_S`` reads as ``cv_pp(107)``, and as ``cv_pp(11)``, its tenth
anniversary, ``WholeLife_US_S``'s month 119. Reconciling ``nsp_table.csv`` with
``mort_table.csv`` would need a guarantee interest rate falling from 5.99% at age 45
to 0.02% at age 99. ``model.md`` and the ``Projection`` docstring carry the
arithmetic; a test pins the mismatch by age so it cannot quietly close.

What *is* guaranteed, because the two consequences the pitfall names would otherwise
bite, is the pair of endpoints: ``nsp = 1.000000`` at attained age 100, so the
paid-up-additions cash value reaches paid-up-additions face at maturity, and
``cv_per_1000 = 1000.00`` on the last policy year of each cell — the schedule's
``policy_year = 100 - issue_age`` row, read by the model at ``t = proj_len() - 1`` — so
the base block endows at face.
Both are asserted by the tests. Every rate is also **sex-distinct**, as the notes
require — including the pay-to-100 cash value schedule.

To swap in a licensed mortality basis, replace ``mort_table.csv`` with a same-schema
file, or point ``mort_table_file`` at a different name, then clear the cache. No
formula changes — but regenerate ``nsp_table.csv``, ``np_guar_table.csv`` and
``cv_table.csv`` from the same basis, or the pitfall above is exactly what happens.
Doing so is the only way to satisfy the notes' one-basis instruction, and it will stop
the worked example reproducing. Replacing the files changes :mod:`~.WholeLife_US_S`
too, which reads the same ones.
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

    Indexed by ``point_id``. Nine columns are the in-force interface: ``policy_count``
    and ``duration_mth``, the completed policy months at the valuation date, as in
    ``basiclife.BasicTerm_SE``, and the seven columns of the opening state, per policy,
    as the policy stands at the start of month 0, before any month-0 event:

    * ``pua_face_init``, ``loan_bal_init`` and ``div_accum_init``: the paid-up-additions
      face, the loan and the accumulation balance entering month 0;
    * ``pua_face_prev_anniv_init`` and ``loan_bal_prev_anniv_init``: the same face and
      loan at the anniversary that opened the policy year under way, the one on or
      before the valuation date, and ``div_prev_anniv_init``, the dividend credited
      there;
    * ``prem_cum_init``: the gross premium paid before the valuation date.

    The rest are ``WholeLife_US_S``'s, except ``row_kind``, ``source_policy_id`` and
    ``source_mth``, which record where the generator took each shipped row from and which
    no formula reads.

    The checks run over the whole table at once, and the first that fails raises
    ``ValueError``, naming the missing column or every point it fails on:

    * the nine in-force columns are present;
    * no ``point_id`` appears twice;
    * ``policy_count`` is a number, zero or more;
    * ``duration_mth`` is a whole number of months: positive for a policy in force, 0
      for one issued at the valuation date, negative for one issued later;
    * no policy is issued more than ``future_horizon_mth`` months after the valuation
      date, so ``duration_mth`` is ``-future_horizon_mth`` or more. At 0 the model takes
      no future new business, and the message says so; a negative horizon is itself
      refused;
    * each opening-state column is a number, zero or more;
    * a policy not yet in force, ``duration_mth`` 0 or less, has no opening state: it is
      issued with none;
    * the non-participating final-expense design has no paid-up additions and no
      dividend;
    * only the ACCUM option has an accumulation balance, which on any other the
      projection would drop from every benefit;
    * on a point valued on a policy anniversary, ``duration_mth`` a multiple of 12, the
      two anniversary columns equal the two entering month 0, which are the same
      instant;
    * in the first policy year, ``duration_mth`` 1 to 11, the year opened at issue and
      has credited no dividend yet, so the three anniversary columns hold their issue
      values, 0, and so does ``div_accum_init``.

    A point whose paid-up additions at the anniversary exceed those entering month 0 is
    accepted. The model never shrinks the block, so such a row records a partial
    surrender of additions, which the model does not implement, and it is projected
    from the values it gives.
    """
    name = model_point_file                                          # noqa: F821
    table = pd.read_csv(input_dir() / name, index_col="point_id")    # noqa: F821
    state = ("pua_face_init", "pua_face_prev_anniv_init", "loan_bal_init",
             "loan_bal_prev_anniv_init", "div_accum_init", "div_prev_anniv_init",
             "prem_cum_init")
    for column in ("policy_count", "duration_mth", *state):
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
    values = {c: pd.to_numeric(table[c], errors="coerce") for c in state}  # noqa: F821
    for column, v in values.items():
        bad = table.index[~((v >= 0) & (v < float("inf")))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a number, zero or more; it is "
                             f"not at point_id {bad}")
    for column, v in values.items():
        bad = table.index[(months <= 0) & (v != 0)].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be 0 on a policy not yet in force, "
                             f"duration_mth 0 or less; it is not at point_id {bad}")
    non_par = table["product"] != "WL_PAR"
    for column in ("pua_face_init", "pua_face_prev_anniv_init", "div_prev_anniv_init"):
        bad = table.index[non_par & (values[column] != 0)].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be 0 on a non-participating "
                             f"product, which pays no dividend; it is not at point_id "
                             f"{bad}")
    bad = table.index[(table["dividend_option"] != "ACCUM")
                      & (values["div_accum_init"] != 0)].tolist()
    if bad:
        raise ValueError(f"{name}: div_accum_init must be 0 unless dividend_option is "
                         f"ACCUM; it is not at point_id {bad}")
    on_anniv = (months > 0) & (months % 12 == 0)
    for anniv, now in (("pua_face_prev_anniv_init", "pua_face_init"),
                       ("loan_bal_prev_anniv_init", "loan_bal_init")):
        bad = table.index[on_anniv & (values[anniv] != values[now])].tolist()
        if bad:
            raise ValueError(f"{name}: on a point valued on a policy anniversary, "
                             f"duration_mth a multiple of 12, {anniv} must equal {now}; "
                             f"it does not at point_id {bad}")
    first_year = (months > 0) & (months < 12)
    for column in ("pua_face_prev_anniv_init", "loan_bal_prev_anniv_init",
                   "div_accum_init", "div_prev_anniv_init"):
        bad = table.index[first_year & (values[column] != 0)].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be 0 in the first policy year, "
                             f"duration_mth 1 to 11, which opened at issue and has "
                             f"credited no dividend yet; it is not at point_id {bad}")
    return table


def cv_table():
    """The guaranteed cash value schedule per $1,000 of face, from *cv_table.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / cv_file,                                       # noqa: F821
        index_col=["premium_period", "sex", "issue_age", "policy_year"])


def nsp_table():
    """The endowment-at-100 net single premiums by attained age, from *nsp_table.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / nsp_file, index_col=["sex", "age"])            # noqa: F821


def np_guar_table():
    """The nonforfeiture net level premiums per $1,000, from *np_guar_table.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / np_guar_file,                                  # noqa: F821
        index_col=["premium_period", "sex", "issue_age"])


def mort_table():
    """The guaranteed mortality table by sex and age, read from *mort_table.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file, index_col=["sex", "age"])     # noqa: F821


def premium_rates():
    """The final-expense premium rates per $1,000, read from *premium_rates.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / premium_rates_file,                            # noqa: F821
        index_col=["product", "sex", "risk_class", "issue_age"])


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table_sec.csv"

cv_file = "cv_table.csv"

nsp_file = "nsp_table.csv"

np_guar_file = "np_guar_table.csv"

mort_table_file = "mort_table.csv"

premium_rates_file = "premium_rates.csv"

future_horizon_mth = 120

pd = ("Module", "pandas")