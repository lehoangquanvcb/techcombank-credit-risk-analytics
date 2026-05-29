import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import plotly.express as px

st.set_page_config(
    page_title="Credit Risk Analytics Platform",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

AUTHOR = "Le Hoang Quan"
DATA_PATH = Path("data/loan_portfolio_sample.csv")

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

df = load_data()

st.sidebar.title("⚙️ Dashboard Settings")
view_mode = st.sidebar.radio("Viewing mode", ["PC / Boardroom", "Mobile friendly"], index=0)
scenario = st.sidebar.selectbox("Stress scenario", ["Base", "Mild Stress", "Severe Stress"])
scenario_multiplier = {"Base":1.0, "Mild Stress":1.35, "Severe Stress":1.85}[scenario]

st.title("🏦 Credit Risk Analytics & IFRS9 Modelling Platform")
st.caption(f"Author: {AUTHOR}")

df["pd_stressed"] = np.clip(df["pd_12m"] * scenario_multiplier, 0.001, 0.95)
df["lgd_stressed"] = np.clip(df["lgd"] * (1 + (scenario_multiplier - 1) * 0.35), 0.05, 0.95)
df["ecl_stressed_bn_vnd"] = df["pd_stressed"] * df["lgd_stressed"] * df["ead"]

total_exposure = df["ead"].sum()
total_ecl = df["ecl_bn_vnd"].sum()
stressed_ecl = df["ecl_stressed_bn_vnd"].sum()
weighted_pd = (df["pd_12m"] * df["ead"]).sum() / total_exposure
stage23 = df.loc[df["stage"].isin(["Stage 2","Stage 3"]),"ead"].sum() / total_exposure

if view_mode == "Mobile friendly":
    st.success("📱 Mobile friendly mode is ON: KPI cards and charts are displayed in a compact vertical layout.")
    st.metric("Total exposure", f"{total_exposure:,.0f} bn VND")
    st.metric("Base ECL", f"{total_ecl:,.1f} bn VND")
    st.metric("Stressed ECL", f"{stressed_ecl:,.1f} bn VND", delta=f"{stressed_ecl-total_ecl:,.1f}")
    st.metric("Weighted PD", f"{weighted_pd*100:.2f}%")
    st.metric("Stage 2+3 exposure", f"{stage23*100:.2f}%")
else:
    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("Total exposure", f"{total_exposure:,.0f} bn VND")
    c2.metric("Base ECL", f"{total_ecl:,.1f} bn VND")
    c3.metric("Stressed ECL", f"{stressed_ecl:,.1f} bn VND", delta=f"{stressed_ecl-total_ecl:,.1f}")
    c4.metric("Weighted PD", f"{weighted_pd*100:.2f}%")
    c5.metric("Stage 2+3 exposure", f"{stage23*100:.2f}%")

st.info("📌 This dashboard has multiple tabs. Please click each numbered tab below to view detailed modules:")

tabs = st.tabs([
    "1️⃣ Executive Overview",
    "2️⃣ Portfolio Quality",
    "3️⃣ IFRS9 ECL",
    "4️⃣ Stress Testing",
    "5️⃣ Early Warning",
    "6️⃣ Model Validation",
    "7️⃣ Management Actions"
])

with tabs[0]:
    st.subheader("1️⃣ Executive Risk Overview")
    st.write("This page summarizes portfolio exposure, expected credit loss and stress impact for senior management.")
    summary = df.groupby("stage", as_index=False).agg(exposure=("ead","sum"), ecl=("ecl_bn_vnd","sum"))
    if view_mode == "Mobile friendly":
        st.plotly_chart(px.bar(summary, x="stage", y="exposure", title="Exposure by IFRS9 Stage"), use_container_width=True)
        st.dataframe(summary, use_container_width=True, height=220)
    else:
        col1,col2 = st.columns(2)
        col1.plotly_chart(px.bar(summary, x="stage", y="exposure", title="Exposure by IFRS9 Stage"), use_container_width=True)
        col2.plotly_chart(px.pie(summary, names="stage", values="ecl", title="ECL by IFRS9 Stage"), use_container_width=True)

with tabs[1]:
    st.subheader("2️⃣ Portfolio Quality")
    by_ind = df.groupby("industry", as_index=False).agg(exposure=("ead","sum"), ecl=("ecl_bn_vnd","sum"), avg_pd=("pd_12m","mean"))
    st.plotly_chart(px.bar(by_ind.sort_values("exposure", ascending=False), x="industry", y="exposure", title="Exposure by Industry"), use_container_width=True)
    st.dataframe(by_ind, use_container_width=True, height=300 if view_mode == "Mobile friendly" else 420)

with tabs[2]:
    st.subheader("3️⃣ IFRS9 ECL")
    st.write("ECL = PD × LGD × EAD. Stage 1 uses 12-month ECL; Stage 2 and Stage 3 can be extended to lifetime ECL in the Python engine.")
    ecl_stage = df.groupby("stage", as_index=False).agg(ecl=("ecl_bn_vnd","sum"), stressed_ecl=("ecl_stressed_bn_vnd","sum"))
    st.plotly_chart(px.bar(ecl_stage, x="stage", y=["ecl","stressed_ecl"], barmode="group", title="Base vs Stressed ECL"), use_container_width=True)

with tabs[3]:
    st.subheader("4️⃣ Stress Testing")
    st.write(f"Selected scenario: **{scenario}**. PD and LGD are stressed using scenario multipliers.")
    stress_summary = pd.DataFrame({
        "Scenario":["Base","Mild Stress","Severe Stress"],
        "ECL_bn_VND":[total_ecl, 
                      (df["pd_12m"]*1.35*np.clip(df["lgd"]*(1+0.35*0.35),0.05,0.95)*df["ead"]).sum(),
                      (df["pd_12m"]*1.85*np.clip(df["lgd"]*(1+0.85*0.35),0.05,0.95)*df["ead"]).sum()]
    })
    st.plotly_chart(px.bar(stress_summary, x="Scenario", y="ECL_bn_VND", title="ECL under Stress Scenarios"), use_container_width=True)

with tabs[4]:
    st.subheader("5️⃣ Early Warning")
    ews = df.copy()
    ews["warning_flag"] = np.where((ews["dpd"]>=30)|(ews["dscr"]<1.1)|(ews["debt_to_ebitda"]>6), "Warning", "Normal")
    st.dataframe(ews[["loan_id","customer_id","industry","rating_grade","dpd","dscr","debt_to_ebitda","warning_flag"]].sort_values("warning_flag"), use_container_width=True, height=350)

with tabs[5]:
    st.subheader("6️⃣ Model Validation")
    st.write("Interview-grade validation metrics to discuss: AUC, Gini, KS, calibration, PSI, model drift, champion-challenger comparison.")
    val = pd.DataFrame({
        "Metric":["AUC","Gini","KS","PSI","Calibration"],
        "Prototype value":[0.74,0.48,0.36,0.08,"Acceptable"],
        "Interpretation":["Discrimination power","2*AUC-1","Max TPR-FPR","Population drift","Observed vs predicted default"]
    })
    st.dataframe(val, use_container_width=True)

with tabs[6]:
    st.subheader("7️⃣ Management Actions")
    st.markdown("""
    Recommended actions:
    - Tighten underwriting for high-PD and high-LGD sectors.
    - Review Stage 2 borrowers with weak DSCR or rising DPD.
    - Reprice high-risk exposures and adjust risk appetite.
    - Increase monitoring for real estate, construction and FX-sensitive borrowers.
    - Prepare provisioning buffer under severe stress scenario.
    """)

st.caption(f"© {AUTHOR}. Prototype for credit risk analytics, IFRS9 ECL and stress testing interview demonstration.")
