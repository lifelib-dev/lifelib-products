# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-contract projection.

The seven input CSVs are read here, **once per model**, and referenced from
:mod:`~.RILA_US_SEC.Projection` as ``data``. :mod:`~.RILA_US_SEC.Projection` is
parameterized by ``point_id``, so each ``Projection[N]`` is a separate ItemSpace with its
own cells cache; if the readers lived there, every model point would re-read every file.
Holding them in an unparameterized Space reads each file once no matter how many
contracts are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/registered_index_linked_annuity/``, rather than data stored inside the model.
The model folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no
embedded values — so a diff of the model shows logic changes only. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``RILA_US_SEC`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

**Five of the tables are RILA_US_S's.** The mortality table, the withdrawal charge
schedule, the guaranteed minimum rates, the base surrender rates and the withdrawal
programmes are the files :mod:`~.RILA_US_S` reads, read here in place by ``RILA_US_S``'s
own readers: one copy of each table serves both models, so an edit to one reaches both.
The model point table and the market scenarios are this model's own,
``model_point_table_sec.csv`` and ``market_scenario_sec.csv``; they sit beside
``RILA_US_S``'s ``model_point_table.csv`` and ``market_scenario.csv``, which this model
never opens.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so the
model works wherever the repository is checked out. Each table has a filename Reference
and a reader Cells:

=========================  ==============================  ==========================
Reference                  Cells                           File
=========================  ==============================  ==========================
model_point_file           model_point_table()             model_point_table_sec.csv
mort_table_file            mort_table()                    mort_table.csv
market_scenario_file       market_scenario()               market_scenario_sec.csv
surr_charge_file           surr_charge_table()             surr_charge_table.csv
guar_min_rate_file         guar_min_rate_table()           guar_min_rate_table.csv
lapse_file                 lapse_table()                   lapse_table.csv
withdrawal_file            withdrawal_table()              withdrawal_table.csv
=========================  ==============================  ==========================

**The model point table is checked as it is read.** Fifteen of its columns are the
in-force interface: ``policy_count`` and ``duration_mth``, as in ``basiclife.BasicTerm_SE``,
and the thirteen columns of a contract's opening state — the investment amount, the Fixed
and Holding Accounts, the account value, the account value at the anniversary on or before
the valuation date, the free withdrawal amount still unused, the return-of-premium base,
and, where the term under way began before the valuation month, the five market values of
its Term Start Date and the cap re-solved there. :func:`model_point_table` refuses a table
that lacks any of them, repeats a ``point_id``, holds a count, a duration, a contract term
or an opening state no contract can have, or a key its tables do not hold. The checks run
in turn, and the first that fails raises, naming the missing column or every point that
fails it. It also refuses a policy to be issued more than ``future_horizon_mth`` months
after the valuation date, 120 months as shipped: future new business is written over a
stated horizon, so that no frame runs longer than cover from issue plus that horizon. Set
to 0, the Reference refuses future new business altogether. Two rules of the product
rather than of the table need ``Projection`` References, and ``Projection.proj_len``
checks them: whether a point is still in cover at the valuation date, and whether the free
withdrawal amount it carries is within the contract year's, where that year's base is 0 or
more.

**So are the five assumption tables and the scenarios**, each by a count cell beside its
reader, which is ``RILA_US_S``'s, unchanged: :func:`market_scenario_count`,
:func:`mort_table_count`, :func:`surr_charge_count`, :func:`guar_min_rate_count`,
:func:`lapse_table_count` and :func:`withdrawal_count`. Each reads its table's keys by
value, once, as the join in ``Projection`` matches them, so that a month written ``36.0``
is 36, and refuses a key that is blank, text or not a whole number, and a key on more than
one row; where a reader reads every key from the first to the last, a gap too. Each
refuses a value that is blank, text, infinite or outside its range, every value a cap, a
``min`` or a ``max`` reads among them, which would lose a blank without a word. Every
message names the file, the column and the lines at fault. Each table's one reader in
``Projection`` asks its count before it reads a value, so a projection meets the checks
first.

``market_scenario`` is the file peculiar to this product. A RILA's *contractual* formula
consumes market data — an index level, a Constant Maturity Treasury yield at the term's
maturity, an implied volatility and a dividend yield — so the market state is an input
class of its own alongside the contractual, declared and behavioural classes, not a
valuation overlay. It is indexed by ``(scenario_id, month_end)`` and read as a step
function of the month end: each row states the market state that holds from that month
end until the next row of the same scenario, so the notes' Scenario A is three rows.

``month_end`` is a **time** in months from the **valuation date**, ``0`` at the valuation
date: the market runs on the valuation clock, which every model point of a block shares.
``market_scenario_sec.csv`` holds ``RILA_US_S``'s scenarios as they stand, under their own
ids, which on a contract issued at the valuation date is ``RILA_US_S``'s own clock, and
for each model point restated in force or issued later a copy of its scenario re-based to
that point's month, under an id of its own. ``Projection.market_state`` reads the file at
the month end ``t + 1`` for the state month ``t`` is valued at, and, for a term that
starts at or after the valuation date, at the time its Term Start Date falls at — a month
*start*; a term that began before the valuation date reads its start from the model point
instead. The name records the commoner of those two uses and not the key's meaning: the
key is a general time, and the row every scenario opens with, ``month_end = 0``, is the
valuation date, an instant no month ends at.

``withdrawal_table`` is indexed by ``(wd_schedule_id, month_end)``, the **policy** month
end the withdrawal is taken at, counted from the Issue Date: the withdrawal programme is a
contractual schedule and stays on the policy clock, and a month end with no row takes no
scheduled withdrawal. ``surr_charge_table`` is indexed by complete contract years
``cy = 0 .. 6``, an elapsed count that is 0-based already; ``guar_min_rate_table`` by
``term_years``, the contractual floors on the declared Cap, Step and Edge rates at 1, 3 and
6 years [S1][S2]; and ``lapse_table`` by ``contract_year`` - the 1-based contractual label,
read through ``Projection.policy_year`` - as a step function, so the notes' three-row
reference shape stays three rows.

To swap in the prescribed mortality basis — the 2012 IAM **Basic** table (VM-M §2.C) with
generational Projection Scale G2 [REG-R59], which may not be redistributed here — replace
``mort_table.csv`` with a same-schema file, or point ``mort_table_file`` at a different
name, before the model computes anything. No formula changes. Replacing a file changes
:mod:`~.RILA_US_S` too, which reads the same one. The same is true of the market data: a
production implementation supplies a volatility *surface* rather than the flat scalar
shipped here, and that is a change to the scenario file plus a strike-and-maturity
lookup, not to the crediting or interim-value formulas.
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

    Indexed by ``point_id``. Fifteen columns are the in-force interface: ``policy_count``,
    the contracts the point stands for, and ``duration_mth``, the months elapsed from issue
    at the valuation date, as in ``basiclife.BasicTerm_SE``; then the opening state, per
    contract, as it stands at the start of month 0, before any month-0 event:

    * ``inv_amt_pp_init``: the Investment Amount entering month 0, the notional the
      month's crediting and interim value apply to;
    * ``fixed_acct_pp_init`` and ``holding_acct_pp_init``: the Fixed and Holding Accounts;
    * ``av_pp_init``: the Account Value, after the previous month's withdrawal;
    * ``av_pp_prev_anniv_init``: the Account Value before withdrawals at the Contract
      Anniversary on or before the valuation date, the base of the contract year's Free
      Withdrawal Amount; the purchase payment in the first contract year;
    * ``free_wd_remain_init``: the Free Withdrawal Amount still unused in the contract year;
    * ``rop_pp_init``: the return-of-premium death benefit base;
    * ``index_at_term_start_init``, ``mvr_at_term_start_init``,
      ``risk_free_at_term_start_init``, ``div_yield_at_term_start_init`` and
      ``impl_vol_at_term_start_init``: where the term under way began before the valuation
      month, the index level, the Market Value Rate and the option-pricing market on its
      Term Start Date; blank otherwise;
    * ``cap_rate_init``: where that term began at a renewal under ``nge_reset``, the cap
      re-solved there; blank otherwise.

    The rest are ``RILA_US_S``'s, ``pols_if_init`` renamed ``policy_count``, except
    ``row_kind``, ``source_policy_id`` and ``source_mth``, which record where the
    generator took each shipped row from and which no formula reads.

    The checks run over the whole table at once, and the first that fails raises
    ``ValueError``, naming the missing column or every point it fails on. First the
    table's own shape:

    * the fifteen in-force columns are present;
    * no ``point_id`` appears twice;
    * ``policy_count`` is a number, zero or more;
    * ``duration_mth`` is a whole number of months, read by value, so that ``12.0`` is
      12: positive for a contract in force, 0 for one issued at the valuation date,
      negative for one issued later;
    * no policy is issued more than ``future_horizon_mth`` months after the valuation
      date, so ``duration_mth`` is ``-future_horizon_mth`` or more. At 0 the model takes
      no future new business, and the message says so; a negative horizon is itself
      refused.

    Then the contract's terms, ``term_years`` before every check that reads the term
    clock:

    * ``age_at_entry`` is a whole number of years, 0 or more, and ``term_years`` a whole
      number of years, 1 or more, each read by value; ``RILA_US_S`` reads both by
      ``int()``, which truncates a fraction without a word, and the term clock counts
      months modulo ``12 x term_years``;
    * ``premium`` is a number above 0, the purchase payment;
    * ``buffer`` and ``floor_rate`` are fractions, 0 or more and below 1, each the strike
      ``I_s (1 - x)`` of a put; ``participation`` is a number above 0, by which the cap's
      strike divides;
    * ``declared_cap`` is blank, for an uncapped option, or a number, zero or more, and
      ``declared_step``, ``declared_edge`` and ``wd_rate_ann`` are numbers, zero or more:
      each reaches a ``max`` or a ``min`` that would lose a blank;
    * ``nge_reset`` is a flag, read by value: ``True`` or ``False``, as pandas reads
      either, or 1 or 0, where ``RILA_US_S``'s ``bool()`` reads any text, a blank among
      them, as ``True``;
    * ``nge_reset`` is set only on a capped Cap Rate option, ``crediting_type`` ``CAP``
      with ``declared_cap`` given. ``RILA_US_S``'s solver prices the at-the-money call,
      the call at the cap and the buffer's put: on a Floor option it would solve the
      wrong portfolio, and on a Step, an Edge or an uncapped option the flag does nothing,
      and ``RILA_US_S`` projects either without a word.

    Then the opening state:

    * the investment amount, the two accounts, the free withdrawal amount unused and the
      return-of-premium base are numbers, zero or more; the account value and the account
      value at the anniversary are finite numbers of either sign, the interim value being
      able to fall below 0 under the contract [S2];
    * each term-start value, where given, is a number in its range: the index level and
      the volatility above 0, the index being what ``Projection.index_perf`` divides by;
      the Market Value Rate, the risk-free rate and the dividend yield above -1, each
      added to 1 under a division or a logarithm; the cap a finite number;
    * a contract not yet in force, ``duration_mth`` 0 or less, holds nothing yet: its
      seven amounts are 0, and it enters with its purchase payment in its issue month;
    * the five term-start values are given exactly where the term under way began before
      the valuation month, ``duration_mth`` positive and not a multiple of
      ``12 x term_years``, and ``cap_rate_init`` exactly where, besides, that term began
      at a renewal, ``duration_mth`` above ``12 x term_years``, under ``nge_reset``: at or
      after the valuation month the projection reads a term's start from the scenario, and
      a cap re-solves there, or is the declared cap. A table written with the value
      entering month 0 on every row is refused here;
    * a contract in force holds an investment amount or an account balance;
      ``RILA_US_S`` reaches a contract holding nothing only by a full withdrawal;
    * ``rop_pp_init`` is at most the purchase payment, to a cent: withdrawals only reduce
      the base;
    * in the first contract year, ``duration_mth`` 1 to 11, ``free_wd_remain_init`` is 0,
      to a cent, the year having no free withdrawal amount, and ``av_pp_prev_anniv_init``
      is the purchase payment, to a cent, the year having opened at issue;
    * before the first Term End Date, ``duration_mth`` 1 to ``12 x term_years - 1``, the
      Fixed and Holding Accounts are 0, to a cent: only a term end transfers to them;
    * on a renewal valuation, ``duration_mth`` a positive multiple of
      ``12 x term_years``, ``av_pp_init`` is the investment amount plus the two accounts,
      to two and a half cents: the month before closed a term, where the interim value is
      the Investment Amount itself. Carried to the cent, each of the four amounts is within
      half a cent of its exact value, so the identity can miss by two cents, and floating
      point may read that as a little more;
    * on an anniversary valuation, ``duration_mth`` a positive multiple of 12,
      ``av_pp_prev_anniv_init``, the account value before the anniversary's withdrawal, is
      at least ``av_pp_init``, the value after it, to a cent.

    Last, each point's keys into the tables it is joined with, each table's count cell
    asked first, so that a malformed table is refused by its own message:

    * ``scenario_id`` names a scenario of ``market_scenario_file`` that sets its levels by
      the point's first month on the books, ``t = 0`` or its issue month if later;
    * ``wd_schedule_id`` names a programme of ``withdrawal_file``;
    * ``term_years`` is a term of ``guar_min_rate_file``;
    * ``mort_table_file`` rates the point's sex at its attained age in its first month on
      the books;
    * ``cap_rate_init``, where given, is at least the guaranteed minimum cap of its term,
      which ``Projection.cap_rate`` floors every re-solved cap at.

    An extract may carry each amount of money to the cent, as an administration system
    holds it, each within half a cent of its exact value, and every rule between amounts
    allows for that without a tie falling to floating point: a cent where a rule compares
    one amount with another or with 0, and two and a half cents in the renewal rule, whose
    four amounts rounding can move apart by two.

    The table is returned with the columns those checks read by value as the numbers they
    were checked as: ``duration_mth``, ``age_at_entry`` and ``term_years`` int64;
    ``policy_count``, ``premium``, the rates and the thirteen opening-state columns
    float64, blank as NaN; and ``nge_reset`` the flags it was checked as. What it cannot
    check, ``Projection.proj_len`` does where it can: whether the point is still in cover
    at the valuation date, which needs ``maturity_age`` and ``maturity_min_years``, and
    whether the free withdrawal amount unused is within the contract year's, where the
    year's base is 0 or more, which needs ``free_wd_rate``. Left to the projection: a
    mortality table that stops before the maturity age, and whether a term-start value is
    the one the point's history ran on, since no scenario holds a path before ``t = 0``.
    """
    name = model_point_file                                          # noqa: F821
    table = pd.read_csv(input_dir() / name, index_col="point_id")    # noqa: F821
    balances = ("inv_amt_pp_init", "fixed_acct_pp_init", "holding_acct_pp_init",
                "free_wd_remain_init", "rop_pp_init")
    signed = ("av_pp_init", "av_pp_prev_anniv_init")
    market = ("index_at_term_start_init", "mvr_at_term_start_init",
              "risk_free_at_term_start_init", "div_yield_at_term_start_init",
              "impl_vol_at_term_start_init")
    amounts = ("inv_amt_pp_init", "fixed_acct_pp_init", "holding_acct_pp_init",
               "av_pp_init", "av_pp_prev_anniv_init", "free_wd_remain_init", "rop_pp_init")
    state = (*amounts, *market, "cap_rate_init")
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
    checked = {"policy_count": count.astype("float64"),
               "duration_mth": months.astype("int64")}
    ages = pd.to_numeric(table["age_at_entry"], errors="coerce")     # noqa: F821
    bad = table.index[~((ages % 1 == 0) & (ages >= 0))].tolist()
    if bad:
        raise ValueError(f"{name}: age_at_entry must be a whole number of years, 0 or "
                         f"more; it is not at point_id {bad}")
    checked["age_at_entry"] = ages.astype("int64")
    term = pd.to_numeric(table["term_years"], errors="coerce")       # noqa: F821
    bad = table.index[~((term % 1 == 0) & (term >= 1))].tolist()
    if bad:
        raise ValueError(f"{name}: term_years must be a whole number of years, 1 or more: "
                         f"the term clock counts months modulo 12 x term_years; it is not "
                         f"at point_id {bad}")
    checked["term_years"] = term.astype("int64")
    premium = pd.to_numeric(table["premium"], errors="coerce")       # noqa: F821
    bad = table.index[~((premium > 0) & (premium < float("inf")))].tolist()
    if bad:
        raise ValueError(f"{name}: premium must be a number above 0, the purchase "
                         f"payment; it is not at point_id {bad}")
    checked["premium"] = premium.astype("float64")
    for column in ("buffer", "floor_rate"):
        value = pd.to_numeric(table[column], errors="coerce")        # noqa: F821
        bad = table.index[~((value >= 0) & (value < 1))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a fraction, 0 or more and below 1, "
                             f"the strike of a put below the index at the Term Start "
                             f"Date; it is not at point_id {bad}")
        checked[column] = value.astype("float64")
    value = pd.to_numeric(table["participation"], errors="coerce")   # noqa: F821
    bad = table.index[~((value > 0) & (value < float("inf")))].tolist()
    if bad:
        raise ValueError(f"{name}: participation must be a number above 0, by which the "
                         f"cap's strike divides; it is not at point_id {bad}")
    checked["participation"] = value.astype("float64")
    cap = pd.to_numeric(table["declared_cap"], errors="coerce")      # noqa: F821
    bad = table.index[~(table["declared_cap"].isna()
                        | ((cap >= 0) & (cap < float("inf"))))].tolist()
    if bad:
        raise ValueError(f"{name}: declared_cap must be blank, for an uncapped option, or "
                         f"a number, zero or more; it is not at point_id {bad}")
    checked["declared_cap"] = cap.astype("float64")
    for column in ("declared_step", "declared_edge", "wd_rate_ann"):
        value = pd.to_numeric(table[column], errors="coerce")        # noqa: F821
        bad = table.index[~((value >= 0) & (value < float("inf")))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a number, zero or more; it is not "
                             f"at point_id {bad}")
        checked[column] = value.astype("float64")
    flag = table["nge_reset"].astype(str).str.strip().str.lower()
    reset = flag.isin(["true", "1", "1.0"])
    bad = table.index[~(reset | flag.isin(["false", "0", "0.0"]))].tolist()
    if bad:
        raise ValueError(f"{name}: nge_reset must be True or False, a flag; it is not at "
                         f"point_id {bad}")
    checked["nge_reset"] = reset
    capped = (table["crediting_type"] == "CAP") & table["declared_cap"].notna()
    bad = table.index[reset & ~capped].tolist()
    if bad:
        raise ValueError(f"{name}: nge_reset re-solves the cap of a capped Cap Rate "
                         f"option, crediting_type CAP with declared_cap given; it is set "
                         f"at point_id {bad}, where there is no cap to re-solve or the "
                         f"solver would price the Cap Rate portfolio for another crediting "
                         f"method")
    values = {c: pd.to_numeric(table[c], errors="coerce") for c in state}  # noqa: F821
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
            raise ValueError(f"{name}: {column} must be a finite number, of either sign, "
                             f"the interim value being able to fall below 0; it is not at "
                             f"point_id {bad}")
    for column, low, what in (
            ("index_at_term_start_init", 0.0, "above 0, the index level index_perf "
             "divides by"),
            ("mvr_at_term_start_init", -1.0, "above -1, 1 + mvr dividing the interim "
             "value's rate adjustment"),
            ("risk_free_at_term_start_init", -1.0, "above -1, an annual effective rate"),
            ("div_yield_at_term_start_init", -1.0, "above -1, an annual effective rate"),
            ("impl_vol_at_term_start_init", 0.0, "above 0, the volatility the option "
             "prices divide by")):
        v = values[column]
        bad = table.index[table[column].notna()
                          & ~((v > low) & (v < float("inf")))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be blank or a number {what}; it is "
                             f"not at point_id {bad}")
    v = values["cap_rate_init"]
    bad = table.index[table["cap_rate_init"].notna()
                      & ~((v > -float("inf")) & (v < float("inf")))].tolist()
    if bad:
        raise ValueError(f"{name}: cap_rate_init must be blank or a finite number; it is "
                         f"not at point_id {bad}")
    issued = months <= 0
    for column in amounts:
        bad = table.index[issued & (values[column] != 0)].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be 0 on a policy not yet in force, "
                             f"duration_mth 0 or less, which enters with its purchase "
                             f"payment in its issue month; it is not at point_id {bad}")
    in_force = months > 0
    mid_term = in_force & (months % (12 * term) != 0)
    for column in market:
        given = table[column].notna()
        bad = table.index[mid_term & ~given].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be given where the term under way "
                             f"began before the valuation month; it is blank at point_id "
                             f"{bad}")
        bad = table.index[~mid_term & given].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be blank unless the term under way "
                             f"began before the valuation month: at or after it the "
                             f"projection reads the term start from the scenario; it is "
                             f"given at point_id {bad}")
    renewed = mid_term & (months > 12 * term) & reset
    given = table["cap_rate_init"].notna()
    bad = table.index[renewed & ~given].tolist()
    if bad:
        raise ValueError(f"{name}: cap_rate_init must be given where the term under way "
                         f"began at a renewal under nge_reset before the valuation month; "
                         f"it is blank at point_id {bad}")
    bad = table.index[~renewed & given].tolist()
    if bad:
        raise ValueError(f"{name}: cap_rate_init must be blank unless the term under way "
                         f"began at a renewal under nge_reset before the valuation month: "
                         f"elsewhere the cap is the declared cap, or is re-solved from the "
                         f"scenario; it is given at point_id {bad}")
    held = (values["inv_amt_pp_init"] + values["fixed_acct_pp_init"]
            + values["holding_acct_pp_init"])
    bad = table.index[in_force & (held == 0)].tolist()
    if bad:
        raise ValueError(f"{name}: a contract in force must hold an investment amount or "
                         f"an account balance; none does at point_id {bad}")
    cent = 0.01
    bad = table.index[~(values["rop_pp_init"] <= premium + cent)].tolist()
    if bad:
        raise ValueError(f"{name}: rop_pp_init must be at most the premium, to a cent: "
                         f"withdrawals only reduce the return-of-premium base; it is not "
                         f"at point_id {bad}")
    first_year = in_force & (months < 12)
    bad = table.index[first_year & ~(values["free_wd_remain_init"] <= cent)].tolist()
    if bad:
        raise ValueError(f"{name}: free_wd_remain_init must be 0 in the first contract "
                         f"year, duration_mth 1 to 11, which has no free withdrawal "
                         f"amount; it is not at point_id {bad}")
    gap = (values["av_pp_prev_anniv_init"] - premium).abs()
    bad = table.index[first_year & ~(gap <= cent)].tolist()
    if bad:
        raise ValueError(f"{name}: av_pp_prev_anniv_init must be the premium in the first "
                         f"contract year, duration_mth 1 to 11, the year having opened at "
                         f"issue; it is not at point_id {bad}")
    first_term = in_force & (months < 12 * term)
    for column in ("fixed_acct_pp_init", "holding_acct_pp_init"):
        bad = table.index[first_term & ~(values[column] <= cent)].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be 0 before the first Term End "
                             f"Date, duration_mth 1 to 12 x term_years - 1: only a term "
                             f"end transfers to it; it is not at point_id {bad}")
    renewal = in_force & (months % (12 * term) == 0)
    gap = (values["av_pp_init"] - held).abs()
    slack = 2.5 * cent          # half a cent from each of the four amounts, and half more
    bad = table.index[renewal & ~(gap <= slack)].tolist()
    if bad:
        raise ValueError(f"{name}: on a renewal valuation, duration_mth a multiple of 12 x "
                         f"term_years, av_pp_init must be inv_amt_pp_init + "
                         f"fixed_acct_pp_init + holding_acct_pp_init, to two and a half "
                         f"cents: the month before closed a term, where the interim value "
                         f"is the Investment Amount; it is not at point_id {bad}")
    anniversary = in_force & (months % 12 == 0)
    low = values["av_pp_init"] - cent
    bad = table.index[anniversary & ~(values["av_pp_prev_anniv_init"] >= low)].tolist()
    if bad:
        raise ValueError(f"{name}: on an anniversary valuation av_pp_prev_anniv_init, the "
                         f"account value before the anniversary's withdrawal, must be at "
                         f"least av_pp_init, the value after it, to a cent; it is not at "
                         f"point_id {bad}")
    # Each point's keys into the tables it is joined with, each table checked first.
    entry = (-months).clip(lower=0)         # the first month the point is on the books
    scenarios, programmes = market_scenario_file, withdrawal_file    # noqa: F821
    floors_file, rates_file = guar_min_rate_file, mort_table_file    # noqa: F821
    market_scenario_count()
    steps = market_scenario().reset_index()
    first = pd.to_numeric(steps["month_end"],                         # noqa: F821
                          errors="coerce").groupby(steps["scenario_id"]).min()
    bad = table.index[~(table["scenario_id"].map(first) <= entry)].tolist()
    if bad:
        raise ValueError(f"{name}: scenario_id must name a scenario of {scenarios} that "
                         f"sets its levels by the point's first month on the books, t = 0 "
                         f"or its issue month if later; it does not at point_id {bad}")
    withdrawal_count()
    held_ids = withdrawal_table().index.get_level_values("wd_schedule_id")
    bad = table.index[~table["wd_schedule_id"].isin(held_ids)].tolist()
    if bad:
        raise ValueError(f"{name}: wd_schedule_id must name a programme of {programmes}; "
                         f"it does not at point_id {bad}")
    guar_min_rate_count()
    floors = guar_min_rate_table()
    terms = pd.to_numeric(floors.index.to_series(), errors="coerce")  # noqa: F821
    bad = table.index[~term.isin(terms)].tolist()
    if bad:
        raise ValueError(f"{name}: term_years must be a term of {floors_file}; it is not "
                         f"at point_id {bad}")
    mort_table_count()
    rates = mort_table().reset_index()
    rated = pd.to_numeric(rates["age"], errors="coerce")             # noqa: F821
    youngest = rated.groupby(rates["sex"]).min()
    oldest = rated.groupby(rates["sex"]).max()
    attained = ages + months.clip(lower=0) // 12
    sexes = table["sex"]
    bad = table.index[~((attained >= sexes.map(youngest))
                        & (attained <= sexes.map(oldest)))].tolist()
    if bad:
        raise ValueError(f"{name}: {rates_file} must rate the point's sex at its attained "
                         f"age in its first month on the books; it does not at point_id "
                         f"{bad}")
    minimum = pd.Series(                                             # noqa: F821
        pd.to_numeric(floors["guar_min_cap"], errors="coerce").to_numpy(),  # noqa: F821
        index=terms.to_numpy())
    cap_given = table["cap_rate_init"].notna()
    bad = table.index[cap_given
                      & ~(values["cap_rate_init"] >= term.map(minimum))].tolist()
    if bad:
        raise ValueError(f"{name}: cap_rate_init must be at least guar_min_cap for its "
                         f"term in {floors_file}; it is not at point_id {bad}")
    return table.assign(**checked, **{c: values[c].astype("float64") for c in state})


def mort_table():
    """Annual mortality by attained age and sex, read from *mort_table.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file, index_col=["age", "sex"])     # noqa: F821


def market_scenario():
    """The exogenous market-data scenarios, read from *market_scenario_sec.csv*.

    Indexed by ``(scenario_id, month_end)`` and read as a step function of the month end:
    each row states the index level, the Market Value Rate, the risk-free rate, the
    dividend yield and the implied volatility that hold from that month end until the next
    row of the same scenario. ``month_end`` is a time in months from the **valuation
    date**, ``0`` at the valuation date, one more than the index ``t`` of the projection
    month it closes. ``RILA_US_S``'s scenarios stand under their own ids, which on a
    contract issued at the valuation date is ``RILA_US_S``'s own clock; each model point
    restated in force or issued later reads its own copy, re-based to its month, which
    holds no level before the point's issue month. :func:`market_scenario_count` checks
    the table, and ``Projection.market_state``, its one reader, asks for the count first.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / market_scenario_file,                          # noqa: F821
        index_col=["scenario_id", "month_end"])


def surr_charge_table():
    """The withdrawal charge schedule by complete contract year.

    Read from *surr_charge_table.csv*, ``RILA_US_S``'s file, in place, and checked by
    :func:`surr_charge_count`.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / surr_charge_file, index_col="contract_year")   # noqa: F821


def guar_min_rate_table():
    """The guaranteed minimum Cap, Step and Edge rates by term.

    Read from *guar_min_rate_table.csv*, ``RILA_US_S``'s file, in place, and checked by
    :func:`guar_min_rate_count`.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / guar_min_rate_file, index_col="term_years")    # noqa: F821


def lapse_table():
    """The un-shocked base annual surrender rate by contract year, from *lapse_table.csv*.

    The charge-expiry shock is not in this file: its size is the ``lapse_shock_mult``
    Reference on ``Projection`` and the year it lands in is derived from
    *surr_charge_table.csv*, so the two cannot drift apart.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / lapse_file, index_col="contract_year")         # noqa: F821


def withdrawal_table():
    """Scheduled gross withdrawals, read from *withdrawal_table.csv*.

    Indexed by ``(wd_schedule_id, month_end)`` - the **policy** month end the withdrawal
    is taken at, counted from the Issue Date, since a withdrawal programme is a contractual
    schedule and stays on the policy clock; a month end with no row takes no withdrawal.
    :func:`withdrawal_count` checks the table, and ``Projection.wd_amount_pm``, its one
    reader, asks for the count first.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / withdrawal_file,                               # noqa: F821
        index_col=["wd_schedule_id", "month_end"])


def market_scenario_count():
    """The number of rows *market_scenario_sec.csv* holds, the scenarios checked: an int.

    :func:`market_scenario` reads the file as ``RILA_US_S`` reads its own, and this cell
    checks it. A ``scenario_id`` that is blank is refused, naming the file, the column and
    the lines it is on; so is a ``month_end`` that is blank, text, not a whole number or
    below 0, read by value, once, as ``Projection.market_state``'s step function compares
    it; and so is a scenario that sets two levels at one month end, naming the lines. And
    so is an ``index_level`` or an ``impl_vol`` that is blank, text, infinite or not above
    0, and an ``mvr``, a ``risk_free`` or a ``div_yield`` that is blank, text, infinite or
    not above -1, naming its lines: the index level divides the index performance and
    every strike, the volatility the Black-Scholes arguments, and each rate is added to 1
    under a division or a logarithm. ``RILA_US_S``'s step function compares the raw months
    with ``t``, so one written as text raises Python's own ``TypeError``, and a blank one
    is a level that never holds. A scenario may start after ``t = 0``, for business issued
    later, so the month a scenario must start by is the point's: :func:`model_point_table`
    refuses a point whose scenario sets no level by its first month on the books.
    ``Projection.market_state``, the table's one reader, asks for the count before it
    reads a level, so a projection meets the checks first.
    """
    name = market_scenario_file                                      # noqa: F821
    rows = market_scenario().reset_index()
    lines = rows.index + 2                  # the header is line 1 of the file
    bad = lines[rows["scenario_id"].isna().to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: scenario_id must not be blank; it is on line {bad}")
    months = pd.to_numeric(rows["month_end"], errors="coerce")       # noqa: F821
    bad = lines[(~((months % 1 == 0) & (months >= 0))).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: month_end must be a whole number, 0 or more; it is not "
                         f"on line {bad}")
    keys = pd.MultiIndex.from_arrays(                                # noqa: F821
        [rows["scenario_id"], months.astype("int64")], names=["scenario_id", "month_end"])
    bad = lines[keys.duplicated(keep=False)].tolist()
    if bad:
        raise ValueError(f"{name}: a scenario must set one level a month end; one sets two "
                         f"on lines {bad}")
    for column, low in (("index_level", 0.0), ("mvr", -1.0), ("risk_free", -1.0),
                        ("div_yield", -1.0), ("impl_vol", 0.0)):
        v = pd.to_numeric(rows[column], errors="coerce")             # noqa: F821
        bad = lines[(~((v > low) & (v < float("inf")))).to_numpy()].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a finite number above {low:g}; it "
                             f"is not on line {bad}")
    return int(len(rows))


def mort_table_count():
    """The number of rows *mort_table.csv* gives a rate for, the table checked: an int.

    :func:`mort_table` reads the table as ``RILA_US_S`` reads it, and this cell checks it.
    The ``age`` key is read by value, once, as ``Projection.mort_rate_base_at``'s join
    matches it, so an age written ``70.0`` is 70. An age that is blank, text or not a whole
    number is refused, naming the file, the column and the lines it is on; so is a ``sex``
    that is not ``M`` or ``F``, the two values a model point's sex can take, a blank among
    them; so is an age and sex on more than one row, naming each with its lines; and so is
    a sex whose ages do not run one row an age, from its first to its last, the message
    naming each age missing. And so is a ``mort_rate`` that is blank, text, infinite or
    below 0, naming its lines: through the cap on mortality the rate reaches every count in
    force, and a blank would survive the cap as a NaN, text fail far from here. A rate
    above 1 is accepted, and capped. ``Projection.mort_rate_base_at``, the table's one
    reader, asks for the count before it reads a rate, so a projection meets the checks
    first.
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


def surr_charge_count():
    """The number of contract years *surr_charge_table.csv* charges, checked: an int.

    :func:`surr_charge_table` reads the table as ``RILA_US_S`` reads it, and this cell
    checks it. The ``contract_year`` key is read by value, once, so that a year written
    ``3.0`` is 3, and the years must run ``0 .. n - 1``, one row a year, without a gap or
    a repeat: ``Projection.surr_charge_rate_at`` reads every complete contract year from
    0, charges nothing from year ``n`` on, and ``Projection.lapse_shock_year`` finds the
    first charge-free year among them. A year that is blank, text or not a whole number is
    refused, naming the file, the column and the lines it is on, and so are years that do
    not run so. And so is a ``surr_charge_rate`` that is blank, text or not a fraction, 0
    to 1, naming its lines: a blank would read as no charge in a comparison. The count is
    ``n``. ``RILA_US_S`` reads a year the table lacks as no charge, so one written as text
    silently removes the charge of every year.
    """
    name = surr_charge_file                                          # noqa: F821
    rows = surr_charge_table().reset_index()
    lines = rows.index + 2                  # the header is line 1 of the file
    years = pd.to_numeric(rows["contract_year"], errors="coerce")    # noqa: F821
    bad = lines[(~(years % 1 == 0)).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: contract_year must be a whole number; it is not on "
                         f"line {bad}")
    if sorted(years.astype("int64").tolist()) != list(range(len(rows))):
        raise ValueError(f"{name}: the contract years must run from 0, one row a year, "
                         f"without a gap or a repeat; they are "
                         f"{years.astype('int64').tolist()} on lines {lines.tolist()}")
    rates = pd.to_numeric(rows["surr_charge_rate"], errors="coerce")  # noqa: F821
    bad = lines[(~((rates >= 0) & (rates <= 1))).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: surr_charge_rate must be a fraction, 0 to 1; it is not "
                         f"on line {bad}")
    return int(len(rows))


def guar_min_rate_count():
    """The number of terms *guar_min_rate_table.csv* floors, the table checked: an int.

    :func:`guar_min_rate_table` reads the table as ``RILA_US_S`` reads it, and this cell
    checks it. The ``term_years`` key is read by value, once, as
    ``Projection.guar_min_rate``'s join on the model point's term matches it, so a term
    written ``6.0`` is 6. A term that is blank, text, not a whole number or below 1 is
    refused, naming the file, the column and the lines it is on, and so is a term on more
    than one row. And so is a ``guar_min_cap``, a ``guar_min_step`` or a ``guar_min_edge``
    that is blank, text, infinite or below 0, naming its lines: each floors a declared
    rate through a ``max``, which would lose a blank. ``Projection.guar_min_rate``, the
    table's one reader, asks for the count before it reads a floor, and
    :func:`model_point_table` refuses a point whose term the table lacks.
    """
    name = guar_min_rate_file                                        # noqa: F821
    rows = guar_min_rate_table().reset_index()
    lines = rows.index + 2                  # the header is line 1 of the file
    terms = pd.to_numeric(rows["term_years"], errors="coerce")       # noqa: F821
    bad = lines[(~((terms % 1 == 0) & (terms >= 1))).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: term_years must be a whole number, 1 or more; it is not "
                         f"on line {bad}")
    bad = lines[terms.duplicated(keep=False).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: each term must have one row; one has two on lines "
                         f"{bad}")
    for column in ("guar_min_cap", "guar_min_step", "guar_min_edge"):
        v = pd.to_numeric(rows[column], errors="coerce")             # noqa: F821
        bad = lines[(~((v >= 0) & (v < float("inf")))).to_numpy()].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a finite number, zero or more; it "
                             f"is not on line {bad}")
    return int(len(rows))


def lapse_table_count():
    """The number of rows *lapse_table.csv* holds, the step function checked: an int.

    :func:`lapse_table` reads the table as ``RILA_US_S`` reads it, and this cell checks
    it. The ``contract_year`` key is read by value, once, as
    ``Projection.lapse_rate_base_py``'s step function compares it, so a year written
    ``7.0`` is 7. A year that is blank, text or not a whole number is refused, naming the
    file, the column and the lines it is on; so is a year on more than one row; and so is
    a table whose first year is not 1, under which a contract year before it would have no
    rate. And so is a ``lapse_rate_base`` that is blank, text or not a fraction, 0 to 1,
    naming its lines: the surrender rate's bound, ``min(lapse_rate_max, ...)``, is written
    first, and would lose a blank. ``Projection.lapse_rate_base_py``, the table's one
    reader, asks for the count before it reads a rate.
    """
    name = lapse_file                                                # noqa: F821
    rows = lapse_table().reset_index()
    lines = rows.index + 2                  # the header is line 1 of the file
    years = pd.to_numeric(rows["contract_year"], errors="coerce")    # noqa: F821
    bad = lines[(~(years % 1 == 0)).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: contract_year must be a whole number; it is not on "
                         f"line {bad}")
    bad = lines[years.duplicated(keep=False).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: each contract year must have one row; one has two on "
                         f"lines {bad}")
    if not years.min() == 1:
        raise ValueError(f"{name}: the first contract year must be 1, so that every "
                         f"contract year has a rate; it is {years.min():g}")
    rates = pd.to_numeric(rows["lapse_rate_base"], errors="coerce")  # noqa: F821
    bad = lines[(~((rates >= 0) & (rates <= 1))).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: lapse_rate_base must be a fraction, 0 to 1; it is not "
                         f"on line {bad}")
    return int(len(rows))


def withdrawal_count():
    """The number of rows *withdrawal_table.csv* holds, the programmes checked: an int.

    :func:`withdrawal_table` reads the table as ``RILA_US_S`` reads it, and this cell
    checks it. A ``wd_schedule_id`` that is blank is refused, naming the file, the column
    and the lines it is on; so is a ``month_end`` that is blank, text, not a whole number or
    below 0, read by value, once, as ``Projection.wd_amount_pm``'s exact-key lookup
    matches it; and so is a programme that withdraws twice at one month end, naming the
    lines. And so is a ``wd_amount`` that is blank, text, infinite or below 0, naming its
    lines: the withdrawal reaches the account value through a ``min``, which would lose a
    blank. ``RILA_US_S``'s lookup matches the raw months, so one written as text turns them
    all to text, and every scheduled withdrawal is then zero. ``Projection.wd_amount_pm``,
    the table's one reader, asks for the count before it reads an amount, and
    :func:`model_point_table` refuses a point whose programme the table lacks.
    """
    name = withdrawal_file                                           # noqa: F821
    rows = withdrawal_table().reset_index()
    lines = rows.index + 2                  # the header is line 1 of the file
    bad = lines[rows["wd_schedule_id"].isna().to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: wd_schedule_id must not be blank; it is on line {bad}")
    months = pd.to_numeric(rows["month_end"], errors="coerce")       # noqa: F821
    bad = lines[(~((months % 1 == 0) & (months >= 0))).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: month_end must be a whole number, 0 or more; it is not "
                         f"on line {bad}")
    keys = pd.MultiIndex.from_arrays(                                # noqa: F821
        [rows["wd_schedule_id"], months.astype("int64")],
        names=["wd_schedule_id", "month_end"])
    bad = lines[keys.duplicated(keep=False)].tolist()
    if bad:
        raise ValueError(f"{name}: a programme must withdraw once a month end at most; one "
                         f"withdraws twice on lines {bad}")
    amounts = pd.to_numeric(rows["wd_amount"], errors="coerce")      # noqa: F821
    bad = lines[(~((amounts >= 0) & (amounts < float("inf")))).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: wd_amount must be a finite number, zero or more; it is "
                         f"not on line {bad}")
    return int(len(rows))


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table_sec.csv"

mort_table_file = "mort_table.csv"

market_scenario_file = "market_scenario_sec.csv"

surr_charge_file = "surr_charge_table.csv"

guar_min_rate_file = "guar_min_rate_table.csv"

lapse_file = "lapse_table.csv"

withdrawal_file = "withdrawal_table.csv"

future_horizon_mth = 120

pd = ("Module", "pandas")
