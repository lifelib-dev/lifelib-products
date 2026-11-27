# mx2cy's spec for IP_UK_SEC: the length of each C-array cache in Projection, by the cells'
# parameters (USLIB-SEC-PLAN.md F4, section 6.1 step 6; UKLIB-SEC-PLAN.md 6.3).  A compiled
# cache raises IndexError for an argument outside [0, size), so each size covers the
# largest argument any cell is called with on a point the contract allows, in its frame
# and in the month after it, t = proj_len(), which the roll-forward reads and C4's full
# sweep evaluates every monthly cell at; plus one because the index starts at 0.  No size
# has headroom past that but the cohorts' months, below: each is held to its derivation by
# a test.  mx2cy keys a size by a cell's parameter names, so every cell taking t alone
# shares one.  The contract is four References and one of Data's.  Projection.proj_len
# refuses a point issued below issue_age_min, 18, or expiring above expiry_age_max, 70;
# and Data refuses a point issued more than future_horizon_mth, 120 months, after the
# valuation date.  And proj_len refuses a cover from issue longer than 624 months or a
# frame longer than 744, the two these sizes are derived from, however the five are set,
# so that no point a report projects outruns these sizes, in modelx as compiled.  A
# contract with longer covers needs the sizes recomputed here, proj_len's two bounds moved
# with them, and the model rebuilt.  The ages bound no cache: an age indexes Data's
# inception and mortality tables, not a cache.
#
# t, months from the valuation date.  The longest frame is the longest cover, a policy
# issued at issue_age_min, 18, to expire at expiry_age_max, 70: 12 * (70 - 18) = 624
# months from issue, issued future_horizon_mth, 120 months, after the valuation date: 744
# months, t = 0 .. 743, and 744 in the month after it; and the roll-forward's residual
# there, check_pols_roll_fwd_resid(744), reads the count carried into 745,
# pols_if_at(745, BEF_NB): 746, which is 12 * (expiry_age_max - issue_age_min) +
# future_horizon_mth + 2.  A longer future_horizon_mth, a higher expiry_age_max or a lower
# issue_age_min needs t raised to 12 * (expiry_age_max - issue_age_min) + the horizon + 2.
# timing, beside t in pols_if_at: BEF_NB = 0 to AFT_DECR = 2, the codes, 3.
# kind, beside t in claims: BENEFIT = 0 to ALL = 3, the codes, 4.  Two 2-D caches of one
# outer size share one inner width, the wider, here 4 (below).  So a code from 4 raises
# IndexError, compiled alone, and the timing 3, inside the width, is a code pols_if_at
# refuses, in either engine.
# z, a claim duration, alone in the cells of one claim duration, rec_rate, rec_rate_mth,
# mort_rate_sick, mort_rate_sick_mth, claim_surv_step, claim_dur_year and
# pols_sick_dur_init: read at 1 to max_dur(), the cover from issue and one cohort of
# headroom, 12 * (70 - 18) + 1 = 625 at the longest cover: 626, which is
# 12 * (expiry_age_max - issue_age_min) + 2, and does not grow with the horizon.
# (t, z), the cohorts, pols_sick_dur: every month of t and every claim duration of z, z's
# 626 wide; and t's months and one more, 747, so that its outer size is no other 2-D
# cache's, whose inner width is 4: one inner width would widen pols_if_at's and claims'
# caches to 626 a month each, about 3.7 MB a point apiece (UKLIB-SEC-PLAN.md 6.3, K11).
# Why the outer size: Cython's unpickle code, __pyx_unpickle__c_Projection__set_state,
# reads each 2-D cache back through a C-array temporary, with a converter named by the
# inner type, __Pyx_carray_from_py_double___5b_626_5d_ for double[626].  It pools its
# temporaries by C type (Code.py's allocate_temp), and its C-array types compare equal on
# the outer size and the element type, the inner size not compared (PyrexTypes.py's
# CArrayType.__eq__): int[746][4] and double[746][4] are two types, double[746][4] and
# double[746][626] one.  So caches of one outer size share a temporary of the first one's
# shape for their values, and another for their flags: claims and pols_if_at share a
# double[746][4] and an int[746][4], and the cohorts, at 747, get a double[747][626] and
# an int[747][626] of their own.  At an outer size of 746 the cohorts' converter would be
# handed the [746][4] temporary, which gcc and clang refuse under
# -Werror=incompatible-pointer-types, as build_sec_cy.py builds on Linux and macOS,
# and gcc 14 by default, and which MSVC only warns of, and then writes 746 x 626 doubles
# into it as a point is unpickled.  This rests on an internal of Cython 3.3.1, measured at
# M8 and read at its review; uslib's rule of one inner width a model (USLIB-SEC-PLAN.md
# 6.1 step 6, 7.2's Record -- M15) is one width an outer size here, held by a test of
# these sizes and one of the generated C's temporaries.  The month past t's, 746, is one
# no call reaches.
{"spaces": {"Projection": {"cells_param_size": {
    "t": 746, ("t", "timing"): (746, 4), ("t", "kind"): (746, 4), "z": 626,
    ("t", "z"): (747, 626)}}}}
