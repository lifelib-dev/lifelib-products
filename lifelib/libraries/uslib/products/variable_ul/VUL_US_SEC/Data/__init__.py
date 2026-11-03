# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The ten input CSVs are read here, **once per model**, and referenced from
:mod:`~.VUL_US_SEC.Projection` as ``data``. :mod:`~.VUL_US_SEC.Projection` is
parameterized by ``point_id``, so each ``Projection[N]`` is a separate ItemSpace with
its own cells cache; if the readers lived there, every model point would re-read every
file. Holding them in an unparameterized Space reads each file once no matter how many
policies are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/variable_ul/``, rather than data stored inside the model. The model folder
therefore holds nothing but formulas -- no ``_data/``, no IOSpec, no embedded values --
so a diff of the model shows logic changes only. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``VUL_US_SEC`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

**Nine of the tables are VUL_US_S's.** The subaccount lineup, the return scenario, the
guaranteed COI scale, the corridor factors, the mortality table, the class factors, the
lapse table, the premium persistency scale and the surrender charge schedules are the
files :mod:`~.VUL_US_S` reads, read here in place: one copy of each table serves both
models, so an edit to one reaches both. The model point table is this model's own,
``model_point_table_sec.csv``; it sits beside ``VUL_US_S``'s ``model_point_table.csv``,
which this model never opens.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so
the model works wherever the repository is checked out. Each table has a filename
Reference and a reader Cells:

======================  ============================  ==============================
Reference               Cells                         File
======================  ============================  ==============================
model_point_file        model_point_table()           model_point_table_sec.csv
subaccount_file         subaccount_table()            subaccount_table.csv
scenario_file           scenario_table()              scenario_table.csv
coi_rates_file          coi_rates()                   coi_rates.csv
corridor_file           corridor_factors()            corridor_factors.csv
mort_table_file         mort_table()                  mort_table.csv
class_factor_file       class_factor_table()          class_factor_table.csv
lapse_table_file        lapse_table()                 lapse_table.csv
prem_persistency_file   prem_persistency_table()      prem_persistency.csv
surr_charge_file        surr_charge_table()           surr_charge_table.csv
======================  ============================  ==============================

**The model point table is checked as it is read.** Ten of its columns are the in-force
interface, with the shipped lineup of two subaccounts: ``policy_count`` and
``duration_mth``, as in ``basiclife.BasicTerm_SE``; six columns of an in-force policy's
opening state, one ``sa_pp_init_<i>`` for each subaccount, the value of the fixed option
and of the loan account, the debt and the face in force; and ``VUL_US_S``'s two
first-month pins, which are not state. :func:`model_point_table` refuses a table that lacks
any of them, or any column of ``VUL_US_S``'s own that the projection reads as a number,
repeats a ``point_id``, holds a count, a duration, an issue age or an amount no policy can
have, a surrender-charge flag that is not ``True`` or ``False``, or an opening state no
policy can be in. The checks run in turn, and the first that fails raises, naming the
missing column or every point that fails it. It also refuses a policy to be issued more
than ``future_horizon_mth`` months after the valuation date, 120 months as shipped:
future new business is written over a stated horizon, so that no frame runs longer than
the projection from issue plus that horizon. Set to 0, the Reference refuses future new
business altogether. Whether a point is still inside the projection at the valuation
date is a rule of the product rather than of the table, and ``Projection.proj_len``
checks it.

**So are the nine assumption tables.** Each table read at a policy year or an attained
age has one reader in ``Projection``, keyed by the year or the age, and that reader takes
the table's extent -- the last policy year, or the first and last ages, beyond which it
reads the nearest row -- from a cell here that reads the key column by value, once, and
checks the table: :func:`prem_persistency_last_year`, :func:`lapse_last_year`,
:func:`corridor_age_first` and :func:`corridor_age_last`, :func:`mort_age_first` and
:func:`mort_age_last`, and, for each issue-age cell of the COI scale,
:func:`coi_rate_last_years`. A key that is blank, text or not a whole number is
refused, naming the file, the column and the lines it is on. So are keys that do not run
one row a year or an age, without a gap or a repeat, policy years from 1, the message
naming each key that repeats, with its lines, and each that is missing. And so is a rate
that is blank, text or infinite, naming the column and its lines, and a lapse or mortality
rate outside 0 to 1: each is a probability, and the monthly rate ``1 - (1 - q)^(1/12)`` has
no real value past 1. :func:`class_count`
and :func:`surr_charge_count` check the class factors and the surrender-charge schedules
the same way, for the per-point joins that read them, and :func:`surr_charge_count`
refuses a run-off that is not a whole number of years, 1 or more, which the projection
divides by and counts policy years on. A class factor, a guaranteed COI rate, a fund
expense, a premium persistency factor and a surrender charge below 0 are refused too: each
would project, with every check passing, a count or a charge no policy can have, a
negative death or premium, a credit for the insurance or the fund, or a surrender charge
that rises once its schedule has run off.
:func:`subaccounts` checks the lineup, whose ids
name the model point table's columns, and :func:`scenario_last_mths` the return
scenario, whose months run one row a month for each scenario and subaccount. Each reader
asks for its extent, the count or the lineup before it reads a value, so a projection
meets the checks first.

``VUL_US_S``'s readers take each extent from the key column as pandas reads it, where a
blank key is a missing value the extent skips: the table is cut short, and every later
year reads the last good row, without a word. A blank value is a missing value to it
too, which shows in its flows or is lost in a ``min`` or a ``max``: a blank corridor
factor reads as no corridor, a blank surrender charge as none, and a blank COI rate, fund
expense or return reaches the account value as a missing value, which the cash value's
floor at zero then reads as nothing to pay on a surrender. Here each is refused, by name,
and so is a blank, text or infinite amount in the model point table.

``scenario_table.csv`` is the **separate-account return scenario**: monthly *gross*
subaccount returns keyed by ``scenario_id``, ``subaccount_id`` and the month ``t``, the
same index as ``Projection``'s ``t``, which counts months from the valuation date: a
scenario is a path of the economy from that date, one path for every point of a block,
however old the policy, with the last month of a scenario repeating for the rest of the
projection. Fund expenses and the M&E charge are applied on top of these in
:func:`~.VUL_US_SEC.Projection.inv_return_mth`, so the table holds gross returns only. A
stochastic set is a data change -- more ``scenario_id`` values -- not a formula change.
The shipped scenarios are deterministic: ``WE`` is the worked example's month (+1.00%
equity, -0.50% bond) followed by a level 6% a year gross path, and ``LEVEL6`` is that
level path throughout. A scenario's months may start after month 0 -- a path re-based to
a policy issued after the valuation date holds nothing before its issue month -- and a
read before a scenario's first month raises.

``coi_rates.csv`` carries the **guaranteed maximum** monthly rate per $1,000 of net
amount at risk; the current scale is that times
``Projection.coi_curr_factor``, or the model point's first-month pin. The notes require
the 2017 CSO ultimate ANB table for the guaranteed maximum and the 2015 VBT for
best-estimate mortality; both are licensed and may not be reproduced here, so
``coi_rates.csv`` and ``mort_table.csv`` ship small illustrative **[std]** tables
instead -- the COI scale anchored on the one disclosed guaranteed point in the notes
(male 45 standard non-tobacco, policy year 1 = $0.22 [S4]) and the mortality table well
below it, because the notes insist the COI *charge* basis and the death *decrement*
basis must never be conflated. To swap in a licensed basis, replace either file with a
same-schema one, or point ``mort_table_file`` at a different name before the model
computes anything. No formula changes. Replacing the file changes :mod:`~.VUL_US_S` too,
which reads the same one.
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

    Indexed by ``point_id``.  Ten columns are the in-force interface, with the shipped
    lineup of two subaccounts: ``policy_count`` and ``duration_mth``, the completed policy
    months at the valuation date, as in ``basiclife.BasicTerm_SE``; six columns of the
    opening state, per policy, as the policy stands at the start of month 0, before any
    month-0 event, one ``sa_pp_init_<i>`` for each subaccount among them; and
    ``VUL_US_S``'s two first-month pins, which are not state:

    * ``sa_pp_init_<i>``, one for each subaccount :func:`subaccounts` lists, and
      ``fa_pp_init``: the value of each subaccount and of the fixed option entering
      month 0, ``VUL_US_S``'s own columns;
    * ``la_pp_init``: the loan account, the collateral the loan has moved out of the
      investment options, entering month 0;
    * ``loan_bal_init``: the policy debt entering month 0, ``VUL_US_S``'s own column;
    * ``sum_assured_init``: the face in force entering month 0, after every Option A
      withdrawal cut to date;
    * ``corridor_override_m1`` and ``coi_rate_override_m1``: ``VUL_US_S``'s first-month
      pins, which apply in the valuation month, ``t = 0``, blank where a point pins
      nothing.

    The rest are ``VUL_US_S``'s, except ``row_kind``, ``source_policy_id`` and
    ``source_mth``, which record where the generator took each shipped row from and which
    no formula reads.

    The checks run over the whole table at once, and the first that fails raises
    ``ValueError``, naming the missing column or every point it fails on:

    * the in-force columns are present, and so are ``age_at_entry``, the
      surrender-charge flag ``has_surr_charge``, the amounts the projection reads as
      numbers, ``sum_assured``, ``premium_pp_ann`` and ``wd_pp``, and the shares it
      reads, ``load_prem_rate``, each ``alloc_<i>`` and ``alloc_fixed``;
    * no ``point_id`` appears twice;
    * ``policy_count`` is a number, zero or more;
    * ``duration_mth`` is a whole number of months: positive for a policy in force, 0
      for one issued at the valuation date, negative for one issued later;
    * no policy is issued more than ``future_horizon_mth`` months after the valuation
      date, so ``duration_mth`` is ``-future_horizon_mth`` or more.  At 0 the model takes
      no future new business, and the message says so; a negative horizon is itself
      refused;
    * ``age_at_entry`` is a whole number of years, 0 or more: the projection takes its
      ``int()`` and counts its frame and every attained age on it;
    * ``sum_assured`` is a number above 0, the face at issue, which every policy holds;
      each of ``premium_pp_ann`` and ``wd_pp`` is a number, zero or more; and each of
      ``load_prem_rate``, ``alloc_<i>`` and ``alloc_fixed``, the share of each premium
      the load takes and the shares of each net premium the accounts take, is a number
      from 0 to 1.  Each reaches the account value, and a blank one would reach it as a
      missing value, which the cash value's floor, the net amount at risk's and the
      corridor's ``max`` then lose without a word: in ``VUL_US_S`` a blank face projects
      no death claim on Option A, and a missing value on Option B.  A load past 1 would
      credit the accounts a net premium below 0, every check passing, and allocations
      past 1 more than the net premium;
    * ``has_surr_charge`` is ``True`` or ``False``, as pandas reads those words in any
      case.  A blank, a number or any other text is refused: one text value turns the
      whole column into text, where ``"False"`` is a true string, so every point would
      read as carrying a surrender charge;
    * each subaccount, the fixed option, the loan account, the debt and the face in force
      is a number, zero or more.  A balance is never negative in force.  ``VUL_US_S``
      lets a subaccount fall below zero once the point is in permanent shortfall, because
      it does not implement the grace cascade that would end such a policy; no policy in
      force can hold that balance, so a point in permanent shortfall is restated no later
      than the last month its subaccounts are still zero or more;
    * a policy not yet in force, ``duration_mth`` 0 or less, has no opening state: it is
      issued with none, at the face :func:`~.VUL_US_SEC.Projection.sum_assured`;
    * ``sum_assured_init`` is above 0 on a policy in force, which holds a face, so an
      extract that leaves the column at zero is refused rather than projected on the
      corridor alone;
    * ``sum_assured_init`` is at most ``sum_assured``, the face at issue, since face
      increases are not modelled.  A face below it is accepted, whether a withdrawal cut
      it or an elective decrease the model does not implement, and is projected from the
      value given;
    * the loan account is above 0 exactly where the debt is: a loan moves value out of
      the investment options into the loan account, and the model takes no new loan and
      no repayment, so the two are held together from the loan's first day, each at its
      own rate;
    * each pin is blank, or a number, zero or more;
    * each pin is blank on a policy issued after the valuation date: a pin applies in the
      valuation month, ``t = 0``, before such a policy is issued, so it would never apply.
    """
    name = model_point_file                                          # noqa: F821
    table = pd.read_csv(input_dir() / name, index_col="point_id")    # noqa: F821
    accounts = []
    allocations = []
    for i in subaccounts().index:
        accounts.append(f"sa_pp_init_{i}")
        allocations.append(f"alloc_{i}")
    state = (*accounts, "fa_pp_init", "la_pp_init", "loan_bal_init", "sum_assured_init")
    pins = ("corridor_override_m1", "coi_rate_override_m1")
    amounts = ("premium_pp_ann", "wd_pp")
    shares = ("load_prem_rate", *allocations, "alloc_fixed")
    for column in ("policy_count", "duration_mth", "age_at_entry", "sum_assured", *amounts,
                   *shares, "has_surr_charge", *state, *pins):
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
    ages = pd.to_numeric(table["age_at_entry"], errors="coerce")     # noqa: F821
    bad = table.index[~((ages % 1 == 0) & (ages >= 0))].tolist()
    if bad:
        raise ValueError(f"{name}: age_at_entry must be a whole number of years, 0 or "
                         f"more; it is not at point_id {bad}")
    face = pd.to_numeric(table["sum_assured"], errors="coerce")      # noqa: F821
    bad = table.index[~((face > 0) & (face < float("inf")))].tolist()
    if bad:
        raise ValueError(f"{name}: sum_assured must be a number above 0, the face at "
                         f"issue, which every policy holds; it is not at point_id {bad}")
    for column in amounts:
        v = pd.to_numeric(table[column], errors="coerce")            # noqa: F821
        bad = table.index[~((v >= 0) & (v < float("inf")))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a number, zero or more; it is "
                             f"not at point_id {bad}")
    for column in shares:
        v = pd.to_numeric(table[column], errors="coerce")            # noqa: F821
        bad = table.index[~((v >= 0) & (v <= 1))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a number from 0 to 1; it is not "
                             f"at point_id {bad}")
    flags = table["has_surr_charge"].astype(str).str.lower()
    bad = table.index[~flags.isin(["true", "false"])].tolist()
    if bad:
        raise ValueError(f"{name}: has_surr_charge must be True or False; it is not at "
                         f"point_id {bad}")
    values = {}
    for column in state:
        values[column] = pd.to_numeric(table[column], errors="coerce")  # noqa: F821
    for column in (*accounts, "fa_pp_init"):
        v = values[column]
        bad = table.index[~((v >= 0) & (v < float("inf")))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a number, zero or more: no "
                             f"policy in force holds a negative account value, so restate "
                             f"a point in permanent shortfall no later than the last month "
                             f"its account value is still zero or more; it is not at "
                             f"point_id {bad}")
    for column in ("la_pp_init", "loan_bal_init", "sum_assured_init"):
        v = values[column]
        bad = table.index[~((v >= 0) & (v < float("inf")))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a number, zero or more; it is "
                             f"not at point_id {bad}")
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
    bad = table.index[(months > 0) & ~(values["sum_assured_init"] <= face)].tolist()
    if bad:
        raise ValueError(f"{name}: sum_assured_init must be at most sum_assured, the "
                         f"face at issue, since face increases are not modelled; it is "
                         f"not at point_id {bad}")
    lent = values["loan_bal_init"] > 0
    bad = table.index[(values["la_pp_init"] > 0) != lent].tolist()
    if bad:
        raise ValueError(f"{name}: la_pp_init must be above 0 where loan_bal_init is, and "
                         f"0 where it is 0: the loan account holds a loan's collateral "
                         f"while the loan is outstanding; it is not at point_id {bad}")
    for column in pins:
        v = pd.to_numeric(table[column], errors="coerce")            # noqa: F821
        bad = table.index[table[column].notna()
                          & ~((v >= 0) & (v < float("inf")))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be blank or a number, zero or more; "
                             f"it is not at point_id {bad}")
    for column in pins:
        bad = table.index[(months < 0) & table[column].notna()].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be blank on a policy issued after "
                             f"the valuation date, duration_mth below 0: a pin applies in "
                             f"the valuation month, t = 0, before such a policy is "
                             f"issued; it is not at point_id {bad}")
    return table


def subaccount_table():
    """The separate-account subaccount lineup, read from *subaccount_table.csv*.

    One row per subaccount, giving its name and its annual fund operating expense
    ratio.  The two-subaccount lineup is a **[std]** collapse of the observed menus.
    The projection reads it through :func:`subaccounts`, its checked copy.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / subaccount_file,                               # noqa: F821
        index_col="subaccount_id")


def subaccounts():
    """The subaccount lineup, checked: *subaccount_table.csv* indexed by id, read by value.

    The table :func:`subaccount_table` reads, with its ``subaccount_id`` column read by
    value, once, as an int: an id written ``1.0`` is subaccount 1, and names the model
    point table's ``alloc_1`` and ``sa_pp_init_1``, where ``VUL_US_S``, which names the
    column from the id as pandas reads it, asks a projection for ``sa_pp_init_1.0`` and
    raises.  An id that is blank, text or not a whole number is refused, naming the file
    and the lines it is on; so is a table with no subaccount, and an id on more than one
    row, naming each such id with its lines; and so is a ``fund_expense_ann`` that is
    blank, text, infinite or below 0, naming its lines.  ``Projection.subaccount_ids`` and
    ``Projection.fund_expense_ann``, the lineup's two readers, read this copy and nothing
    else, and :func:`model_point_table` names the columns it checks from its ids, so a
    projection meets the checks first.  Rows keep the file's order.
    """
    name = subaccount_file                                           # noqa: F821
    rows = subaccount_table().reset_index()
    ids = pd.to_numeric(rows["subaccount_id"], errors="coerce")      # noqa: F821
    bad = (rows.index[~(ids % 1 == 0)] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: subaccount_id must be a whole number; it is not on "
                         f"line {bad}")
    if not len(rows):
        raise ValueError(f"{name}: no line holds a subaccount")
    ids = ids.astype("int64")
    faults = []
    for key in sorted(set(ids[ids.duplicated()])):
        faults.append(f"subaccount_id {key} is on line "
                      f"{(ids.index[ids == key] + 2).tolist()}")
    if faults:
        raise ValueError(f"{name}: each subaccount_id must have one row; "
                         + "; ".join(faults))
    values = pd.to_numeric(rows["fund_expense_ann"], errors="coerce")  # noqa: F821
    bad = (rows.index[~((values >= 0) & (values < float("inf")))] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: fund_expense_ann must be a number, zero or more; it is "
                         f"not on line {bad}")
    return rows.assign(subaccount_id=ids,
                       fund_expense_ann=values).set_index("subaccount_id")


def scenario_rows():
    """Monthly gross subaccount returns, read from *scenario_table.csv* in the file's order.

    The table's one read, a plain table on a default index, so that a refusal can name
    the lines a fault is on: :func:`scenario_last_mths` checks it, and
    :func:`scenario_table` indexes it for the projection.
    """
    return pd.read_csv(input_dir() / scenario_file)                  # noqa: F821


def scenario_table():
    """Monthly gross subaccount returns, from *scenario_table.csv*, indexed for lookup.

    Keyed by ``scenario_id``, ``subaccount_id`` and the month ``t``, counted from the
    valuation date, 0-based; months past a scenario's last row repeat it.  Returns are
    **gross**: fund expenses and the M&E charge are applied on top of them in the
    projection, so a table row is the fund's own return before any charge.  The index is
    sorted so partial slices of the three-level key are lexsorted.  It is
    :func:`scenario_rows` indexed, the same frame ``VUL_US_S``'s reader reads, and
    ``Projection.gross_return_mth``, its one reader, asks :func:`scenario_last_mths`
    first, which checks the table.
    """
    return scenario_rows().set_index(
        ["scenario_id", "subaccount_id", "t"]).sort_index()


def scenario_last_mths():
    """The last month of each scenario and subaccount in *scenario_table.csv*, checked.

    A Series of ints, indexed by ``scenario_id`` and ``subaccount_id``: one entry a cell,
    the rows the return path of one subaccount on one scenario is read from, months past
    the last repeating it.  ``scenario_id`` may not be blank, and the two numeric keys,
    ``subaccount_id`` and ``t``, are read by value, once: a key that is blank, text or not
    a whole number is refused, naming the file, the column and the lines it is on.  So is
    a cell whose months do not run one row a month, from 0 or later, without a gap or a
    repeat: the message names the cell, each month that repeats or falls below 0, with
    its lines, and each month missing between the cell's first and its last.  A cell may
    start after month 0: a path re-based to a policy issued after the valuation date holds
    nothing before its issue month, so that a read there raises.  And a
    ``gross_return_mth`` that is blank, text or infinite is refused, naming its lines.
    ``Projection.scenario_last_mth`` takes a point's extent from here before
    ``Projection.gross_return_mth`` reads a return.
    """
    name = scenario_file                                             # noqa: F821
    rows = scenario_rows()
    bad = (rows.index[rows["scenario_id"].isna()] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: scenario_id must not be blank; it is on line {bad}")
    for column in ("subaccount_id", "t"):
        keys = pd.to_numeric(rows[column], errors="coerce")          # noqa: F821
        bad = (rows.index[~(keys % 1 == 0)] + 2).tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a whole number; it is not on line "
                             f"{bad}")
    rows = rows.assign(
        subaccount_id=pd.to_numeric(rows["subaccount_id"]).astype("int64"),  # noqa: F821
        t=pd.to_numeric(rows["t"]).astype("int64"))                          # noqa: F821
    months = rows.groupby(["scenario_id", "subaccount_id"])["t"]
    last = months.max()
    count = months.count()
    run = ((months.min() >= 0) & (last - months.min() + 1 == count)
           & (months.nunique() == count))
    faults = []
    for cell in last.index[~run].tolist():
        held = months.get_group(cell)
        for key in sorted(set(held[held.duplicated() | (held < 0)])):
            faults.append(f"at {cell}, t {key} is on line "
                          f"{(held.index[held == key] + 2).tolist()}")
        cell_run = sorted(set(held[held >= 0]))
        for a, b in zip(cell_run, cell_run[1:]):
            if b - a > 1:
                faults.append(f"at {cell}, no line holds t {a + 1}"
                              + (f" to {b - 1}" if b - a > 2 else ""))
    if faults:
        raise ValueError(f"{name}: the months of each scenario_id and subaccount_id must "
                         f"run one row a month, from 0 or later, without a gap or a "
                         f"repeat; " + "; ".join(faults))
    values = pd.to_numeric(rows["gross_return_mth"], errors="coerce")  # noqa: F821
    bad = (rows.index[~(values.abs() < float("inf"))] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: gross_return_mth must be a number; it is not on line "
                         f"{bad}")
    return last


def coi_rates():
    """Guaranteed maximum monthly COI rates, read from *coi_rates.csv*.

    Per $1,000 of net amount at risk, keyed by issue-age cell and policy year.  An
    illustrative **[std]** stand-in for the licensed 2017 CSO ultimate ANB table.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / coi_rates_file,                                # noqa: F821
        index_col=["sex", "rate_class", "age_at_entry", "policy_year"])


def corridor_factors():
    """The GPT corridor factor table by attained age, read from *corridor_factors.csv*."""
    return pd.read_csv(input_dir() / corridor_file, index_col="age")  # noqa: F821


def mort_table():
    """The best-estimate annual mortality table by age, read from *mort_table.csv*."""
    return pd.read_csv(input_dir() / mort_table_file, index_col="age")  # noqa: F821


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
    face and the number of policy years over which it runs off linearly.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / surr_charge_file,                              # noqa: F821
        index_col="surr_charge_id")


def prem_persistency_last_year():
    """The last policy year *prem_persistency.csv* gives a factor for, the table checked.

    The ``policy_year`` column is read by value, once, as the lookup matches it, so a year
    written ``5.0`` is year 5.  A key that is blank, text or not a whole number is
    refused, naming the file, the column and the lines it is on.  So are policy years
    that do not run from 1, one row a year, without a gap or a repeat: the message names
    each year that repeats or falls below 1, with its lines, and each year missing from 1
    to the last.  And so is a ``prem_persistency`` factor that is blank, text, infinite or
    below 0, naming its lines: a fraction of the planned premium, which below 0 would pay
    a negative premium, every check passing.  ``Projection.prem_persistency_py``, the
    table's one reader, takes its extent from here before it reads a factor, so a
    projection meets the checks first.
    Only the behaviour module reads the table, so a run with ``dyn_behavior_on`` off never
    asks for it.
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
    bad = (factors.index[~((factors >= 0) & (factors < float("inf")))] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: prem_persistency must be a number, zero or more; it is "
                         f"not on line {bad}")
    return int(years.max())


def lapse_last_year():
    """The last policy year *lapse_table.csv* gives a rate for, the table checked.

    Read and checked as :func:`prem_persistency_last_year` reads and checks its own
    table, the rate checked being ``lapse_rate_ann``, which must be from 0 to 1, as a
    probability: ``Projection.lapse_rate_mth``'s ``1 - (1 - q)^(1/12)`` has no real value
    past 1, and below 0 the count would grow by its lapses.
    ``Projection.lapse_rate_base_py``, the table's one reader, takes its extent from here
    before it reads a rate.
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
    bad = (rates.index[~((rates >= 0) & (rates <= 1))] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: lapse_rate_ann must be a number from 0 to 1; it is not "
                         f"on line {bad}")
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
    reads a factor.  A blank factor is a missing value to ``VUL_US_S``, whose death
    benefit, the ``max`` of the option's amount and the corridor's, then reads it as no
    corridor at all.
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
    checked being ``mort_rate``, which must also be from 0 to 1, as a probability; the
    shipped table reaches 1.0 at attained age 119.  ``Projection.mort_rate_base_at``, the
    table's one reader, takes both of its extents, this and :func:`mort_age_first`, before
    it reads a rate.  A blank rate is a missing value to ``VUL_US_S``, whose mortality is
    then not a number, and to ``Projection.mort_rate``, whose cap, ``min(q, 1.0)``, keeps it
    missing; a negative one would project negative deaths.
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
    bad = (rates.index[~((rates >= 0) & (rates <= 1))] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: mort_rate must be a number from 0 to 1; it is not on "
                         f"line {bad}")
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
    from 1 to the last.  And so is a ``coi_rate_guar`` that is blank, text, infinite or
    below 0, naming its lines: a charge per $1,000 of net amount at risk, which may pass 1,
    as the current scale does from attained age 72, but is never a credit.
    ``Projection.coi_rate_last_year`` takes a point's extent from here
    before ``Projection.coi_rate_guar_at`` reads its scale.  A blank rate is a missing
    value to ``VUL_US_S``, whose account value is then not a number, and whose cash value
    and net amount at risk, each floored at zero by a ``max``, then read it as nothing.
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
    bad = (rates.index[~((values >= 0) & (values < float("inf")))] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: coi_rate_guar must be a number, zero or more; it is not "
                         f"on line {bad}")
    return last


def class_count():
    """The number of classes *class_factor_table.csv* gives a factor for, the table checked.

    A ``rate_class`` that is blank is refused, naming the file and the lines it is on, and
    so is one on more than one row, naming each such class with its lines; and so is a
    ``factor`` that is blank, text, infinite or below 0, naming its lines: a multiple of the
    base mortality, which below 0 would project negative deaths.
    ``Projection.class_factor``, the table's one reader, asks for the count before it reads
    a factor, so a projection meets the checks first.  A blank factor is a missing value to
    ``VUL_US_S``, whose mortality is then not a number, and to ``Projection.mort_rate``,
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
    bad = (factors.index[~((factors >= 0) & (factors < float("inf")))] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: factor must be a number, zero or more; it is not on "
                         f"line {bad}")
    return len(table)


def surr_charge_count():
    """The number of schedules *surr_charge_table.csv* gives, the table checked.

    A ``surr_charge_id`` that is blank is refused, naming the file and the lines it is on,
    and so is one on more than one row, naming each such schedule with its lines.  So is a
    ``sc_per_1000_init`` that is blank, text, infinite or below 0, naming its lines, and a
    ``runoff_years`` that is not a whole number of years, 1 or more -- blank, text,
    infinite, a fraction or below 1 alike -- naming its lines: the projection divides the
    charge by the run-off and counts policy years on it, where ``VUL_US_S`` truncates a
    fraction with ``int()`` and divides by zero at 0.  ``Projection.surr_charge_rate_max``
    and ``Projection.surr_charge_runoff_years``, the table's two readers, ask for the count
    before they read a value, so a projection meets the checks first.  A blank charge is a
    missing value to ``VUL_US_S``, whose surrender charge rate, the ``max`` of 0 and the
    charge left, is then 0 in every policy year, as though the schedule had run off.  A
    charge below 0 leaves a charge below 0 through the schedule's years, which the ``max``
    reads as none, and after them, where the share of the run-off left turns negative, a
    charge above 0 that rises each policy year, every check passing: the shipped schedule
    written at -18.00 charges $1.29 per $1,000 in policy year 16.
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
    values = pd.to_numeric(pd.Series(table["sc_per_1000_init"].to_numpy()),  # noqa: F821
                           errors="coerce")
    bad = (values.index[~((values >= 0) & (values < float("inf")))] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: sc_per_1000_init must be a number, zero or more; it is "
                         f"not on line {bad}")
    years = pd.to_numeric(pd.Series(table["runoff_years"].to_numpy()),  # noqa: F821
                          errors="coerce")
    bad = (years.index[~((years % 1 == 0) & (years >= 1))] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: runoff_years must be a whole number of years, 1 or "
                         f"more; it is not on line {bad}")
    return len(table)


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table_sec.csv"

subaccount_file = "subaccount_table.csv"

scenario_file = "scenario_table.csv"

coi_rates_file = "coi_rates.csv"

corridor_file = "corridor_factors.csv"

mort_table_file = "mort_table.csv"

class_factor_file = "class_factor_table.csv"

lapse_table_file = "lapse_table.csv"

prem_persistency_file = "prem_persistency.csv"

surr_charge_file = "surr_charge_table.csv"

future_horizon_mth = 120

pd = ("Module", "pandas")
