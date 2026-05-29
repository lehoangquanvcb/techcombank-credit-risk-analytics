
# Techcombank Credit Risk Analytics Platform - Full v3

This is a full interview-grade Credit Risk Analytics and Modelling package.

## Main Files
- `excel/Techcombank_Credit_Risk_Model_Full_v3.xlsx`
- `data/loan_portfolio_sample_1000.csv`
- `data/vietnam_macro_template.csv`
- `python/credit_risk_model_engine.py`
- `python/ifrs9_ecl_engine.py`
- `python/stress_testing_engine.py`
- `sql/credit_risk_datamart_schema.sql`
- `streamlit_app/app.py`
- `powerbi/PowerBI_Dashboard_Specification.md`
- `governance/Model_Governance_Pack.md`
- `interview_pack/Techcombank_Interview_Demo_Script.md`

## How to Use
1. Open the Excel file first.
2. Review `01_Macro_Input`, `02_Loan_Portfolio`, and `08_Dashboard`.
3. To run Python:
   ```bash
   cd python
   pip install -r requirements.txt
   python credit_risk_model_engine.py
   python ifrs9_ecl_engine.py
   python stress_testing_engine.py
   ```
4. To run Streamlit:
   ```bash
   cd streamlit_app
   pip install -r requirements.txt
   streamlit run app.py
   ```

## Important Notes
- Loan-level data is synthetic.
- Macro data is a template based partly on public references and partly on planning assumptions.
- Percent variables in Excel are designed for normal inputs: type `8.02` for 8.02%, not `0.0802`.
