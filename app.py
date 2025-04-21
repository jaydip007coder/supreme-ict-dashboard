import streamlit as st
import pandas as pd

st.set_page_config(page_title="Supreme ICT Dashboard", layout="wide")
st.title("📊 Supreme ICT Trade Dashboard")

uploaded_file = st.file_uploader("📂 Upload Your Trade Log (.xlsx or .csv)", type=["xlsx", "csv"])

if uploaded_file is not None:
    try:
        # 📥 Read uploaded file
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # 🧼 Clean column names
        df.columns = df.columns.str.strip().str.title()

        # 🕵️ Preview cleaned columns
        st.success("✅ Columns Detected:")
        st.write(df.columns.tolist())

        # 🛡️ Try auto-fixing common column names
        if 'Symbol' not in df.columns:
            potential_matches = [col for col in df.columns if 'symbol' in col.lower()]
            if potential_matches:
                df.rename(columns={potential_matches[0]: 'Symbol'}, inplace=True)
                st.warning(f"⚠️ Auto-renamed '{potential_matches[0]}' to 'Symbol'")
        
        # 🎯 Now access Symbol column safely
        if 'Symbol' in df.columns:
            symbol_list = df['Symbol'].dropna().unique()
            st.success("🪙 Unique Symbols Found:")
            st.write(symbol_list)
        else:
            st.error("❌ Could not find a 'Symbol' column even after cleaning. Please check your file format.")

    except Exception as e:
        st.error("🚨 Error reading file or processing columns.")
        st.exception(e)

else:
    st.info("📎 Please upload a trade log file (.csv or .xlsx) to begin.")
