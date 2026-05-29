
-- Top obligors by ECL proxy
SELECT loan_id, customer_id, rating_grade, ead_vnd, pd_12m, lgd, pd_12m*lgd*ead_vnd AS ecl_proxy
FROM fact_loan_portfolio
ORDER BY ecl_proxy DESC
LIMIT 20;

-- Sector concentration
SELECT industry, SUM(ead_vnd) AS ead_vnd, AVG(pd_12m) AS avg_pd
FROM fact_loan_portfolio
GROUP BY industry
ORDER BY ead_vnd DESC;

-- IFRS9 stage distribution
SELECT ifrs9_stage, COUNT(*) AS loan_count, SUM(ead_vnd) AS ead_vnd
FROM fact_loan_portfolio
GROUP BY ifrs9_stage
ORDER BY ifrs9_stage;
