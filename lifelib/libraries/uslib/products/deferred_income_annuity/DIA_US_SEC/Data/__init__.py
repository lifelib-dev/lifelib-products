# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-contract projection.

The six input CSVs are read here, **once per model**, and referenced from
:mod:`~.DIA_US_SEC.Projection` as ``data``. :mod:`~.DIA_US_SEC.Projection` is
parameterized by ``point_id``, so each ``Projection[N]`` is a separate ItemSpace with its
own cells cache; if the readers lived there, every model point would re-read every file.
Holding them in an unparameterized Space reads each file once no matter how many
contracts are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/deferred_income_annuity/``, rather than data stored inside the model. The
model folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no
embedded values — so a diff of the model shows logic changes only. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``DIA_US_SEC`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

**Four of the tables are DIA_US_S's.** The mortality table, the improvement scale and
the two factor tables are the files :mod:`~.DIA_US_S` reads, read here in place: one copy
of each table serves both models, so an edit to one reaches both. The model point table
and the premium schedule are this model's own, ``model_point_table_sec.csv`` and
``premium_schedule_sec.csv``; they sit beside ``DIA_US_S``'s ``model_point_table.csv``
and ``premium_schedule.csv``, which this model never opens.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so the
model works wherever the repository is checked out. Each table has a filename Reference
and a reader Cells:

========================  ==============================  ==========================
Reference                 Cells                           File
========================  ==============================  ==========================
model_point_file          model_point_table()             model_point_table_sec.csv
premium_schedule_file     premium_schedule_table()        premium_schedule_sec.csv
mort_table_file           mort_table()                    mort_table.csv
improvement_scale_file    improvement_scale()             improvement_scale.csv
payout_factor_file        payout_factor_table()           payout_factor_table.csv
rop_factor_file           rop_factor_table()              rop_factor_table.csv
========================  ==============================  ==========================

**The model point table is checked as it is read.** Ten of its columns are the in-force
interface: ``policy_count`` and ``duration_mth``, as in ``basiclife.BasicTerm_SE``, and
the eight columns of a contract's opening state — each covered life's survival at the
valuation date, the premiums paid and the income bought by then, the guarantee period the
kernel prices with, the two frozen cohort weights and the reference rate's change since
issue. :func:`model_point_table` refuses a table that lacks any of them, repeats a
``point_id``, holds a count, a duration, a month or a contract term no contract can have,
or holds an opening state no contract can be in. The checks run in turn, and the first
that fails raises, naming the missing column or every point that fails it. It also
refuses a policy to be issued more than ``future_horizon_mth`` months after the valuation
date, 120 months as shipped: future new business is written over a stated horizon, so
that no frame runs longer than the stop rule from issue plus that horizon. Set to 0, the
Reference refuses future new business altogether. Whether a contract still owes a payment
at the valuation date is a rule of the product rather than of the table, and
``Projection.proj_len`` checks it.

**So is the premium schedule.** A DIA is a flexible-premium contract: "any number of
premiums during the deferral period" [S2][S3][S4][R13], each buying its own paid-up income
slice at the purchase rate then in force. A fixed set of premium columns on the model
point table would cap that number, so the schedule is a long table keyed by ``point_id``
with one row per slice, and :func:`~.DIA_US_SEC.Projection.premium_by_mth` collapses it
to a month-to-amount mapping once per contract. This model's schedule holds the premiums
**still due** at the valuation date: those paid before it are in the contract's opening
state, as the premiums paid and the income they bought. :func:`premium_schedule_table`
refuses a row that names no point of the table, a month or an amount no premium can have,
a premium before the valuation date or at or after the income start month, and a point
that buys no income at all, which ``DIA_US_S`` would project silently.

**So are the four assumption tables**, each by a count cell beside ``DIA_US_S``'s reader,
which is unchanged: :func:`mort_table_count`, :func:`improvement_scale_count`,
:func:`payout_factor_count` and :func:`rop_factor_count`. Each reads its table's keys by
value, once, as the per-point join in ``Projection`` matches them, so that an age written
``70.0`` is 70, and refuses a key that is blank, text or not a whole number, a sex or a
payout form no join reads, and a key on more than one row; the mortality table and the
improvement scale, read at every age from a life's issue age up, refuse a gap in a sex's
ages too. Each refuses a value that is blank, text, infinite or outside its table's range.
Every message names the file, the column and the lines at fault. A rate, a scale or a
factor reaches the projection through survival and the purchase rates, where the refund
balance's ``max(0, ·)`` and the payment factor's ``max`` would lose a blank,
``max(0.0, nan)`` being 0.0; mortality's cap, written with the rate first, keeps it a NaN
until then. Each join asks its table's count before it reads a value, so a projection
meets the checks first, and reads ``DIA_US_S``'s frame.

**The two factor tables are the pricing kernel's data, and both are [std].** No
purchase-rate table was obtained and none is published — the Compact expressly relieves
the insurer of disclosing the deferral-period mortality and interest basis
[R13 §1.B(1)(a)] — so ``payout_factor_table.csv`` and ``rop_factor_table.csv`` carry the
technical notes' *illustrative* factors, marked as such in their ``provenance`` columns.
A model point can bypass them entirely by setting ``factor_basis = "formula"``, which
computes equation (2) and the equation (3) mid-band approximation from the shipped
mortality table instead.

The mortality table and the improvement scale are keyed by ``(age, sex)``. They are
separate files on purpose: the technical notes prescribe the **2012 IAM Basic** table
projected generationally with **Projection Scale G2** [R9][REG-R59], two distinct
objects with distinct provenance, and neither may be embedded in the model — the shipped
tables are illustrative **[std]** stand-ins, the mortality table being the one that
reproduces the notes' worked-example survival anchors. To swap in a licensed basis,
replace ``mort_table.csv`` with a same-schema file, or point ``mort_table_file`` at a
different name before the model computes anything. No formula changes. Replacing a file
changes :mod:`~.DIA_US_S` too, which reads the same one.
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

    Indexed by ``point_id``. Ten columns are the in-force interface: ``policy_count``, the
    contracts the point stands for, and ``duration_mth``, the months elapsed from issue at
    the valuation date, as in ``basiclife.BasicTerm_SE``; then the opening state, per
    contract, as it stands at the start of month 0, before any month-0 event:

    * ``lives_if_init_1`` and ``lives_if_init_2``: each covered life's probability of
      being alive at the valuation date, 1 or 0 on a real record, where a joint contract
      may carry one life already dead, and 0 for the second life of a single-life
      contract;
    * ``cum_premium_pp_init`` and ``annual_income_init``: the premiums paid and the
      guaranteed annual income they bought, per contract, before the valuation date;
    * ``guarantee_mths_pricing_init``: on a cash or installment refund in force, the
      guarantee period in months with which the pricing kernel prices every slice, a
      fixed point over the whole premium schedule; blank otherwise;
    * ``surv_to_payout_init``: where the income start month precedes the valuation month,
      the cohort that reached the income phase, ``l_last(T)``; blank otherwise;
    * ``commute_weight_init``: where the commutation month precedes the valuation month,
      the cohort that commuted, ``l_last(t_c)``; blank otherwise;
    * ``ref_rate_shift_init``: the reference rate at the valuation date less the reference
      rate at issue, as a decimal.

    The rest are ``DIA_US_S``'s, ``pols_if_init`` renamed ``policy_count``, except
    ``row_kind``, ``source_policy_id`` and ``source_mth``, which record where the
    generator took each shipped row from and which no formula reads.

    The checks run over the whole table at once, and the first that fails raises
    ``ValueError``, naming the missing column or every point it fails on. First the
    table's own shape:

    * the ten in-force columns are present;
    * no ``point_id`` appears twice;
    * ``policy_count`` is a number, zero or more;
    * ``duration_mth`` is a whole number of months, read by value, so that ``12.0`` is
      12: positive for a contract in force, 0 for one issued at the valuation date,
      negative for one issued later;
    * no policy is issued more than ``future_horizon_mth`` months after the valuation
      date, so ``duration_mth`` is ``-future_horizon_mth`` or more. At 0 the model takes
      no future new business, and the message says so; a negative horizon is itself
      refused.

    Then the contract's terms, the income start month in force first, because the later
    checks read it:

    * ``income_start_mth`` is a whole number of months, 0 or more, a policy month;
    * each option month, ``adjust_mth``, ``adjust_start_mth``, ``accel_mth`` and
      ``commute_mth``, is blank or a whole number of months, a policy month; a negative
      month reads as never, as ``DIA_US_S`` reads -1;
    * the start-date adjustment's two months go together, and the new start month
      follows the exercise, so the income start month in force,
      ``adjust_start_mth`` where an adjustment is named and ``income_start_mth``
      otherwise, is a policy month after every premium priced to the old one;
    * a start-date adjustment is a deferral option: ``adjust_mth`` precedes the
      ``income_start_mth`` it moves, where ``DIA_US_S`` would pay nothing from that month
      to the exercise;
    * an acceleration and a commutation, payout-phase options, fall at or after the income
      start month in force;
    * an acceleration and a commutation fall six months apart or more, the product's
      interlock between its two payout options [S4]: inside the acceleration's blackout,
      ``DIA_US_S``'s commuted value counts the instalments the lump sum has paid;
    * ``joint`` is a flag, read by value: ``True`` or ``False``, as pandas reads either, or
      1 or 0, where ``DIA_US_S``'s ``bool()`` reads any text, a blank among them, as
      ``True``; ``sex`` is ``M`` or ``F``, and so is ``joint_sex`` on a joint contract,
      the two values the tables keyed by sex hold;
    * ``issue_age``, ``certain_period`` and, on a joint contract, ``joint_age`` are whole
      numbers of years, 0 or more; ``frequency`` is a whole number of payments a year and
      ``issue_year`` a whole calendar year; ``purchase_rate_dp`` is blank or a whole number
      of decimal places, 0 or more. Each is read by value, so that ``60.0`` is 60;
    * ``survivor_pct`` is a probability, and ``cola_rate`` and ``other_qlac_premium``
      numbers zero or more, each reaching a ``max`` or a comparison that would lose a
      blank; ``commute_frac`` is blank, for none, or a fraction, 0 to 1;
    * the table basis is single-life: a joint contract carries
      ``factor_basis = "formula"``.

    Then the opening state:

    * each covered life is a probability, 0 to 1; the premiums paid and the income
      bought are numbers, zero or more; the guarantee period is blank or a number of
      months, zero or more; each frozen weight is blank or a probability; the reference
      rate's change is a number, of either sign, the floor applying to the whole change
      since issue in ``Projection.commute_disc_rate``;
    * a single-life contract has no second life: ``lives_if_init_2`` is 0;
    * a contract not yet in force, ``duration_mth`` 0 or less, holds its values at issue:
      each covered life 1, no premium paid, no income bought and no change in the
      reference rate;
    * ``guarantee_mths_pricing_init`` is given exactly on a contract in force on a refund
      form, ``income_form`` CR or IR, and blank on every other: on new business the kernel
      derives it from the premium schedule, and the other forms fix it;
    * ``surv_to_payout_init`` is given exactly where ``duration_mth`` is after the income
      start month in force, and ``commute_weight_init`` exactly where the commutation month
      precedes ``duration_mth``: at or after the valuation month the projection derives
      each from the lives;
    * a commutation is taken in the income phase by part of the cohort that reached it, so
      ``commute_weight_init`` is at most ``surv_to_payout_init``, and each frozen weight is
      at least the probability that a covered life is alive at the valuation date, the
      cohort it weighs including every life still alive;
    * each frozen weight, where given, is above 0: a contract in force past its income start
      month reached it, and a commutation is exercised by an owner alive to exercise it, so
      neither cohort is empty. At 0 the guarantee of a contract whose lives have all died
      would pay nothing, a contract owing nothing that would project.

    The table is returned with the columns those checks read by value, the policy months
    and the contract's whole numbers and rates, as the numbers they were checked as (int64
    where a whole-number column has no blank, float64 otherwise, blank as NaN), which the
    ``Projection`` accessors read with ``int()`` and ``float()``, and ``joint`` as the flags
    it was checked as. Whether the contract still owes a payment at the valuation date needs
    the certain period, which an installment refund derives in ``Projection``, so
    ``Projection.proj_len`` checks it.
    """
    name = model_point_file                                          # noqa: F821
    table = pd.read_csv(input_dir() / name, index_col="point_id")    # noqa: F821
    state = ("lives_if_init_1", "lives_if_init_2", "cum_premium_pp_init",
             "annual_income_init", "guarantee_mths_pricing_init", "surv_to_payout_init",
             "commute_weight_init", "ref_rate_shift_init")
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
    checked = {}
    start = pd.to_numeric(table["income_start_mth"], errors="coerce")  # noqa: F821
    bad = table.index[~((start % 1 == 0) & (start >= 0))].tolist()
    if bad:
        raise ValueError(f"{name}: income_start_mth must be a whole number of months, 0 "
                         f"or more, a policy month; it is not at point_id {bad}")
    checked["income_start_mth"] = start
    options = {}
    for column in ("adjust_mth", "adjust_start_mth", "accel_mth", "commute_mth"):
        month = pd.to_numeric(table[column], errors="coerce")        # noqa: F821
        bad = table.index[~(table[column].isna() | (month % 1 == 0))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be blank or a whole number of "
                             f"months, a policy month; it is not at point_id {bad}")
        checked[column] = month
        options[column] = month.where(month >= 0)
    adjust, moved = options["adjust_mth"], options["adjust_start_mth"]
    bad = table.index[adjust.notna() != moved.notna()].tolist()
    if bad:
        raise ValueError(f"{name}: adjust_mth and adjust_start_mth go together, both "
                         f"blank or both a policy month; they do not at point_id {bad}")
    bad = table.index[adjust.notna() & ~(moved > adjust)].tolist()
    if bad:
        raise ValueError(f"{name}: adjust_start_mth must follow adjust_mth: an income "
                         f"start date moves to a month after the exercise; it does not "
                         f"at point_id {bad}")
    bad = table.index[adjust.notna() & ~(adjust < start)].tolist()
    if bad:
        raise ValueError(f"{name}: adjust_mth must precede income_start_mth: a start-date "
                         f"adjustment is a deferral option; it does not at point_id {bad}")
    start = moved.where(adjust.notna(), start)
    for column, option in (("accel_mth", "payment acceleration"),
                           ("commute_mth", "commutation")):
        bad = table.index[options[column] < start].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be blank or the income start month "
                             f"in force or later: {option} is a payout-phase option; it "
                             f"is not at point_id {bad}")
    apart = (options["accel_mth"] - options["commute_mth"]).abs()
    bad = table.index[apart < 6].tolist()
    if bad:
        raise ValueError(f"{name}: accel_mth and commute_mth must fall six months apart or "
                         f"more, the product's interlock between its two payout options; "
                         f"they do not at point_id {bad}")
    flag = table["joint"].astype(str).str.strip().str.lower()
    joint = flag.isin(["true", "1", "1.0"])
    bad = table.index[~(joint | flag.isin(["false", "0", "0.0"]))].tolist()
    if bad:
        raise ValueError(f"{name}: joint must be True or False, a flag; it is not at "
                         f"point_id {bad}")
    checked["joint"] = joint
    bad = table.index[~(table["sex"].isin(["M", "F"])
                        & (table["joint_sex"].isin(["M", "F"]) | ~joint))].tolist()
    if bad:
        raise ValueError(f"{name}: sex must be M or F, and so must joint_sex on a joint "
                         f"contract; it is not at point_id {bad}")
    every = pd.Series(True, index=table.index)                       # noqa: F821
    for column, what, read, least in (
            ("issue_age", "a whole number of years, 0 or more", every, 0),
            ("joint_age", "a whole number of years, 0 or more, on a joint contract",
             joint, 0),
            ("certain_period", "a whole number of years, 0 or more", every, 0),
            ("frequency", "a whole number of payments a year", every, None),
            ("issue_year", "a whole number, a calendar year", every, None)):
        value = pd.to_numeric(table[column], errors="coerce")        # noqa: F821
        whole = value % 1 == 0
        if least is not None:
            whole = whole & (value >= least)
        bad = table.index[read & ~whole].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be {what}; it is not at point_id "
                             f"{bad}")
        checked[column] = value
    digits = pd.to_numeric(table["purchase_rate_dp"], errors="coerce")  # noqa: F821
    bad = table.index[~(table["purchase_rate_dp"].isna()
                        | ((digits % 1 == 0) & (digits >= 0)))].tolist()
    if bad:
        raise ValueError(f"{name}: purchase_rate_dp must be blank, for full precision, "
                         f"or a whole number of decimal places, 0 or more; it is not at "
                         f"point_id {bad}")
    checked["purchase_rate_dp"] = digits
    for column, what, most in (("survivor_pct", "a probability, 0 to 1", 1.0),
                               ("cola_rate", "a number, zero or more", None),
                               ("other_qlac_premium", "a number, zero or more", None)):
        value = pd.to_numeric(table[column], errors="coerce")        # noqa: F821
        if most is None:
            ok = (value >= 0) & (value < float("inf"))
        else:
            ok = (value >= 0) & (value <= most)
        bad = table.index[~ok].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be {what}; it is not at point_id "
                             f"{bad}")
        checked[column] = value
    frac = pd.to_numeric(table["commute_frac"], errors="coerce")     # noqa: F821
    bad = table.index[~(table["commute_frac"].isna()
                        | ((frac >= 0) & (frac <= 1)))].tolist()
    if bad:
        raise ValueError(f"{name}: commute_frac must be blank or a fraction, 0 to 1; it "
                         f"is not at point_id {bad}")
    checked["commute_frac"] = frac
    bad = table.index[joint & (table["factor_basis"] == "table")].tolist()
    if bad:
        raise ValueError(f"{name}: factor_basis must be formula on a joint contract: the "
                         f"table basis, equation (1), factors a single life's survival "
                         f"out of the payout factor; it is not at point_id {bad}")
    values = {c: pd.to_numeric(table[c], errors="coerce") for c in state}  # noqa: F821
    for column in ("lives_if_init_1", "lives_if_init_2"):
        v = values[column]
        bad = table.index[~((v >= 0) & (v <= 1))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a probability, 0 to 1; it is "
                             f"not at point_id {bad}")
    for column in ("cum_premium_pp_init", "annual_income_init"):
        v = values[column]
        bad = table.index[~((v >= 0) & (v < float("inf")))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a number, zero or more; it is "
                             f"not at point_id {bad}")
    column = "guarantee_mths_pricing_init"
    v = values[column]
    bad = table.index[~(table[column].isna()
                        | ((v >= 0) & (v < float("inf"))))].tolist()
    if bad:
        raise ValueError(f"{name}: {column} must be blank or a number of months, zero or "
                         f"more; it is not at point_id {bad}")
    for column in ("surv_to_payout_init", "commute_weight_init"):
        v = values[column]
        bad = table.index[~(table[column].isna() | ((v >= 0) & (v <= 1)))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be blank or a probability, 0 to 1; "
                             f"it is not at point_id {bad}")
    shift = values["ref_rate_shift_init"]
    bad = table.index[~((shift > -float("inf")) & (shift < float("inf")))].tolist()
    if bad:
        raise ValueError(f"{name}: ref_rate_shift_init must be a number, the change in "
                         f"the reference rate since issue; it is not at point_id {bad}")
    bad = table.index[~joint & (values["lives_if_init_2"] != 0)].tolist()
    if bad:
        raise ValueError(f"{name}: lives_if_init_2 must be 0 on a single-life "
                         f"contract, which covers no second life; it is not at "
                         f"point_id {bad}")
    issued = months <= 0
    for column, at_issue in (("lives_if_init_1", 1.0),
                             ("lives_if_init_2", joint.astype(float)),
                             ("cum_premium_pp_init", 0.0),
                             ("annual_income_init", 0.0),
                             ("ref_rate_shift_init", 0.0)):
        bad = table.index[issued & (values[column] != at_issue)].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must hold its value at issue on a "
                             f"contract not yet in force, duration_mth 0 or less: each "
                             f"covered life alive, no premium paid, no income bought and "
                             f"no change in the reference rate; it does not at point_id "
                             f"{bad}")
    in_force = months > 0
    refund = in_force & table["income_form"].isin(["CR", "IR"])
    given = table["guarantee_mths_pricing_init"].notna()
    bad = table.index[refund & ~given].tolist()
    if bad:
        raise ValueError(f"{name}: guarantee_mths_pricing_init must be given on a "
                         f"contract in force on a refund form, income_form CR or IR, "
                         f"whose premiums still due the kernel prices with it; it is "
                         f"blank at point_id {bad}")
    bad = table.index[~refund & given].tolist()
    if bad:
        raise ValueError(f"{name}: guarantee_mths_pricing_init must be blank unless the "
                         f"contract is in force on a refund form: on new business the "
                         f"kernel derives it from the premium schedule, and the other "
                         f"forms fix it; it is not at point_id {bad}")
    paying = months > start
    given = table["surv_to_payout_init"].notna()
    bad = table.index[paying & ~given].tolist()
    if bad:
        raise ValueError(f"{name}: surv_to_payout_init must be given on a contract past "
                         f"its income start month in force; it is blank at point_id "
                         f"{bad}")
    bad = table.index[~paying & given].tolist()
    if bad:
        raise ValueError(f"{name}: surv_to_payout_init must be blank unless duration_mth "
                         f"is after the income start month in force, where the "
                         f"projection derives it; it is not at point_id {bad}")
    commuted = options["commute_mth"] < months
    given = table["commute_weight_init"].notna()
    bad = table.index[commuted & ~given].tolist()
    if bad:
        raise ValueError(f"{name}: commute_weight_init must be given on a contract whose "
                         f"commutation month precedes the valuation date; it is blank "
                         f"at point_id {bad}")
    bad = table.index[~commuted & given].tolist()
    if bad:
        raise ValueError(f"{name}: commute_weight_init must be blank unless the "
                         f"commutation month precedes the valuation date, where the "
                         f"projection derives it; it is not at point_id {bad}")
    weight, reached = values["commute_weight_init"], values["surv_to_payout_init"]
    bad = table.index[weight > reached].tolist()
    if bad:
        raise ValueError(f"{name}: commute_weight_init must be at most "
                         f"surv_to_payout_init: a commutation is taken in the income "
                         f"phase, by part of the cohort that reached it; it is not at "
                         f"point_id {bad}")
    l1, l2 = values["lives_if_init_1"], values["lives_if_init_2"]
    alive = (l1 + l2 - l1 * l2).where(joint, l1)
    for column in ("surv_to_payout_init", "commute_weight_init"):
        bad = table.index[values[column] < alive].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be at least the probability that a "
                             f"covered life is alive at the valuation date: the cohort "
                             f"it weighs includes every life still alive; it is not at "
                             f"point_id {bad}")
    for column, why in (("surv_to_payout_init", "a contract in force past its income "
                         "start month reached it"),
                        ("commute_weight_init", "a commutation is exercised by an owner "
                         "alive to exercise it")):
        bad = table.index[values[column] <= 0].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be above 0 where it is given: {why}, "
                             f"so the cohort it weighs is not empty; it is not at point_id "
                             f"{bad}")
    return table.assign(**checked)


def premium_schedule_table():
    """The premiums still due, from *premium_schedule_sec.csv*, checked as they are read.

    Long format, one row per premium slice, keyed by ``point_id`` - deliberately not
    indexed, so that selecting a contract's rows returns a DataFrame whether it has one
    slice or many - with ``DIA_US_S``'s columns: ``point_id``, ``slice``, ``premium_mth``,
    the policy month whose start the premium is paid at, ``premium_amt``, the amount per
    contract, and ``provenance``. The point key is the ``point_id`` column, and nothing else
    in the file names a point.

    It holds each contract's premiums **still due** at the valuation date, the premiums of
    policy months ``duration_mth`` and later, on a point in force, and its whole schedule on
    a point issued at or after the valuation date. A premium paid before the valuation date
    is in the contract's opening state, in ``cum_premium_pp_init`` and, through the slice it
    bought, ``annual_income_init``, so the schedule holds none.

    It is checked against :func:`model_point_table`, as checked, and the first check that
    fails raises ``ValueError``, naming the column, the label or every point at fault:

    * the ``point_id``, ``premium_mth`` and ``premium_amt`` columns are present;
    * each ``point_id`` is a whole number, a model point's label, and labels a point of
      the model point table;
    * each ``premium_mth`` is a whole number of months, 0 or more, a policy month, read by
      value, so that ``60.0`` is 60; ``DIA_US_S`` takes ``int()`` of the raw month, so
      ``60.5`` is 60 there and text raises Python's own message;
    * each ``premium_amt`` is a number, zero or more;
    * no premium falls before the valuation date on a point in force, ``premium_mth``
      below ``duration_mth``: those paid are in the opening state;
    * no premium falls at or after the income start month in force. The product takes no
      premium within 13 months of it, and the projection's payout schedule rests on a
      level income from the income start month on, as ``DIA_US_S``'s refund base
      ``CP(T)`` does, which a premium after it would leave out;
    * every point buys an income: a point with no income bought by the valuation date,
      ``annual_income_init`` 0, has a positive premium due. ``DIA_US_S`` projects a point
      with no premium row silently, with no premium and no income.

    Returns the table with ``point_id`` and ``premium_mth`` as int64 and ``premium_amt``
    as float64, the numbers checked, every other column as read.
    """
    name = premium_schedule_file                                     # noqa: F821
    points = model_point_table()
    tbl = pd.read_csv(input_dir() / name)                            # noqa: F821
    for column in ("point_id", "premium_mth", "premium_amt"):
        if column not in tbl.columns:
            raise ValueError(f"{name} has no {column} column")
    pid = pd.to_numeric(tbl["point_id"], errors="coerce")            # noqa: F821
    bad = tbl["point_id"][~(pid % 1 == 0)].tolist()
    if bad:
        raise ValueError(f"{name}: point_id must be a whole number, a model point's "
                         f"label; {bad} is not")
    pid = pid.astype("int64")
    known = pid.isin(points.index)
    bad = sorted(set(pid[~known].tolist()))
    if bad:
        raise ValueError(f"{name}: point_id {bad} is no model point of "
                         f"{model_point_file}")                       # noqa: F821
    month = pd.to_numeric(tbl["premium_mth"], errors="coerce")       # noqa: F821
    bad = sorted(set(pid[~((month % 1 == 0) & (month >= 0))].tolist()))
    if bad:
        raise ValueError(f"{name}: premium_mth must be a whole number of months, 0 or "
                         f"more, a policy month; it is not at point_id {bad}")
    amount = pd.to_numeric(tbl["premium_amt"], errors="coerce")      # noqa: F821
    bad = sorted(set(pid[~((amount >= 0) & (amount < float("inf")))].tolist()))
    if bad:
        raise ValueError(f"{name}: premium_amt must be a number, zero or more; it is "
                         f"not at point_id {bad}")
    duration = pid.map(points["duration_mth"])
    bad = sorted(set(pid[(duration > 0) & (month < duration)].tolist()))
    if bad:
        raise ValueError(f"{name}: a premium falls before the valuation date at point_id "
                         f"{bad}: those paid before it are in cum_premium_pp_init and "
                         f"annual_income_init, and the schedule holds the premiums still "
                         f"due")
    moved = points["adjust_mth"] >= 0
    start = points["adjust_start_mth"].where(moved, points["income_start_mth"])
    bad = sorted(set(pid[month >= pid.map(start)].tolist()))
    if bad:
        raise ValueError(f"{name}: a premium falls at or after the income start month in "
                         f"force at point_id {bad}: the income is level in payout")
    due = amount.groupby(pid).sum()
    bought = pd.to_numeric(points["annual_income_init"], errors="coerce")  # noqa: F821
    paying = due.reindex(points.index, fill_value=0.0) > 0
    bad = points.index[(bought == 0) & ~paying].tolist()
    if bad:
        raise ValueError(f"{name}: point_id {bad} buys no income: annual_income_init is 0 "
                         f"and no premium is due")
    return tbl.assign(point_id=pid, premium_mth=month.astype("int64"),
                      premium_amt=amount.astype("float64"))


def mort_table():
    """The base annuitant mortality table by age and sex, read from *mort_table.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file, index_col=["age", "sex"])     # noqa: F821


def improvement_scale():
    """The generational improvement scale by age and sex, from *improvement_scale.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / improvement_scale_file, index_col=["age", "sex"])  # noqa: F821


def payout_factor_table():
    """The illustrative payout annuity factors, from *payout_factor_table.csv*.

    Keyed by ``(income_start_age, sex, payout_form)``; the value is
    ``a^(m)_y(f; i_p)``, the APV at the income start age of $1 per annum of income.
    **[std]** - no insurer publishes payout factors for this product.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / payout_factor_file,                            # noqa: F821
        index_col=["income_start_age", "sex", "payout_form"])


def rop_factor_table():
    """The illustrative return-of-premium factors, from *rop_factor_table.csv*.

    Keyed by ``(issue_age, sex, deferral_years)``; the value is ``A_rop(x, d; i_p)``,
    the APV at the premium date of $1 payable at the end of the month of death within a
    ``d``-year deferral.  **[std]**.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / rop_factor_file,                               # noqa: F821
        index_col=["issue_age", "sex", "deferral_years"])


def mort_table_count():
    """The number of rows *mort_table.csv* gives a rate for, the table checked: an int.

    :func:`mort_table` reads the table as ``DIA_US_S`` reads it, and this cell checks it.
    The ``age`` key is read by value, once, as ``Projection.mort_rate_base_at``'s join
    matches it, so an age written ``70.0`` is 70. An age that is blank, text or not a whole
    number is refused, naming the file, the column and the lines it is on; so is a ``sex``
    that is not ``M`` or ``F``, the two values a model point's sex can take, a blank among
    them; so is an age and sex on more than one row, naming each with its lines; and so is
    a sex whose ages do not run one row an age, from its first to its last, the message
    naming each age missing. And so is a ``mort_rate`` that is blank, text, infinite or
    below 0, naming its lines: through the cap on mortality the rate reaches every
    survival probability, and a blank would survive the cap as a NaN, text fail far from
    here. A rate above 1 is accepted, and capped. ``Projection.mort_rate_base_at``, the
    table's one reader, asks for the count before it reads a rate, so a projection meets
    the checks first.
    """
    name = mort_table_file                                           # noqa: F821
    rows = mort_table().reset_index()
    lines = rows.index + 2                  # the header is line 1 of the file
    ages = pd.to_numeric(rows["age"], errors="coerce")               # noqa: F821
    bad = lines[(~(ages % 1 == 0)).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: age must be a whole number; it is not on line {bad}")
    bad = lines[(~rows["sex"].isin(["M", "F"])).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: sex must be M or F; it is not on line {bad}")
    ages = ages.astype("int64")
    where = {}
    for line, key in zip(lines.tolist(), zip(ages.tolist(), rows["sex"].tolist())):
        where.setdefault(key, []).append(line)
    repeated = []
    for key in sorted(where):
        if len(where[key]) > 1:
            repeated.append(f"age {key[0]}, sex {key[1]} is on line {where[key]}")
    if repeated:
        raise ValueError(f"{name}: each age and sex must have one row; "
                         + "; ".join(repeated))
    missing = []
    for sex in sorted(set(rows["sex"])):
        run = sorted(set(ages[rows["sex"] == sex].tolist()))
        for a, b in zip(run, run[1:]):
            if b - a > 1:
                missing.append(f"no line holds age {a + 1}"
                               + (f" to {b - 1}" if b - a > 2 else "") + f" of sex {sex}")
    if missing:
        raise ValueError(f"{name}: the ages of each sex must run one row an age, without a "
                         f"gap; " + "; ".join(missing))
    rates = pd.to_numeric(rows["mort_rate"], errors="coerce")        # noqa: F821
    bad = lines[(~((rates >= 0) & (rates < float("inf")))).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: mort_rate must be a finite number, zero or more; it is "
                         f"not on line {bad}")
    return int(len(rows))


def improvement_scale_count():
    """The number of rows *improvement_scale.csv* gives a rate for, the table checked.

    An int. :func:`improvement_scale` reads the scale as ``DIA_US_S`` reads it, and this
    cell checks its keys as :func:`mort_table_count` checks the mortality table's, for
    ``Projection.improvement_rate_at``'s join. And it refuses an ``improvement_rate`` that
    is blank, text, infinite, or 1 or more, naming its lines: at 1 or more ``1 - G2`` is
    zero or negative, and the improved rate is 0 or changes sign with the calendar year. A
    negative rate is a deterioration, which the generational basis projects as
    ``DIA_US_S`` does, the improved rate rising year on year, and it is accepted.
    ``Projection.improvement_rate_at``, the scale's one reader, asks for the count before
    it reads a rate, so a projection meets the checks first.
    """
    name = improvement_scale_file                                    # noqa: F821
    rows = improvement_scale().reset_index()
    lines = rows.index + 2                  # the header is line 1 of the file
    ages = pd.to_numeric(rows["age"], errors="coerce")               # noqa: F821
    bad = lines[(~(ages % 1 == 0)).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: age must be a whole number; it is not on line {bad}")
    bad = lines[(~rows["sex"].isin(["M", "F"])).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: sex must be M or F; it is not on line {bad}")
    ages = ages.astype("int64")
    where = {}
    for line, key in zip(lines.tolist(), zip(ages.tolist(), rows["sex"].tolist())):
        where.setdefault(key, []).append(line)
    repeated = []
    for key in sorted(where):
        if len(where[key]) > 1:
            repeated.append(f"age {key[0]}, sex {key[1]} is on line {where[key]}")
    if repeated:
        raise ValueError(f"{name}: each age and sex must have one row; "
                         + "; ".join(repeated))
    missing = []
    for sex in sorted(set(rows["sex"])):
        run = sorted(set(ages[rows["sex"] == sex].tolist()))
        for a, b in zip(run, run[1:]):
            if b - a > 1:
                missing.append(f"no line holds age {a + 1}"
                               + (f" to {b - 1}" if b - a > 2 else "") + f" of sex {sex}")
    if missing:
        raise ValueError(f"{name}: the ages of each sex must run one row an age, without a "
                         f"gap; " + "; ".join(missing))
    rates = pd.to_numeric(rows["improvement_rate"], errors="coerce")  # noqa: F821
    bad = lines[(~((rates > -float("inf")) & (rates < 1))).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: improvement_rate must be a finite number below 1; it is "
                         f"not on line {bad}")
    return int(len(rows))


def payout_factor_count():
    """The number of rows *payout_factor_table.csv* gives a factor for, the table checked.

    An int. :func:`payout_factor_table` reads the table as ``DIA_US_S`` reads it, and this
    cell checks it for ``Projection.payout_factor``'s join, which reads one key a point. An
    ``income_start_age`` that is blank, text or not a whole number is refused, naming the
    file, the column and the lines it is on; so is a ``sex`` that is not ``M`` or ``F`` and
    a ``payout_form`` that is not ``LO``, ``CR``, ``IR`` or ``PC``, the forms the join
    reads, a blank among them; and so is a key on more than one row, naming each with its
    lines. And so is a ``payout_factor`` that is blank, text, infinite or not above zero,
    naming its lines: the factor divides the purchase rate, through
    ``Projection.annuity_factor_def``, where ``DIA_US_S``'s guard turns a factor of zero
    into a purchase rate of 0, a premium that buys nothing. ``Projection.payout_factor``
    asks for the count before it reads a factor, so a projection meets the checks first.
    """
    name = payout_factor_file                                        # noqa: F821
    rows = payout_factor_table().reset_index()
    lines = rows.index + 2                  # the header is line 1 of the file
    ages = pd.to_numeric(rows["income_start_age"], errors="coerce")  # noqa: F821
    bad = lines[(~(ages % 1 == 0)).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: income_start_age must be a whole number; it is not on "
                         f"line {bad}")
    for column, held, what in (("sex", ["M", "F"], "M or F"),
                               ("payout_form", ["LO", "CR", "IR", "PC"],
                                "LO, CR, IR or PC")):
        bad = lines[(~rows[column].isin(held)).to_numpy()].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be {what}; it is not on line {bad}")
    where = {}
    for line, key in zip(lines.tolist(), zip(ages.astype("int64").tolist(),
                                             rows["sex"].tolist(),
                                             rows["payout_form"].tolist())):
        where.setdefault(key, []).append(line)
    repeated = []
    for key in sorted(where):
        if len(where[key]) > 1:
            repeated.append(f"income_start_age {key[0]}, sex {key[1]}, payout_form "
                            f"{key[2]} is on line {where[key]}")
    if repeated:
        raise ValueError(f"{name}: each income_start_age, sex and payout_form must have "
                         f"one row; " + "; ".join(repeated))
    factors = pd.to_numeric(rows["payout_factor"], errors="coerce")  # noqa: F821
    bad = lines[(~((factors > 0) & (factors < float("inf")))).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: payout_factor must be a finite number above zero; it is "
                         f"not on line {bad}")
    return int(len(rows))


def rop_factor_count():
    """The number of rows *rop_factor_table.csv* gives a factor for, the table checked.

    An int. :func:`rop_factor_table` reads the table as ``DIA_US_S`` reads it, and this cell
    checks it for ``Projection.rop_factor``'s join, which reads one key a premium. An
    ``issue_age`` or a ``deferral_years`` that is blank, text or not a whole number is
    refused, naming the file, the column and the lines it is on; so is a ``sex`` that is
    not ``M`` or ``F``, a blank among them; and so is a key on more than one row, naming
    each with its lines. And so is a ``rop_factor`` that is blank, text, infinite or below
    zero, naming its lines; zero is a return of premium that costs nothing.
    ``Projection.rop_factor`` asks for the count before it reads a factor, so a projection
    meets the checks first.
    """
    name = rop_factor_file                                           # noqa: F821
    rows = rop_factor_table().reset_index()
    lines = rows.index + 2                  # the header is line 1 of the file
    whole = {}
    for column in ("issue_age", "deferral_years"):
        whole[column] = pd.to_numeric(rows[column], errors="coerce")  # noqa: F821
        bad = lines[(~(whole[column] % 1 == 0)).to_numpy()].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a whole number; it is not on line "
                             f"{bad}")
    bad = lines[(~rows["sex"].isin(["M", "F"])).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: sex must be M or F; it is not on line {bad}")
    where = {}
    for line, key in zip(lines.tolist(), zip(whole["issue_age"].astype("int64").tolist(),
                                             rows["sex"].tolist(),
                                             whole["deferral_years"].astype("int64")
                                             .tolist())):
        where.setdefault(key, []).append(line)
    repeated = []
    for key in sorted(where):
        if len(where[key]) > 1:
            repeated.append(f"issue_age {key[0]}, sex {key[1]}, deferral_years {key[2]} is "
                            f"on line {where[key]}")
    if repeated:
        raise ValueError(f"{name}: each issue_age, sex and deferral_years must have one "
                         f"row; " + "; ".join(repeated))
    factors = pd.to_numeric(rows["rop_factor"], errors="coerce")     # noqa: F821
    bad = lines[(~((factors >= 0) & (factors < float("inf")))).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: rop_factor must be a finite number, zero or more; it is "
                         f"not on line {bad}")
    return int(len(rows))


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table_sec.csv"

premium_schedule_file = "premium_schedule_sec.csv"

mort_table_file = "mort_table.csv"

improvement_scale_file = "improvement_scale.csv"

payout_factor_file = "payout_factor_table.csv"

rop_factor_file = "rop_factor_table.csv"

future_horizon_mth = 120

pd = ("Module", "pandas")