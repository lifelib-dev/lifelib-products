"""Run the TermLifeUS reference model and print its cash flow statement.

    python us/models/term-life/run.py            # anchor cell (point_id = 1)
    python us/models/term-life/run.py 3          # another model point

Output is ASCII-only so it prints on a Windows console under any code page.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "TermLifeUS")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
print("model point {}: {} - {}{} {} {} face {:,.0f}".format(
    point_id, proj.mp()["policy_id"], proj.sex(), proj.issue_age(),
    proj.rate_class(), proj.plan(), proj.face_amount()))
print("jump ratio J = {:.4f}   shock lapse = {:.0%}   M(1) = {}   "
      "expiry = attained age 95 (policy year {})".format(
          proj.J(), proj.shock_lapse(), proj.M1(), proj.max_t()))
print()
print(proj.result_cf().head(12).round(2).to_string())

model.close()
