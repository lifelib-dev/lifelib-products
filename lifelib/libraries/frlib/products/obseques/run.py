"""Run the Obseques_FR_S reference model and print its cash flow statement.

    python products/obseques/run.py            # the RefOBS-VIA anchor cell
    python products/obseques/run.py 3          # the prime unique cell

Output is ASCII-only so it prints on a Windows console under any code page.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "Obseques_FR_S")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
print("model point {}: {} - {} cell, {}{}, capital {:,.0f} EUR, {} premium {:,.2f}/year".format(
    point_id, proj.model_point()["policy_id"], proj.cell(), proj.sex(),
    proj.age_at_entry(), proj.capital_0(), proj.premium_form(), proj.annual_premium()))
cease = proj.prem_cease_age()
print("carence = {} months   accidental multiplier = {:.0f}x   "
      "premiums {}   instalments {}/year".format(
          proj.carence_months(), proj.accident_mult(),
          "cease at attained age {}".format(cease) if cease else "payable to the end",
          proj.prem_freq()))
print("revalorisation = {:.2%} p.a. {}   premiums linked = {}   reduction share = {:.0%}".format(
    proj.reval_rate(), "simple" if proj.reval_simple() else "compound",
    proj.reval_prem_linked(), proj.reduction_share()))
xi, xc = proj.crossover_mth("ISSUE"), proj.crossover_mth("CURRENT")
print("surrender scale = {}   crossover: vs capital at issue {}, vs revalorised {}".format(
    proj.surr_scale(),
    "month {} (year {})".format(xi, (xi - 1) // 12 + 1) if xi else "none",
    "month {} (year {})".format(xc, (xc - 1) // 12 + 1) if xc else "none"))
print()
rows = [1, 6, 12, 13, 24, 60, 120, 240]
print(proj.result_cf().loc[[t for t in rows if t <= proj.proj_len()]].round(2).to_string())

model.close()
