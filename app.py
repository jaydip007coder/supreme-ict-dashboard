import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

# --- Load Data ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("your_trades.csv")  # Replace with your actual file
        df.columns = df.columns.str.strip().str.title()
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = load_data()

# --- Sidebar ---
st.sidebar.title("📊 Dashboard Filters")
st.sidebar.markdown("---")

# Theme Toggle
theme_toggle = st.sidebar.radio("🌗 Theme", ["Light", "Dark"])

# Filter Controls
symbol_list = df['Symbol'].unique() if not df.empty else []
selected_symbols = st.sidebar.multiselect("Select Symbol(s)", symbol_list, default=symbol_list)
session_options = ['Asian', 'London', 'New York', 'Post-News', 'Non-Killzone']
selected_sessions = st.sidebar.multiselect("Select Session(s)", session_options, default=session_options)
outcomes = df['Outcome'].unique() if not df.empty else []
selected_outcomes = st.sidebar.multiselect("Select Outcome(s)", outcomes, default=outcomes)

# Date Range
if not df.empty:
    df['Date'] = pd.to_datetime(df['Date'])
    min_date, max_date = df['Date'].min(), df['Date'].max()
    date_range = st.sidebar.date_input("📅 Date Range", [min_date, max_date])
else:
    date_range = [datetime.date.today(), datetime.date.today()]

st.sidebar.markdown("---")
st.sidebar.markdown("🔁 [Export PDF] | [Export Excel]")

# --- Main Header ---
st.title("💥 Supreme ICT Trade Dashboard")
st.markdown("Use filters from the sidebar to dynamically update the visuals below.")
st.markdown("---")

# --- Filtered Data ---
if not df.empty:
    df_filtered = df[
        (df['Symbol'].isin(selected_symbols)) &
        (df['Session'].isin(selected_sessions)) &
        (df['Outcome'].isin(selected_outcomes)) &
        (df['Date'] >= pd.to_datetime(date_range[0])) &
        (df['Date'] <= pd.to_datetime(date_range[1]))
    ]
else:
    df_filtered = pd.DataFrame()

# --- Summary Row ---
st.subheader("📌 Trade Summary")
if not df_filtered.empty:
    st.write(f"**Total Trades:** {len(df_filtered)}")
    st.write(f"**Win Rate:** {round((df_filtered['Outcome'] == 'Win').mean() * 100, 2)}%")
else:
    st.warning("No trades to show. Adjust filters.")

# --- Charts Section ---
st.subheader("📈 Equity Curve & PnL Chart")
st.plotly_chart(px.line(df_filtered, x='Date', y='Equity', title='Equity Curve'), use_container_width=True)

st.subheader("📊 Setup Tag vs. PnL Matrix")
st.plotly_chart(px.bar(df_filtered, x='Setup', y='Profit', color='Outcome', title='Setup Performance'), use_container_width=True)

# --- Psychology Tracker ---
st.subheader("🧠 Psychology Tracker")
if 'Psych_Notes' in df_filtered.columns:
    for idx, row in df_filtered.iterrows():
        with st.expander(f"📝 {row['Date'].date()} – {row['Symbol']}"):
            st.write(row.get('Psych_Notes', "No notes"))

# --- Screenshot Upload System ---
st.subheader("📸 Trade Screenshot Viewer")
if 'Screenshot_Link' in df_filtered.columns:
    for idx, row in df_filtered.iterrows():
        if pd.notna(row['Screenshot_Link']):
            st.markdown(f"**{row['Date'].date()} – {row['Symbol']}**")
            st.image(row['Screenshot_Link'], use_column_width=True)

# --- Footer ---
st.markdown("---")
st.markdown("🧪 *Supreme ICT Dashboard v2.0 – Streamlit Edition*")
