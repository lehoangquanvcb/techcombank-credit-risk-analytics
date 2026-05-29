
# Model Governance Pack

## Model Objective
Estimate credit risk, IFRS9 expected credit loss, stress impact, and early warning signals for a commercial bank portfolio.

## Scope
Corporate, SME, retail mortgage, and consumer finance exposures using synthetic data for demonstration.

## Model Components
- PD model: scorecard/logistic regression/challenger XGBoost
- LGD model: collateral and LTV-driven downturn LGD
- EAD model: outstanding balance plus credit conversion factor for undrawn commitments
- IFRS9 ECL: Stage 1 12-month ECL; Stage 2/3 lifetime ECL
- Stress testing: Base, Mild Stress, Severe Stress macro scenarios

## Validation
- Discrimination: AUC, Gini, KS
- Stability: PSI
- Calibration: Brier score and actual-vs-predicted default buckets
- Governance: independent validation and approval workflow

## Limitations
This package uses synthetic loan-level data. Real-life use requires audited bank data, data lineage checks, model validation, regulatory review, and approval by model risk governance.
