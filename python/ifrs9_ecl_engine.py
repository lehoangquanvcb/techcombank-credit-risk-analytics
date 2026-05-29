
"""
IFRS9 ECL Engine
ECL = PD x LGD x EAD
Stage 1 uses 12M PD; Stage 2/3 use lifetime PD.
"""
from pathlib import Path
import pandas as pd
import numpy as np

BASE = Path(__file__).resolve().parents[1]
INP = BASE / "data" / "loan_portfolio_sample_1000.csv"
OUT = BASE / "data" / "ifrs9_ecl_output.csv"

def assign_stage(row):
    if row["dpd"] >= 90:
        return 3
    if row["dpd"] >= 30 or row["rating_downgrade_notches"] >= 2 or row["lifetime_pd"] / max(row["pd_12m"], 1e-6) >= 2.5:
        return 2
    return 1

def main():
    df = pd.read_csv(INP)
    df["ifrs9_stage_calc"] = df.apply(assign_stage, axis=1)
    df["selected_pd"] = np.where(df["ifrs9_stage_calc"] == 1, df["pd_12m"], df["lifetime_pd"])
    df["ecl_calc_vnd"] = df["selected_pd"] * df["lgd"] * df["ead_vnd"]
    df.to_csv(OUT, index=False)
    print(df.groupby("ifrs9_stage_calc")[["ead_vnd","ecl_calc_vnd"]].sum())

if __name__ == "__main__":
    main()
