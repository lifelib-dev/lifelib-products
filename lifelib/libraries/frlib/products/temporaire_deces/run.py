"""Run the TD_FR_A reference model and print its cash flow statement.

    python products/temporaire_deces/run.py            # anchor cell (point_id = 1)
    python products/temporaire_deces/run.py 2          # another model point

Output is ASCII-only so it prints on a Windows console under any code page.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "TD_FR_A")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
print("model point {}: {} - {}{} {} - capital {:,.0f} EUR, cover to {}, "
      "PTIA to {}".format(
          point_id, proj.model_point()["policy_id"], proj.sex(),
          proj.issue_age(), proj.smoker(), proj.sum_assured(),
          proj.cover_end_age(), proj.ptia_end_age()))
print("premium form = {}   cotisation {:,.2f} -> {:,.2f} EUR over {} years   "
      "frequency = {}".format(
          proj.premium_form(), proj.prem_pp(1), proj.prem_pp(proj.proj_len()),
          proj.proj_len(), proj.prem_freq()))
print("rating factor = {:.2f}   waiting period = {} y   "
      "accident multiplier = {:.2f}".format(
          proj.rating_factor(), proj.waiting_period_y(),
          proj.accident_multiplier()))
print()
print(proj.result_cf().head(12).round(2).to_string())
print()
print("totals over {} years: premiums {:,.2f}  claims {:,.2f}  "
      "expenses {:,.2f}  net_cf {:,.2f}".format(
          proj.proj_len(),
          proj.result_cf()["premiums"].sum(),
          proj.result_cf()["claims_death"].sum()
          + proj.result_cf()["claims_ptia"].sum(),
          proj.result_cf()["expenses"].sum(),
          proj.result_cf()["net_cf"].sum()))
print("checks: roll forward {}  closure {}  PTIA gate {}  no cash value {}".format(
    proj.check_pols_roll_fwd(), proj.check_decrement_closure(),
    proj.check_ptia_gate(), proj.check_no_cash_value()))

model.close()
