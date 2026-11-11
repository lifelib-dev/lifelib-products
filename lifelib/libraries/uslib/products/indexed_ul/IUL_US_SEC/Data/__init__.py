# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The eight input CSVs are read here, **once per model**, and referenced from
:mod:`~.IUL_US_SEC.Projection` as ``data``. :mod:`~.IUL_US_SEC.Projection` is
parameterized by ``point_id``, so each ``Projection[N]`` is a separate ItemSpace with
its own cells cache; if the readers lived there, every model point would re-read every
file. Holding them in an unparameterized Space reads each file once no matter how many
policies are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/indexed_ul/``, rather than data stored inside the model. The model folder
therefore holds nothing but formulas -- no ``_data/``, no IOSpec, no embedded values --
so a diff of the model shows logic changes only. This follows ``annuallife.TradLife_A``;
contrast ``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model through
modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``IUL_US_SEC`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

**Six of the tables are IUL_US_S's.** The guaranteed COI scale, the corridor factors,
the mortality table, the class factors, the lapse table and the surrender charge
schedules are the files :mod:`~.IUL_US_S` reads, read here in place: one copy of each
table serves both models, so an edit to one reaches both. The model point table and the
segment ladder are this model's own, ``model_point_table_sec.csv`` and
``inforce_segments_sec.csv``; the first sits beside ``IUL_US_S``'s
``model_point_table.csv``, which this model never opens.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so
the model works wherever the repository is checked out. Each table has a filename
Reference and a reader Cells:

======================  ==========================  ==============================
Reference               Cells                       File
======================  ==========================  ==============================
model_point_file        model_point_table()         model_point_table_sec.csv
inforce_segments_file   inforce_segments()          inforce_segments_sec.csv
coi_rates_file          coi_rates()                 coi_rates.csv
corridor_file           corridor_factors()          corridor_factors.csv
mort_table_file         mort_table()                mort_table.csv
class_factor_file       class_factor_table()        class_factor_table.csv
lapse_table_file        lapse_table()               lapse_table.csv
surr_charge_file        surr_charge_table()         surr_charge_table.csv
======================  ==========================  ==============================

**The model point table is checked as it is read.** Ten of its columns are the in-force
interface: ``policy_count`` and ``duration_mth``, as in ``basiclife.BasicTerm_SE``, and
eight columns of an in-force policy's opening state, the account value and the loan,
which are ``IUL_US_S``'s own, the fixed account and the loan collateral apart from the
loan, the face in force, the premiums paid to date, the no-lapse accumulator and the MEC
latch. :func:`model_point_table` refuses a table that lacks any of them, or any column of
``IUL_US_S``'s own that the projection reads as a number or a flag, repeats a
``point_id``, holds a count, a duration, an age, a policy year or an amount no policy can
have, a share of the premium or of the fixed account outside 0 to 1, a flag that is not
``True`` or ``False``, or an opening state no policy can be in. The checks run in turn, by
20 rules, and the first that fails raises, naming the missing column or every point that
fails it. It also refuses a policy to be issued more than ``future_horizon_mth`` months
after the valuation date, 120 months as shipped: future new business is written over a
stated horizon, so that no frame runs longer than the projection from issue plus that
horizon. Set to 0, the Reference refuses future new business altogether. Whether a point
is still inside the projection at the valuation date, issued at an age with any cover,
withdrawing less than its fee, or holding one ladder row for each live segment is a rule
of the product rather than of the table, and ``Projection.proj_len`` checks it.

**So is the segment ladder.** ``IUL_US_S`` opens a point with no live segment, its whole
account value outside the collateral in the fixed account, which re-opening a policy in
force restates wrongly. So each live segment of a point in force is a row of
``inforce_segments_sec.csv``, keyed by ``point_id`` and ``slot``, the months since the
segment's creation at the valuation date, with its balance, the deductions and draws
charged to it, the index level at its creation and the cap declared then.
:func:`inforce_segments` refuses a row that names no point of the table, repeats a
slot, has a slot outside its point's life, or holds a value no segment can, and a point
whose account value is not its fixed account, its collateral and its segments, to the
cent. :func:`inforce_segment_count` and :func:`inforce_segment_last` give each point's
row count and last slot, which ``Projection.proj_len`` holds to the segments a policy in
force holds, one a month for its last twelve.

**So are the six assumption tables.** Each table read at an attained age or a policy
year has one reader in ``Projection``, keyed by the age or the year, and that reader
takes the table's extent -- the first and last ages, or the last policy year, beyond
which it reads the nearest row -- from a cell here that reads the key column by value,
once, and checks the table: :func:`corridor_age_first` and :func:`corridor_age_last`,
:func:`mort_age_first` and :func:`mort_age_last`, :func:`lapse_last_year`, and, for each
issue-age cell of the COI scale, :func:`coi_rate_last_years`. A key that is blank, text
or not a whole number is refused, naming the file, the column and the lines it is on. So
are keys that do not run one row an age or a year, without a gap or a repeat, policy
years from 1, the message naming each key that repeats, with its lines, and each that is
missing. And so is a rate that is blank, text or infinite, naming the column and its
lines, and a lapse or mortality rate outside 0 to 1: each is a probability, and the
monthly rate ``1 - (1 - q)^(1/12)`` has no real value past 1. :func:`class_count` and
:func:`surr_charge_count` check the class factors and the surrender-charge schedules the
same way, for the per-point joins that read them, and :func:`surr_charge_count` refuses a
run-off that is not a whole number of years, 1 or more, which the projection divides by.
A class factor, a guaranteed COI rate and a surrender charge below 0 are refused too:
each would project, with every check passing, a negative death, a credit for the
insurance, or a surrender charge that rises once its schedule has run off. So is a
corridor factor below 0, which no statutory percentage is, and which ``IUL_US_S``'s death
benefit, the ``max`` of the face and the corridor's amount with no floor on the account
value, would turn above the face on an exhausted account. Each reader asks for its extent
or its count before it reads a value, so a projection meets the checks first.

``IUL_US_S``'s readers take each extent from the key column as pandas reads it, where a
blank key is a missing value the extent skips: the table is cut short, and every later
age or year reads the last good row, without a word. A blank value is a missing value
to it too, which shows in its flows or is lost in a ``min`` or a ``max``: a blank lapse
rate reaches the lapse cap's ``min`` and is read as the cap, a blank corridor factor
reads as no corridor, and a blank surrender charge as none. Here each is refused, by
name, and so is a blank, text or infinite amount in the model point table.

``coi_rates.csv`` carries the *guaranteed maximum* monthly rate per $1,000 of net amount
at risk; the notes set that basis at 2017 CSO ANB ultimate [REG-R17], which may not be
reproduced here, and the current scale is the guaranteed scale times
``Projection.coi_curr_factor`` (65% **[std]**) because carrier COI tables are not public.
``mort_table.csv`` is a small illustrative best-estimate table **[std]**, not the 2015
VBT the notes recommend [REG-R18]; it is the same illustrative table shipped with
``UL_US_S``, so the chassis and this model share a basis.

There is deliberately **no premium persistency table**. The universal life chassis reads
one, because its notes give a 16-row schedule; these notes instead give a closed form --
``expected premium_y = planned x 0.98^(y-1)`` -- which is implemented as
:func:`~.IUL_US_SEC.Projection.prem_persistency` with the rate in a Reference. Nor is
there an index scenario file: the base deterministic run generates
:func:`~.IUL_US_SEC.Projection.index_level` from a level annual return on the valuation
clock, and a stochastic or historical path is substituted by overriding that one cell.

To swap in a licensed mortality basis, replace ``mort_table.csv`` with a same-schema
file, or point ``mort_table_file`` at a different name before the model computes
anything. No formula changes. Replacing the file changes :mod:`~.IUL_US_S` too, which
reads the same one.
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

    Indexed by ``point_id``.  Ten columns are the in-force interface: ``policy_count``
    and ``duration_mth``, the completed policy months at the valuation date, as in
    ``basiclife.BasicTerm_SE``; and eight columns of the opening state, per policy, as the
    policy stands at the start of month 0, before any month-0 event:

    * ``av_pp_init`` and ``loan_bal_init``: the account value and the loan entering month
      0, ``IUL_US_S``'s own columns;
    * ``fa_pp_init`` and ``lca_pp_init``: the fixed (holding) account and the loan
      collateral account entering month 0, which ``IUL_US_S`` takes as the account value
      less the loan and as the loan;
    * ``sum_assured_init``: the face in force entering month 0, after every Option A
      withdrawal cut to date;
    * ``cum_prem_init`` and ``cum_prem_net_init``: the premiums less withdrawals paid to
      date, and the same less loans, the no-lapse guarantee's accumulator, each of which
      ``IUL_US_S`` opens at 0;
    * ``is_mec_init``: 1 where the 7-pay test failed before the valuation date, 0
      otherwise, an int code.

    The live index segments are the companion :func:`inforce_segments`.  The rest are
    ``IUL_US_S``'s, except ``row_kind``, ``source_policy_id`` and ``source_mth``, which
    record where the generator took each shipped row from and which no formula reads.

    The checks run over the whole table at once, by 20 rules in turn, and the first that
    fails raises ``ValueError``, naming the missing column or every point it fails on:

    1. the in-force columns are present, and so are the columns of ``IUL_US_S``'s own
       that the projection reads as a number or a flag: ``age_at_entry``,
       ``wd_first_year``, ``loan_first_year``, ``sum_assured``, ``premium_pp_ann``,
       ``wd_pp``, ``loan_new_pp_ann``, ``mnlp_rate``, ``gsp``, ``glp``,
       ``seven_pay_prem``, ``load_prem_rate``, ``index_alloc_rate`` and the flag
       ``has_surr_charge``;
    2. no ``point_id`` appears twice;
    3. ``policy_count`` is a number, zero or more;
    4. ``duration_mth`` is a whole number of months: positive for a policy in force, 0
       for one issued at the valuation date, negative for one issued later;
    5. no policy is issued more than ``future_horizon_mth`` months after the valuation
       date, so ``duration_mth`` is ``-future_horizon_mth`` or more.  At 0 the model takes
       no future new business, and the message says so; a negative horizon is itself
       refused;
    6. ``age_at_entry`` is a whole number of years, 0 or more: the projection takes its
       ``int()`` and counts its frame and every attained age on it;
    7. each of ``wd_first_year`` and ``loan_first_year`` is a whole number of policy
       years, 1 or more: ``IUL_US_S`` takes the ``int()`` of each and compares the policy
       year with it, so a fraction would move the first year without a word;
    8. ``sum_assured`` is a number above 0, the face at issue, which every policy holds:
       it reaches the death benefit's ``max``, the per-unit charge and the surrender
       charge, and a blank one would reach them as a missing value;
    9. each of ``premium_pp_ann``, ``wd_pp``, ``loan_new_pp_ann``, ``mnlp_rate``, ``gsp``,
       ``glp`` and ``seven_pay_prem`` is a number, zero or more: ``gsp`` and ``glp`` are
       read by the guideline limit's ``max`` and the single premium's ``min``, which a
       blank one would be lost in;
    10. ``load_prem_rate`` and ``index_alloc_rate``, the share of each premium the load
        takes and the share of the fixed account each month's sweep moves into a segment,
        are numbers from 0 to 1;
    11. ``has_surr_charge`` is ``True`` or ``False``, as pandas reads those words in any
        case.  A blank, a number or any other text is refused: one text value turns the
        whole column into text, where ``"False"`` is a true string, so every point would
        read as carrying a surrender charge;
    12. each of ``av_pp_init`` and ``fa_pp_init`` is a number, of either sign.
        ``IUL_US_S`` lapses no policy for insufficiency and charges an exhausted policy on,
        its fixed account carrying every deduction and draw the segments cannot, so the
        fixed account and then the account value run below zero, as its point 5's do,
        from policy months 383 and 604; a model restating ``IUL_US_S`` restates those
        states, and :func:`inforce_segments` holds the two together;
    13. each of ``lca_pp_init``, ``loan_bal_init`` and ``sum_assured_init`` is a number,
        zero or more.  The face in force may be 0: withdrawals under Option A can cut it
        to nothing while the policy stays in force, as ``IUL_US_S`` carries it;
    14. each of ``cum_prem_init`` and ``cum_prem_net_init`` is a number, of either sign:
        each is a tax or guarantee measure, not a balance, and withdrawals and loans can
        exceed the premiums paid;
    15. ``is_mec_init`` is 0 or 1, an int code, read by value, so that 1.0 is 1;
    16. a policy not yet in force, ``duration_mth`` 0 or less, has no opening state: each
        of the eight columns is 0, and the issue values come from the formulas;
    17. ``sum_assured_init`` is at most ``sum_assured``, the face at issue, on a policy in
        force, since face increases are not modelled.  A face below it is accepted,
        whether a withdrawal cut it or an elective decrease the model does not implement,
        and is projected from the value given;
    18. ``lca_pp_init`` is above 0 exactly where ``loan_bal_init`` is: a standard loan
        moves value into the collateral account on the day it is taken, and the model
        takes no repayment, so the two are held together from the loan's first day, each
        at its own rate;
    19. ``cum_prem_net_init`` is at most ``cum_prem_init``, to a cent and a half -- half a
        cent for each of the two and half a cent more -- since loans only lower it;
    20. ``is_mec_init`` is 1 where the 7-pay test has already failed in the month before
        the valuation date: ``cum_prem_init`` above ``seven_pay_prem`` times the policy
        years to date, inside the first seven.

    The text columns ``sex``, ``rate_class``, ``db_option``, ``qual_test``,
    ``premium_type``, ``premium_mode`` and ``surr_charge_id`` are keys and labels, which
    the projection decodes or joins on at their first read, naming the point where none
    fits.
    """
    name = model_point_file                                          # noqa: F821
    table = pd.read_csv(input_dir() / name, index_col="point_id")    # noqa: F821
    state = ("av_pp_init", "loan_bal_init", "fa_pp_init", "lca_pp_init",
             "sum_assured_init", "cum_prem_init", "cum_prem_net_init", "is_mec_init")
    years = ("wd_first_year", "loan_first_year")
    amounts = ("premium_pp_ann", "wd_pp", "loan_new_pp_ann", "mnlp_rate", "gsp", "glp",
               "seven_pay_prem")
    shares = ("load_prem_rate", "index_alloc_rate")
    for column in ("policy_count", "duration_mth", "age_at_entry", *years, "sum_assured",
                   *amounts, *shares, "has_surr_charge", *state):
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
    for column in years:
        v = pd.to_numeric(table[column], errors="coerce")            # noqa: F821
        bad = table.index[~((v % 1 == 0) & (v >= 1))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a whole number of policy years, "
                             f"1 or more; it is not at point_id {bad}")
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
    for column in ("av_pp_init", "fa_pp_init"):
        v = values[column]
        bad = table.index[~(v.abs() < float("inf"))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a number; it is not at point_id "
                             f"{bad}")
    for column in ("lca_pp_init", "loan_bal_init", "sum_assured_init"):
        v = values[column]
        bad = table.index[~((v >= 0) & (v < float("inf")))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a number, zero or more; it is "
                             f"not at point_id {bad}")
    for column in ("cum_prem_init", "cum_prem_net_init"):
        v = values[column]
        bad = table.index[~(v.abs() < float("inf"))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a number; it is not at point_id "
                             f"{bad}")
    bad = table.index[~values["is_mec_init"].isin([0, 1])].tolist()
    if bad:
        raise ValueError(f"{name}: is_mec_init must be 0 or 1, an int code; it is not "
                         f"at point_id {bad}")
    for column in state:
        bad = table.index[(months <= 0) & (values[column] != 0)].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be 0 on a policy not yet in force, "
                             f"duration_mth 0 or less; it is not at point_id {bad}")
    bad = table.index[(months > 0) & ~(values["sum_assured_init"] <= face)].tolist()
    if bad:
        raise ValueError(f"{name}: sum_assured_init must be at most sum_assured, the "
                         f"face at issue, since face increases are not modelled; it is "
                         f"not at point_id {bad}")
    lent = values["loan_bal_init"] > 0
    bad = table.index[(values["lca_pp_init"] > 0) != lent].tolist()
    if bad:
        raise ValueError(f"{name}: lca_pp_init must be above 0 where loan_bal_init is, "
                         f"and 0 where it is 0: the collateral account holds a loan's "
                         f"collateral while the loan is outstanding; it is not at "
                         f"point_id {bad}")
    over = values["cum_prem_net_init"] > values["cum_prem_init"] + 0.015
    bad = table.index[over].tolist()
    if bad:
        raise ValueError(f"{name}: cum_prem_net_init must be at most cum_prem_init, to a "
                         f"cent and a half, since loans only lower it; it is not at "
                         f"point_id {bad}")
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


def inforce_segments():
    """The live index segments of each point in force, from *inforce_segments_sec.csv*.

    Indexed by ``point_id`` and ``slot``, both read by value as ints.  One row per live
    segment of a point in force at the valuation date, as it stands entering month 0:
    ``slot`` is the months since the segment's creation at the valuation date, 1 to 12,
    so the segment in slot ``k`` was born in policy month ``duration_mth - k``, and the
    one in slot 12 matures at ``t = 0``.  Its columns, per policy:

    * ``seg_bal_pp_init``: the segment's balance;
    * ``seg_ded_cum_pp_init`` and ``seg_wd_cum_pp_init``: the monthly deductions, and the
      withdrawals and loan transfers, charged to it since its creation, which with the
      balance are its credit base;
    * ``seg_index_start_init``: the index level at its creation, on the valuation-clock
      path, whose level at the valuation date is ``Projection.index_level_init``;
    * ``seg_index_cap_init``: the cap declared at its creation.

    ``point_id`` is the only key to a point, and nothing else in the file names one.  A
    point not yet in force holds no row; a point in force holds one for each of its last
    ``min(12, duration_mth)`` months, a month that swept nothing included, which
    ``Projection.proj_len`` checks, since the twelve is ``Projection.seg_term_mth``.

    The checks run over the whole file at once, by 9 rules in turn, and the first that
    fails raises ``ValueError``, naming the missing column or the lines, the header line
    1, or the points it fails on:

    1. the seven columns are present;
    2. each of ``point_id`` and ``slot`` is a whole number;
    3. each ``point_id`` is a point of :func:`model_point_table`;
    4. no ``point_id`` and ``slot`` appear together twice;
    5. ``slot`` is from 1 to its point's ``duration_mth``: no segment predates issue, and a
       point not yet in force holds none;
    6. each of ``seg_bal_pp_init``, ``seg_ded_cum_pp_init`` and ``seg_wd_cum_pp_init`` is
       a number, ``-1e-8`` or more: a balance a draw or a deduction took to exactly
       nothing can close on a rounding about zero of either sign, which an extract carried
       to the cent writes as 0, and ``Projection.check_seg_ladder`` holds every live
       balance to the same ``-1e-8``, ``IUL_US_S``'s tolerance;
    7. ``seg_index_start_init`` is a number above 0, the level the segment's return
       divides by;
    8. ``seg_index_cap_init`` is a number, zero or more: the credited rate's ``min``
       reads the cap first, so a blank cap would credit the floor without a word;
    9. each point's ``av_pp_init`` is its ``fa_pp_init`` plus its ``lca_pp_init`` plus the
       balances of its segments here, to half a cent an amount and half a cent more: the
       identity ``Projection.check_av_components`` holds every month, the opening state
       being the close of the month before.  The projection opens the account value from
       the parts, so the column is held to them, not read.
    """
    name = inforce_segments_file                                     # noqa: F821
    points = model_point_file                                        # noqa: F821
    table = pd.read_csv(input_dir() / name)                          # noqa: F821
    values = ("seg_bal_pp_init", "seg_ded_cum_pp_init", "seg_wd_cum_pp_init",
              "seg_index_start_init", "seg_index_cap_init")
    for column in ("point_id", "slot", *values):
        if column not in table.columns:
            raise ValueError(f"{name} has no {column} column")
    keys = {}
    for column in ("point_id", "slot"):
        v = pd.to_numeric(table[column], errors="coerce")            # noqa: F821
        bad = (table.index[~(v % 1 == 0)] + 2).tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a whole number; it is not on "
                             f"line {bad}")
        keys[column] = v.astype("int64")
    model_points = model_point_table()
    known = keys["point_id"].isin(model_points.index)
    bad = (table.index[~known] + 2).tolist()
    if bad:
        ids = sorted(set(keys["point_id"][~known]))
        raise ValueError(f"{name}: point_id {ids} on line {bad} is no point of {points}")
    pairs = pd.MultiIndex.from_arrays([keys["point_id"], keys["slot"]])  # noqa: F821
    faults = []
    for p, k in sorted(set(pairs[pairs.duplicated()])):
        lines = (table.index[(keys["point_id"] == p) & (keys["slot"] == k)] + 2).tolist()
        faults.append(f"point_id {p} slot {k} is on line {lines}")
    if faults:
        raise ValueError(f"{name}: each point_id and slot must have one row; "
                         + "; ".join(faults))
    months = pd.to_numeric(model_points["duration_mth"], errors="coerce")  # noqa: F821
    life = months.reindex(keys["point_id"].to_numpy()).to_numpy()
    bad = (table.index[~((keys["slot"] >= 1) & (keys["slot"] <= life))] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: slot must be from 1 to its point's duration_mth, the "
                         f"months since the segment's creation at the valuation date; it "
                         f"is not on line {bad}")
    numbers = {}
    for column in values:
        numbers[column] = pd.to_numeric(table[column], errors="coerce")  # noqa: F821
    for column in values[:3]:
        v = numbers[column]
        bad = (table.index[~((v >= -1e-8) & (v < float("inf")))] + 2).tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a number, -1e-8 or more, zero "
                             f"to IUL_US_S's tolerance; it is not on line {bad}")
    v = numbers["seg_index_start_init"]
    bad = (table.index[~((v > 0) & (v < float("inf")))] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: seg_index_start_init must be a number above 0, the "
                         f"level the segment's return divides by; it is not on line {bad}")
    v = numbers["seg_index_cap_init"]
    bad = (table.index[~((v >= 0) & (v < float("inf")))] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: seg_index_cap_init must be a number, zero or more; it "
                         f"is not on line {bad}")
    held = pd.Series(numbers["seg_bal_pp_init"].to_numpy(),          # noqa: F821
                     index=keys["point_id"].to_numpy())
    segments = held.groupby(level=0).sum().reindex(model_points.index, fill_value=0.0)
    count = held.groupby(level=0).size().reindex(model_points.index, fill_value=0)
    av = pd.to_numeric(model_points["av_pp_init"], errors="coerce")  # noqa: F821
    parts = (pd.to_numeric(model_points["fa_pp_init"], errors="coerce")  # noqa: F821
             + pd.to_numeric(model_points["lca_pp_init"], errors="coerce")  # noqa: F821
             + segments)
    slack = 0.005 * (count + 3) + 0.005
    bad = model_points.index[~((av - parts).abs() <= slack)].tolist()
    if bad:
        raise ValueError(f"{points}: av_pp_init must be fa_pp_init plus lca_pp_init plus "
                         f"the point's segments in {name}, to half a cent an amount and "
                         f"half a cent more; it is not at point_id {bad}")
    out = table.assign(point_id=keys["point_id"], slot=keys["slot"])
    return out.set_index(["point_id", "slot"]).sort_index()


def inforce_segment_count():
    """The number of live segments *inforce_segments_sec.csv* holds for each point.

    A Series of ints over every point of :func:`model_point_table`, 0 where the file holds
    none, read from :func:`inforce_segments`, which checks the file first.
    ``Projection.proj_len`` holds it, with :func:`inforce_segment_last`, to the segments
    a policy in force holds: one for each of its last ``min(seg_term_mth, duration_mth)``
    months.
    """
    held = inforce_segments().groupby(level="point_id").size()
    return held.reindex(model_point_table().index, fill_value=0).astype("int64")


def inforce_segment_last():
    """The last slot *inforce_segments_sec.csv* holds for each point.

    A Series of ints over every point of :func:`model_point_table`, 0 where the file holds
    no segment, read from :func:`inforce_segments`, which checks the file first and
    refuses a slot below 1 or held twice.  So a point whose last slot equals its count
    holds slots 1 to that count, one each, which is what ``Projection.proj_len`` asks.
    """
    tbl = inforce_segments().reset_index()
    last = tbl.groupby("point_id")["slot"].max()
    return last.reindex(model_point_table().index, fill_value=0).astype("int64")


def coi_rates():
    """Guaranteed maximum monthly COI rates, read from *coi_rates.csv*.

    Per $1,000 of net amount at risk, keyed by issue-age cell and policy year.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / coi_rates_file,                                # noqa: F821
        index_col=["sex", "rate_class", "age_at_entry", "policy_year"])


def corridor_factors():
    """The GPT corridor factor table by attained age, read from *corridor_factors.csv*.

    The IRC 7702(d)(2) applicable percentages [R4]: 250% to attained age 40, grading to
    100% at 90-95.
    """
    return pd.read_csv(input_dir() / corridor_file, index_col="age")  # noqa: F821


def mort_table():
    """The best-estimate annual mortality table by age, read from *mort_table.csv*."""
    return pd.read_csv(input_dir() / mort_table_file, index_col="age")  # noqa: F821


def class_factor_table():
    """The underwriting-class factors, read from *class_factor_table.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / class_factor_file, index_col="rate_class")    # noqa: F821


def lapse_table():
    """The base annual lapse rates by policy year, read from *lapse_table.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / lapse_table_file, index_col="policy_year")    # noqa: F821


def surr_charge_table():
    """The surrender charge schedules, read from *surr_charge_table.csv*.

    One row per ``surr_charge_id``, giving the initial charge per $1,000 of initial
    face and the number of years over which it runs off linearly.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / surr_charge_file,                              # noqa: F821
        index_col="surr_charge_id")


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
    as the current scale does from attained age 69, but is never a credit.
    ``Projection.coi_rate_last_year`` takes a point's extent from here, and refuses a cell
    it lacks, before ``Projection.coi_rate_guar_py`` reads its scale.
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


def corridor_age_last():
    """The last attained age *corridor_factors.csv* gives a factor for, the table checked.

    The ``age`` column is read by value, once, so an age written ``40.0`` is 40.  A key
    that is blank, text or not a whole number is refused, naming the file, the column and
    the lines it is on.  So are ages that do not run one row an age, without a gap or a
    repeat: the message names each age that repeats, with its lines, and each age missing
    between the first and the last.  And so is a ``corridor_factor`` that is blank, text,
    infinite or below 0, naming its lines: a multiple of the account value, which the
    statute's applicable percentages hold to 100% or more.
    ``Projection.corridor_factor_at``, the table's one reader, takes both of its extents,
    this and :func:`corridor_age_first`, before it reads a factor.  A blank factor is a
    missing value to ``IUL_US_S``, whose death benefit, the ``max`` of the face and the
    corridor's amount, then reads it as no corridor at all.  A factor below 1 only makes
    the corridor bind later, or never; below 0 it would make the corridor's amount on an
    account value below 0 a positive one, which ``IUL_US_S``'s death benefit, with no floor
    on the account value, would pay: at -0.5 from attained age 95, its point 5 pays
    58,155,653.50 on a face of 92,200 at its month 800, every account check passing.
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
    bad = (factors.index[~((factors >= 0) & (factors < float("inf")))] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: corridor_factor must be a number, zero or more; it is "
                         f"not on line {bad}")
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
    it reads a rate.  A blank rate is a missing value to ``IUL_US_S``, whose mortality is
    then not a number, and to ``Projection.mort_rate``, whose cap, ``min(q, 1.0)``, keeps
    it missing; a negative one would project negative deaths.
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


def lapse_last_year():
    """The last policy year *lapse_table.csv* gives a rate for, the table checked.

    The ``policy_year`` column is read by value, once, as the lookup matches it, so a year
    written ``5.0`` is year 5.  A key that is blank, text or not a whole number is
    refused, naming the file, the column and the lines it is on.  So are policy years that
    do not run from 1, one row a year, without a gap or a repeat: the message names each
    year that repeats or falls below 1, with its lines, and each year missing from 1 to the
    last.  And so is a ``lapse_rate_ann`` that is blank, text or outside 0 to 1, naming its
    lines: a probability, which below 0 would grow the count by its lapses, and past 1
    would leave ``Projection.lapse_rate_mth``'s ``1 - (1 - q)^(1/12)`` no real value.
    ``Projection.lapse_rate_base_py``, the table's one reader, takes its extent from here
    before it reads a rate.  A blank rate is a missing value to ``IUL_US_S``, which its
    lapse cap, ``min(lapse_rate_cap, rate)``, a bound written first, then reads as the
    cap.
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


def class_count():
    """The number of classes *class_factor_table.csv* gives a factor for, the table checked.

    A ``rate_class`` that is blank is refused, naming the file and the lines it is on, and
    so is one on more than one row, naming each such class with its lines; and so is a
    ``factor`` that is blank, text, infinite or below 0, naming its lines: a multiple of the
    base mortality, which below 0 would project negative deaths.
    ``Projection.class_factor``, the table's one reader, asks for the count before it reads
    a factor, so a projection meets the checks first.  A blank factor is a missing value to
    ``IUL_US_S``, whose mortality is then not a number, and to ``Projection.mort_rate``,
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
    charge by the run-off and counts policy years on it, where ``IUL_US_S`` divides by the
    float, takes the ``int()`` of a fraction for its lapse spike, and divides by zero at 0.
    ``Projection.surr_charge_rate_max`` and ``Projection.surr_charge_runoff_years``, the
    table's two readers, ask for the count before they read a value, so a projection meets
    the checks first.  A blank charge is a missing value to ``IUL_US_S``, whose surrender
    charge rate, the ``max`` of 0 and the charge left, then reads it as no charge at all.
    A charge below 0 leaves a charge below 0 through the schedule's years, which the
    ``max`` reads as none, and after them, where the share of the run-off left turns
    negative, a charge above 0 that rises each month, every check passing.
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

inforce_segments_file = "inforce_segments_sec.csv"

coi_rates_file = "coi_rates.csv"

corridor_file = "corridor_factors.csv"

mort_table_file = "mort_table.csv"

class_factor_file = "class_factor_table.csv"

lapse_table_file = "lapse_table.csv"

surr_charge_file = "surr_charge_table.csv"

future_horizon_mth = 120

pd = ("Module", "pandas")