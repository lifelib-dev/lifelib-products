"""Run the EC_FR_A reference model and print its provision and cash flow statements.

    python products/eurocroissance/run.py            # Chassis A, the worked example
    python products/eurocroissance/run.py 2          # Chassis B, same asset path
    python products/eurocroissance/run.py 7          # an in-force Chassis A cell

Output is ASCII-only so it prints on a Windows console under any code page.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "EC_FR_A")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
t0 = proj.proj_start()
n = proj.proj_len()
chassis = ("A (1 deg: euros and parts)" if proj.is_euro_leg()
           else "B (2 deg: parts only)")
print("model point {}: {} - chassis {}, {}{}, term {} years, in force {}".format(
    point_id, proj.model_point()["policy_id"], chassis, proj.sex(),
    proj.issue_age(), n, proj.duration_inforce()))
print("guarantee {:.0%} of net versements = {:,.2f} at t = {}   scenario {}".format(
    proj.guarantee_rate(), proj.mg(n), n, proj.scenario()))
print("charges: entry {:.2%}  parts {:.2%} p.a.  performance {:.0%}  exit {:.2%}"
      .format(proj.entry_charge_rate(), proj.parts_charge_rate(),
              proj.perf_charge_rate(), proj.exit_charge_rate()))
print("part value {:.4f} at inception, floor {:.4f}   i_pm {:.2%} at t = {} "
      "to {:.2%} at t = {}".format(
          proj.part_value_init(), proj.min_part_value(), proj.i_pm(t0), t0,
          proj.i_pm(n), n))
print("decrements {}   partial rachat factor {:.2f}   lock-up {} years".format(
    proj.decrement_basis(), proj.wd_factor(), proj.lock_up_years()))
print()
print("Provisions (per policy):")
prov = proj.result_provisions()
# i_pm and asset_return are rates in a table of money amounts; rounding them to 2
# would print a 2.25% discount rate as 0.02.
print(prov.round({c: (4 if c in ("i_pm", "asset_return", "part_value", "parts")
                      else 2) for c in prov.columns}).to_string())
print()
print("Cash flows:")
print(proj.result_cf().round(2).to_string())
print()
print("Exit values at t = {}: surrender {:,.2f}  death {:,.2f}  "
      "maturity at t = {} {:,.2f}".format(
          min(t0 + 6, n), proj.surrender_value(min(t0 + 6, n)),
          proj.death_payout(min(t0 + 6, n)), n, proj.maturity_value(n)))
print("Insurer own funds, peak: contribution {:,.2f}   PGT {:,.2f}".format(
    max(proj.insurer_contribution(t) for t in range(t0, n + 1)),
    max(proj.pgt(t) for t in range(t0, n + 1))))
print()
print("Checks: assets {}  parts {}  guarantee {}  policies {}".format(
    proj.check_assets_roll_fwd(), proj.check_parts_roll_fwd(),
    proj.check_guarantee_roll_fwd(), proj.check_pols_roll_fwd()))
print("        PM funds the guarantee {}  PGT covers it {}  part value floor {}"
      .format(proj.check_guarantee_funding(), proj.check_pgt_covers_guarantee(),
              proj.check_part_value_floor()))
print("        own funds not paid {}  in-force PM re-struck {}".format(
    proj.check_own_funds_not_paid(), proj.check_pm_restruck()))

model.close()
