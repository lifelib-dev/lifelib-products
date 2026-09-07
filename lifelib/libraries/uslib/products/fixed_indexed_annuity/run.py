"""Run the FIA_US_S reference model and print its cash flow statement.

    python products/fixed_indexed_annuity/run.py            # anchor cell (point_id = 1)
    python products/fixed_indexed_annuity/run.py 2          # another model point

Output is ASCII-only so it prints on a Windows console under any code page.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "FIA_US_S")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
entry = proj.entry_year()
print("model point {}: {} - {}{} {} premium {:,.0f}, bonus {:.0%}, {} indexed".format(
    point_id, proj.policy_id(), proj.sex(), proj.age_at_entry(), proj.tax_status(),
    proj.premium_pp(), proj.bonus_rate(), "{:.0%}".format(proj.alloc_indexed())))
print("entered {} at anniversary {}: AV {:,.2f}  BB {:,.2f}  MGV {:,.2f}".format(
    "in force" if entry else "at issue", entry,
    proj.av_pp_at(entry, "BEF_INV"), proj.benefit_base_pp_at(entry, "BEF_ROLLUP"),
    proj.mgsv_pp_init()))
print("GLWB {}  basis {}  income from age {}  utilization {:.0%}  "
      "cap {:.2%}  rollup {}  stack {:.2f}x".format(
          "elected" if proj.glwb_elected() else "not elected", proj.glwb_basis(),
          proj.income_start_age(), proj.utilization_intensity(),
          proj.cap_rate_in_force(), proj.rollup_id(), proj.stack_factor()))

exercise = [t for t in range(entry, proj.proj_len()) if proj.is_exercise(t)]
depleted = [t for t in range(entry, proj.proj_len())
            if proj.phase(t) in ("DEPLETED", "TERMINATED")]
print("periods t = {}..{} (contract years {}..{}, to attained age {}); "
      "first lifetime withdrawal {}; account value runs out {}".format(
          entry, proj.proj_len() - 1,
          proj.policy_year(entry), proj.policy_year(proj.proj_len() - 1),
          proj.age(proj.proj_len() - 1) + 1,
          "in t = {}".format(exercise[0]) if exercise else "never",
          "in t = {} ({})".format(depleted[0], proj.phase(depleted[0]))
          if depleted else "never"))
print()

print("account value, benefit base and lifetime withdrawal (per contract):")
cols = ["av_pp_bef_inv", "index_credit_pp", "rider_charge_pp", "wd_pp", "av_pp", "mgsv_pp"]
av = proj.result_av().loc[:, cols]
bb = proj.result_glwb().loc[:, ["benefit_base_pp", "lw_pp", "phase"]]
print(av.join(bb).head(14).round(2).to_string())
print()

print("cash flows:")
print(proj.result_cf().head(14).round(2).to_string())

model.close()
