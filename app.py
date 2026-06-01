import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. MOCK DATA GENERATOR ---
# In a real app, this would load from your verified database/CSV
def load_mock_data():
    data = [
        {"Plant Name": "Raízen Costa Pinto", "State": "SP", "Lat": -22.70, "Long": -47.64, "Status": "Active", "Capacity": 600000, "Year": 2003},
        {"Plant Name": "FS Bioenergia Lucas", "State": "MT", "Lat": -13.06, "Long": -55.91, "Status": "Active", "Capacity": 530000, "Year": 2017},
        {"Plant Name": "São Martinho Usina", "State": "SP", "Lat": -21.31, "Long": -48.11, "Status": "Active", "Capacity": 700000, "Year": 2005},
        {"Plant Name": "Inpasa Sinop", "State": "MT", "Lat": -11.85, "Long": -55.50, "Status": "Active", "Capacity": 800000, "Year": 2019},
        {"Plant Name": "Arezzo Ethanol Project", "State": "GO", "Lat": -17.92, "Long": -51.72, "Status": "Under Construction", "Capacity": 300000, "Year": 2024},
        {"Plant Name": "Neomille Maracaju", "State": "MS", "Lat": -21.61, "Long": -55.16, "Status": "Planned", "Capacity": 450000, "Year": 2025},
        {"Plant Name": "Cerradinho Bio", "State": "GO", "Lat": -17.88, "Long": -51.71, "Status": "Active", "Capacity": 400000, "Year": 2011},
        {"Plant Name": "Albioma Solar-Eth", "State": "MT", "Lat": -15.60, "Long": -56.09, "Status": "Planned", "Capacity": 200000, "Year": 2026},
    ]
    return pd.DataFrame(data)

# --- 2. PAGE CONFIG ---
st.set_page_config(layout="wide", page_title="Brazil Ethanol Map 2003-2026")

st.title("🌎 Global Ethanol Tracker: Brazil Dashboard")
st.markdown("### Visualization of Active, Planned, and Under Construction Plants (2003 - 2026)")

# --- 3. SIDEBAR FILTERS ---
st.sidebar.header("Filter Options")

# Year Slider
year_range = st.sidebar.slider(
    "Select Operational Year Range",
    min_value=2003,
    max_value=2026,
    value=(2003, 2026)
)

# Status Filter
status_options = ["Active", "Planned", "Under Construction"]
selected_status = st.sidebar.multiselect("Plant Status", status_options, default=status_options)

# Load and Filter Data
df = load_mock_data()
filtered_df = df[
    (df['Year'] >= year_range[0]) & 
    (df['Year'] <= year_range[1]) & 
    (df['Status'].isin(selected_status))
]

# --- 4. KPI METRICS ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Plants", len(filtered_df))
col2.metric("Total Capacity (m3/y)", f"{filtered_df['Capacity'].sum():,}")
col3.metric("Active Plants", len(filtered_df[filtered_df['Status'] == 'Active']))
col4.metric("Pipeline (Planned/UC)", len(filtered_df[filtered_df['Status'] != 'Active']))

# --- 5. MAP VISUALIZATION (PLOTLY) ---
st.subheader("Interactive Plant Geography")

if not filtered_df.empty:
    fig = px.scatter_mapbox(
        filtered_df,
        lat="Lat",
        lon="Long",
        size="Capacity",
        color="Status",
        hover_name="Plant Name",
        hover_data={"Lat": False, "Long": False, "Capacity": True, "Year": True},
        color_discrete_map={
            "Active": "#2ecc71",            # Green
            "Under Construction": "#f1c40f", # Yellow
            "Planned": "#e67e22"             # Orange
        },
        zoom=3.5,
        height=600,
        center={"lat": -15.79, "lon": -47.88} # Focused on Brazil
    )

    # Styling the Map
    fig.update_layout(
        mapbox_style="carto-darkmatter", # High-contrast professional look
        margin={"r":0,"t":0,"l":0,"b":0},
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No plants match the selected filters.")

# --- 6. DATA TABLE ---
st.subheader("Verified Plant Details")
st.dataframe(filtered_df.sort_values(by="Year", ascending=False), use_container_width=True)

# --- 7. EXPORT BUTTON ---
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📂 Export Filtered Data to Template",
    data=csv,
    file_name="brazil_ethanol_tracker.csv",
    mime="text/csv",
)
