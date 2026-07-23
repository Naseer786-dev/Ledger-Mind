import streamlit as st
import pandas as pd

st.set_page_config(page_title="Ledger-Mind", layout="wide")
st.title("📒 Ledger-Mind: Excel Scanner")
st.write("Upload your company Excel file to scan for errors")

uploaded_file = st.file_uploader("Choose an Excel or CSV file", type=["xlsx", "csv"])

if uploaded_file:
    # Read file
    if uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)
    else:
        df = pd.read_csv(uploaded_file)
    
    st.success(f"Loaded {len(df)} rows")
    st.dataframe(df.head(20))

    st.subheader("🔍 Scan Results")
    
    # Basic checks
    missing = df.isnull().sum()
    missing = missing[missing > 0]
    if not missing.empty:
        st.warning("Missing values:")
        st.write(missing)
    
    dups = df.duplicated().sum()
    st.write(f"**Duplicate rows:** {dups}")

    # TODO: Add your company specific checks here
