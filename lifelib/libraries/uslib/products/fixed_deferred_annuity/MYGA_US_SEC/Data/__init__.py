# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-contract projection.

The seven input CSVs are read here, **once per model**, and referenced from
:mod:`~.MYGA_US_SEC.Projection` as ``data``. :mod:`~.MYGA_US_SEC.Projection` is
parameterized by ``point_id``, so each ``Projection[N]`` is a separate ItemSpace with its
own cells cache; if the readers lived there, every model point would re-read every file.
Holding them in an unparameterized Space reads each file once no matter how many
contracts are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/fixed_deferred_annuity/``, rather than data stored inside the model. The model
folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded
values — so a diff of the model shows logic changes only. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``MYGA_US_SEC`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

**Six of the tables are MYGA_US_S's.** The mortality table, the surrender charge
schedules and their attained-age cap, the rate scenarios, the withdrawal programmes and
the declared-differential MVA factors are the files :mod:`~.MYGA_US_S` reads, read here in
place: one copy of each table serves both models, so an edit to one reaches both. The
model point table is this model's own, ``model_point_table_sec.csv``; it sits beside
``MYGA_US_S``'s ``model_point_table.csv``, which this model never opens.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so the
model works wherever the repository is checked out. Each table has a filename Reference
and a reader Cells:

=========================  ==============================  ==========================
Reference                  Cells                           File
=========================  ==============================  ==========================
model_point_file           model_point_table()             model_point_table_sec.csv
mort_table_file            mort_table()                    mort_table.csv
surr_charge_file           surr_charge_table()             surr_charge_table.csv
surr_charge_age_cap_file   surr_charge_age_cap_table()     surr_charge_age_cap.csv
rate_scenario_file         rate_scenario()                 rate_scenario.csv
withdrawal_file            withdrawal_table()              withdrawal_table.csv
mva_factor_file            mva_factor_table()              mva_factor_table.csv
=========================  ==============================  ==========================

**The model point table is checked as it is read.** Twelve of its columns are the
in-force interface: ``policy_count`` and ``duration_mth``, as in
``basiclife.BasicTerm_SE``, and the ten columns of an in-force contract's opening state.
:func:`model_point_table` refuses a table that lacks any of them, repeats a ``point_id``,
holds a count or a duration no contract can have, holds an opening state no contract
can be in, or holds a key that the table it joins lacks: a scenario that sets no level by
the point's first month on the books, a withdrawal programme, or a sex and an attained
age the mortality table gives no rate at. The checks run in turn, and the first that
fails raises, naming the missing column or every point that fails it. It also refuses a
contract to be issued more than ``future_horizon_mth`` months after the valuation date,
120 months as shipped: future new business is written over a stated horizon, so that no
frame runs longer than cover from issue plus that horizon. Set to 0, the Reference
refuses future new business altogether. Whether a point is still in cover at the
valuation date is a rule of the product rather than of the table, and
``Projection.proj_len`` checks it.

**So are the keys of the six assumption tables.** Each table's reader above is
``MYGA_US_S``'s, unchanged, and beside it a cell reads the table's keys by value, once,
checks them and its values, and returns the table indexed by the checked keys:
:func:`mort_rates`, :func:`surr_charge_scales`, :func:`surr_charge_age_caps`,
:func:`rate_scenario_steps`, :func:`wd_schedules` and :func:`mva_factors`. The
projection reads each table there and nowhere else, and takes the age cap's extents,
:func:`surr_charge_age_cap_first` and :func:`surr_charge_age_cap_last`, and the
duration factors' last year, :func:`mva_factor_last_year`, from the same checked keys, so
a projection meets each table's check before it reads a value. A key that is not a whole
number, text and a blank among them, is refused, naming the file, the column and the
lines it is on, and so are a blank text key, a value that is not a number in its range,
a repeated key, and, where the projection reads every year or age between a table's first
and last, keys that do not run one row a year or an age, and so is a surrender charge
table without both the schedules the projection reads. A key written as a float, ``1.0``,
is the whole number it holds, as ``MYGA_US_S``'s lookups match it. Those lookups take the
keys as pandas reads them: one key written as text turns its whole column to text, so that
every lookup misses, and a surrender charge or a withdrawal is then zero without a word,
or the read raises a ``KeyError`` that names no file.

Four of the tables carry a compound key. ``surr_charge_table`` is indexed by
``(schedule, contract_year)`` so the initial 9/8/7/6/5 schedule [S10] and the renewal
5/4/3/2/1 schedule [S2] sit in one file; ``mort_table`` by ``(age, sex)``;
``rate_scenario`` by ``(scenario_id, t)``, read as a step function of ``t``, and
``withdrawal_table`` by ``(wd_schedule_id, t)``, an exact-key lookup, so a scenario or a
withdrawal programme is a handful of rows rather than one row per month. The two ``t`` are
on different clocks. A scenario's ``t`` is a
**valuation** month: the scenario is a path in calendar time, shared by every contract of
a block, and a row keyed ``t = 12`` holds from twelve months after the valuation date. A
withdrawal's ``t`` is a **policy** month, read at ``duration_mth(t)``: a row keyed
``t = 12`` falls in the first month of contract year 2, however old the contract is at
the valuation date.

To swap in a licensed mortality basis — the 2012 IAM Basic table with Projection Scale G2
and the VM-22 Table 6.7 factors that the notes prescribe and that may not be redistributed
here — replace ``mort_table.csv`` with a same-schema file, or point ``mort_table_file`` at
a different name, before the model computes anything. No formula changes. Replacing a file
changes :mod:`~.MYGA_US_S` too, which reads the same ones.
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

    Inputs are *external* files, not data stored inside the model, so the model folder
    is pure formulas.  The path is resolved at run time from where the model was read,
    following ``annuallife.TradLife_A``.
    """
    return _model.path.parent                                        # noqa: F821


def model_point_table():
    """The model point table, read from *model_point_table_sec.csv* and checked.

    Indexed by ``point_id``. Twelve columns are the in-force interface: ``policy_count``
    and ``duration_mth``, the completed policy months at the valuation date, as in
    ``basiclife.BasicTerm_SE``, and the ten columns of the opening state, per contract,
    as the contract stands at the start of month 0, before any month-0 event:

    * ``av_pp_init``, ``mgsv_pp_init`` and ``prem_accum_gmir_pp_init``: the account
      value, the Model #805 floor and ``P_accum@GMIR`` entering month 0;
    * ``interest_credited_pp_init``: the interest credited from issue to the valuation
      date;
    * ``interest_credited_pp_prev_anniv_init``: the same to the anniversary on or before
      the valuation date, the one that opened the contract year under way;
    * ``free_wd_allow_init`` and ``free_wd_remain_init``: that year's free-withdrawal
      allowance, and the part of it unused entering month 0;
    * ``tax_basis_pp_init``: the IRC 72 basis entering month 0, or at issue for a
      contract not yet in force; ``MYGA_US_S``'s ``tax_basis_initial``, renamed;
    * ``credit_rate_init`` and ``mva_ref_yield_locked_init``: the declared rate and the
      MVA reference yield ``i0`` in force entering month 0.

    The rest are ``MYGA_US_S``'s, except ``row_kind``, ``source_policy_id`` and
    ``source_mth``, which record where the generator took each shipped row from and which
    no formula reads.

    The checks run over the whole table at once, and the first that fails raises
    ``ValueError``, naming the missing column or every point it fails on:

    * the twelve in-force columns are present;
    * no ``point_id`` appears twice;
    * ``policy_count`` is a number, zero or more;
    * ``duration_mth`` is a whole number of months: positive for a contract in force, 0
      for one issued at the valuation date, negative for one issued later;
    * ``age_at_entry`` and ``guar_period`` are whole numbers of years. ``MYGA_US_S`` reads
      both by ``int()``, which would truncate a fraction without a word, and the
      initial-term check below reads ``guar_period`` as written;
    * ``guar_period`` is 1 year or more: at 0 the guarantee-period index divides by zero,
      naming no point, and below it the projection runs a period no contract has;
    * no contract is issued more than ``future_horizon_mth`` months after the valuation
      date, so ``duration_mth`` is ``-future_horizon_mth`` or more. At 0 the model takes
      no future new business, and the message says so; a negative horizon is itself
      refused;
    * the account value, the two interest columns, the allowance, the remainder and the
      basis are each a finite number, zero or more;
    * the floor, ``P_accum``, the declared rate and ``i0`` are each a finite number. The
      first two may be negative: every withdrawal is deducted from both, and nothing
      floors either;
    * a contract not yet in force, ``duration_mth`` 0 or less, has no opening state:
      every state column is 0 but ``tax_basis_pp_init``, its basis at issue;
    * a contract in force, ``duration_mth`` 1 or more, has an account value above 0: one
      fully withdrawn is no longer in force, and the dynamic lapse, which reads the
      surrender benefit as a share of the account value, would have nothing to divide by;
    * in the first contract year, ``duration_mth`` 1 to 11, the year opened at issue
      with nothing credited, so ``interest_credited_pp_prev_anniv_init`` is 0, and
      ``free_wd_allow_init`` is the issue allowance, ``free_wd_rate x premium`` under
      ``pct_av`` and 0 under ``interest_only``;
    * on a point valued on a policy anniversary, ``duration_mth`` a multiple of 12, the
      interest at the anniversary equals the interest entering month 0: the two are one
      instant;
    * the interest at the anniversary does not exceed the interest to the valuation date;
    * under ``interest_only``, from the second contract year on, ``duration_mth`` 12 or
      more, the year's allowance, the interest credited over the year before, does not
      exceed the interest credited to the anniversary that opened the year, and in the
      second contract year, ``duration_mth`` 12 to 23, it is that interest, the first
      year's;
    * off an anniversary, the remainder does not exceed the year's allowance;
    * entering a month of the initial guarantee period, ``duration_mth`` 1 to
      ``12 x guar_period``, the first renewal month included, the declared rate and
      ``i0`` are ``declared_rate_initial`` and ``mva_ref_yield_at_issue``: the rate
      entering that month is still the initial one;
    * after it, the declared rate is the GMIR or more;
    * on a point valued on a policy anniversary under ``pct_av``, the year's allowance is
      ``free_wd_rate`` times the account value entering month 0, since the anniversary
      fixes the year's base at that value;
    * last, each point's keys into the tables it is joined with: its ``scenario_id`` is a
      scenario of :func:`rate_scenario_steps` that sets its levels by the first month the
      point is on the books, ``t = 0`` or its issue month if later; its
      ``wd_schedule_id`` is a programme of :func:`wd_schedules`; and :func:`mort_rates`
      gives a rate at its ``sex`` and its attained age in that first month. So reading
      the table reads those three tables, checked.

    Amounts of money are compared to a cent, so that an extract may carry each to the
    cent, as an administration system holds it. Each amount so carried is within half a
    cent of its exact value, so a rule that holds between the exact amounts can miss by
    half a cent from each: from the allowance, and from the base it is a share of, the
    account value or the premium, scaled by ``free_wd_rate``, 0.0055 in all at the
    product's 10%. A cent holds every such pair with room for the floating-point error of
    the comparison, where half a cent left the ties to it: point 11's allowance and
    account value, 12,432.034927 and 124,320.349270, carried as 12,432.03 and 124,320.35,
    are 0.005 apart, and so is an issue allowance carried as 864.18 or 864.19 at 7% of a
    premium of 12,345.50, which is 864.185. So are read an allowance of 10,445.00 on an
    account value of 104,449.99, and one of 7,000.00 at 7% of 100,000, which is
    7,000.000000000001 in floating point. A stale allowance, last year's or one a dollar
    out, is still refused.

    Accepted, because a contract can be in each state: a negative floor or ``P_accum``;
    any basis at issue on a contract not yet in force, 0 for a qualified one; on a point
    valued on an anniversary a remainder above the year's allowance, last year's, which
    lapses there unread; and a ``duration_mth``, an ``age_at_entry`` or a ``guar_period``
    written as a float, read as the whole number it holds.

    Left to the projection: an attained age past the mortality table's last before the
    deemed maturity raises a ``KeyError`` there, as in ``MYGA_US_S``, because the maturity
    age is a ``Projection`` Reference, which ``Data`` cannot read. The shipped table runs
    to 120, past every contract's cover.
    """
    name = model_point_file                                          # noqa: F821
    table = pd.read_csv(input_dir() / name, index_col="point_id")    # noqa: F821
    balances = ("av_pp_init", "interest_credited_pp_init",
                "interest_credited_pp_prev_anniv_init", "free_wd_allow_init",
                "free_wd_remain_init", "tax_basis_pp_init")
    signed = ("mgsv_pp_init", "prem_accum_gmir_pp_init", "credit_rate_init",
              "mva_ref_yield_locked_init")
    state = ("av_pp_init", "mgsv_pp_init", "prem_accum_gmir_pp_init",
             "interest_credited_pp_init", "interest_credited_pp_prev_anniv_init",
             "free_wd_allow_init", "free_wd_remain_init", "tax_basis_pp_init",
             "credit_rate_init", "mva_ref_yield_locked_init")
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
    for column in ("age_at_entry", "guar_period"):
        years = pd.to_numeric(table[column], errors="coerce")       # noqa: F821
        bad = table.index[~(years % 1 == 0)].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a whole number of years; it is "
                             f"not at point_id {bad}")
    period = pd.to_numeric(table["guar_period"], errors="coerce")      # noqa: F821
    bad = table.index[~(period >= 1)].tolist()
    if bad:
        raise ValueError(f"{name}: guar_period must be 1 year or more; it is not at "
                         f"point_id {bad}")
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
    for column in balances:
        v = values[column]
        bad = table.index[~((v >= 0) & (v < float("inf")))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a number, zero or more; it is "
                             f"not at point_id {bad}")
    for column in signed:
        v = values[column]
        bad = table.index[~((v > -float("inf")) & (v < float("inf")))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a number; it is not at "
                             f"point_id {bad}")
    for column in state:
        if column == "tax_basis_pp_init":
            continue
        bad = table.index[(months <= 0) & (values[column] != 0)].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be 0 on a policy not yet in force, "
                             f"duration_mth 0 or less; it is not at point_id {bad}")
    bad = table.index[(months > 0) & ~(values["av_pp_init"] > 0)].tolist()
    if bad:
        raise ValueError(f"{name}: av_pp_init must be more than 0 on a policy in force, "
                         f"duration_mth 1 or more: a contract fully withdrawn is not in "
                         f"force; it is not at point_id {bad}")
    # Amounts of money are compared to a cent, so that an extract may carry each to the
    # cent: half a cent from each of two amounts so carried, the base's scaled by the rate
    # (the docstring).
    cent = 0.01
    allow = values["free_wd_allow_init"]
    prior = values["interest_credited_pp_prev_anniv_init"]
    interest = values["interest_credited_pp_init"]
    first_year = (months > 0) & (months < 12)
    bad = table.index[first_year & (prior != 0)].tolist()
    if bad:
        raise ValueError(f"{name}: interest_credited_pp_prev_anniv_init must be 0 in the "
                         f"first policy year, duration_mth 1 to 11, which opened at issue "
                         f"with no interest credited; it is not at point_id {bad}")
    rate = pd.to_numeric(table["free_wd_rate"], errors="coerce")     # noqa: F821
    premium = pd.to_numeric(table["premium"], errors="coerce")       # noqa: F821
    pct_av = table["free_wd_rule"] == "pct_av"
    interest_only = table["free_wd_rule"] == "interest_only"
    issue = (rate * premium).where(pct_av, 0.0)
    bad = table.index[first_year & ~((allow - issue).abs() <= cent)].tolist()
    if bad:
        raise ValueError(f"{name}: free_wd_allow_init must be the issue allowance in the "
                         f"first policy year, duration_mth 1 to 11: free_wd_rate x premium "
                         f"under pct_av, 0 under interest_only, to a cent; it is not at "
                         f"point_id {bad}")
    on_anniv = (months > 0) & (months % 12 == 0)
    bad = table.index[on_anniv & ~((prior - interest).abs() <= cent)].tolist()
    if bad:
        raise ValueError(f"{name}: on a point valued on a policy anniversary, "
                         f"duration_mth a multiple of 12, "
                         f"interest_credited_pp_prev_anniv_init must equal "
                         f"interest_credited_pp_init, to a cent; it does not at point_id "
                         f"{bad}")
    bad = table.index[prior > interest + cent].tolist()
    if bad:
        raise ValueError(f"{name}: interest_credited_pp_prev_anniv_init, the interest "
                         f"credited to the anniversary, must not exceed "
                         f"interest_credited_pp_init, that credited to the valuation "
                         f"date; it does at point_id {bad}")
    bad = table.index[(months >= 12) & interest_only & (allow > prior + cent)].tolist()
    if bad:
        raise ValueError(f"{name}: under interest_only, free_wd_allow_init, the interest "
                         f"credited over the contract year before the one under way, must "
                         f"not exceed interest_credited_pp_prev_anniv_init, the interest "
                         f"credited to the anniversary that opened the year; it does at "
                         f"point_id {bad}")
    second_year = (months >= 12) & (months < 24)
    bad = table.index[second_year & interest_only
                      & ~((allow - prior).abs() <= cent)].tolist()
    if bad:
        raise ValueError(f"{name}: under interest_only in the second policy year, "
                         f"duration_mth 12 to 23, free_wd_allow_init must equal "
                         f"interest_credited_pp_prev_anniv_init, the interest credited "
                         f"over the first, to a cent; it does not at point_id {bad}")
    mid_year = (months > 0) & (months % 12 != 0)
    bad = table.index[mid_year & (values["free_wd_remain_init"] > allow + cent)].tolist()
    if bad:
        raise ValueError(f"{name}: off an anniversary, free_wd_remain_init must not "
                         f"exceed free_wd_allow_init, the allowance of the contract year "
                         f"under way; it does at point_id {bad}")
    n12 = 12 * pd.to_numeric(table["guar_period"], errors="coerce")  # noqa: F821
    initial = (months > 0) & (months <= n12)
    for column, issued in (("credit_rate_init", "declared_rate_initial"),
                           ("mva_ref_yield_locked_init", "mva_ref_yield_at_issue")):
        fixed = pd.to_numeric(table[issued], errors="coerce")        # noqa: F821
        bad = table.index[initial & (values[column] != fixed)].tolist()
        if bad:
            raise ValueError(f"{name}: entering a month of the initial guarantee period, "
                             f"duration_mth 1 to 12 x guar_period, {column} must equal "
                             f"{issued}; it does not at point_id {bad}")
    gmir = pd.to_numeric(table["gmir"], errors="coerce")             # noqa: F821
    bad = table.index[(months > n12) & (values["credit_rate_init"] < gmir)].tolist()
    if bad:
        raise ValueError(f"{name}: credit_rate_init must be gmir or more, the guaranteed "
                         f"minimum interest rate; it is not at point_id {bad}")
    base = rate * values["av_pp_init"]
    bad = table.index[on_anniv & pct_av & ~((allow - base).abs() <= cent)].tolist()
    if bad:
        raise ValueError(f"{name}: on a point valued on a policy anniversary under "
                         f"pct_av, duration_mth a multiple of 12, free_wd_allow_init must "
                         f"be free_wd_rate x av_pp_init, to a cent, the allowance the "
                         f"anniversary fixes on the account value entering month 0; it is "
                         f"not at point_id {bad}")
    # Each point's keys into the tables it is joined with, read through their checks.
    entry = (-months).clip(lower=0)         # the first month the point is on the books
    steps = rate_scenario_steps().reset_index()
    first = steps.groupby("scenario_id")["t"].min()
    bad = table.index[~(table["scenario_id"].map(first) <= entry)].tolist()
    if bad:
        raise ValueError(f"{name}: scenario_id must be a scenario of {rate_scenario_file} "
                         f"that sets its levels by the first month the point is on the "
                         f"books, t = 0 or its issue month if later; it is not at "
                         f"point_id {bad}")
    programmes = wd_schedules().index.get_level_values("wd_schedule_id")
    bad = table.index[~table["wd_schedule_id"].isin(programmes)].tolist()
    if bad:
        raise ValueError(f"{name}: wd_schedule_id must be a programme of "
                         f"{withdrawal_file}; it is not at point_id {bad}")
    rates = mort_rates().reset_index()
    youngest = rates.groupby("sex")["age"].min()
    oldest = rates.groupby("sex")["age"].max()
    issued = pd.to_numeric(table["age_at_entry"], errors="coerce")  # noqa: F821
    attained = issued + months.clip(lower=0) // 12
    sexes = table["sex"]
    bad = table.index[~((attained >= sexes.map(youngest))
                        & (attained <= sexes.map(oldest)))].tolist()
    if bad:
        raise ValueError(f"{name}: {mort_table_file} must give a rate at the point's sex "
                         f"and its attained age in the first month it is on the books; it "
                         f"does not at point_id {bad}")
    return table


def mort_table():
    """Annual mortality by attained age and sex, read from *mort_table.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file, index_col=["age", "sex"])     # noqa: F821


def surr_charge_table():
    """Surrender charge rates by schedule and contract year.

    Read from *surr_charge_table.csv*.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / surr_charge_file,                              # noqa: F821
        index_col=["schedule", "contract_year"])


def surr_charge_age_cap_table():
    """The attained-age cap on the renewal surrender charge.

    Read from *surr_charge_age_cap.csv*, indexed by attained age.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / surr_charge_age_cap_file, index_col="age")     # noqa: F821


def rate_scenario():
    """The exogenous rate scenarios, read from *rate_scenario.csv*.

    Indexed by ``(scenario_id, t)``, ``t`` a **valuation** month, 0 at the valuation
    date, and read as a step function of ``t``: each row states the MVA reference yield
    and the market competitor rate that hold from that month until the next row of the
    same scenario, so a flat path is one row at ``t = 0``. ``MYGA_US_S`` reads the same
    rows on its own ``t``, which on a contract issued at the valuation date is the same
    month.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / rate_scenario_file,                            # noqa: F821
        index_col=["scenario_id", "t"])


def withdrawal_table():
    """Scheduled gross withdrawals, read from *withdrawal_table.csv*.

    Indexed by ``(wd_schedule_id, t)``, ``t`` a **policy** month, which the projection
    reads at ``duration_mth(t)``; a month with no row takes no withdrawal. The worked
    example's $4,000 sits at ``t = 12``, the first month of contract year 2, however old
    the contract is at the valuation date.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / withdrawal_file,                               # noqa: F821
        index_col=["wd_schedule_id", "t"])


def mva_factor_table():
    """The declared-differential MVA duration factors, from *mva_factor_table.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mva_factor_file, index_col="years_remaining")  # noqa: F821


def mort_rates():
    """Annual mortality by attained age and sex, as :func:`mort_table` reads it, checked.

    Indexed by ``(age, sex)``, the age read by value, once, so that an age written
    ``61.0`` is 61, as ``MYGA_US_S``'s lookup matches it. ``Projection.mort_rate``, the
    table's one reader, reads it here, so a projection meets the check first. An age that
    is not a whole number, text and a blank among them, a blank sex, a rate that is not a
    number from 0 to 1, and a sex whose ages do not run one row an age, without a gap or a
    repeat, are refused, naming the file, the column and the lines they are on.
    """
    name = mort_table_file                                           # noqa: F821
    rows = mort_table().reset_index()
    lines = rows.index + 2                  # the header is line 1 of the file
    ages = pd.to_numeric(rows["age"], errors="coerce")               # noqa: F821
    bad = lines[(~(ages % 1 == 0)).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: age must be a whole number; it is not on line {bad}")
    bad = lines[rows["sex"].isna().to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: sex must not be blank; it is on line {bad}")
    rates = pd.to_numeric(rows["mort_rate"], errors="coerce")        # noqa: F821
    bad = lines[(~((rates >= 0) & (rates <= 1))).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: mort_rate must be a number from 0 to 1; it is not on "
                         f"line {bad}")
    ages = ages.astype("int64")
    for sex, run in ages.groupby(rows["sex"]):
        if sorted(run.tolist()) != list(range(int(run.min()), int(run.max()) + 1)):
            raise ValueError(f"{name}: the ages of sex {sex} must run one row an age, "
                             f"without a gap or a repeat")
    keys = pd.MultiIndex.from_arrays([ages, rows["sex"]], names=["age", "sex"])  # noqa
    return pd.DataFrame({"mort_rate": rates.to_numpy(dtype="float64")},  # noqa: F821
                        index=keys)


def surr_charge_scales():
    """The surrender charge schedules, as :func:`surr_charge_table` reads them, checked.

    Indexed by ``(schedule, contract_year)``, the year read by value, once, as
    ``MYGA_US_S``'s lookup matches it. ``Projection.surr_charge_rate``, the table's one
    reader, reads it here, so a projection meets the check first. A contract year that is
    not a whole number, text and a blank among them, a blank schedule, a rate that is not a
    number from 0 to 1, and a schedule whose years do not run from 1, one row a year,
    without a gap or a repeat, are refused, naming the file, the column and the lines they
    are on, and so is a table that lacks ``initial`` or ``renewal``, the two schedules
    ``Projection.surr_charge_id`` names: ``MYGA_US_S`` reads a schedule it cannot find as
    no charge, so one misspelt, ``Renewal``, would leave every renewal period free of
    charge without a word. A year past a schedule's last has no charge.
    """
    name = surr_charge_file                                          # noqa: F821
    rows = surr_charge_table().reset_index()
    lines = rows.index + 2                  # the header is line 1 of the file
    years = pd.to_numeric(rows["contract_year"], errors="coerce")    # noqa: F821
    bad = lines[(~(years % 1 == 0)).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: contract_year must be a whole number; it is not on "
                         f"line {bad}")
    bad = lines[rows["schedule"].isna().to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: schedule must not be blank; it is on line {bad}")
    rates = pd.to_numeric(rows["surr_charge_rate"], errors="coerce")  # noqa: F821
    bad = lines[(~((rates >= 0) & (rates <= 1))).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: surr_charge_rate must be a number from 0 to 1; it is "
                         f"not on line {bad}")
    years = years.astype("int64")
    for schedule, run in years.groupby(rows["schedule"]):
        if sorted(run.tolist()) != list(range(1, len(run) + 1)):
            raise ValueError(f"{name}: the contract years of schedule {schedule} must run "
                             f"from 1, one row a year, without a gap or a repeat")
    for schedule in ("initial", "renewal"):
        if not (rows["schedule"] == schedule).any():
            raise ValueError(f"{name}: schedule {schedule} must be in the table, one of "
                             f"the two the projection reads, initial and renewal; it is "
                             f"not")
    keys = pd.MultiIndex.from_arrays(                                # noqa: F821
        [rows["schedule"], years], names=["schedule", "contract_year"])
    return pd.DataFrame({"surr_charge_rate": rates.to_numpy(dtype="float64")},  # noqa
                        index=keys)


def surr_charge_age_caps():
    """The attained-age cap, as :func:`surr_charge_age_cap_table` reads it, checked.

    Indexed by attained age, read by value, once, as ``MYGA_US_S``'s lookup matches it.
    ``Projection.surr_charge_age_cap_at``, the table's one reader, reads it here, and takes
    its extents, :func:`surr_charge_age_cap_first` and :func:`surr_charge_age_cap_last`,
    from the same checked ages before it reads a cap, so a projection meets the check
    first. An age that is not a whole number, text and a blank among them, a cap that is
    not a number from 0 to 1, and ages that do not run one row an age, without a gap or a
    repeat, are refused, naming the file, the column and the lines they are on.
    ``MYGA_US_S`` takes ``int()`` of the raw ages for its extents: one written ``94x``
    turns them to text, the extents then compare as text, and the cap vanishes.
    """
    name = surr_charge_age_cap_file                                  # noqa: F821
    rows = surr_charge_age_cap_table().reset_index()
    lines = rows.index + 2                  # the header is line 1 of the file
    ages = pd.to_numeric(rows["age"], errors="coerce")               # noqa: F821
    bad = lines[(~(ages % 1 == 0)).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: age must be a whole number; it is not on line {bad}")
    caps = pd.to_numeric(rows["surr_charge_cap"], errors="coerce")   # noqa: F821
    bad = lines[(~((caps >= 0) & (caps <= 1))).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: surr_charge_cap must be a number from 0 to 1; it is "
                         f"not on line {bad}")
    ages = ages.astype("int64")
    if not len(ages) or sorted(ages.tolist()) != list(
            range(int(ages.min()), int(ages.max()) + 1)):
        raise ValueError(f"{name}: the ages must run one row an age, without a gap or a "
                         f"repeat")
    return pd.DataFrame({"surr_charge_cap": caps.to_numpy(dtype="float64")},  # noqa
                        index=pd.Index(ages, name="age"))           # noqa: F821


def surr_charge_age_cap_first():
    """The first attained age :func:`surr_charge_age_caps` gives a cap for, an int."""
    return int(surr_charge_age_caps().index.min())


def surr_charge_age_cap_last():
    """The last attained age :func:`surr_charge_age_caps` gives a cap for, an int."""
    return int(surr_charge_age_caps().index.max())


def rate_scenario_steps():
    """The rate scenarios, as :func:`rate_scenario` reads them, checked.

    Indexed by ``(scenario_id, t)``, each ``t`` a valuation month read by value, once, as
    ``MYGA_US_S``'s step function compares it. ``Projection.scenario_rate``, the table's
    one reader, reads it here, so a projection meets the check first. A month that is not a
    whole number, text and a blank among them, a blank ``scenario_id``, a yield or a market
    rate that is not a finite number, and a scenario that sets two levels at one month are
    refused, naming the file, the column and the lines they are on. ``MYGA_US_S``'s step
    function compares the raw months with ``t``: one written as text raises Python's own
    ``TypeError``, and a blank one is a level that never holds. A scenario may start after
    ``t = 0``, for business issued later, so the month a scenario must start by is the
    point's: :func:`model_point_table` refuses a point whose scenario sets no level by the
    first month the point is on the books, where the step function would find none and
    raise Python's own ``ValueError``.
    """
    name = rate_scenario_file                                        # noqa: F821
    rows = rate_scenario().reset_index()
    lines = rows.index + 2                  # the header is line 1 of the file
    months = pd.to_numeric(rows["t"], errors="coerce")               # noqa: F821
    bad = lines[(~(months % 1 == 0)).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: t must be a whole number; it is not on line {bad}")
    bad = lines[rows["scenario_id"].isna().to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: scenario_id must not be blank; it is on line {bad}")
    levels = {}
    for column in ("mva_ref_yield", "market_rate"):
        levels[column] = pd.to_numeric(rows[column], errors="coerce")  # noqa: F821
        v = levels[column]
        bad = lines[(~((v > -float("inf")) & (v < float("inf")))).to_numpy()].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a number; it is not on line {bad}")
    months = months.astype("int64")
    keys = pd.MultiIndex.from_arrays(                                # noqa: F821
        [rows["scenario_id"], months], names=["scenario_id", "t"])
    bad = lines[keys.duplicated(keep=False)].tolist()
    if bad:
        raise ValueError(f"{name}: a scenario must set one level a month; one sets two on "
                         f"lines {bad}")
    return pd.DataFrame(                                             # noqa: F821
        {"mva_ref_yield": levels["mva_ref_yield"].to_numpy(dtype="float64"),
         "market_rate": levels["market_rate"].to_numpy(dtype="float64")}, index=keys)


def wd_schedules():
    """The withdrawal programmes, as :func:`withdrawal_table` reads them, checked.

    Indexed by ``(wd_schedule_id, t)``, each ``t`` a policy month read by value, once, as
    ``MYGA_US_S``'s exact-key lookup matches it. ``Projection.wd_scheduled_pp``, the
    table's one reader, reads it here, so a projection meets the check first. A month that
    is not a whole number, text and a blank among them, a blank ``wd_schedule_id``, an
    amount that is not a number, zero or more, and a programme that withdraws twice in one
    month are refused, naming the file, the column and the lines they are on.
    ``MYGA_US_S``'s lookup matches the raw months: one written as text turns them all to
    text, and every withdrawal of every programme is then zero.
    """
    name = withdrawal_file                                           # noqa: F821
    rows = withdrawal_table().reset_index()
    lines = rows.index + 2                  # the header is line 1 of the file
    months = pd.to_numeric(rows["t"], errors="coerce")               # noqa: F821
    bad = lines[(~(months % 1 == 0)).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: t must be a whole number; it is not on line {bad}")
    bad = lines[rows["wd_schedule_id"].isna().to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: wd_schedule_id must not be blank; it is on line {bad}")
    amounts = pd.to_numeric(rows["wd_amount"], errors="coerce")      # noqa: F821
    bad = lines[(~((amounts >= 0) & (amounts < float("inf")))).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: wd_amount must be a number, zero or more; it is not on "
                         f"line {bad}")
    months = months.astype("int64")
    keys = pd.MultiIndex.from_arrays(                                # noqa: F821
        [rows["wd_schedule_id"], months], names=["wd_schedule_id", "t"])
    bad = lines[keys.duplicated(keep=False)].tolist()
    if bad:
        raise ValueError(f"{name}: a programme must withdraw once a month at most; one "
                         f"withdraws twice on lines {bad}")
    return pd.DataFrame({"wd_amount": amounts.to_numpy(dtype="float64")},  # noqa: F821
                        index=keys)


def mva_factors():
    """The declared-differential duration factors, as :func:`mva_factor_table` reads them,
    checked.

    Indexed by whole years remaining, read by value, once, as ``MYGA_US_S``'s lookup
    matches them. ``Projection.mva_factor_at``, the table's one reader, reads it here, and
    ``Projection.mva_duration_factor`` takes the table's last year,
    :func:`mva_factor_last_year`, from the same checked years before it reads a factor,
    so a projection meets the check first. A year that is not a whole number, text and a
    blank among them, a factor that is not a finite number, and years that do not run from
    0, one row a year, without a gap or a repeat, are refused, naming the file, the column
    and the lines they are on. ``MYGA_US_S`` takes ``int()`` of the raw years for the last
    one: one written as text raises a ``KeyError`` that names no file.
    """
    name = mva_factor_file                                           # noqa: F821
    rows = mva_factor_table().reset_index()
    lines = rows.index + 2                  # the header is line 1 of the file
    years = pd.to_numeric(rows["years_remaining"], errors="coerce")  # noqa: F821
    bad = lines[(~(years % 1 == 0)).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: years_remaining must be a whole number; it is not on "
                         f"line {bad}")
    factors = {}
    for column in ("factor_lo", "factor_hi"):
        factors[column] = pd.to_numeric(rows[column], errors="coerce")  # noqa: F821
        v = factors[column]
        bad = lines[(~((v > -float("inf")) & (v < float("inf")))).to_numpy()].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a number; it is not on line {bad}")
    years = years.astype("int64")
    if sorted(years.tolist()) != list(range(len(years))):
        raise ValueError(f"{name}: the years remaining must run from 0, one row a year, "
                         f"without a gap or a repeat")
    return pd.DataFrame(                                             # noqa: F821
        {"factor_lo": factors["factor_lo"].to_numpy(dtype="float64"),
         "factor_hi": factors["factor_hi"].to_numpy(dtype="float64")},
        index=pd.Index(years, name="years_remaining"))              # noqa: F821


def mva_factor_last_year():
    """The last whole year remaining :func:`mva_factors` gives a factor for, an int."""
    return int(mva_factors().index.max())


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table_sec.csv"

mort_table_file = "mort_table.csv"

surr_charge_file = "surr_charge_table.csv"

surr_charge_age_cap_file = "surr_charge_age_cap.csv"

rate_scenario_file = "rate_scenario.csv"

withdrawal_file = "withdrawal_table.csv"

mva_factor_file = "mva_factor_table.csv"

future_horizon_mth = 120

pd = ("Module", "pandas")
