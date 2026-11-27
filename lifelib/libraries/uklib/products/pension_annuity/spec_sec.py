# mx2cy's spec for PA_UK_SEC: the length of each C-array cache in Projection, by the
# cells' parameters (USLIB-SEC-PLAN.md F4, section 6.1 step 6; UKLIB-SEC-PLAN.md 6.7).  A
# compiled cache raises IndexError for an argument outside [0, size), so each size covers
# the largest argument any cell is called with on a point the contract allows, in its
# frame and in the month after it, t = proj_len(), the frame's closing time point, which
# lives_if and the payments to date read and C4's full sweep evaluates every monthly cell
# at; plus one because the index starts at 0; and one of headroom where that leaves room,
# as uslib's SPIA_US_SEC, this model's chassis, sizes its own (USLIB-SEC-PLAN.md 7.9, Record
# -- M23).  mx2cy keys a size by a cell's parameter names, so every cell taking t alone
# shares one.  The contract is three Projection References and one of Data's.
# Projection.proj_len refuses a point any of whose covered lives was below issue_age_min,
# 0, at the start date, since PA_UK_S projects any age on the scenario basis and a frame
# runs to the age stop on its youngest life; on the table basis an omega_age above
# omega_age_max, 116, the shipped mortality table's last age plus one, so that every
# limiting age the shipped table admits fits these sizes and a longer table's is refused
# (UKLIB-SEC-PLAN.md 6.6, Record -- M10); a guarantee above 12 * (omega_age -
# issue_age_min) months; and on either basis a frame longer than 12 * (omega_age_max -
# issue_age_min) = 1,392 months from the start date, the longest the table basis
# projects.  The scenario basis reads no table, and proj_len holds its omega_age to no
# bound, as the in-force step held it to none, so there the frame's rule refuses a life
# issued younger than omega_age - omega_age_max, or a guarantee past 1,392 months, which
# the in-force step projected.  The age stop ends the frame when the youngest life reaches
# omega_age; and Data refuses an annuity starting more than future_horizon_mth, 120
# months, after the valuation date.  So no point a report projects at these References,
# on either basis, outruns these sizes.  A larger omega_age_max or future_horizon_mth
# needs these sizes recomputed here and the model rebuilt; proj_len refuses an
# issue_age_min below 0.
#
# t, months from the valuation date.  The longest frame is a life issued at 0, the
# youngest, to the age stop, 12 * (116 - 0) = 1,392 months, or a guarantee of as many, the
# longest frame proj_len admits, starting 120 months on: 1,512 months, t = 0 .. 1,511, and
# 1,512 in the month after, the closing time point, where lives_if reads survival and C4's
# sweep evaluates every monthly cell: 1,513, and one of headroom, 1,514.  Nothing reads
# t + 1 at t = proj_len().  In general 12 * (omega_age_max - issue_age_min) +
# future_horizon_mth + 2.
# timing, beside t in pols_if_at: BEF_NB 0 and BEF_DECR 1; kind, beside t in claims: VP 0,
# PROP 1 and ALL 3, the codes numbered as one with cum_annuity_pp's ANNUITANT 2, so that
# each kind's cell refuses the other's; life, beside t in the per-life monthly cells: 1
# and 2.  Every 2-D cache of a model has one inner width, the widest, the kinds' 4, because
# Cython's generated unpickle code converts the 2-D caches of a space with one function for
# each inner width: given two widths, it passes the narrower array where the wider is
# expected, which gcc 14 refuses (-Wincompatible-pointer-types, made an error on every gcc
# and clang by build_sec_cy.py) and MSVC accepts, and would write past its end.  So
# (1,514, 4) for each.  A timing 2 or 3, a kind ANNUITANT in claims, or a life 0 or 3, is
# inside the cache, where the cell refuses it as modelx does, ValueError("invalid timing"),
# ValueError("invalid kind") or ValueError("invalid life"); a code of 4 raises IndexError,
# compiled alone.
# k, a policy month or the time point opening it, from the start date: the schedule is
# read at every policy month of the frame, to the stop rule's month less one, 1,391 on a
# youngest life of 0 and on a guarantee of 1,392 months; the annuitant's payments to date,
# cum_annuity_pp(k, ANNUITANT), at the policy time point of every time point of the frame
# and the closing one, up to the stop rule's month itself, 1,392; cum_annuity_pp(k, ALL) at
# the same.  So k is at most 12 * (omega_age_max - issue_age_min) = 1,392: 1,393, and one
# of headroom, 1,394.  In general 12 * (omega_age_max - issue_age_min) + 2.  Beside it
# kind, 4 wide, as every 2-D cache: ANNUITANT 2 and ALL 3, and VP 0 and PROP 1, which the
# cell refuses.
# y, a policy year, read by annual_income at the schedule's policy months and in the
# proportionate payment, to the policy year of the frame's last month, 1,391 // 12 + 1 =
# 116; and by the openings of the three chains blocked by policy year, lives_if_py,
# cum_annuity_all_py and cum_annuity_pp_py, at a time point or a key that opens a policy
# year, up to the frame's closing one, the stop rule's month, 1,392 // 12 + 1 = 117: 118,
# and no headroom, since that is the largest a frame reaches.  In general omega_age_max -
# issue_age_min + 2.  Beside it life, 4 wide, in lives_if_py.
# a, an anniversary from the start date, read by the RPI's index and the ratchet's peak at
# y - 1 for every year the income reads, to 115: 116, and one of headroom, 117;
# omega_age_max - issue_age_min + 1.
# x, an attained age, read by the mortality table's one reader below omega_age alone,
# from issue_age_min: 0 .. 115: 116, and one of headroom, 117; omega_age_max + 1.  Beside
# it life, 4 wide, as every 2-D cache.  The reader's extent check runs before the array is
# read, so an age below the table's first, 50 as shipped, is refused by name.
# life, alone in age_at_entry, sex, mort_schedule, rating_factor, death_mth and
# lives_if_init: 1 and 2, widened to the inner width, 4, as Term_UK_SEC's are, so that a
# life of 0 or 3 is refused by the formula in both engines.
{"spaces": {"Projection": {"cells_param_size": {
    "t": 1514, ("t", "life"): (1514, 4), ("t", "timing"): (1514, 4),
    ("t", "kind"): (1514, 4), "k": 1394, ("k", "kind"): (1394, 4), "y": 118,
    ("y", "life"): (118, 4), "a": 117, ("x", "life"): (117, 4), "life": 4}}}}
