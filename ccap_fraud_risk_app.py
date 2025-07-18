
import streamlit as st
import pandas as pd

st.set_page_config(page_title="CCAP Fraud Risk Scoring", layout="wide")

st.title("Child Care Center Fraud Risk Scoring Tool")
st.write("Upload provider-level data and compute composite CCFRI scores to identify high-risk centers.")

uploaded_file = st.file_uploader("Upload CSV with metric values", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("Uploaded Data:", df.head())

    # Define weights
    weights = {
        "Overbilling Ratio (OBR)": 0.1,
        "No-Show Record Frequency (NSRF)": 0.1,
        "Locked/Empty Visit Alert (LEVA)": 0.1,
        "Attendance Pattern Anomaly (APA)": 0.1,
        "Revenue Per Child Index (RPCI)": 0.1,
        "License Violation Risk (LVR)": 0.1,
        "Cross-Program Funding Flag (CPFF)": 0.1,
        "Staffing Ratio Conflict (SRC)": 0.05,
        "Ghost Staff Indicator (GSI)": 0.05,
        "Rapid Payment Growth Flag (RPGF)": 0.05,
        "Non-Operating Hour Billing": 0.05,
        "Suspicious Relationship Index (SRI)": 0.05,
        "Cluster Risk Score (CRS)": 0.05,
    }

    # Ensure all required columns exist
    for metric in weights:
        if metric not in df.columns:
            st.error(f"Missing column: {metric}")
            st.stop()

    # Compute score
    df["CCFRI"] = sum(df[metric] * weight for metric, weight in weights.items())
    st.success("Scoring complete!")
    st.write(df[["CCFRI"] + list(weights.keys())])

    st.download_button("Download Scored Data", df.to_csv(index=False), file_name="Scored_CCAP_Data.csv", mime="text/csv")
else:
    st.info("Awaiting CSV file with metric columns.")
