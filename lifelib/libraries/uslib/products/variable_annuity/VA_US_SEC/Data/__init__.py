# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-contract projection.

The eight input CSVs are read here, **once per model**, and referenced from
:mod:`~.VA_US_SEC.Projection` as ``data``. :mod:`~.VA_US_SEC.Projection` is parameterized
by ``point_id``, so each ``Projection[N]`` is a separate ItemSpace with its own cells cache;
if the readers lived there, every model point would re-read every file. Holding them in an
unparameterized Space reads each file once no matter how many contracts are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/variable_annuity/``, rather than data stored inside the model. The model
folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded
values — so a diff of the model shows logic changes only. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``VA_US_SEC`` folder without its parent's CSVs produces a model that reads and then fails
on first evaluation.

**Five of the tables are VA_US_S's.** The mortality table, the fund table, the GAWA% grid,
the withdrawal charge scale and the transaction programmes are the files
:mod:`~.VA_US_S` reads, read here in place: one copy of each table serves both models, so
an edit to one reaches both. The other three are this model's own, each generated from
:mod:`~.VA_US_S` and its inputs, never typed: ``model_point_table_sec.csv``, beside
``VA_US_S``'s ``model_point_table.csv``, and ``return_scenario_sec.csv`` and
``rate_scenario_sec.csv``, the two scenarios moved onto the valuation clock, beside
``VA_US_S``'s ``return_scenario.csv`` and ``rate_scenario.csv``. This model opens none of
``VA_US_S``'s three.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so the
model works wherever the repository is checked out. Each table has a filename Reference
and a reader Cells:

=========================  ==============================  ==========================
Reference                  Cells                           File
=========================  ==============================  ==========================
model_point_file           model_point_table()             model_point_table_sec.csv
mort_table_file            mort_table()                    mort_table.csv
fund_file                  fund_table()                    fund_table.csv
return_scenario_file       return_scenario()               return_scenario_sec.csv
rate_scenario_file         rate_scenario()                 rate_scenario_sec.csv
gawa_pct_file              gawa_pct_table()                gawa_pct_table.csv
cdsc_file                  cdsc_table()                    cdsc_table.csv
transaction_file           transaction_table()             transaction_table.csv
=========================  ==============================  ==========================

**The model point table is checked as it is read.** Twenty-two of its columns are the
in-force interface: ``policy_count`` and ``duration_mth``, as in
``basiclife.BasicTerm_SE``, and the twenty columns of an in-force contract's opening
state, the two subaccount values among them. :func:`model_point_table` refuses a table that
lacks any of them, repeats a ``point_id``, holds a count, a duration, an age or a contract
parameter no contract can have, holds an opening state no contract can be in, or holds a
key that the table it joins lacks: a fund set, a scenario that sets no level by the
point's first month on the books, a programme, a grid, a withdrawal charge schedule, or a
sex and an attained age the mortality table gives no rate at. The checks run in turn, and
the first that fails raises, naming the missing column or every point that fails it. It
also refuses a contract to be issued more than ``future_horizon_mth`` months after the
valuation date, 120 months as shipped: future new business is written over a stated
horizon, so that no frame runs longer than cover from issue plus that horizon. Set to 0,
the Reference refuses future new business altogether. Whether a point is still in cover at
the valuation date is a rule of the product rather than of the table, and
``Projection.proj_len`` checks it. :func:`fund_values_init` reads the subaccount values out
of the checked table, one column a subaccount.

**So are the keys and values of the seven assumption tables.** The reader of each in the
table above is ``VA_US_S``'s, unchanged, :func:`model_point_table` alone being rewritten,
and beside it a cell reads the table's keys by value, once, checks them and its values,
and returns the table indexed by the checked keys. The projection reads each table there
and nowhere else, and takes the mortality table's last age from the same checked keys, as
an int cell:

=========================  ================================  ===========================
VA_US_S's reader           Checked cell                      Its extents
=========================  ================================  ===========================
mort_table()               mort_rates()                      mort_last_age()
fund_table()               fund_sets()
return_scenario()          return_scenario_steps()
rate_scenario()            rate_scenario_steps()
gawa_pct_table()           gawa_pct_bands()
cdsc_table()               cdsc_scale()
transaction_table()        transactions()
=========================  ================================  ===========================

A key that is not a whole number, text and a blank among them, is refused, naming the
file, the column and the lines it is on, and so are a blank text key, a value that is not
a number in its range, blank, text and infinite values among them, a repeated key, and,
where the projection reads every year or age between a table's first and last, keys that
do not run one row a year or an age: the message names each repeated key with its lines
and each key or span of keys missing. A key written as a float, ``1.0``, is the whole
number it holds, as ``VA_US_S``'s lookups match it. Those lookups take the keys as pandas
reads them: one key written as text turns its whole column to text, so that every
scheduled premium and withdrawal is then zero without a word, and every other lookup on
the column raises Python's own ``TypeError``, ``KeyError`` or ``ValueError``, naming no
file. And every value a ``min`` or a ``max`` reads is refused blank, as text or infinite,
because ``min`` and ``max`` lose a NaN in a later argument without a word.

All seven carry a compound key. ``mort_table`` is indexed by ``(age, sex)``;
``fund_table`` by ``(fund_set, sub_id)``, so one row per subaccount describes an
allocation set; ``return_scenario`` by ``(scenario_id, sub_id, t)`` and ``rate_scenario``
by ``(scenario_id, t)``, both read as step functions of ``t`` so a flat path is one row
per subaccount; ``gawa_pct_table`` by ``(gawa_grid, age_from)``, read as a banded lookup
on the attained age; ``cdsc_table`` by ``(cdsc_schedule, completed_years)``; and
``transaction_table`` by ``(txn_id, t)``, a month with no row taking neither premium nor
withdrawal.

The two scenarios run on the **valuation clock**: the ``t`` of *return_scenario_sec.csv*
and *rate_scenario_sec.csv* is a valuation month, 0 at the valuation date, and each row
holds from its month until the next row of the same scenario (and subaccount). A market
path is a path in calendar time, shared by every point of a block, so a projection reads
it at its own ``t``. ``VA_US_S`` keys the same paths by the **elapsed policy month**, so on
the valuation clock a contract needs them where its own policy months fall: each file
holds ``VA_US_S``'s scenarios under their own ids, for the contracts issued at the
valuation date, whose policy month is ``t``, and a copy of a contract's path re-based to
its ``duration_mth`` for every row valued in force or issued later, under an id of its
own, ``{id}-M{m}`` or ``{id}-F{k}``. The transaction programmes stay on the policy clock:
the ``t`` of *transaction_table.csv* is the elapsed policy month, 0-based, read as
``Projection.duration_mth(t)``. ``completed_years`` in *cdsc_table.csv* is an elapsed
count too, read as ``Projection.duration(t)``, and is 0-based already.

The mortality table shipped here is an illustrative **[std]** annuitant curve, *not* a
published basis. The prescribed basis is the 2012 IAM **Basic** Table improved to
December 31, 2017 on Projection Scale G2 [R1][REG-R59], which may not be redistributed
here; swap it in by replacing ``mort_table.csv`` with a same-schema file, or point
``mort_table_file`` at a different name, before the model computes anything. No formula
changes. Replacing a file changes :mod:`~.VA_US_S` too, which reads the same ones.
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

    Indexed by ``point_id``. Twenty-two columns are the in-force interface:
    ``policy_count`` and ``duration_mth``, the completed policy months at the valuation
    date, as in ``basiclife.BasicTerm_SE``, and the twenty columns of the opening state,
    per contract, as the contract stands at the start of month 0, before any month-0
    event:

    * ``sa_pp_init_1`` and ``sa_pp_init_2``: the value of each subaccount, one column for
      every subaccount a fund set holds;
    * ``gwb_pp_init``, ``bb_pp_init``, ``gawa_pp_init``, ``rb_pp_init``, ``np_pp_init``,
      ``rp_pp_init`` and ``adj_pp_init``: the GWB, the Bonus Base, the GAWA, the GMDB
      Benefit Base, the cumulative Net Premiums, the Remaining Premium and the GWB
      Adjustment;
    * ``gawa_pct_init``: the GAWA% locked at the first withdrawal or at depletion, 0
      before either;
    * ``bonus_end_init``: the contract year the Bonus Period ends;
    * ``has_wd_init``: whether a withdrawal has been taken;
    * ``sum_wd_pp_ytd_init``, ``free_wd_used_cum_pp_ytd_init``,
      ``gmdb_dfd_acc_pp_ytd_init`` and ``gmdb_factor_acc_ytd_init``: the contract year to
      date, the withdrawals, the free allowance they used, the GMDB's dollar-for-dollar
      reduction and its proportional factor, empty (0, 0, 0 and 1) at a year's start;
    * ``wd_this_year_init``: whether a withdrawal was taken in the year under way;
    * ``rb_pp_prev_anniv_init``: the Benefit Base at the anniversary that opened the year
      under way, the base of the year's dollar-for-dollar allowance;
    * ``stepup_base_pp_ytd_init``: the largest account value at the year's quarterly
      anniversaries before the valuation month, 0 where none has passed;
    * ``phi_glwb_init``: on the ``vix`` fee rule, the rate of the last contract quarter to
      end before the valuation month, the clip's prior for the first fee on the books.

    Nine are ``VA_US_S``'s columns renamed: ``duration_mth_init`` becomes
    ``duration_mth``, ``pols_if_init`` ``policy_count``, and ``gwb_init``, ``bb_init``,
    ``gawa_init``, ``rb_init``, ``np_init``, ``rp_init`` and ``adj_init`` the ``_init`` of
    the cell each opens; ``av_init``, the account value, gives way to the subaccount
    values, which ``VA_US_S`` derives by splitting it by the target allocation. The rest
    are ``VA_US_S``'s, except ``row_kind``, ``source_policy_id`` and ``source_mth``, which
    record where the generator took each shipped row from and which no formula reads.

    The checks run over the whole table at once, and the first that fails raises
    ``ValueError``, naming the missing column or every point it fails on:

    * the in-force columns are present, the subaccount values apart, which are checked
      with the fund sets below;
    * no ``point_id`` appears twice;
    * ``policy_count`` is a number, zero or more;
    * ``duration_mth`` is a whole number of months: positive for a contract in force, 0
      for one issued at the valuation date, negative for one issued later;
    * ``age_at_entry``, ``wd_start_age`` and ``bonus_end_init`` are whole numbers, 0 or
      more. ``VA_US_S`` reads each by ``int()``, which would truncate a fraction without a
      word;
    * no contract is issued more than ``future_horizon_mth`` months after the valuation
      date, so ``duration_mth`` is ``-future_horizon_mth`` or more. At 0 the model takes
      no future new business, and the message says so; a negative horizon is itself
      refused;
    * ``has_wd_init`` and ``wd_this_year_init`` are True or False, read by value, as
      ``True``, ``False``, ``1`` or ``0``: one cell written as text turns the column to
      text as pandas reads it, so ``"True"`` and ``"False"`` are read as the flags they
      name, and the table is returned holding bools;
    * the premium and the withdrawal intensity are each a finite number, zero or more, and
      the premium tax rate a number from 0 to below 1;
    * the twelve money columns of the opening state are each a finite number, zero or
      more, and ``gawa_pct_init``, ``gmdb_factor_acc_ytd_init`` and ``phi_glwb_init``
      numbers from 0 to 1;
    * a contract not yet in force, ``duration_mth`` 0 or less, has no opening state: every
      state column is 0, or False;
    * on a contract valued at a contract year's start, ``duration_mth`` a multiple of 12,
      the year to date is empty, exactly: the three sums 0, the factor 1 and
      ``wd_this_year_init`` False; and ``rb_pp_prev_anniv_init`` equals ``rb_pp_init``,
      the two being one instant;
    * before the contract year's first quarterly anniversary, ``duration_mth % 12`` below
      3, no quarter of the year has ended, so ``stepup_base_pp_ytd_init`` is 0;
    * ``phi_glwb_init`` is 0 on a contract in force unless it is on the ``vix`` fee rule and
      past its first contract quarter, ``duration_mth`` 3 or more: before then, and off the
      rule, no quarter's rate is the clip's prior;
    * in the first policy year, ``duration_mth`` 1 to 11, the year opened at issue, so
      ``rb_pp_prev_anniv_init`` is the issue value, to a cent: the premium credited at
      issue, ``(premium + the programme's month-0 premium) x (1 - premium_tax_rate)``;
    * in force, ``bonus_end_init`` is 1 or more: it is a contract year;
    * a contract that has withdrawn, ``has_wd_init`` True, has no GWB Adjustment:
      ``adj_pp_init`` is 0, any withdrawal voiding it;
    * a GAWA above 0 has a locked percentage above 0, the GAWA being the locked percentage
      of a base;
    * off a contract year's start, a withdrawal this year is a withdrawal, so
      ``wd_this_year_init`` True needs ``has_wd_init`` True; withdrawals to date above 0
      need ``wd_this_year_init`` True; the free allowance used and the dollar-for-dollar
      reduction are each part of the withdrawals to date, so neither exceeds them by more
      than a cent; and the proportional factor is below 1 only where the year has
      withdrawals;
    * last, each point's keys into the tables it is joined with: its ``fund_set`` is a set
      of :func:`fund_sets`, and each subaccount the set holds has its ``sa_pp_init_<i>``
      column, a finite number, zero or more to within a cent, and 0 on a contract not yet
      in force; its ``scenario_id`` is a scenario of :func:`return_scenario_steps` that
      sets a return for each of those subaccounts by the first month the point is on the
      books, ``t = 0`` or its issue month if later, and, on a point the ``vix`` fee or the
      ``cmt_linked`` roll-up reads it for, a scenario of :func:`rate_scenario_steps` that
      sets its levels by then; its ``txn_id`` is a programme of :func:`transactions`; its
      ``glwb_option`` a grid of :func:`gawa_pct_bands`, and, in force, ``has_wd_init`` True
      needs ``gawa_pct_init`` above 0 unless that grid gives 0% at an attained age the
      contract reached before the valuation month (:func:`gawa_pct_zero_band`), since the
      first withdrawal locks the percentage of the age it is taken at, and a ``gwb_pp_init``
      and a ``gawa_pct_init`` above 0 need a ``gawa_pp_init`` above 0 unless the grid did,
      since the withdrawal or the depletion that locked the percentage set the GAWA to it
      times the GWB, and nothing after takes the GAWA to 0 while a GWB is left; its
      ``cdsc_schedule`` a schedule of :func:`cdsc_scale`; and :func:`mort_rates` gives a
      rate at its ``sex`` and its attained age in its first month on the books. So reading
      the table reads every assumption table, checked.

    Amounts of money are compared to a cent, so that an extract may carry each to the cent,
    as an administration system holds it: each amount so carried is within half a cent of
    its exact value. Two columns that hold one amount at instants that coincide, on a
    year's start, are compared exactly. A subaccount value is held to 0 or more to within a
    cent, as a rule holding one carried amount to 0 is: ``VA_US_S`` runs an account down by
    scaling each subaccount by one less the share of the account a charge or a withdrawal
    takes, so a depletion can close on a rounding of either sign about 0, of the order of
    1e-14, the one amount of the opening state its arithmetic leaves below 0, the bases
    being held at 0 or more by its floors.

    Accepted, because a contract can be in each state: an account value of 0 in force,
    where the GLWB pays on and the projection reads the contract as depleted from month 0,
    or the rounding about 0 that a depletion closed on, above 0 or below it, which the
    same test reads as depleted; a locked percentage above 0 with no withdrawal taken,
    where the account value ran out first, which the projection checks; free allowance
    used and a dollar-for-dollar reduction above the allowance the month allows at the
    valuation date, since the allowance is recomputed every month from the earnings and
    the Remaining Premium; and a ``duration_mth``, an age or ``bonus_end_init`` written as
    a float, and a flag written as 1 or 0, read as the value each holds.

    Left to the projection, because each needs a ``Projection`` Reference, which ``Data``
    cannot read, and refused by ``Projection.proj_len``, naming the point: whether a point
    is still in cover, against ``omega_age``; whether it is depleted at the valuation date,
    which the projection derives from its opening account value and
    ``av_depletion_threshold``, and the GAWA% that goes with each: 0 on a contract that has
    neither withdrawn nor depleted, and above 0 on one depleted without a withdrawal unless
    its grid gave 0% at an age it reached (:func:`gawa_pct_zero_by_point`); on the
    ``highest_quarterly_CV`` basis, a step-up history above the threshold on a contract not
    depleted and three months or more into its contract year, since every quarter end of
    the year closed above it; and, on the ``vix`` fee rule, ``phi_glwb_init`` the first
    quarter's rate, ``phi_glwb_curr``, in the second contract quarter, and from the third at
    most ``vix_corridor_hi``, and at least ``vix_corridor_lo`` where ``phi_glwb_curr`` is,
    the clip holding every rate after the first there. The rest of the year to date, the
    step-up base and the VIX prior are history, which nothing here can check beyond these
    rules.
    """
    name = model_point_file                                          # noqa: F821
    table = pd.read_csv(input_dir() / name, index_col="point_id")    # noqa: F821
    money = ("gwb_pp_init", "gawa_pp_init", "bb_pp_init", "rb_pp_init", "np_pp_init",
             "rp_pp_init", "adj_pp_init", "sum_wd_pp_ytd_init",
             "free_wd_used_cum_pp_ytd_init", "gmdb_dfd_acc_pp_ytd_init",
             "rb_pp_prev_anniv_init", "stepup_base_pp_ytd_init")
    rates = ("gawa_pct_init", "gmdb_factor_acc_ytd_init", "phi_glwb_init")
    flags = ("has_wd_init", "wd_this_year_init")
    state = (*money, *rates, "bonus_end_init", *flags)
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
    for column in ("age_at_entry", "wd_start_age", "bonus_end_init"):
        v = pd.to_numeric(table[column], errors="coerce")           # noqa: F821
        bad = table.index[~((v % 1 == 0) & (v >= 0))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a whole number, 0 or more; it "
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
    read = {True: True, False: False, "True": True, "False": False, 1: True, 0: False}
    for column in flags:
        mapped = table[column].map(lambda v: read.get(v) if not isinstance(v, float)
                                   or v == v else None)
        bad = table.index[mapped.isna()].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be True or False, or 1 or 0; it is "
                             f"not at point_id {bad}")
        table = table.assign(**{column: mapped.astype(bool)})
    for column in ("premium", "wd_intensity"):
        v = pd.to_numeric(table[column], errors="coerce")          # noqa: F821
        bad = table.index[~((v >= 0) & (v < float("inf")))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a number, zero or more; it is "
                             f"not at point_id {bad}")
    tax = pd.to_numeric(table["premium_tax_rate"], errors="coerce")  # noqa: F821
    bad = table.index[~((tax >= 0) & (tax < 1))].tolist()
    if bad:
        raise ValueError(f"{name}: premium_tax_rate must be a number from 0 to below 1; "
                         f"it is not at point_id {bad}")
    values = {c: pd.to_numeric(table[c], errors="coerce") for c in (*money, *rates)}  # noqa
    for column in money:
        v = values[column]
        bad = table.index[~((v >= 0) & (v < float("inf")))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a number, zero or more; it is "
                             f"not at point_id {bad}")
    for column in rates:
        v = values[column]
        bad = table.index[~((v >= 0) & (v <= 1))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a number from 0 to 1; it is not "
                             f"at point_id {bad}")
    bonus_end = pd.to_numeric(table["bonus_end_init"], errors="coerce")  # noqa: F821
    in_force = months > 0
    for column in state:
        v = (table[column] if column in flags else bonus_end if column == "bonus_end_init"
             else values[column])
        bad = table.index[(months <= 0) & (v != 0)].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be 0 on a policy not yet in force, "
                             f"duration_mth 0 or less; it is not at point_id {bad}")
    has_wd, this_year = table["has_wd_init"], table["wd_this_year_init"]
    total = values["sum_wd_pp_ytd_init"]
    cent = 0.01
    start = in_force & (months % 12 == 0)
    for column, empty in (("sum_wd_pp_ytd_init", 0.0),
                          ("free_wd_used_cum_pp_ytd_init", 0.0),
                          ("gmdb_dfd_acc_pp_ytd_init", 0.0),
                          ("gmdb_factor_acc_ytd_init", 1.0)):
        bad = table.index[start & (values[column] != empty)].tolist()
        if bad:
            raise ValueError(f"{name}: on a point valued at a contract year's start, "
                             f"duration_mth a multiple of 12, {column} must be {empty:g}; "
                             f"it is not at point_id {bad}")
    bad = table.index[start & this_year].tolist()
    if bad:
        raise ValueError(f"{name}: on a point valued at a contract year's start, "
                         f"wd_this_year_init must be False; it is not at point_id {bad}")
    bad = table.index[start & (values["rb_pp_prev_anniv_init"]
                               != values["rb_pp_init"])].tolist()
    if bad:
        raise ValueError(f"{name}: on a point valued at a contract year's start, "
                         f"rb_pp_prev_anniv_init must equal rb_pp_init; it does not at "
                         f"point_id {bad}")
    bad = table.index[in_force & (months % 12 < 3)
                      & (values["stepup_base_pp_ytd_init"] != 0)].tolist()
    if bad:
        raise ValueError(f"{name}: stepup_base_pp_ytd_init must be 0 before the contract "
                         f"year's first quarterly anniversary, duration_mth % 12 below 3; "
                         f"it is not at point_id {bad}")
    vix = table["fee_reset_rule"] == "vix"
    bad = table.index[in_force & ~(vix & (months >= 3))
                      & (values["phi_glwb_init"] != 0)].tolist()
    if bad:
        raise ValueError(f"{name}: phi_glwb_init must be 0 on a policy in force unless it "
                         f"is on the vix rule and past its first contract quarter, "
                         f"duration_mth 3 or more; it is not at point_id {bad}")
    premium = pd.to_numeric(table["premium"], errors="coerce")      # noqa: F821
    steps = transactions()
    issue_prem = table["txn_id"].map(
        lambda i: float(steps.loc[(i, 0), "prem_amount"]) if (i, 0) in steps.index
        else 0.0)
    issued = (premium + issue_prem) * (1.0 - tax)
    first = in_force & (months < 12)
    bad = table.index[first & ~((values["rb_pp_prev_anniv_init"] - issued).abs()
                                <= cent)].tolist()
    if bad:
        raise ValueError(f"{name}: rb_pp_prev_anniv_init must be its issue value in the "
                         f"first policy year, duration_mth 1 to 11, the premium credited "
                         f"at issue, to a cent; it is not at point_id {bad}")
    bad = table.index[in_force & ~(bonus_end >= 1)].tolist()
    if bad:
        raise ValueError(f"{name}: bonus_end_init must be 1 or more on a policy in force; "
                         f"it is not at point_id {bad}")
    bad = table.index[in_force & has_wd & (values["adj_pp_init"] != 0)].tolist()
    if bad:
        raise ValueError(f"{name}: adj_pp_init must be 0 on a policy that has withdrawn, "
                         f"has_wd_init True: any withdrawal voids the GWB Adjustment; it "
                         f"is not at point_id {bad}")
    bad = table.index[in_force & (values["gawa_pp_init"] > 0)
                      & ~(values["gawa_pct_init"] > 0)].tolist()
    if bad:
        raise ValueError(f"{name}: gawa_pct_init must be more than 0 where gawa_pp_init "
                         f"is: the GAWA is the locked percentage of a base; it is not at "
                         f"point_id {bad}")
    mid = in_force & ~start
    bad = table.index[mid & this_year & ~has_wd].tolist()
    if bad:
        raise ValueError(f"{name}: has_wd_init must be True where wd_this_year_init is: a "
                         f"withdrawal this year is a withdrawal; it is not at point_id "
                         f"{bad}")
    bad = table.index[mid & (total > 0) & ~this_year].tolist()
    if bad:
        raise ValueError(f"{name}: wd_this_year_init must be True where "
                         f"sum_wd_pp_ytd_init is more than 0; it is not at point_id {bad}")
    for column in ("free_wd_used_cum_pp_ytd_init", "gmdb_dfd_acc_pp_ytd_init"):
        bad = table.index[mid & (values[column] > total + cent)].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must not exceed sum_wd_pp_ytd_init, the "
                             f"withdrawals it is part of, to a cent; it does at point_id "
                             f"{bad}")
    bad = table.index[mid & (values["gmdb_factor_acc_ytd_init"] < 1)
                      & ~(total > 0)].tolist()
    if bad:
        raise ValueError(f"{name}: gmdb_factor_acc_ytd_init must be 1 where "
                         f"sum_wd_pp_ytd_init is 0: only a withdrawal reduces it; it is "
                         f"not at point_id {bad}")
    # join keys, last
    sets = fund_sets()
    held = set(sets.index.get_level_values("fund_set"))
    bad = table.index[~table["fund_set"].isin(held)].tolist()
    if bad:
        raise ValueError(f"{name}: fund_set must be a fund set of {fund_file}; it is not "
                         f"at point_id {bad}")
    for i in sorted(set(sets.index.get_level_values("sub_id"))):
        column = f"sa_pp_init_{i}"
        users = table["fund_set"].map(lambda f, i=i: (f, i) in sets.index)
        if column not in table.columns:
            bad = table.index[users].tolist()
            if bad:
                raise ValueError(f"{name} has no {column} column, which point_id {bad} "
                                 f"needs: its fund set holds subaccount {i}")
            continue
        v = pd.to_numeric(table[column], errors="coerce")           # noqa: F821
        bad = table.index[users & ~((v >= -cent) & (v < float("inf")))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a number, zero or more to within "
                             f"a cent; it is not at point_id {bad}")
        bad = table.index[(months <= 0) & users & (v != 0)].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be 0 on a policy not yet in force, "
                             f"duration_mth 0 or less; it is not at point_id {bad}")
    entry = (-months).clip(lower=0)
    returns = return_scenario_steps().reset_index()
    firsts = returns.groupby(["scenario_id", "sub_id"])["t"].min()
    bad = []
    for point_id in table.index:
        sid, fset = table.at[point_id, "scenario_id"], table.at[point_id, "fund_set"]
        for i in sets.loc[fset].index:
            if not ((sid, i) in firsts.index and firsts[(sid, i)] <= entry[point_id]):
                bad.append(point_id)
                break
    if bad:
        raise ValueError(f"{name}: scenario_id must be a scenario of "
                         f"{return_scenario_file} that sets a return for each subaccount "
                         f"of the point's fund set by the first month the point is on "
                         f"the books, t = 0 or its issue month if later; it is not at "
                         f"point_id {bad}")
    levels = rate_scenario_steps().reset_index().groupby("scenario_id")["t"].min()
    reads = (table["fee_reset_rule"] == "vix") | (table["rollup_rule"] == "cmt_linked")
    bad = table.index[reads & ~(table["scenario_id"].map(levels) <= entry)].tolist()
    if bad:
        raise ValueError(f"{name}: scenario_id must be a scenario of {rate_scenario_file} "
                         f"that sets its levels by the first month the point is on the "
                         f"books, on a point the vix fee or the cmt_linked roll-up reads "
                         f"it for; it is not at point_id {bad}")
    ids = set(steps.index.get_level_values("txn_id"))
    bad = table.index[~table["txn_id"].isin(ids)].tolist()
    if bad:
        raise ValueError(f"{name}: txn_id must be a programme of {transaction_file}; it "
                         f"is not at point_id {bad}")
    bands = gawa_pct_bands()
    grids = set(bands.index.get_level_values("gawa_grid"))
    bad = table.index[~table["glwb_option"].isin(grids)].tolist()
    if bad:
        raise ValueError(f"{name}: glwb_option must be a grid of {gawa_pct_file}; it is "
                         f"not at point_id {bad}")
    issue_age = pd.to_numeric(table["age_at_entry"], errors="coerce")  # noqa: F821
    pct, gawa = values["gawa_pct_init"], values["gawa_pp_init"]
    locked = in_force & has_wd & ~(pct > 0)
    bare = in_force & (values["gwb_pp_init"] > 0) & ~(gawa > 0) & (pct > 0)
    zero = {}
    for point_id in table.index[locked | bare]:
        youngest = int(issue_age[point_id])
        zero[point_id] = gawa_pct_zero_band(table.at[point_id, "glwb_option"], youngest,
                                            youngest + (int(months[point_id]) - 1) // 12)
    bad = [point_id for point_id in table.index[locked] if not zero[point_id]]
    if bad:
        raise ValueError(f"{name}: gawa_pct_init must be more than 0 where has_wd_init is "
                         f"True: the first withdrawal locks the GAWA% of the attained age "
                         f"it is taken at, which the point's grid gives as more than 0 at "
                         f"every attained age the policy reached before the valuation "
                         f"month; it is not at point_id {bad}")
    bad = [point_id for point_id in table.index[bare] if not zero[point_id]]
    if bad:
        raise ValueError(f"{name}: gawa_pp_init must be more than 0 where gwb_pp_init "
                         f"and gawa_pct_init are: the withdrawal or the depletion that "
                         f"locked the GAWA% set the GAWA to it times the GWB, unless the "
                         f"point's grid gave 0% at an attained age the policy reached "
                         f"before the valuation month; it is not at point_id {bad}")
    schedules = set(cdsc_scale().index.get_level_values("cdsc_schedule"))
    bad = table.index[~table["cdsc_schedule"].isin(schedules)].tolist()
    if bad:
        raise ValueError(f"{name}: cdsc_schedule must be a schedule of {cdsc_file}; it is "
                         f"not at point_id {bad}")
    rows = mort_rates().reset_index()
    youngest = rows.groupby("sex")["age"].min()
    oldest = rows.groupby("sex")["age"].max()
    attained = issue_age + months.clip(lower=0) // 12
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


def fund_table():
    """Subaccount allocations and fund expense ratios, from *fund_table.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / fund_file, index_col=["fund_set", "sub_id"])   # noqa: F821


def return_scenario():
    """Gross subaccount returns, read from *return_scenario_sec.csv*.

    Indexed by ``(scenario_id, sub_id, t)``, where ``t`` is a **valuation** month, 0 at
    the valuation date, and read as a step function of ``t``: each row states the monthly
    gross fund return that holds from that month until the next row for the same scenario
    and subaccount. ``VA_US_S``'s reader, unchanged and pointed at this model's own file
    through ``return_scenario_file``.

    The file is generated from ``VA_US_S``'s *return_scenario.csv*, whose ``t`` is the
    elapsed **policy** month. Each of ``VA_US_S``'s scenarios is here under its own id,
    which is where the policy months of a contract issued at the valuation date fall. Each
    row of the model point table valued in force at policy month ``m`` reads a copy of its
    path re-based to ``m``, ``{id}-M{m}``: the returns ``VA_US_S`` set before month ``m``
    collapse to the return in force at ``m``, at ``t = 0``, and the later rows move ``m``
    months earlier, each subaccount on its own rows. Each row issued ``k`` months after the
    valuation date reads a copy moved ``k`` months later, ``{id}-F{k}``, which sets no
    return before its issue month. Rows that move alike share a copy. So every row reads
    each policy month's return at the valuation month that policy month falls in, and the
    model reproduces ``VA_US_S`` there.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / return_scenario_file,                          # noqa: F821
        index_col=["scenario_id", "sub_id", "t"])


def rate_scenario():
    """The exogenous market rate series, read from *rate_scenario_sec.csv*.

    Indexed by ``(scenario_id, t)``, where ``t`` is a **valuation** month, 0 at the
    valuation date, and read as a step function of ``t``. It carries the quarterly average
    of daily VIX-squared driving the optional non-discretionary fee reset [S4][S6] and the
    10-year Constant Maturity Treasury rate driving the optional formula-linked GMDB roll-up
    [S7]. Neither is used by the base run. ``VA_US_S``'s reader, unchanged and pointed at
    this model's own file through ``rate_scenario_file``.

    The file is generated from ``VA_US_S``'s *rate_scenario.csv*, whose ``t`` is the elapsed
    policy month, re-based as :func:`return_scenario` is: ``VA_US_S``'s scenarios under
    their own ids, and a copy ``{id}-M{m}`` or ``{id}-F{k}`` for each row valued in force
    or issued later.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / rate_scenario_file,                            # noqa: F821
        index_col=["scenario_id", "t"])


def gawa_pct_table():
    """The GAWA% grid by attained age band, read from *gawa_pct_table.csv*.

    Indexed by ``(gawa_grid, age_from)``; the applicable row is the highest ``age_from``
    at or below the attained age at the first withdrawal [S3].
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / gawa_pct_file, index_col=["gawa_grid", "age_from"])  # noqa: F821


def cdsc_table():
    """The withdrawal charge scale, read from *cdsc_table.csv*.

    Indexed by ``(cdsc_schedule, completed_years)``, where the key is completed years
    **since receipt of the premium being withdrawn**, not the contract year [S2].
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / cdsc_file,                                     # noqa: F821
        index_col=["cdsc_schedule", "completed_years"])


def transaction_table():
    """Scheduled policyholder transactions, read from *transaction_table.csv*.

    Indexed by ``(txn_id, t)``, the elapsed policy month (0-based), with a gross premium
    and a gross withdrawal per month; a month with no row takes neither. Scheduled
    withdrawals are **added to** the utilization withdrawal the base run derives from the
    GLWB, which is how the excess algebra is exercised.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / transaction_file, index_col=["txn_id", "t"])   # noqa: F821


def fund_values_init():
    """The subaccount values of the opening state, one column a subaccount, by point.

    Indexed by ``point_id``, with a float column for each subaccount any fund set of
    :func:`fund_sets` holds, read from the checked table's ``sa_pp_init_<i>`` column: the
    value per contract of subaccount ``i`` entering month 0, before any month-0 event.
    ``Projection.sa_pp_init``, its one reader, reads a point's value there.
    :func:`model_point_table` has already required the column of every subaccount a point's
    set holds, a finite number, zero or more to within a cent, and 0 on a contract not yet
    in force; a blank cell of a subaccount the point's set lacks, which no projection reads,
    is 0.0 here.
    """
    table = model_point_table()
    ids = sorted(set(fund_sets().index.get_level_values("sub_id")))
    cols = {i: pd.to_numeric(table[f"sa_pp_init_{i}"], errors="coerce")  # noqa: F821
            .fillna(0.0).astype("float64")
            for i in ids if f"sa_pp_init_{i}" in table.columns}
    return pd.DataFrame(cols, index=table.index)                     # noqa: F821


def mort_rates():
    """Annual mortality by attained age and sex, as :func:`mort_table` reads it, checked.

    Indexed by ``(age, sex)``, the age read by value, once, so that an age written ``61.0``
    is 61, as ``VA_US_S``'s lookup matches it, and sorted. ``Projection.mort_rate_base_at``,
    the table's one reader, reads it here, and takes its last age,
    :func:`mort_last_age`, from the same checked ages, so a projection meets the check
    first. An age that is not a whole number, text and a blank among them, a blank sex, a
    rate that is not a number from 0 to 1, blank and text among them, and a sex whose ages
    do not run one row an age, without a gap or a repeat, are refused, naming the file, the
    column and the lines they are on: for the last, each age a sex repeats, with its lines,
    and each age or span of ages it lacks between its first and its last, every one of them
    in one message. ``VA_US_S`` takes the raw ages' largest for its last: one written as
    text raises Python's own ``TypeError``, naming no file.
    """
    name = mort_table_file                                           # noqa: F821
    rows = mort_table().reset_index()
    lines = rows.index + 2
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
    faults = []
    for sex, run in ages.groupby(rows["sex"]):
        for key in sorted(set(run[run.duplicated()])):
            on = lines[((rows["sex"] == sex) & (ages == key)).to_numpy()].tolist()
            faults.append(f"sex {sex} age {key} repeats on lines {on}")
        held = sorted(set(run))
        for a, b in zip(held, held[1:]):
            if b - a > 1:
                faults.append(f"no line holds sex {sex} " + (
                    f"ages {a + 1} to {b - 1}" if b - a > 2 else f"age {a + 1}"))
    if faults:
        raise ValueError(f"{name}: the ages of each sex must run one row an age, without a "
                         f"gap or a repeat; " + "; ".join(faults))
    keys = pd.MultiIndex.from_arrays([ages, rows["sex"]], names=["age", "sex"])  # noqa
    return pd.DataFrame({"mort_rate": rates.to_numpy(dtype="float64")},  # noqa: F821
                        index=keys).sort_index()


def mort_last_age():
    """The last attained age :func:`mort_rates` gives a rate for, an int.

    ``Projection.mort_rate_base_at`` reads every older age at it, as ``VA_US_S`` caps the
    age at the table's last. No attained age in cover is older than 119 at the shipped
    ``Projection.omega_age``, 120, where cover ends, and the shipped table runs to 120.
    """
    return int(mort_rates().index.get_level_values("age").max())


def fund_sets():
    """The fund sets, as :func:`fund_table` reads them, checked.

    Indexed by ``(fund_set, sub_id)``, the subaccount read by value, once, and kept in file
    order, which ``Projection.sub_ids`` returns. ``Projection.sub_ids``, ``alloc`` and
    ``fund_expense_rate``, the table's three readers, read it here, so a projection meets
    the check first. A blank ``fund_set``, a subaccount that is not a whole number, 1 or
    more, text and a blank among them, an allocation or a fund expense ratio that is not a
    number from 0 to 1, blank and text among them, a set that holds a subaccount twice, and
    a set whose allocations do not sum to 1 within 1e-12 are refused, naming the file, the
    column and the lines, or the sets, they are on.
    """
    name = fund_file                                                 # noqa: F821
    rows = fund_table().reset_index()
    lines = rows.index + 2
    bad = lines[rows["fund_set"].isna().to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: fund_set must not be blank; it is on line {bad}")
    subs = pd.to_numeric(rows["sub_id"], errors="coerce")            # noqa: F821
    bad = lines[(~((subs % 1 == 0) & (subs >= 1))).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: sub_id must be a whole number, 1 or more; it is not on "
                         f"line {bad}")
    cols = {}
    for column in ("alloc", "fund_expense"):
        v = pd.to_numeric(rows[column], errors="coerce")             # noqa: F821
        bad = lines[(~((v >= 0) & (v <= 1))).to_numpy()].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a number from 0 to 1; it is not "
                             f"on line {bad}")
        cols[column] = v.to_numpy(dtype="float64")
    keys = pd.MultiIndex.from_arrays([rows["fund_set"], subs.astype("int64")],  # noqa
                                     names=["fund_set", "sub_id"])
    bad = lines[keys.duplicated(keep=False)].tolist()
    if bad:
        raise ValueError(f"{name}: a fund set must hold each subaccount once; one holds "
                         f"one twice on lines {bad}")
    out = pd.DataFrame(cols, index=keys)                             # noqa: F821
    sums = out["alloc"].groupby(level="fund_set").sum()
    bad = sorted(sums.index[~((sums - 1.0).abs() <= 1e-12)])
    if bad:
        raise ValueError(f"{name}: the allocations of a fund set must sum to 1; they do "
                         f"not in fund set {bad}")
    return out


def return_scenario_steps():
    """The return scenarios, as :func:`return_scenario` reads them, checked.

    Indexed by ``(scenario_id, sub_id, t)``, each subaccount and each ``t``, a valuation
    month, read by value, once, and sorted. ``Projection.inv_return_mth``, the table's one
    reader, reads it here, so a projection meets the check first. A month that is not a
    whole number, 0 or more, text and a blank among them, a blank ``scenario_id``, a
    subaccount that is not a whole number, 1 or more, a gross return that is not a finite
    number above -1, blank and text among them, and a scenario that sets two returns for
    one subaccount at one month are refused, naming the file, the column and the lines they
    are on. A scenario may start after ``t = 0``, for business issued later, so the month a
    scenario must start by is the point's: :func:`model_point_table` refuses a point whose
    scenario sets no return for a subaccount of its fund set by the first month the point
    is on the books.
    """
    name = return_scenario_file                                      # noqa: F821
    rows = return_scenario().reset_index()
    lines = rows.index + 2
    months = pd.to_numeric(rows["t"], errors="coerce")               # noqa: F821
    bad = lines[(~((months % 1 == 0) & (months >= 0))).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: t must be a whole number, 0 or more; it is not on line "
                         f"{bad}")
    bad = lines[rows["scenario_id"].isna().to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: scenario_id must not be blank; it is on line {bad}")
    subs = pd.to_numeric(rows["sub_id"], errors="coerce")            # noqa: F821
    bad = lines[(~((subs % 1 == 0) & (subs >= 1))).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: sub_id must be a whole number, 1 or more; it is not on "
                         f"line {bad}")
    r = pd.to_numeric(rows["gross_return"], errors="coerce")         # noqa: F821
    bad = lines[(~((r > -1) & (r < float("inf")))).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: gross_return must be a number above -1; it is not on "
                         f"line {bad}")
    keys = pd.MultiIndex.from_arrays(                                # noqa: F821
        [rows["scenario_id"], subs.astype("int64"), months.astype("int64")],
        names=["scenario_id", "sub_id", "t"])
    bad = lines[keys.duplicated(keep=False)].tolist()
    if bad:
        raise ValueError(f"{name}: a scenario must set one return a month for each "
                         f"subaccount; one sets two on lines {bad}")
    return pd.DataFrame({"gross_return": r.to_numpy(dtype="float64")},  # noqa: F821
                        index=keys).sort_index()


def rate_scenario_steps():
    """The rate scenarios, as :func:`rate_scenario` reads them, checked.

    Indexed by ``(scenario_id, t)``, each ``t`` a valuation month read by value, once, and
    sorted. ``Projection.scenario_rate``, the table's one reader, reads it here, so a
    projection meets the check first. A month that is not a whole number, 0 or more, text
    and a blank among them, a blank ``scenario_id``, a VIX-squared average that is not a
    finite number, zero or more, a CMT rate that is not a finite number above -1, and a
    scenario that sets two levels at one month are refused, naming the file, the column and
    the lines they are on. The month a scenario must start by is the point's, as for
    :func:`return_scenario_steps`, and only on a point the ``vix`` fee or the
    ``cmt_linked`` roll-up reads it for: on any other point no level is read.
    """
    name = rate_scenario_file                                        # noqa: F821
    rows = rate_scenario().reset_index()
    lines = rows.index + 2
    months = pd.to_numeric(rows["t"], errors="coerce")               # noqa: F821
    bad = lines[(~((months % 1 == 0) & (months >= 0))).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: t must be a whole number, 0 or more; it is not on line "
                         f"{bad}")
    bad = lines[rows["scenario_id"].isna().to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: scenario_id must not be blank; it is on line {bad}")
    cols = {}
    for column, low in (("vix_sq", 0.0), ("cmt10", -1.0)):
        v = pd.to_numeric(rows[column], errors="coerce")             # noqa: F821
        ok = (v >= low) if column == "vix_sq" else (v > low)
        bad = lines[(~(ok & (v < float("inf")))).to_numpy()].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a number "
                             + ("zero or more" if column == "vix_sq" else "above -1")
                             + f"; it is not on line {bad}")
        cols[column] = v.to_numpy(dtype="float64")
    keys = pd.MultiIndex.from_arrays(                                # noqa: F821
        [rows["scenario_id"], months.astype("int64")], names=["scenario_id", "t"])
    bad = lines[keys.duplicated(keep=False)].tolist()
    if bad:
        raise ValueError(f"{name}: a scenario must set one level a month; one sets two on "
                         f"lines {bad}")
    return pd.DataFrame(cols, index=keys).sort_index()               # noqa: F821


def gawa_pct_bands():
    """The GAWA% grids, as :func:`gawa_pct_table` reads them, checked.

    Indexed by ``(gawa_grid, age_from)``, each band's first age read by value, once, and
    sorted. ``Projection.gawa_pct_at_age``, the table's one reader, reads it here, so a
    projection meets the check first. A blank ``gawa_grid``, an ``age_from`` that is not a
    whole number, 0 or more, text and a blank among them, a percentage that is not a number
    from 0 to 1, blank and text among them, and a grid that starts a band twice at one age
    are refused, naming the file, the column and the lines they are on. A grid is banded,
    so its ages need not run one a year: each band holds from its ``age_from`` until the
    next band of the same grid, and an age below the first band reads 0%.
    """
    name = gawa_pct_file                                             # noqa: F821
    rows = gawa_pct_table().reset_index()
    lines = rows.index + 2
    bad = lines[rows["gawa_grid"].isna().to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: gawa_grid must not be blank; it is on line {bad}")
    ages = pd.to_numeric(rows["age_from"], errors="coerce")          # noqa: F821
    bad = lines[(~((ages % 1 == 0) & (ages >= 0))).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: age_from must be a whole number, 0 or more; it is not "
                         f"on line {bad}")
    pct = pd.to_numeric(rows["gawa_pct"], errors="coerce")           # noqa: F821
    bad = lines[(~((pct >= 0) & (pct <= 1))).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: gawa_pct must be a number from 0 to 1; it is not on "
                         f"line {bad}")
    keys = pd.MultiIndex.from_arrays([rows["gawa_grid"], ages.astype("int64")],  # noqa
                                     names=["gawa_grid", "age_from"])
    bad = lines[keys.duplicated(keep=False)].tolist()
    if bad:
        raise ValueError(f"{name}: a grid must start each band once; one starts a band "
                         f"twice on lines {bad}")
    return pd.DataFrame({"gawa_pct": pct.to_numpy(dtype="float64")},  # noqa: F821
                        index=keys).sort_index()


def gawa_pct_zero_band(grid, youngest, oldest):
    """Whether GAWA% grid ``grid`` gives 0% at an attained age ``youngest`` to ``oldest``.

    Below the grid's first band, which reads 0% as ``Projection.gawa_pct_at_age`` reads it,
    or in a band at 0%, which a grid may hold: an explicit loop over the ages, each read at
    the band starting at the largest ``age_from`` at or below it, in
    :func:`gawa_pct_bands`, the grids with their keys checked.  Called with the ages a
    contract in force reached before the valuation month, from its issue age to its age in
    the month before, by :func:`model_point_table`, whose rules of the locked GAWA% read
    it, and by :func:`gawa_pct_zero_by_point`; the GAWA% the first withdrawal or the
    depletion locks is the grid's at the age it falls at, so it is 0 only where this is
    True.
    """
    bands = gawa_pct_bands().loc[grid]
    starts = list(bands.index)
    for a in range(youngest, oldest + 1):
        held = -1
        for b in starts:
            if held < b <= a:
                held = b
        if held < 0 or bands.loc[held, "gawa_pct"] == 0:
            return True
    return False


def gawa_pct_zero_by_point():
    """Whether each point's grid gave 0% at an attained age it reached before month 0.

    Indexed by ``point_id``, a bool for each point of :func:`model_point_table`: on a
    contract in force, :func:`gawa_pct_zero_band` over its ``glwb_option`` from its issue
    age to its attained age in the month before the valuation month; False on one not yet
    in force, which has reached no age.  ``Projection.proj_len``, its one reader, checks
    against it the GAWA% of a depleted contract that has not withdrawn, a rule that needs
    ``Projection.av_depletion_threshold``; a vector built here from inputs that live here
    (R2), so that the projection reads the grid at no age before its first on the books.
    """
    table = model_point_table()
    flags = []
    for point_id in table.index:
        d = int(table.at[point_id, "duration_mth"])
        youngest = int(table.at[point_id, "age_at_entry"])
        flags.append(d > 0 and gawa_pct_zero_band(table.at[point_id, "glwb_option"],
                                                   youngest, youngest + (d - 1) // 12))
    return pd.Series(flags, index=table.index, dtype=bool)          # noqa: F821


def cdsc_scale():
    """The withdrawal charge schedules, as :func:`cdsc_table` reads them, checked.

    Indexed by ``(cdsc_schedule, completed_years)``, the years read by value, once, and
    sorted. ``Projection.surr_charge_rate_at``, the table's one reader, reads it here, and
    takes each schedule's last year from the same checked years, so a projection meets the
    check first. A blank ``cdsc_schedule``, a year that is not a whole number, text and a
    blank among them, a charge that is not a number from 0 to 1, blank and text among them,
    and years that do not run from 0, one row a year, without a gap or a repeat, are
    refused, naming the file, the column and the lines they are on: for the last, each year
    below 0 or repeated, with its lines, and each year or span of years a schedule lacks
    from 0 to its last, every one of them in one message. Each schedule's last row holds
    for every later year. ``VA_US_S`` takes ``int()`` of the raw years' largest: one
    written as text raises Python's own message, naming no file.
    """
    name = cdsc_file                                                 # noqa: F821
    rows = cdsc_table().reset_index()
    lines = rows.index + 2
    bad = lines[rows["cdsc_schedule"].isna().to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: cdsc_schedule must not be blank; it is on line {bad}")
    years = pd.to_numeric(rows["completed_years"], errors="coerce")  # noqa: F821
    bad = lines[(~(years % 1 == 0)).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: completed_years must be a whole number; it is not on "
                         f"line {bad}")
    rate = pd.to_numeric(rows["surr_charge_rate"], errors="coerce")  # noqa: F821
    bad = lines[(~((rate >= 0) & (rate <= 1))).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: surr_charge_rate must be a number from 0 to 1; it is "
                         f"not on line {bad}")
    years = years.astype("int64")
    faults = []
    for sched, run in years.groupby(rows["cdsc_schedule"]):
        mine = (rows["cdsc_schedule"] == sched).to_numpy()
        for key in sorted(set(run[run < 0])):
            faults.append(f"schedule {sched} completed_years {key}, below 0, is on lines "
                          f"{lines[mine & (years == key).to_numpy()].tolist()}")
        for key in sorted(set(run[run.duplicated() & (run >= 0)])):
            faults.append(f"schedule {sched} completed_years {key} repeats on lines "
                          f"{lines[mine & (years == key).to_numpy()].tolist()}")
        held = [-1] + sorted(set(run[run >= 0]))
        if len(held) == 1:
            faults.append(f"no line holds schedule {sched} completed_years 0")
        for a, b in zip(held, held[1:]):
            if b - a > 1:
                faults.append(f"no line holds schedule {sched} completed_years {a + 1}"
                              + (f" to {b - 1}" if b - a > 2 else ""))
    if faults:
        raise ValueError(f"{name}: the completed years of each schedule must run from 0, "
                         f"one row a year, without a gap or a repeat; " + "; ".join(faults))
    keys = pd.MultiIndex.from_arrays([rows["cdsc_schedule"], years],  # noqa: F821
                                     names=["cdsc_schedule", "completed_years"])
    return pd.DataFrame({"surr_charge_rate": rate.to_numpy(dtype="float64")},  # noqa
                        index=keys).sort_index()


def transactions():
    """The transaction programmes, as :func:`transaction_table` reads them, checked.

    Indexed by ``(txn_id, t)``, each ``t`` an elapsed policy month read by value, once, as
    ``VA_US_S``'s exact-key lookup matches it, and sorted.
    ``Projection.prem_scheduled_pm`` and ``Projection.wd_scheduled_pm``, the readers of its
    two columns, read it here, so a projection meets the check first; so does
    :func:`model_point_table`, for a programme's month-0 premium. A blank ``txn_id``, a
    month that is not a whole number, 0 or more, text and a blank among them, an amount
    that is not a finite number, zero or more, blank and text among them, and a programme
    that holds two rows at one month are refused, naming the file, the column and the lines
    they are on. ``VA_US_S``'s lookup matches the raw months: one written as text turns
    them all to text, and every scheduled premium and withdrawal of every programme is then
    zero.
    """
    name = transaction_file                                          # noqa: F821
    rows = transaction_table().reset_index()
    lines = rows.index + 2
    bad = lines[rows["txn_id"].isna().to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: txn_id must not be blank; it is on line {bad}")
    months = pd.to_numeric(rows["t"], errors="coerce")               # noqa: F821
    bad = lines[(~((months % 1 == 0) & (months >= 0))).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: t must be a whole number, 0 or more; it is not on line "
                         f"{bad}")
    cols = {}
    for column in ("prem_amount", "wd_amount"):
        v = pd.to_numeric(rows[column], errors="coerce")             # noqa: F821
        bad = lines[(~((v >= 0) & (v < float("inf")))).to_numpy()].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a number, zero or more; it is not "
                             f"on line {bad}")
        cols[column] = v.to_numpy(dtype="float64")
    keys = pd.MultiIndex.from_arrays([rows["txn_id"], months.astype("int64")],  # noqa
                                     names=["txn_id", "t"])
    bad = lines[keys.duplicated(keep=False)].tolist()
    if bad:
        raise ValueError(f"{name}: a programme must hold one row a month; one holds two on "
                         f"lines {bad}")
    return pd.DataFrame(cols, index=keys).sort_index()               # noqa: F821


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table_sec.csv"

mort_table_file = "mort_table.csv"

fund_file = "fund_table.csv"

return_scenario_file = "return_scenario_sec.csv"

rate_scenario_file = "rate_scenario_sec.csv"

gawa_pct_file = "gawa_pct_table.csv"

cdsc_file = "cdsc_table.csv"

transaction_file = "transaction_table.csv"

future_horizon_mth = 120

pd = ("Module", "pandas")
