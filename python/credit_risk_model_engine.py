
"""
Credit Risk Analytics Engine
- Loads synthetic loan portfolio
- Trains Logistic Regression PD model
- Tries XGBoost as challenger when installed
- Exports model scores, validation metrics, and feature importance
"""
from pathlib import Path
import json
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, confusion_matrix, precision_score, recall_score
from sklearn.inspection import permutation_importance

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / "data" / "loan_portfolio_sample_1000.csv"
OUT = BASE / "data" / "model_output_scores.csv"
METRICS = BASE / "data" / "model_validation_metrics.json"

def ks_statistic(y_true, score):
    df = pd.DataFrame({"y": y_true, "score": score}).sort_values("score", ascending=False)
    df["bad"] = df["y"]
    df["good"] = 1 - df["y"]
    bad_total = df["bad"].sum()
    good_total = df["good"].sum()
    if bad_total == 0 or good_total == 0:
        return np.nan
    df["cum_bad"] = df["bad"].cumsum() / bad_total
    df["cum_good"] = df["good"].cumsum() / good_total
    return float((df["cum_bad"] - df["cum_good"]).abs().max())

def main():
    df = pd.read_csv(DATA)
    target = "default_flag"
    features_num = ["ltv", "dscr", "leverage", "dpd", "rating_downgrade_notches", "revenue_growth", "cash_flow_margin"]
    features_cat = ["segment", "industry", "region", "rating_grade", "collateral_type"]
    X = df[features_num + features_cat]
    y = df[target]

    pre = ColumnTransformer([
        ("num", StandardScaler(), features_num),
        ("cat", OneHotEncoder(handle_unknown="ignore"), features_cat)
    ])
    model = Pipeline([
        ("pre", pre),
        ("clf", LogisticRegression(max_iter=1000, class_weight="balanced"))
    ])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42, stratify=y)
    model.fit(X_train, y_train)
    prob = model.predict_proba(X_test)[:, 1]
    pred = (prob >= 0.5).astype(int)

    auc = roc_auc_score(y_test, prob)
    metrics = {
        "model": "Logistic Regression",
        "auc": float(auc),
        "gini": float(2 * auc - 1),
        "ks": ks_statistic(y_test, prob),
        "precision": float(precision_score(y_test, pred, zero_division=0)),
        "recall": float(recall_score(y_test, pred, zero_division=0)),
        "confusion_matrix": confusion_matrix(y_test, pred).tolist(),
    }

    # Try XGBoost challenger
    try:
        from xgboost import XGBClassifier
        xgb = Pipeline([
            ("pre", pre),
            ("clf", XGBClassifier(
                n_estimators=150, max_depth=3, learning_rate=0.05,
                subsample=0.85, colsample_bytree=0.85, eval_metric="logloss",
                random_state=42
            ))
        ])
        xgb.fit(X_train, y_train)
        p2 = xgb.predict_proba(X_test)[:,1]
        auc2 = roc_auc_score(y_test, p2)
        metrics["challenger_model"] = "XGBoost"
        metrics["challenger_auc"] = float(auc2)
        metrics["challenger_gini"] = float(2 * auc2 - 1)
        metrics["recommended_model"] = "XGBoost" if auc2 > auc else "Logistic Regression"
    except Exception as exc:
        metrics["challenger_model"] = "XGBoost not available"
        metrics["challenger_error"] = str(exc)

    df["pd_model_score"] = model.predict_proba(X)[:,1]
    df.to_csv(OUT, index=False)
    METRICS.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(json.dumps(metrics, indent=2))

if __name__ == "__main__":
    main()
