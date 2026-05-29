CREATE TABLE loan_portfolio (
    loan_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20),
    segment VARCHAR(50),
    industry VARCHAR(100),
    rating_grade VARCHAR(10),
    outstanding_balance_bn_vnd NUMERIC,
    undrawn_bn_vnd NUMERIC,
    interest_rate_pct NUMERIC,
    dpd INTEGER,
    dscr NUMERIC,
    debt_to_ebitda NUMERIC,
    collateral_type VARCHAR(100),
    collateral_value_bn_vnd NUMERIC,
    pd_12m NUMERIC,
    lgd NUMERIC,
    ead NUMERIC,
    stage VARCHAR(20),
    ecl_bn_vnd NUMERIC
);

CREATE TABLE macro_scenario (
    scenario_name VARCHAR(50),
    gdp_growth_pct NUMERIC,
    inflation_pct NUMERIC,
    policy_rate_pct NUMERIC,
    usd_vnd NUMERIC,
    property_price_change_pct NUMERIC,
    pd_multiplier NUMERIC,
    lgd_multiplier NUMERIC
);
