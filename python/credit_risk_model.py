import pandas as pd
import numpy as np

def calculate_ecl(df: pd.DataFrame, scenario_multiplier: float = 1.0) -> pd.DataFrame:
    out = df.copy()
    out["pd_stressed"] = np.clip(out["pd_12m"] * scenario_multiplier, 0.001, 0.95)
    out["lgd_stressed"] = np.clip(out["lgd"] * (1 + (scenario_multiplier - 1) * 0.35), 0.05, 0.95)
    out["ecl_stressed_bn_vnd"] = out["pd_stressed"] * out["lgd_stressed"] * out["ead"]
    return out

def portfolio_summary(df: pd.DataFrame) -> dict:
    return {
        "total_exposure_bn_vnd": round(df["ead"].sum(), 2),
        "total_ecl_bn_vnd": round(df["ecl_bn_vnd"].sum(), 2),
        "weighted_pd_pct": round((df["pd_12m"] * df["ead"]).sum()/df["ead"].sum()*100, 2),
        "weighted_lgd_pct": round((df["lgd"] * df["ead"]).sum()/df["ead"].sum()*100, 2),
        "stage2_3_ratio_pct": round(df.loc[df["stage"].isin(["Stage 2","Stage 3"]),"ead"].sum()/df["ead"].sum()*100, 2)
    }

if __name__ == "__main__":
    df = pd.read_csv("data/loan_portfolio_sample.csv")
    print(portfolio_summary(df))
