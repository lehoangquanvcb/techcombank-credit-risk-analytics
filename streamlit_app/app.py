
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

st.set_page_config(page_title="Techcombank Credit Risk Analytics Demo", layout="wide")
st.title("Credit Risk Analytics & IFRS9 ECL Platform - Boardroom Demo")

BASE = Path(__file__).resolve().parents[1]
df = pd.read_csv(BASE / "data" / "loan_portfolio_sample_1000.csv")

st.sidebar.header("Scenario Controls")
pd_mult = st.sidebar.slider("PD multiplier", 0.8, 3.0, 1.35, 0.05)
lgd_mult = st.sidebar.slider("LGD multiplier", 0.8, 2.0, 1.10, 0.05)
sector = st.sidebar.multiselect("Industry filter", sorted(df["industry"].unique()), default=sorted(df["industry"].unique()))

dff = df[df["industry"].isin(sector)].copy()
dff["stressed_pd"] = np.minimum(0.99, dff["pd_12m"] * pd_mult)
dff["stressed_lgd"] = np.minimum(0.95, dff["lgd"] * lgd_mult)
dff["stressed_ecl_vnd"] = dff["stressed_pd"] * dff["stressed_lgd"] * dff["ead_vnd"]

c1,c2,c3,c4 = st.columns(4)
c1.metric("Total EAD (VND bn)", f"{dff['ead_vnd'].sum()/1e9:,.0f}")
c2.metric("Base ECL (VND bn)", f"{dff['ecl_vnd'].sum()/1e9:,.0f}")
c3.metric("Stressed ECL (VND bn)", f"{dff['stressed_ecl_vnd'].sum()/1e9:,.0f}")
c4.metric("Stage 3 Ratio", f"{(dff.loc[dff['ifrs9_stage']==3,'ead_vnd'].sum()/dff['ead_vnd'].sum()):.2%}")

tab1, tab2, tab3, tab4 = st.tabs(["1. Portfolio", "2. IFRS9", "3. Stress Test", "4. Early Warning"])
with tab1:
    st.subheader("Portfolio by Industry")
    st.bar_chart(dff.groupby("industry")["ead_vnd"].sum()/1e9)
with tab2:
    st.subheader("IFRS9 Stage Distribution")
    st.dataframe(dff.groupby("ifrs9_stage")[["ead_vnd","ecl_vnd"]].sum()/1e9)
with tab3:
    st.subheader("Stress Test Output")
    st.dataframe(dff[["loan_id","industry","rating_grade","pd_12m","lgd","ead_vnd","stressed_pd","stressed_lgd","stressed_ecl_vnd"]].head(100))
with tab4:
    st.subheader("Early Warning List")
    ews = dff[(dff["dpd"]>=30) | (dff["dscr"]<1.1) | (dff["leverage"]>5)]
    st.dataframe(ews[["loan_id","industry","rating_grade","dpd","dscr","leverage","pd_12m","ecl_vnd"]].head(100))
