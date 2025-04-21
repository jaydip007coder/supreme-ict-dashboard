import streamlit as st
import pandas as pd
import datetime as dt
import os

st.set_page_config(page_title="Supreme ICT Trade Dashboard v2", layout="wide")

# --- Title
st.title("📊 Supreme ICT Trade Dashboard v2")

# --- Load Data
uploaded_file = st.file_uploader("Upload Your Trade Log (Excel)", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # --- Basic Info
    st.subheader("Trade Summary")
    st.write(f"Total Trades: {len(df)}")

    # --- Killzone Tagging (IST - 12hr format)
    def get_killzone_label(t):
        if isinstance(t, str):
            t = pd.to_datetime(t).time()

        time = dt.datetime.combine(dt.date.today(), t)

        if dt.time(3,30) <= time.time() < dt.time(6,30):
            return "Asian (3:30AM–6:30AM)"
        elif dt.time(11,30) <= time.time() < dt.time(14,30):
            return "London Open (11:30AM–2:30PM)"
        elif dt.time(16,30) <= time.time() < dt.time(19,30):
            return "New York Open (4:30PM–7:30PM)"
        elif dt.time(19,30) <= time.time() < dt.time(21,30):
            return "London Close (7:30PM–9:30PM)"
        else:
            return "Non-Killzone"

    if 'Entry Time' in df.columns:
        df['Killzone (IST)'] = df['Entry Time'].apply(get_killzone_label)

    # --- Filters
    st.sidebar.header("🔍 Filters")
    symbol_list = df['Symbol'].unique()
    symbol = st.sidebar.multiselect("Symbol", symbol_list, default=list(symbol_list))
    result_filter = st.sidebar.multiselect("Result", df['Result'].unique(), default=list(df['Result'].unique()))

    df_filtered = df[(df['Symbol'].isin(symbol)) & (df['Result'].isin(result_filter))]

    # --- Equity Curve
    st.subheader("📈 Equity Curve")
    if 'Balance' in df_filtered.columns:
        df_filtered['Cumulative PnL'] = df_filtered['Balance'].cumsum()
        st.line_chart(df_filtered['Cumulative PnL'])

    # --- Session Heatmap
    st.subheader("🔥 Session Killzone Heatmap")
    heatmap = df_filtered.groupby('Killzone (IST)').size().reset_index(name='Trades')
    st.dataframe(heatmap)

    # --- Export Data
    st.download_button("📥 Export Filtered Data", data=df_filtered.to_csv(index=False), file_name="Filtered_Trades.csv")

    # --- Data Table
    st.subheader("📋 Trade Data")
    st.dataframe(df_filtered)

else:
    st.info("Please upload your Excel trade log file to begin.")
