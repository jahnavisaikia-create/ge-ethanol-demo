import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import pydeck as pdk
from datetime import datetime

# Set up browser tab title and wide executive layout
st.set_page_config(page_title="GE Global Ethanol Intelligence Dashboard", layout="wide")

# --- MOCK DATA GENERATION (Brazil Focus for Phase 1) ---
@st.cache_data
def load_mock_data():
    plants = [
        {"Plant Name": "Unid. Barra", "Company": "Raízen", "Parent Group": "Cosan & Shell", "State": "São Paulo", "City": "Barra Bonita", "Lat": -22.4042, "Lon": -48.5564, "Status": "Operating", "Capacity": 180, "Feedstock": "Sugarcane Bagasse", "Start Year": 2004},
        {"Plant Name": "Unid. Maracaí", "Company": "Raízen", "Parent Group": "Cosan & Shell", "State": "São Paulo", "City": "Maracaí", "Lat": -22.6124, "Lon": -50.6345, "Status": "Operating", "Capacity": 120, "Feedstock": "Sugarcane Bagasse", "Start Year": 2008},
        {"Plant Name": "Unid. Gasa", "Company": "Raízen", "Parent Group": "Cosan & Shell", "State": "São Paulo", "City": "Andradina", "Lat": -20.8961, "Lon": -51.3794, "Status": "Capacity Expanded (+15%)", "Capacity": 95, "Feedstock": "Sugarcane Bagasse", "Start Year": 2003},
        {"Plant Name": "Sinop Biofuel Plant", "Company": "Inpasa", "Parent Group": "Inpasa Brasil", "State": "Mato Grosso", "City": "Sinop", "Lat": -11.8541, "Lon": -55.5085, "Status": "Planned/Under Construction", "Capacity": 400, "Feedstock": "Corn", "Start Year": 2026},
        {"Plant Name": "Boa Vista Biorefinery", "Company": "São Martinho", "Parent Group": "São Martinho Group", "State": "Goiás", "City": "Quirinópolis", "Lat": -18.4483, "Lon": -50.4514, "Status": "Closed", "Capacity": 50, "Feedstock": "Sugarcane Bagasse", "Start Year": 2012}
    ]
    return pd.DataFrame(plants)

df = load_mock_data()

# --- SIDEBAR NAVIGATION PANEL ---
st.sidebar.title("🧭 Navigation Hub")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Go To Module:",
    [
        "🏠 Home / Workflow Overview",
        "🗺️ Geospatial Intelligence Map",
        "🔍 Automated Research & Extraction Hub",
        "🖥️ Human-in-the-Loop Review Queue",
        "🔔 Maintenance Alerts & Lifecycle"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("**Project Scope Flags:**\n- Target Country: Brazil 🇧🇷\n- Window: 2003 - 2026\n- Target Metrics: 33 Attributes")

# ==========================================
# PAGE 1: HOME (THE GLOW-UP UPGRADE)
# ==========================================
if page == "🏠 Home / Workflow Overview":
    # Executive Top Banner Layout
    st.title("⚡ Global Ethanol Production Intelligence Hub")
    st.subheader("Automated Asset Discovery, HITL Verification & Maintenance Framework")
    st.markdown("---")
    
    # 🌟 NEW VISUAL FIX: High-Impact Operations Dashboard Cards
    st.markdown("### 📊 Operational Queue Health Status")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.info("📂 **Total Located Assets**\n## 5 Plants")
        st.caption("Active Phase 1 Scope: Brazil")
    with col2:
        st.warning("⏳ **Pending Review**\n## 2 Plants")
        st.caption("Awaiting Analyst Validation")
    with col3:
        st.success("✅ **Verified Assets**\n## 3 Plants")
        st.caption("100% Precise Match Profile")
    with col4:
        st.error("🚨 **Active Lifecycle Alerts**\n## 1 Alert")
        st.caption("Capacity Shift Flag Triggered")

    st.markdown("---")
    
    # Split Layout for Core Workflow & Data Visualization Tracking
    col_left, col_right = st.columns([3, 2])
    
    with col_left:
        st.markdown("### ⚙️ Pipeline Integration Blueprint")
        
        with st.container(border=True):
            st.markdown("#### 🤖 1. Automated Machine Learning Discovery")
            st.write("Background scraping protocols monitor public enterprise directories, regulatory updates, and global news indices to flag newly commissioned, planned, or updating ethanol facilities.")
            
        with st.container(border=True):
            st.markdown("#### 🖥️ 2. Human-In-The-Loop (HITL) Verification")
            st.write("To satisfy absolute correctness constraints, analysts evaluate auto-extracted entity attributes against real-time side-by-side original documentation snippets before committing logs to production.")
            
        with st.container(border=True):
            st.markdown("#### 🔔 3. 3-Year Strategic Continuous Maintenance")
            st.write("Automated delta-checks process spatial and quantitative variations (decommissioning events, facility growth adjustments) to issue urgent analyst dashboard warnings.")

    with col_right:
        st.markdown("### 🗺️ Project Execution Roadmap")
        
        # 🌟 NEW VISUAL FIX: Interactive Phase Chart demonstrating immediate deployment vs expansion targets
        roadmap_data = pd.DataFrame({
            "Market Horizon Target": ["Phase 1: Brazil (Months 1-2)", "Phase 2: United States", "Phase 3: EU & Asian Markets"],
            "Target Asset Target Coverage (%)": [100, 0, 0],
            "Operational Focus Status": ["Active Alpha Build", "Pipeline Backlog", "Pipeline Backlog"]
        })
        
        fig = px.bar(
            roadmap_data, 
            y="Market Horizon Target", 
            x="Target Asset Target Coverage (%)", 
            color="Operational Focus Status",
            orientation="h",
            color_discrete_map={"Active Alpha Build": "#2ecc71", "Pipeline Backlog": "#7f8c8d"},
            title="Deployment Velocity Timeline Track"
        )
        fig.update_layout(xaxis_range=[0, 100], height=280, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### 📋 33 Metric Verification Coverage")
        with st.expander("🔍 View Required Data Category Partitions"):
            st.markdown("""
            * **Asset Identity:** Name, Operating Owner, Parent Entity, Status
            * **Geographic Profile:** Lat, Long Coordinates (Google Maps verification)
            * **Capacity Matrix:** Nameplate, Engineering Design, Normalized Scale Capacity
            * **Feedstocks:** Input Mix Breakdown, Byproduct Yield Profile, Efficiency Coefficients
            """)

# ==========================================
# PAGE 2: GEOSPATIAL INTELLIGENCE MAP
# ==========================================
elif page == "🗺️ Geospatial Intelligence Map":
    st.title("🗺️ Geospatial Intelligence Map")
    st.subheader("Phase 1 Production Target Tracking: Brazil Clusters")
    
    df['radius'] = df['Capacity'] * 200  
    
    def get_color(status):
        if status == "Operating": return [46, 204, 113, 200]
        elif status == "Closed": return [231, 76, 60, 200]
        else: return [241, 196, 15, 200]
        
    df['color'] = df['Status'].apply(get_color)
    
    layer = pdk.Layer(
        "ScatterplotLayer",
        df,
        get_position=["Lon", "Lat"],
        get_color="color",
        get_radius="radius",
        pickable=True,
    )
    
    view_state = pdk.ViewState(latitude=-18.0, longitude=-48.0, zoom=4, pitch=0)
    
    r = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "{Plant Name}\nCompany: {Company}\nStatus: {Status}\nCapacity: {Capacity}M Liters/Yr"})
    st.pydeck_chart(r)
    
    st.markdown("💡 *Map Legend: **Green** = Operational | **Yellow** = Planned/Under Construction | **Red** = Closed/Decommissioned (Circle scales with Production Capacity Volume)*")
    st.dataframe(df[["Plant Name", "Company", "State", "Status", "Capacity", "Feedstock"]])

# ==========================================
# PAGE 3: AUTOMATED RESEARCH HUB
# ==========================================
elif page == "🔍 Automated Research & Extraction Hub":
    st.title("🔍 Automated Research & Extraction Hub")
    
    country_sel = st.selectbox("Select Target Deployment Market Region:", ["Brazil", "India", "United States"])
    
    if st.button("Trigger Automated AI Web Scraper Engine"):
        with st.spinner("Scouting company portals, regional news indices, and government registries..."):
            st.success(f"AI Search Complete for {country_sel}! Populating Extraction Queue below.")
            
    st.markdown("### Staged Raw Source Data Available for Parsing:")
    st.code("""
    [Source Index Match ID #81023]
    URL: https://www.bloomberg.com/news/articles/brazil-biofuel-expansion-raizen
    Text Segment Saved: 'Raízen Group executing capacity build-out at Andradina cluster, targeting a structured output expansion adjustment...'
    Confidence Score: 94.2%
    """)

# ==========================================
# PAGE 4: HUMAN-IN-THE-LOOP (HITL) QUEUE
# ==========================================
elif page == "🖥️ Human-in-the-Loop Review Queue":
    st.title("🖥️ Analyst Split-Screen Verification Queue")
    st.subheader("Human-In-The-Loop (HITL) 100% Precision Data Verification Layout")
    
    left_pane, right_pane = st.columns(2)
    
    with left_pane:
        st.subheader("📄 Raw Text Source Documents")
        st.info("""
        **Document Excerpt from Bloomberg Industrial Index:**
        
        "Raízen's Gasa facility near Andradina, São Paulo, has logged structural optimizations. The company website confirms an adjustment to the original design layout, expanding baseline capacity by roughly 15% to hit an effective production capability of 95 Million Liters per year..."
        """)
        st.caption("Source URL Match: https://www.bloomberg.com/news/articles/brazil-biofuel-expansion-raizen")
        
        st.markdown("### 🧮 Methodology Standards Engine")
        st.info("Dynamic calibration applied per standard operating procedure rules:")
        st.latex(r"Capacity_{Effective} = Capacity_{Design} \times \text{Energy Density Scale Factor}")
        
    with right_pane:
        st.subheader("📝 AI-Extracted Framework (33 Attributes)")
        
        with st.form("hitl_form"):
            with st.accordion("📋 Section A: Asset Identification Profile", expanded=True):
                p_name = st.text_input("Project Name (Attribute #1)", value="Unid. Gasa")
                p_comp = st.text_input("Operating Company (Attribute #2)", value="Raízen")
                p_parent = st.text_input("Parent Group (Attribute #3)", value="Cosan & Shell")
                
            with st.accordion("🗺️ Section B: Geospatial Coordinates (Google Maps)", expanded=False):
                p_lat = st.text_input("Latitude (Attribute #6)", value="-20.8961")
                p_lon = st.text_input("Longitude (Attribute #7)", value="-51.3794")
                
            with st.accordion("⚙️ Section C: Technical Production Capacities", expanded=False):
                p_status = st.selectbox("Operational Status (Attribute #11)", ["Operating", "Planned", "Capacity Expanded (+15%)", "Closed"], index=2)
                p_cap = st.number_input("Effective Annual Capacity in M Liters/Yr (Attribute #15)", value=95)
                
            with st.accordion("🌾 Section D: Feedstock Material Profile & Byproducts", expanded=False):
                p_feed = st.text_input("Feedstock Raw Material (Attribute #22)", value="Sugarcane Bagasse")
                p_byprod = st.text_input("Primary Generated Byproduct (Attribute #25)", value="Evinasse Bio-Compost")
            
            submit = st.form_submit_button("Verify & Push to Production Database")
            if submit:
                st.balloons()
                st.success("Asset Data Verified Successfully! Logged to Client Template Sheet.")

    st.markdown("---")
    st.subheader("📥 Export Finalized Verification Delivery Documents")
    
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M")
    export_filename = f"Brazil_{len(df)}_Projects_{timestamp_str}_FinalReport.csv"
    csv_data = df[["Plant Name", "Company", "Parent Group", "State", "Status", "Capacity", "Feedstock"]].to_csv(index=False)
    
    st.download_button(
        label="Download Generated Spreadsheet Template (.CSV)",
        data=csv_data,
        file_name=export_filename,
        mime="text/csv"
    )
    st.caption(f"Target Output Pattern Generated: `{export_filename}`")

# ==========================================
# PAGE 5: MAINTENANCE & LIFECYCLE ALERTS
# ==========================================
elif page == "🔔 Maintenance Alerts & Lifecycle":
    st.title("🔔 Asset Lifecycle Maintenance Engine")
    st.subheader("Dynamic Delta Notifications & Status Alarm Rules")
    
    st.markdown("The maintenance script evaluates live web sources to map operational changes against historical asset profiles.")
    
    st.warning("""
    ⚠️ **System Delta Warning Flag Alert (ID: #AL-90182)**
    * **Asset:** Unid. Gasa Plant (Operating Company: Raízen)
    * **Trigger Condition Detect Event:** 15% Capacity change detected via newly published Corporate Sustainability Report.
    * **Action Required:** Analyst validation review missing in verified production schema.
    """)
    
    col_a, col_b = st.columns(2)
    if col_a.button("Open Operational Override Verification Window"):
        st.info("Routing process to HITL Screen...")
    if col_b.button("Dismiss System Status Warning Flag"):
        st.success("Alert dismissed.")
