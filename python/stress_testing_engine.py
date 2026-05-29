
"""
Macro Stress Testing Engine
Applies scenario multipliers to PD and LGD and exports ECL impact.
"""
from pathlib import Path
import pandas as pd
import numpy as np

BASE = Path(__file__).resolve().parents[1]
INP = BASE / "data" / "loan_portfolio_sample_1000.csv"
OUT = BASE / "data" / "stress_testing_output.csv"

SCENARIOS = {
    "Base": {"pd_mult": 1.00, "lgd_mult": 1.00},
    "Mild Stress": {"pd_mult": 1.35, "lgd_mult": 1.10},
    "Severe Stress": {"pd_mult": 1.90, "lgd_mult": 1.30},
}

def main():
    df = pd.read_csv(INP)
    rows = []
    for name, s in SCENARIOS.items():
        tmp = df.copy()
        tmp["scenario"] = name
        tmp["stressed_pd"] = np.minimum(0.99, tmp["pd_12m"] * s["pd_mult"])
        tmp["stressed_lgd"] = np.minimum(0.95, tmp["lgd"] * s["lgd_mult"])
        tmp["stressed_ecl_vnd"] = tmp["stressed_pd"] * tmp["stressed_lgd"] * tmp["ead_vnd"]
        rows.append(tmp[["loan_id","scenario","stressed_pd","stressed_lgd","ead_vnd","stressed_ecl_vnd"]])
    out = pd.concat(rows, ignore_index=True)
    out.to_csv(OUT, index=False)
    print(out.groupby("scenario")["stressed_ecl_vnd"].sum())

if __name__ == "__main__":
    main()
