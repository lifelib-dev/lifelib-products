# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-contract projection.

The four input CSVs are read here, **once per model**, and referenced from
:mod:`~.SPIA_US_SEC.Projection` as ``data``. :mod:`~.SPIA_US_SEC.Projection` is
parameterized by ``point_id``, so each ``Projection[N]`` is a separate ItemSpace with its
own cells cache; if the readers lived there, every model point would re-read every file.
Holding them in an unparameterized Space reads each file once no matter how many
contracts are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/immediate_annuity/``, rather than data stored inside the model. The model
folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded
values — so a diff of the model shows logic changes only. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``SPIA_US_SEC`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

**Three of the tables are SPIA_US_S's.** The mortality table, the improvement scale and
the surrender-charge scale are the files :mod:`~.SPIA_US_S` reads, read here in place: one
copy of each table serves both models, so an edit to one reaches both. The model point
table is this model's own, ``model_point_table_sec.csv``; it sits beside
``SPIA_US_S``'s ``model_point_table.csv``, which this model never opens.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so
the model works wherever the repository is checked out. Each table has a filename
Reference and a reader Cells:

========================  ==============================  ==========================
Reference                 Cells                           File
========================  ==============================  ==========================
model_point_file          model_point_table()             model_point_table_sec.csv
mort_table_file           mort_table()                    mort_table.csv
improvement_scale_file    improvement_scale()             improvement_scale.csv
surr_charge_file          surr_charge_table()             surr_charge_table.csv
========================  ==============================  ==========================

**The model point table is checked as it is read.** Six of its columns are the
in-force interface: ``policy_count`` and ``duration_mth``, as in
``basiclife.BasicTerm_SE``, and the four columns of a contract's opening state, each
covered life's survival at the valuation date, the commutation fraction taken by then and
the 10-year CMT's change since the annuity date. :func:`model_point_table` refuses a
table that lacks any of them, repeats a ``point_id``, holds a count, a duration or a month
of death no contract can have, or holds an opening state no contract can be in. The checks
run in turn, and the first that fails raises, naming the missing column or every point
that fails it. It also refuses an annuity to commence more than ``future_horizon_mth``
months after the valuation date, 120 months as shipped: future new business is written
over a stated horizon, so that no frame runs longer than the stop rule from the annuity
date plus that horizon. Set to 0, the Reference refuses future new business altogether.
Whether a contract still owes a payment at the valuation date is a rule of the product
rather than of the table, and ``Projection.proj_len`` checks it.

**So is the surrender-charge scale.** :func:`surr_charge_scale` reads its policy years by
value, once, and refuses a year that is not a whole number, a gap, a repeat or a blank
rate, naming the file; ``Projection.surr_charge_rate`` takes the scale's first and last
years and its rates from there, never from the raw column.

The two mortality tables are keyed by ``(age, sex)`` and the surrender-charge table by
``policy_year``. They are separate files on purpose: the technical notes require the
best-estimate basis to be the **2012 IAM Basic** table projected with **Projection Scale
G2**, two distinct objects with distinct provenance, and neither may be embedded in the
model — the shipped tables are illustrative **[std]** stand-ins. To swap in a licensed
basis, replace ``mort_table.csv`` with a same-schema file, or point ``mort_table_file``
at a different name before the model computes anything. No formula changes. The
improvement scale is swappable the same way, which is how the notes' first sensitivity —
a 50% / 150% scaling of tabulated improvement — is run. Replacing a file changes
:mod:`~.SPIA_US_S` too, which reads the same one.
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

    Indexed by ``point_id``. Six columns are the in-force interface: ``policy_count``,
    the contracts the point stands for, and ``duration_mth``, the months elapsed from the
    annuity date at the valuation date, as in ``basiclife.BasicTerm_SE``; then the opening
    state, per contract, as it stands at the start of month 0, before any month-0 event:

    * ``lives_if_init_1`` and ``lives_if_init_2``: each covered life's probability of
      being alive at the valuation date, 1 or 0 on a real record, where a joint contract
      may carry one life already dead, and 0 for the second life of a single-life
      contract;
    * ``commute_frac_cum_init``: the cumulative commutation fraction applying in month 0,
      before any month-0 withdrawal;
    * ``cmt10_shift_init``: the 10-year CMT at the valuation date less the 10-year CMT at
      the annuity date, as a decimal, which moves the commutation discount rate.

    The rest are ``SPIA_US_S``'s, ``pols_if_init`` renamed ``policy_count``, except
    ``row_kind``, ``source_policy_id`` and ``source_mth``, which record where the
    generator took each shipped row from and which no formula reads.

    The checks run over the whole table at once, and the first that fails raises
    ``ValueError``, naming the missing column or every point it fails on:

    * the six in-force columns are present;
    * no ``point_id`` appears twice;
    * ``policy_count`` is a number, zero or more;
    * ``duration_mth`` is a whole number of months, read by value, so that ``12.0`` is
      12: positive for a contract in payment, 0 for one whose annuity date is the
      valuation date, negative for one commencing later;
    * no annuity commences more than ``future_horizon_mth`` months after the valuation
      date, so ``duration_mth`` is ``-future_horizon_mth`` or more. At 0 the model takes
      no future new business, and the message says so; a negative horizon is itself
      refused;
    * ``lives_if_init_1`` and ``lives_if_init_2`` are probabilities, 0 to 1;
    * ``commute_frac_cum_init`` is a number, 0 or more and below 1;
    * ``cmt10_shift_init`` is a number, of either sign;
    * a single-life contract has no second life: ``lives_if_init_2`` is 0;
    * a contract not yet in payment, ``duration_mth`` 0 or less, holds its values at
      the annuity date: each covered life 1, no commutation and no change in the CMT;
    * each month of death, ``death_mth_1`` and ``death_mth_2``, is blank or a whole
      number of months, read by value, so that ``13.0`` is 13 and a fraction or text is
      refused, on every basis. The table is returned with the two columns as the numbers
      they were checked as, which is what ``Projection.death_mth`` reads;
    * on the scenario basis, each life's opening status is its death month's: 1 while
      the life survives to the valuation date, ``death_mth`` blank, negative or
      ``duration_mth`` or later, as ``Projection.death_mth`` and ``Projection.lives_if``
      read it, and 0 once it has died. So the scenario's step function, which
      ``lives_if`` follows after the valuation date, agrees with the opening value at it;
    * a commutation fraction appears only where a commutation could have been taken
      before the valuation date: the contract holds the right, its issue state allows
      it, it has a certain period, an elected one or an installment refund's, and
      ``duration_mth`` is 13 or more, the first withdrawal being taken in policy month 12
      and reducing the instalments from month 13. That is a necessary condition only: the
      check cannot see an installment refund's derived period, which needs the projection,
      nor whether a certain period long enough for a withdrawal remained, and it does not
      ask whether the model's own utilization assumption would have taken one, since a
      real record's withdrawals do not depend on it.

    Whether the contract still owes a payment at the valuation date needs the certain
    period, which an installment refund derives in ``Projection``, so
    ``Projection.proj_len`` checks it.
    """
    name = model_point_file                                          # noqa: F821
    table = pd.read_csv(input_dir() / name, index_col="point_id")    # noqa: F821
    state = ("lives_if_init_1", "lives_if_init_2", "commute_frac_cum_init",
             "cmt10_shift_init")
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
    for column in ("lives_if_init_1", "lives_if_init_2"):
        v = values[column]
        bad = table.index[~((v >= 0) & (v <= 1))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a probability, 0 to 1; it is "
                             f"not at point_id {bad}")
    theta = values["commute_frac_cum_init"]
    bad = table.index[~((theta >= 0) & (theta < 1))].tolist()
    if bad:
        raise ValueError(f"{name}: commute_frac_cum_init must be a number, 0 or more "
                         f"and below 1; it is not at point_id {bad}")
    shift = values["cmt10_shift_init"]
    bad = table.index[~((shift > -float("inf")) & (shift < float("inf")))].tolist()
    if bad:
        raise ValueError(f"{name}: cmt10_shift_init must be a number, the change in the "
                         f"10-year CMT since the annuity date; it is not at point_id {bad}")
    joint = table["joint"].astype(bool)
    bad = table.index[~joint & (values["lives_if_init_2"] != 0)].tolist()
    if bad:
        raise ValueError(f"{name}: lives_if_init_2 must be 0 on a single-life "
                         f"contract, which covers no second life; it is not at "
                         f"point_id {bad}")
    issued = months <= 0
    for column, at_issue in (("lives_if_init_1", 1.0),
                             ("lives_if_init_2", joint.astype(float)),
                             ("commute_frac_cum_init", 0.0),
                             ("cmt10_shift_init", 0.0)):
        bad = table.index[issued & (values[column] != at_issue)].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must hold its value at issue on a "
                             f"contract not yet in force, duration_mth 0 or less: each "
                             f"covered life alive, no commutation taken and no change in "
                             f"the CMT; it does not at point_id {bad}")
    deaths = {}
    for life in (1, 2):
        column = f"death_mth_{life}"
        death = pd.to_numeric(table[column], errors="coerce")        # noqa: F821
        bad = table.index[~(table[column].isna() | (death % 1 == 0))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be blank or a whole number of "
                             f"months, a policy month; it is not at point_id {bad}")
        deaths[life] = death
    scenario = table["mort_basis"] == "scenario"
    for life in (1, 2):
        death = deaths[life]
        alive = death.isna() | (death < 0) | (death >= months)
        covered = joint if life == 2 else pd.Series(True, index=table.index)  # noqa: F821
        want = alive.astype(float).where(covered, 0.0)
        column = f"lives_if_init_{life}"
        bad = table.index[scenario & (values[column] != want)].tolist()
        if bad:
            raise ValueError(f"{name}: on the scenario basis {column} must be 1 while "
                             f"the life survives to the valuation date, death_mth_{life} "
                             f"blank, negative or duration_mth or later, and 0 once it "
                             f"has died; it is not at point_id {bad}")
    form = table["form"]
    certain = (form.isin(["life_certain", "certain_only"])
               & (pd.to_numeric(table["certain_months"], errors="coerce") > 0)  # noqa: F821
               | (form == "installment_refund"))
    may = (table["commutation_enabled"].astype(bool)
           & ~table["issue_state_excludes_withdrawal"].astype(bool)
           & certain & (months >= 13))
    bad = table.index[(theta > 0) & ~may].tolist()
    if bad:
        raise ValueError(f"{name}: commute_frac_cum_init must be 0 unless a commutation "
                         f"could have been taken before the valuation date: the right "
                         f"held, the issue state allowing it, a certain period, and "
                         f"duration_mth 13 or more; it is not at point_id {bad}")
    return table.assign(death_mth_1=deaths[1], death_mth_2=deaths[2])


def mort_table():
    """The base annuitant mortality table by age and sex, read from *mort_table.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file, index_col=["age", "sex"])     # noqa: F821


def improvement_scale():
    """The generational improvement scale by age and sex, from *improvement_scale.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / improvement_scale_file, index_col=["age", "sex"])  # noqa: F821


def surr_charge_table():
    """The commutation surrender-charge scale by contract year, *surr_charge_table.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / surr_charge_file, index_col="policy_year")     # noqa: F821


def surr_charge_scale():
    """The surrender-charge scale by contract year, as :func:`surr_charge_table` reads it,
    checked.

    The rates of *surr_charge_table.csv*, indexed by its policy years read by value, as
    ``SPIA_US_S``'s lookup matches them, so that a year written ``2.0`` is year 2.
    ``Projection.surr_charge_rate`` takes the scale's first and last years and its rates
    from here, so the extents and the values come from one checked column. A year that is
    not a whole number, text and a blank among them, is refused, naming every such year;
    so is a scale with no year, or whose years do not run from the first to the last
    without a gap or a repeat, from year 1 on, each with a rate. ``SPIA_US_S`` takes
    ``int()`` of the raw years for the extents, so a year written ``x`` raises Python's own
    message there, and one written ``3a`` turns the years to text and makes every lookup
    miss.
    """
    file = surr_charge_file                                          # noqa: F821
    tbl = surr_charge_table()
    if len(tbl) == 0:
        raise ValueError(f"{file} has no policy year")
    years = pd.to_numeric(pd.Series(tbl.index), errors="coerce")     # noqa: F821
    bad = tbl.index[~(years % 1 == 0).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{file}: a policy year must be a whole number; {bad} is not")
    whole = years.astype("int64").tolist()
    first, last = min(whole), max(whole)
    rates = pd.to_numeric(tbl["surr_charge_rate"], errors="coerce")  # noqa: F821
    if (first < 1 or sorted(whole) != list(range(first, last + 1))
            or rates.isna().any()):
        raise ValueError(f"{file}: the policy years must run from {first} to {last} "
                         f"without a gap or a repeat, from 1 on, each with a rate")
    return pd.DataFrame(                                             # noqa: F821
        {"surr_charge_rate": rates.to_numpy(dtype="float64")},
        index=pd.Index(whole, name="policy_year"))                   # noqa: F821


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table_sec.csv"

mort_table_file = "mort_table.csv"

improvement_scale_file = "improvement_scale.csv"

surr_charge_file = "surr_charge_table.csv"

future_horizon_mth = 120

pd = ("Module", "pandas")