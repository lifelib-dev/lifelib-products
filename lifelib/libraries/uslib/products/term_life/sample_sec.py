"""mx2cy's sample run for Term_US_SEC: the calls that type every cell.

mx2cy compiles the model's export, and it types each cell from the values this run passes
it and gets back: a cell it never calls compiles as a Python object, with a dict cache,
and the typing guard fails on it (USLIB-SEC-PLAN.md F3, C3).  So the run calls every
``Projection`` cell at least once, on every point of the committed table.  The three
reports reach all but eight: ``model_point`` and the four label accessors, which only a
reader asks for; ``band``, which no cell reads, since ``Data`` bands the face itself;
``point_id``, which only a refusal names; and ``phase``, which no report shows.  Those are
called here too, the phase before issue, in cover and from the month cover ends, and so
is the count in that month, which the roll-forward reads.

The run takes the committed points alone, and they leave branches untaken: the
semi-annual, quarterly and monthly cycles, a level period of twenty years, the conversion
window's age limit, cover that ends with the level period, the cap on mortality.  That is
enough to type every cell, because every branch of a cell returns the one type its other
branches return, a count a float in every branch.  What the compiled model computes on
those branches is not traced but tested: the compile tests run it on points that take
them, and compare it with modelx.
"""
import sys

# The export does not raise the recursion limit as modelx does (F7).  The deepest call the
# contract allows, a cold net_cf in the last month of the longest frame, needs a limit of
# 1,881 in the export, and the reports below, which run in ascending t, need 48 (measured
# at M14).  10,000 is five times the first.
sys.setrecursionlimit(10_000)

from Term_US_SEC_nomx import mx_model  # noqa: E402

projection = mx_model.Projection
for idx in range(len(mx_model.Data.model_point_table())):
    p = projection[idx]
    p.result_cf()
    p.result_pols()
    p.result_cf_annual()
    p.model_point(), p.sex(), p.rate_class(), p.plan(), p.premium_mode()
    p.band(), p.point_id()
    for t in range(p.proj_len() + 1):
        p.phase(t)
    p.pols_if_at(p.proj_len(), projection.BEF_NB)
