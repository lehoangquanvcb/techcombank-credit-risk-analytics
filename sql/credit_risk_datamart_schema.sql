
-- Credit Risk Analytics Data Mart - PostgreSQL compatible
DROP TABLE IF EXISTS fact_ifrs9_ecl;
DROP TABLE IF EXISTS fact_loan_portfolio;
DROP TABLE IF EXISTS dim_customer;
DROP TABLE IF EXISTS dim_macro_scenario;

CREATE TABLE dim_customer (
    customer_id VARCHAR(30) PRIMARY KEY,
    segment VARCHAR(100),
    industry VARCHAR(100),
    region VARCHAR(100)
);

CREATE TABLE fact_loan_portfolio (
    loan_id VARCHAR(30) PRIMARY KEY,
    customer_id VARCHAR(30),
    rating_grade VARCHAR(10),
    outstanding_balance_vnd NUMERIC(22,0),
    undrawn_commitment_vnd NUMERIC(22,0),
    collateral_type VARCHAR(100),
    ltv NUMERIC(8,4),
    dscr NUMERIC(8,3),
    leverage NUMERIC(8,3),
    dpd INTEGER,
    pd_12m NUMERIC(12,8),
    lgd NUMERIC(12,8),
    ccf NUMERIC(8,4),
    ead_vnd NUMERIC(22,0),
    ifrs9_stage INTEGER,
    lifetime_pd NUMERIC(12,8),
    default_flag INTEGER,
    reporting_date DATE DEFAULT CURRENT_DATE
);

CREATE TABLE dim_macro_scenario (
    scenario_id SERIAL PRIMARY KEY,
    scenario_name VARCHAR(100),
    gdp_shock_pp NUMERIC(8,3),
    policy_rate_shock_pp NUMERIC(8,3),
    fx_shock_pct NUMERIC(8,3),
    property_price_shock_pct NUMERIC(8,3),
    pd_multiplier NUMERIC(8,3),
    lgd_multiplier NUMERIC(8,3)
);

CREATE TABLE fact_ifrs9_ecl (
    loan_id VARCHAR(30),
    reporting_date DATE,
    selected_pd NUMERIC(12,8),
    lgd NUMERIC(12,8),
    ead_vnd NUMERIC(22,0),
    ecl_vnd NUMERIC(22,0),
    stage INTEGER,
    scenario_name VARCHAR(100),
    PRIMARY KEY (loan_id, reporting_date, scenario_name)
);

CREATE OR REPLACE VIEW vw_portfolio_kpi AS
SELECT
    SUM(ead_vnd) AS total_ead_vnd,
    SUM(ead_vnd * pd_12m) / NULLIF(SUM(ead_vnd),0) AS weighted_avg_pd,
    SUM(ead_vnd * lgd) / NULLIF(SUM(ead_vnd),0) AS weighted_avg_lgd,
    SUM(CASE WHEN ifrs9_stage = 2 THEN ead_vnd ELSE 0 END) / NULLIF(SUM(ead_vnd),0) AS stage2_ratio,
    SUM(CASE WHEN ifrs9_stage = 3 THEN ead_vnd ELSE 0 END) / NULLIF(SUM(ead_vnd),0) AS stage3_ratio
FROM fact_loan_portfolio;
