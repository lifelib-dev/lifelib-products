# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The eight input CSVs are read here, **once per model**, and referenced from
:mod:`~.UL_US_SEC.Projection` as ``data``. :mod:`~.UL_US_SEC.Projection` is
parameterized by ``point_id``, so each ``Projection[N]`` is a separate ItemSpace with
its own cells cache; if the readers lived there, every model point would re-read every
file. Holding them in an unparameterized Space reads each file once no matter how many
policies are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/universal_life/``, rather than data stored inside the model. The model
folder therefore holds nothing but formulas -- no ``_data/``, no IOSpec, no embedded
values -- so a diff of the model shows logic changes only. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``UL_US_SEC`` folder without its parent's CSVs produces a model that reads and
then fails on first evaluation.

**Seven of the tables are UL_US_S's.** The guaranteed COI scale, the corridor factors,
the mortality table, the class factors, the lapse table, the premium persistency scale
and the surrender charge schedules are the files :mod:`~.UL_US_S` reads, read here in
place: one copy of each table serves both models, so an edit to one reaches both. The
model point table is this model's own, ``model_point_table_sec.csv``; it sits beside
``UL_US_S``'s ``model_point_table.csv``, which this model never opens.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so
the model works wherever the repository is checked out. Each table has a filename
Reference and a reader Cells:

======================  ==========================  ==============================
Reference               Cells                       File
======================  ==========================  ==============================
model_point_file        model_point_table()         model_point_table_sec.csv
coi_rates_file          coi_rates()                 coi_rates.csv
corridor_file           corridor_factors()          corridor_factors.csv
mort_table_file         mort_table()                mort_table.csv
class_factor_file       class_factor_table()        class_factor_table.csv
lapse_table_file        lapse_table()               lapse_table.csv
prem_persistency_file   prem_persistency_table()    prem_persistency.csv
surr_charge_file        surr_charge_table()         surr_charge_table.csv
======================  ==========================  ==============================

**The model point table is checked as it is read.** Eight of its columns are the
in-force interface: ``policy_count`` and ``duration_mth``, as in
``basiclife.BasicTerm_SE``, and the six columns of an in-force policy's opening state.
:func:`model_point_table` refuses a table that lacks any of them, repeats a
``point_id``, holds a count or a duration no policy can have, or holds an opening state
no policy can be in. The checks run in turn, and the first that fails raises, naming the
missing column or every point that fails it. It also refuses a policy to be issued more
than ``future_horizon_mth`` months after the valuation date, 120 months as shipped:
future new business is written over a stated horizon, so that no frame runs longer than
the projection from issue plus that horizon. Set to 0, the Reference refuses future new
business altogether. Whether a point is still inside the projection at the valuation
date is a rule of the product rather than of the table, and ``Projection.proj_len``
checks it.

**So are the seven assumption tables.**  Each table read at a policy year or an attained
age has one reader in ``Projection``, keyed by the year or the age, and that reader takes
the table's extent -- the last policy year, or the first and last ages, beyond which it
reads the nearest row -- from a cell here that reads the key column by value, once, and
checks the table: :func:`prem_persistency_last_year`, :func:`lapse_last_year`,
:func:`corridor_age_first` and :func:`corridor_age_last`, :func:`mort_age_first` and
:func:`mort_age_last`, and, for each issue-age cell of the COI scale,
:func:`coi_rate_last_years`.  A key that is blank, text or not a whole number is
refused, naming the file, the column and the lines it is on.  So are keys that do not run
one row a year or an age, without a gap or a repeat, policy years from 1, the message
naming each key that repeats, with its lines, and each that is missing.  And so is a rate
that is blank, text or infinite, naming the column and its lines.  :func:`class_count`
and :func:`surr_charge_count` check the class factors and the surrender-charge schedules
the same way, for the per-point joins that read them.  Each reader asks for its extent,
or the count, before it reads a value, so a projection meets the checks first.

``UL_US_S``'s readers take the extent from the key column as pandas reads it, where a blank
key is a missing value the extent skips: the table is cut short, and every later year reads
the last good row, without a word.  A blank rate is a missing value to it too, which shows
in its flows or is lost in a ``min`` or a ``max``: a blank lapse rate reads as the cap of
35%, a blank corridor factor as no corridor and a blank surrender charge as none.  Here
a blank rate or class factor would make the mortality rate a missing value, as in
``UL_US_S``, and every flow after it, so each is refused, by name.

``coi_rates.csv`` carries the *guaranteed maximum* monthly rate per $1,000 of net
amount at risk; the current scale is the guaranteed scale times
``Projection.coi_curr_factor``, because current COI scales are not published **[std]**.
``mort_table.csv`` is a small illustrative best-estimate table **[std]**, not a
published one -- the notes forbid hard-coding the licensed 2015 VBT and 2017 CSO
families. To swap in a licensed basis, replace the file with a same-schema one, or
point ``mort_table_file`` at a different name before the model computes anything. No
formula changes. Replacing the file changes :mod:`~.UL_US_S` too, which reads the same
one.
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

    Indexed by ``point_id``.  Eight columns are the in-force interface: ``policy_count``
    and ``duration_mth``, the completed policy months at the valuation date, as in
    ``basiclife.BasicTerm_SE``, and the six columns of the opening state, per policy, as
    the policy stands at the start of month 0, before any month-0 event:

    * ``av_pp_init`` and ``loan_bal_init``: the account value and the loan entering month
      0, ``UL_US_S``'s own two columns;
    * ``sum_assured_init``: the face in force entering month 0, after every withdrawal
      cut to date;
    * ``wd_used_year_init``: the free withdrawal allowance already used in the policy
      year under way;
    * ``cum_prem_init``: the premiums less withdrawals paid before the valuation date;
    * ``is_mec_init``: the MEC latch, an int code, 1 for a policy that has already
      failed the 7-pay test and 0 for one that has not.

    The rest are ``UL_US_S``'s, except ``row_kind``, ``source_policy_id`` and
    ``source_mth``, which record where the generator took each shipped row from and which
    no formula reads.

    The checks run over the whole table at once, and the first that fails raises
    ``ValueError``, naming the missing column or every point it fails on:

    * the eight in-force columns are present;
    * no ``point_id`` appears twice;
    * ``policy_count`` is a number, zero or more;
    * ``duration_mth`` is a whole number of months: positive for a policy in force, 0
      for one issued at the valuation date, negative for one issued later;
    * no policy is issued more than ``future_horizon_mth`` months after the valuation
      date, so ``duration_mth`` is ``-future_horizon_mth`` or more.  At 0 the model takes
      no future new business, and the message says so; a negative horizon is itself
      refused;
    * the account value, the loan, the face and the year's usage are each a number, zero
      or more.  A balance is never negative in force.  ``UL_US_S`` lets a point's account
      value fall below zero once it is in permanent shortfall, because it does not
      implement the grace cascade that would end such a policy; no policy in force can
      hold that balance, so a point in permanent shortfall is restated no later than the
      last month its account value is still zero or more.  Without a loan that is the
      month its shortfall begins, as point 7 is; with one, the shortfall test, which nets
      the loan, fails months earlier;
    * ``cum_prem_init`` is a number, of either sign.  Premiums less withdrawals is a tax
      measure, not a balance, and withdrawals taken in full count against it **[std]**;
    * ``is_mec_init`` is 0 or 1, an int code; 1.0 reads as True;
    * a policy not yet in force, ``duration_mth`` 0 or less, has no opening state: it is
      issued with none, at the face :func:`~.UL_US_SEC.Projection.sum_assured`;
    * ``sum_assured_init`` is above 0 on a policy in force, which holds a face, so an
      extract that leaves the column at zero is refused rather than projected on the
      corridor alone;
    * ``sum_assured_init`` is at most ``sum_assured``, the face at issue, since face
      increases are not modelled.  A face below it is accepted, whether a withdrawal cut
      it or an elective decrease the model does not implement, and is projected from the
      value given;
    * on a point valued on a policy anniversary, ``duration_mth`` a multiple of 12,
      ``wd_used_year_init`` is 0: the year's free allowance restarts there, before any
      usage is read, so any other value would be dropped without a word;
    * ``is_mec_init`` is 1 where the 7-pay test has already failed in the month before
      the valuation date: ``cum_prem_init`` above ``seven_pay_prem`` times the policy
      years to date, in the first seven.  An earlier failure the cumulative premium no
      longer shows is the column's to record, and is accepted either way.
    """
    name = model_point_file                                          # noqa: F821
    table = pd.read_csv(input_dir() / name, index_col="point_id")    # noqa: F821
    state = ("av_pp_init", "loan_bal_init", "sum_assured_init", "wd_used_year_init",
             "cum_prem_init", "is_mec_init")
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
    values = {}
    for column in state:
        values[column] = pd.to_numeric(table[column], errors="coerce")  # noqa: F821
    v = values["av_pp_init"]
    bad = table.index[~((v >= 0) & (v < float("inf")))].tolist()
    if bad:
        raise ValueError(f"{name}: av_pp_init must be a number, zero or more: no policy "
                         f"in force holds a negative account value, so restate a point in "
                         f"permanent shortfall no later than the last month its account "
                         f"value is still zero or more; it is not at point_id {bad}")
    for column in ("loan_bal_init", "sum_assured_init", "wd_used_year_init"):
        v = values[column]
        bad = table.index[~((v >= 0) & (v < float("inf")))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a number, zero or more; it is "
                             f"not at point_id {bad}")
    v = values["cum_prem_init"]
    bad = table.index[~(v.abs() < float("inf"))].tolist()
    if bad:
        raise ValueError(f"{name}: cum_prem_init must be a number; it is not at "
                         f"point_id {bad}")
    bad = table.index[~values["is_mec_init"].isin([0, 1])].tolist()
    if bad:
        raise ValueError(f"{name}: is_mec_init must be 0 or 1, an int code; it is not "
                         f"at point_id {bad}")
    for column in state:
        bad = table.index[(months <= 0) & (values[column] != 0)].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be 0 on a policy not yet in force, "
                             f"duration_mth 0 or less; it is not at point_id {bad}")
    bad = table.index[(months > 0) & ~(values["sum_assured_init"] > 0)].tolist()
    if bad:
        raise ValueError(f"{name}: sum_assured_init must be above 0 on a policy in force, "
                         f"duration_mth above 0, which holds a face; it is not at "
                         f"point_id {bad}")
    face = pd.to_numeric(table["sum_assured"], errors="coerce")      # noqa: F821
    bad = table.index[(months > 0) & ~(values["sum_assured_init"] <= face)].tolist()
    if bad:
        raise ValueError(f"{name}: sum_assured_init must be at most sum_assured, the "
                         f"face at issue, since face increases are not modelled; it is "
                         f"not at point_id {bad}")
    on_anniv = (months > 0) & (months % 12 == 0)
    bad = table.index[on_anniv & (values["wd_used_year_init"] != 0)].tolist()
    if bad:
        raise ValueError(f"{name}: wd_used_year_init must be 0 on a point valued on a "
                         f"policy anniversary, duration_mth a multiple of 12, where the "
                         f"year's free allowance restarts; it is not at point_id {bad}")
    year = (months - 1) // 12 + 1
    limit = (pd.to_numeric(table["seven_pay_prem"], errors="coerce")  # noqa: F821
             * year.where(year <= 7, 7))
    failed = (months > 0) & (year <= 7) & (values["cum_prem_init"] > limit)
    bad = table.index[failed & (values["is_mec_init"] != 1)].tolist()
    if bad:
        raise ValueError(f"{name}: is_mec_init must be 1 where the 7-pay test has "
                         f"already failed, cum_prem_init above seven_pay_prem times the "
                         f"policy years to date, in the first seven; it is not at "
                         f"point_id {bad}")
    return table


def coi_rates():
    """Guaranteed maximum monthly COI rates, read from *coi_rates.csv*.

    Per $1,000 of net amount at risk, keyed by issue-age cell and policy year.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / coi_rates_file,                                # noqa: F821
        index_col=["sex", "rate_class", "age_at_entry", "policy_year"])


def corridor_factors():
    """The GPT corridor factor table by attained age, from *corridor_factors.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / corridor_file, index_col="age")                # noqa: F821


def mort_table():
    """The best-estimate annual mortality table by age, read from *mort_table.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file, index_col="age")              # noqa: F821


def class_factor_table():
    """The underwriting-class factors, read from *class_factor_table.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / class_factor_file, index_col="rate_class")     # noqa: F821


def lapse_table():
    """The base annual lapse rates by policy year, read from *lapse_table.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / lapse_table_file, index_col="policy_year")     # noqa: F821


def prem_persistency_table():
    """Premium persistency (paid/planned) by policy year, from *prem_persistency.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / prem_persistency_file,                         # noqa: F821
        index_col="policy_year")


def surr_charge_table():
    """The surrender charge schedules, read from *surr_charge_table.csv*.

    One row per ``surr_charge_id``, giving the initial charge per $1,000 of initial
    face and the number of years over which it runs off linearly.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / surr_charge_file,                              # noqa: F821
        index_col="surr_charge_id")


def prem_persistency_last_year():
    """The last policy year *prem_persistency.csv* gives a factor for, the table checked.

    The ``policy_year`` column is read by value, once, as the lookup matches it, so a year
    written ``16.0`` is year 16.  A key that is blank, text or not a whole number is
    refused, naming the file, the column and the lines it is on.  So are policy years
    that do not run from 1, one row a year, without a gap or a repeat: the message names
    each year that repeats or falls below 1, with its lines, and each year missing from 1
    to the last.  And so is a ``prem_persistency`` factor that is blank, text or infinite,
    naming its lines.  ``Projection.prem_persistency_py``, the table's one reader, takes
    its extent from here before it reads a factor, so a projection meets the checks first.
    """
    name = prem_persistency_file                                     # noqa: F821
    table = prem_persistency_table()
    years = pd.to_numeric(pd.Series(table.index), errors="coerce")   # noqa: F821
    bad = (years.index[~(years % 1 == 0)] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: policy_year must be a whole number; it is not on line "
                         f"{bad}")
    years = years.astype("int64")
    faults = []
    for key in sorted(set(years[years.duplicated() | (years < 1)])):
        faults.append(f"policy_year {key} is on line "
                      f"{(years.index[years == key] + 2).tolist()}")
    run = [0] + sorted(set(years[years >= 1]))
    if len(run) == 1:
        faults.append("no line holds policy_year 1")
    for a, b in zip(run, run[1:]):
        if b - a > 1:
            faults.append(f"no line holds policy_year {a + 1}"
                          + (f" to {b - 1}" if b - a > 2 else ""))
    if faults:
        raise ValueError(f"{name}: the policy years must run from 1, one row a year, "
                         f"without a gap or a repeat; " + "; ".join(faults))
    factors = pd.to_numeric(pd.Series(table["prem_persistency"].to_numpy()),  # noqa: F821
                            errors="coerce")
    bad = (factors.index[~(factors.abs() < float("inf"))] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: prem_persistency must be a number; it is not on line "
                         f"{bad}")
    return int(years.max())


def lapse_last_year():
    """The last policy year *lapse_table.csv* gives a rate for, the table checked.

    Read and checked as :func:`prem_persistency_last_year` reads and checks its own
    table, the rate checked being ``lapse_rate_ann``.  ``Projection.lapse_rate_base_py``,
    the table's one reader, takes its extent from here before it reads a rate.
    """
    name = lapse_table_file                                          # noqa: F821
    table = lapse_table()
    years = pd.to_numeric(pd.Series(table.index), errors="coerce")   # noqa: F821
    bad = (years.index[~(years % 1 == 0)] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: policy_year must be a whole number; it is not on line "
                         f"{bad}")
    years = years.astype("int64")
    faults = []
    for key in sorted(set(years[years.duplicated() | (years < 1)])):
        faults.append(f"policy_year {key} is on line "
                      f"{(years.index[years == key] + 2).tolist()}")
    run = [0] + sorted(set(years[years >= 1]))
    if len(run) == 1:
        faults.append("no line holds policy_year 1")
    for a, b in zip(run, run[1:]):
        if b - a > 1:
            faults.append(f"no line holds policy_year {a + 1}"
                          + (f" to {b - 1}" if b - a > 2 else ""))
    if faults:
        raise ValueError(f"{name}: the policy years must run from 1, one row a year, "
                         f"without a gap or a repeat; " + "; ".join(faults))
    rates = pd.to_numeric(pd.Series(table["lapse_rate_ann"].to_numpy()),  # noqa: F821
                          errors="coerce")
    bad = (rates.index[~(rates.abs() < float("inf"))] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: lapse_rate_ann must be a number; it is not on line "
                         f"{bad}")
    return int(years.max())


def corridor_age_last():
    """The last attained age *corridor_factors.csv* gives a factor for, the table checked.

    The ``age`` column is read by value, once, so an age written ``40.0`` is 40.  A key
    that is blank, text or not a whole number is refused, naming the file, the column and
    the lines it is on.  So are ages that do not run one row an age, without a gap or a
    repeat: the message names each age that repeats, with its lines, and each age missing
    between the first and the last.  And so is a ``corridor_factor`` that is blank, text
    or infinite, naming its lines.  ``Projection.corridor_factor_at``, the table's one
    reader, takes both of its extents, this and :func:`corridor_age_first`, before it
    reads a factor.
    """
    name = corridor_file                                             # noqa: F821
    table = corridor_factors()
    ages = pd.to_numeric(pd.Series(table.index), errors="coerce")    # noqa: F821
    bad = (ages.index[~(ages % 1 == 0)] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: age must be a whole number; it is not on line {bad}")
    ages = ages.astype("int64")
    faults = []
    for key in sorted(set(ages[ages.duplicated()])):
        faults.append(f"age {key} is on line {(ages.index[ages == key] + 2).tolist()}")
    run = sorted(set(ages))
    if not run:
        faults.append("no line holds an age")
    for a, b in zip(run, run[1:]):
        if b - a > 1:
            faults.append(f"no line holds age {a + 1}"
                          + (f" to {b - 1}" if b - a > 2 else ""))
    if faults:
        raise ValueError(f"{name}: the ages must run one row an age, without a gap or a "
                         f"repeat; " + "; ".join(faults))
    factors = pd.to_numeric(pd.Series(table["corridor_factor"].to_numpy()),  # noqa: F821
                            errors="coerce")
    bad = (factors.index[~(factors.abs() < float("inf"))] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: corridor_factor must be a number; it is not on line "
                         f"{bad}")
    return int(ages.max())


def corridor_age_first():
    """The first attained age *corridor_factors.csv* gives a factor for.

    Counted back from :func:`corridor_age_last`, which checks the table's keys first: the
    ages run one row an age, so the first is the last less the rows after it.
    """
    return corridor_age_last() - len(corridor_factors()) + 1


def mort_age_last():
    """The last attained age *mort_table.csv* gives a rate for, the table checked.

    Read and checked as :func:`corridor_age_last` reads and checks its own table, the rate
    checked being ``mort_rate``.  ``Projection.mort_rate_base_at``, the table's one
    reader, takes both of its extents, this and :func:`mort_age_first`, before it reads a
    rate.  A blank rate is a missing value to ``UL_US_S``, whose mortality is then not a
    number, and to ``Projection.mort_rate``, whose cap, ``min(q, 1.0)``, keeps it missing.
    """
    name = mort_table_file                                           # noqa: F821
    table = mort_table()
    ages = pd.to_numeric(pd.Series(table.index), errors="coerce")    # noqa: F821
    bad = (ages.index[~(ages % 1 == 0)] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: age must be a whole number; it is not on line {bad}")
    ages = ages.astype("int64")
    faults = []
    for key in sorted(set(ages[ages.duplicated()])):
        faults.append(f"age {key} is on line {(ages.index[ages == key] + 2).tolist()}")
    run = sorted(set(ages))
    if not run:
        faults.append("no line holds an age")
    for a, b in zip(run, run[1:]):
        if b - a > 1:
            faults.append(f"no line holds age {a + 1}"
                          + (f" to {b - 1}" if b - a > 2 else ""))
    if faults:
        raise ValueError(f"{name}: the ages must run one row an age, without a gap or a "
                         f"repeat; " + "; ".join(faults))
    rates = pd.to_numeric(pd.Series(table["mort_rate"].to_numpy()),  # noqa: F821
                          errors="coerce")
    bad = (rates.index[~(rates.abs() < float("inf"))] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: mort_rate must be a number; it is not on line {bad}")
    return int(ages.max())


def mort_age_first():
    """The first attained age *mort_table.csv* gives a rate for.

    Counted back from :func:`mort_age_last`, which checks the table's keys first, as
    :func:`corridor_age_first` counts its own.
    """
    return mort_age_last() - len(mort_table()) + 1


def coi_rate_last_years():
    """The last policy year of each issue-age cell of *coi_rates.csv*, the table checked.

    A Series of ints, indexed by ``sex``, ``rate_class`` and ``age_at_entry``: one entry a
    cell, the rows the scale of a point on that cell is sliced from.  The two text keys
    may not be blank, and the two numeric keys, ``age_at_entry`` and ``policy_year``, are
    read by value, once: a key that is blank, text or not a whole number is refused,
    naming the file, the column and the lines it is on.  So is a cell whose policy years
    do not run from 1, one row a year, without a gap or a repeat: the message names the
    cell, each year that repeats or falls below 1, with its lines, and each year missing
    from 1 to the last.  And so is a ``coi_rate_guar`` that is blank, text or infinite,
    naming its lines.  ``Projection.coi_rate_last_year`` takes a point's extent from here
    before ``Projection.coi_rate_guar_py`` reads its scale.
    """
    name = coi_rates_file                                            # noqa: F821
    rates = coi_rates().reset_index()
    for column in ("sex", "rate_class"):
        bad = (rates.index[rates[column].isna()] + 2).tolist()
        if bad:
            raise ValueError(f"{name}: {column} must not be blank; it is on line {bad}")
    for column in ("age_at_entry", "policy_year"):
        keys = pd.to_numeric(rates[column], errors="coerce")         # noqa: F821
        bad = (rates.index[~(keys % 1 == 0)] + 2).tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a whole number; it is not on line "
                             f"{bad}")
    rates = rates.assign(
        age_at_entry=pd.to_numeric(rates["age_at_entry"]).astype("int64"),  # noqa: F821
        policy_year=pd.to_numeric(rates["policy_year"]).astype("int64"))    # noqa: F821
    years = rates.groupby(["sex", "rate_class", "age_at_entry"])["policy_year"]
    last = years.max()
    count = years.count()
    run = (years.min() == 1) & (last == count) & (years.nunique() == count)
    faults = []
    for cell in last.index[~run].tolist():
        held = years.get_group(cell)
        for key in sorted(set(held[held.duplicated() | (held < 1)])):
            faults.append(f"at {cell}, policy_year {key} is on line "
                          f"{(held.index[held == key] + 2).tolist()}")
        cell_run = [0] + sorted(set(held[held >= 1]))
        if len(cell_run) == 1:
            faults.append(f"at {cell}, no line holds policy_year 1")
        for a, b in zip(cell_run, cell_run[1:]):
            if b - a > 1:
                faults.append(f"at {cell}, no line holds policy_year {a + 1}"
                              + (f" to {b - 1}" if b - a > 2 else ""))
    if faults:
        raise ValueError(f"{name}: the policy years of each sex, rate_class and "
                         f"age_at_entry must run from 1, one row a year, without a gap or "
                         f"a repeat; " + "; ".join(faults))
    values = pd.to_numeric(rates["coi_rate_guar"], errors="coerce")  # noqa: F821
    bad = (rates.index[~(values.abs() < float("inf"))] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: coi_rate_guar must be a number; it is not on line "
                         f"{bad}")
    return last


def class_count():
    """The number of classes *class_factor_table.csv* gives a factor for, the table checked.

    A ``rate_class`` that is blank is refused, naming the file and the lines it is on, and
    so is one on more than one row, naming each such class with its lines; and so is a
    ``factor`` that is blank, text or infinite, naming its lines.
    ``Projection.class_factor``, the table's one reader, asks for the count before it reads
    a factor, so a projection meets the checks first.  A blank factor is a missing value to
    ``UL_US_S``, whose mortality is then not a number, and to ``Projection.mort_rate``,
    whose cap, ``min(q, 1.0)``, keeps it missing.
    """
    name = class_factor_file                                         # noqa: F821
    table = class_factor_table()
    classes = pd.Series(table.index)                                 # noqa: F821
    bad = (classes.index[classes.isna()] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: rate_class must not be blank; it is on line {bad}")
    faults = []
    for label in sorted(set(classes[classes.duplicated()])):
        faults.append(f"rate_class {label} is on line "
                      f"{(classes.index[classes == label] + 2).tolist()}")
    if faults:
        raise ValueError(f"{name}: each rate_class must have one row; "
                         + "; ".join(faults))
    factors = pd.to_numeric(pd.Series(table["factor"].to_numpy()),   # noqa: F821
                            errors="coerce")
    bad = (factors.index[~(factors.abs() < float("inf"))] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: factor must be a number; it is not on line {bad}")
    return len(table)


def surr_charge_count():
    """The number of schedules *surr_charge_table.csv* gives, the table checked.

    A ``surr_charge_id`` that is blank is refused, naming the file and the lines it is on,
    and so is one on more than one row, naming each such schedule with its lines; and so
    is a ``sc_per_1000_init`` or a ``runoff_years`` that is blank, text or infinite,
    naming the column and its lines.  ``Projection.surr_charge_rate_max`` and
    ``Projection.surr_charge_runoff_years``, the table's two readers, ask for the count
    before they read a value, so a projection meets the checks first.  A blank charge is a
    missing value to ``UL_US_S``, whose surrender charge rate, the ``max`` of 0 and the
    charge left, is then 0 in every month, as though the schedule had run off.
    """
    name = surr_charge_file                                          # noqa: F821
    table = surr_charge_table()
    ids = pd.Series(table.index)                                     # noqa: F821
    bad = (ids.index[ids.isna()] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: surr_charge_id must not be blank; it is on line {bad}")
    faults = []
    for label in sorted(set(ids[ids.duplicated()])):
        faults.append(f"surr_charge_id {label} is on line "
                      f"{(ids.index[ids == label] + 2).tolist()}")
    if faults:
        raise ValueError(f"{name}: each surr_charge_id must have one row; "
                         + "; ".join(faults))
    for column in ("sc_per_1000_init", "runoff_years"):
        values = pd.to_numeric(pd.Series(table[column].to_numpy()),  # noqa: F821
                               errors="coerce")
        bad = (values.index[~(values.abs() < float("inf"))] + 2).tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a number; it is not on line "
                             f"{bad}")
    return len(table)


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table_sec.csv"

coi_rates_file = "coi_rates.csv"

corridor_file = "corridor_factors.csv"

mort_table_file = "mort_table.csv"

class_factor_file = "class_factor_table.csv"

lapse_table_file = "lapse_table.csv"

prem_persistency_file = "prem_persistency.csv"

surr_charge_file = "surr_charge_table.csv"

future_horizon_mth = 120

pd = ("Module", "pandas")