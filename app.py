import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import pydeck as pdk
from datetime import datetime
import time

# --- FORTUNE 500 EXECUTIVE CONFIGURATION ---
st.set_page_config(
    page_title="GE Global Ethanol Intelligence Command Center", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SYSTEM STYLES & CONTAINER ALIGNMENT ---
st.markdown("""
<style>
    .reportview-container { background: #f5f7f9; }
    .main-header { font-size: 2.2rem; font-weight: 800; color: #1e293b; margin-bottom: 0.5rem; }
    .sub-header { font-size: 1.1rem; color: #64748b; margin-bottom: 2rem; }
    .card-title { font-size: 1.2rem; font-weight: 700; color: #0f172a; }
</style>
""", unsafe_allow_html=True)

# --- GLOBAL DATABASE MEMORY INITIALIZATION ---
if "production_db" not in st.session_state:
    st.session_state.production_db = pd.DataFrame([
        {"Plant Name": "Unid. Barra", "Company": "Raízen", "Parent Group": "Cosan & Shell", "State": "São Paulo", "City": "Barra Bonita", "Lat": -22.4042, "Lon": -48.5564, "Status": "Operating", "Capacity": 180, "Feedstock": "Sugarcane Bagasse", "Start Year": 2004, "Verification Date": "2026-05-15"},
        {"Plant Name": "Unid. Maracaí", "Company": "Raízen", "Parent Group": "Cosan & Shell", "State": "São Paulo", "City": "Maracaí", "Lat": -22.6124, "Lon": -50.6345, "Status": "Operating", "Capacity": 120, "Feedstock": "Sugarcane Bagasse", "Start Year": 2008, "Verification Date": "2026-05-20"},
        {"Plant Name": "Boa Vista Biorefinery", "Company": "São Martinho", "Parent Group": "São Martinho Group", "State": "Goiás", "City": "Quirinópolis", "Lat": -18.4483, "Lon": -50.4514, "Status": "Closed", "Capacity": 50, "Feedstock": "Sugarcane Bagasse", "Start Year": 2012, "Verification Date": "2026-05-28"}
    ])

if "pending_queue" not in st.session_state:
    st.session_state.pending_queue = [
        {"Plant Name": "Unid. Gasa", "Company": "Raízen", "Parent Group": "Cosan & Shell", "State": "São Paulo", "City": "Andradina", "Lat": -20.8961, "Lon": -51.3794, "Status": "Capacity Expanded (+15%)", "Capacity": 95, "Feedstock": "Sugarcane Bagasse", "Start Year": 2003, "Confidence": 94.2, "Source": "Bloomberg Industrial Index", "ExtractDate": "2026-06-01"},
        {"Plant Name": "Sinop Biofuel Plant", "Company": "Inpasa", "Parent Group": "Inpasa Brasil", "State": "Mato Grosso", "City": "Sinop", "Lat": -11.8541, "Lon": -55.5085, "Status": "Planned/Under Construction", "Capacity": 400, "Feedstock": "Corn", "Start Year": 2026, "Confidence": 89.7, "Source": "Mato Grosso Regional Registry", "ExtractDate": "2026-06-01"}
    ]

if "scraper_triggered" not in st.session_state:
    st.session_state.scraper_triggered = False

if "alerts_active" not in st.session_state:
    st.session_state.alerts_active = 1

# --- SIDEBAR COMPONENT ---
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
st.sidebar.markdown("### 🛠️ Simulation Settings")
if st.sidebar.button("Reset Staging Environment Databases", use_container_width=True):
    st.session_state.clear()
    st.rerun()

# --- REUSABLE PERSISTENT EXECUTIVE HEADER BLOCK ---
def render_executive_header(title, subtitle):
    st.markdown(f'<div class="main-header">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-header">{subtitle}</div>', unsafe_allow_html=True)
    st.sidebar.markdown("---")
    
# ==========================================
# PAGE 1: HOME
# ==========================================
if page == "🏠 Home / Workflow Overview":
    render_executive_header("⚡ Global Ethanol Production Intelligence Hub", "Enterprise Asset Tracking, Automated NLP Data Extraction & Verification System")
    
    # KPI Display Blocks
    st.markdown("### 📊 Platform Metrics & Operational Health Status")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Verified Assets (Production)", f"{len(st.session_state.production_db)} Plants", delta="Active Master Assets")
    with col2:
        st.metric("Pending Verification", f"{len(st.session_state.pending_queue)} Plants", delta="-1 Resolved", delta_color="inverse")
    with col3:
        st.metric("Total System Records Discovered", len(st.session_state.production_db) + len(st.session_state.pending_queue))
    with col4:
        st.metric("Active Maintenance Anomalies", f"{st.session_state.alerts_active} Flags", delta="Action Required", delta_color="off")

    st.markdown("---")
    
    col_left, col_right = st.columns([3, 2])
    
    with col_left:
        st.markdown("### 🏗️ Integrated Data Pipeline Process Architecture")
        
        c1 = st.container(border=True)
        c1.markdown("#### 🤖 1. Automated Machine Learning Discovery")
        c1.write("Background scraping protocols and entity extraction pipelines continuously monitor global corporate portals, investor decks, regulatory indices, and regional news to map newly planned, built, or modified assets.")
        
        c2 = st.container(border=True)
        c2.markdown("#### 🖥️ 2. Human-In-The-Loop (HITL) Verification Matrix")
        c2.write("To preserve 100% data fidelity constraints required for commercial deployment, structured data records are staged inside a secure review environment where data engineers cross-validate fields side-by-side with source text.")
        
        c3 = st.container(border=True)
        c3.markdown("#### 🔔 3. Continuous Strategic Maintenance Engine")
        c3.write("Post-verification assets undergo continuous evaluation. Automated baseline delta engines flag capacity modifications or plant closures across a 3-year timeline horizon.")

    with col_right:
        st.markdown("### 🎯 Verification Horizon Roadmap")
        total_scope = len(st.session_state.production_db) + len(st.session_state.pending_queue)
        progress_val = int((len(st.session_state.production_db) / total_scope) * 100) if total_scope > 0 else 100
        
        roadmap_data = pd.DataFrame({
            "Market Target Region": ["Phase 1: Brazil Data Processing", "Phase 2: United States Infrastructure", "Phase 3: EU & Asian Expansion"],
            "Target Operational Progress (%)": [progress_val, 0, 0]
        })
        
        fig = px.bar(
            roadmap_data, 
            y="Market Target Region", 
            x="Target Operational Progress (%)", 
            orientation="h",
            color_discrete_sequence=["#0284c7"],
            text="Target Operational Progress (%)"
        )
        fig.update_layout(xaxis_range=[0, 100], height=240, margin=dict(t=10, b=10, l=10, r=10))
        st.plotly_chart(fig, use_container_width=True)
        
        # 33-Attribute Context Block
        st.markdown("### 📋 33 Metric Parameter Scope Matrix")
        with st.expander("Expand Global Template Attribute Profiles", expanded=False):
            st.markdown("""
            * **Identification Logs:** Project Registry Name, Operating Entity Owner, Parent Strategic Group, Flagged Status.
            * **Geospatial Tracking:** Latitude, Longitude, City Boundaries, Regional State Classification.
            * **Capacity Profiles:** Nameplate Structural Output, Design Capacity Framework, Standardized Effective Annual Volume.
            * **Feedstock Matrices:** Raw Input Mix Profiles, Coproduct/Byproduct Output Scales, Factory Production Coefficients.
            """)

# ==========================================
# PAGE 2: GEOSPATIAL INTELLIGENCE MAP
# ==========================================
elif page == "🗺️ Geospatial Intelligence Map":
    render_executive_header("🗺️ Geospatial Intelligence Engine Map", "Phase 1 High-Density Production Asset Clusters Location Mapping")
    
    map_df = st.session_state.production_db.copy()
    
    if map_df.empty:
        st.warning("No validated records currently present in production data structures. Route to the HITL Queue to commit entries.")
    else:
        # Scale mapping points dynamically to visual display volumes
        map_df['radius'] = map_df['Capacity'] * 150  
        
        def get_color(status):
            if status == "Operating": return [14, 165, 233, 220]      # Deep Cyan Sky
            elif status == "Closed": return [239, 68, 68, 220]       # Alert Red
            else: return [245, 158, 11, 220]                         # Amber Alert
            
        map_df['color'] = map_df['Status'].apply(get_color)
        
        # Build premium Pydeck Layer
        layer = pdk.Layer(
            "ScatterplotLayer",
            map_df,
            get_position=["Lon", "Lat"],
            get_color="color",
            get_radius="radius",
            pickable=True,
        )
        
        view_state = pdk.ViewState(latitude=-18.0, longitude=-48.0, zoom=4, pitch=15)
        
        r = pdk.Deck(
            layers=[layer], 
            initial_view_state=view_state, 
            map_style="mapbox://styles/mapbox/light-v9",
            tooltip={"text": "Plant: {Plant Name}\nOperator: {Company}\nStatus: {Status}\nVerified Capacity: {Capacity}M Liters/Yr"}
        )
        
        st.pydeck_chart(r)
        st.markdown("💡 *Spatial Mapping Legend: **Blue Points** = Verified Operating Assets | **Yellow Points** = Infrastructure Change/Planned | **Red Points** = Decommissioned/Closed*")
        
        st.markdown("### 📋 Production Registry Matrix")
        st.dataframe(map_df[["Plant Name", "Company", "Parent Group", "State", "Status", "Capacity", "Feedstock", "Verification Date"]], use_container_width=True)

# ==========================================
# PAGE 3: AUTOMATED RESEARCH HUB
# ==========================================
elif page == "🔍 Automated Research & Extraction Hub":
    render_executive_header("🔍 Automated AI Discovery & NLP Extraction Center", "Machine Learning Web Scraping Processing Interfaces & Raw Telemetry Output")
    
    col_control, col_console = st.columns([1, 2])
    
    with col_control:
        st.markdown("#### 🎛️ Execution Controls")
        country_sel = st.selectbox("Select Target Deployment Market Context:", ["Brazil Regional Scope (Phase 1)", "India Regional Scope", "United States Scope"])
        source_filter = st.multiselect("Allowed Scraping Protocols:", ["Enterprise Websites", "Regulatory Registries", "Bloomberg RSS Directories", "Government Gazettes"], default=["Enterprise Websites", "Bloomberg RSS Directories"])
        
        trigger_btn = st.button("Launch Extraction Sequence Pipeline", use_container_width=True, type="primary")
        if trigger_btn:
            st.session_state.scraper_triggered = True
            
    with col_console:
        st.markdown("#### 🖥️ ML Processing Terminal Console Logs")
        if st.session_state.scraper_triggered:
            placeholder = st.empty()
            with placeholder.container():
                st.code("System Initializing internal scraping worker arrays... OK\nDeploying isolated network routing keys... OK\nQuerying Raízen Group corporate sustainability indices...")
            time.sleep(0.5)
            with placeholder.container():
                st.code("Payload Target Matches Identified: ID #81023\nDownloading asset data string matrices...\nParsing structural string layout using text analytics v2.4...")
            time.sleep(0.5)
            with placeholder.container():
                st.code("Parsing complete. Document layout elements successfully extracted:\n -> Target Plant: Unid. Gasa\n -> Mapped Metric Fields: 33/33 Attributes Parsed\n -> Algorithmic Match Confidence: 94.2%\n[Pipeline Notification]: Moving unverified records to staging queue.")
            st.success("Web crawler execution loop successfully concluded. Records transferred to validation workspaces.")
        else:
            st.info("System Engine idling. Execute 'Launch Extraction Sequence Pipeline' to begin processing live web scrapers.")

    st.markdown("---")
    st.markdown("### 📥 Extracted Pipeline Payload Fields (Awaiting Analyst HITL Check)")
    
    if len(st.session_state.pending_queue) == 0:
        st.success("🎉 Staging environment cleared. All discovered records successfully verified and pushed to master production.")
    else:
        pending_df = pd.DataFrame(st.session_state.pending_queue)
        st.dataframe(pending_df[["Plant Name", "Company", "Source", "Confidence", "Status", "Capacity", "ExtractDate"]], use_container_width=True)

# ==========================================
# PAGE 4: HUMAN-IN-THE-LOOP (HITL) QUEUE
# ==========================================
elif page == "🖥️ Human-in-the-Loop Review Queue":
    render_executive_header("🖥️ Human-In-The-Loop Data Validation Interface", "100% Data Fidelity Verification Environment for Senior Corporate Leadership Validation")
    
    if len(st.session_state.pending_queue) == 0:
        st.balloons()
        st.success("🎉 **Validation Queue Completely Clear!** All discovered industrial assets are safely locked to production databases and active across the interactive map layouts.")
    else:
        current_target = st.session_state.pending_queue[0]
        
        st.warning(f"👉 **Awaiting Action:** Evaluating Extraction Target Record **1 of {len(st.session_state.pending_queue)}**: **{current_target['Plant Name']}** (AI Parsing Match Confidence Value: {current_target['Confidence']}%)")
        
        left_pane, right_pane = st.columns(2)
        
        with left_pane:
            st.markdown("#### 📄 Original Raw Source Excerpt")
            st.info(f"""
            **Document Excerpt Source Reference ({current_target['Source']}):**
            
            "The corporate engineering registries for cluster assets detail significant structural expansions. The operating management firm, {current_target['Company']}, has approved capital project layouts. Historical metrics verify an immediate modification to spatial design criteria, increasing active nameplate production capacity metrics to achieve an effective annual baseline yield capability of {current_target['Capacity']} Million Liters per annum..."
            """)
            st.caption("Primary Reference Source Track URL String: https://www.bloomberg.com/news/articles/brazil-biofuel-expansion-raizen")
            
            # Formatted engineering mathematical calibration formula
            st.markdown("#### 🧮 Normalized Capacity Verification Standard Rules")
            st.info("System conversion factor models match baseline standard operating procedure requirements:")
            st.latex(r"Capacity_{Effective} = Capacity_{Design} \times \text{Energy Density Scale Factor}")
            st.caption("Mathematical Rule Applied: Volumetric Conversion Baseline Factor v1.2")
            
        with right_pane:
            st.markdown("#### 📝 Verified Enterprise Data Editor Form")
            
            with st.form("hitl_interactive_form"):
                # Clean structural configuration mapping the 33 target fields into functional design workspaces
                tab_id, tab_geo, tab_tech, tab_feed = st.tabs(["📋 Identity Profiles", "🗺️ Geographic Assets", "⚙️ Volumetric Capacities", "🌾 Feedstocks & Inputs"])
                
                with tab_id:
                    form_name = st.text_input("Project Factory Registration Name (Field #1)", value=current_target["Plant Name"])
                    form_company = st.text_input("Primary Operating Management Entity (Field #2)", value=current_target["Company"])
                    form_parent = st.text_input("Parent Corporate Umbrella Group (Field #3)", value=current_target["Parent Group"])
                    
                with tab_geo:
                    form_lat = st.text_input("Verified Latitude Node (Field #6)", value=str(current_target["Lat"]))
                    form_lon = st.text_input("Verified Longitude Node (Field #7)", value=str(current_target["Lon"]))
                    form_city = st.text_input("Target City Boundaries (Field #5)", value=current_target["City"])
                    form_state = st.text_input("Regional State Classification (Field #4)", value=current_target["State"])
                    
                with tab_tech:
                    form_status = st.selectbox("Active Operational Pipeline Status (Field #11)", ["Operating", "Planned/Under Construction", "Capacity Expanded (+15%)", "Closed"], index=2)
                    form_capacity = st.number_input("Standardized Normalized Capacity Volume [M Liters/Yr] (Field #15)", value=current_target["Capacity"])
                    form_year = st.number_input("Operational Asset Construction Launch Year (Field #12)", value=current_target["Start Year"])
                    
                with tab_feed:
                    form_feedstock = st.text_input("Feedstock Biomass Input Mix Profile (Field #22)", value=current_target["Feedstock"])
                    form_byprod = st.text_input("Primary Coproduct/Byproduct Stream Profile (Field #25)", value="Vinasse Bio-Compost Base")
                
                submit_verification = st.form_submit_button("Commit Checked Attributes to Master Database Schema", use_container_width=True)
                
                if submit_verification:
                    validated_record = {
                        "Plant Name": form_name,
                        "Company": form_company,
                        "Parent Group": form_parent,
                        "State": form_state,
                        "City": form_city,
                        "Lat": float(form_lat),
                        "Lon": float(form_lon),
                        "Status": form_status,
                        "Capacity": int(form_capacity),
                        "Feedstock": form_feedstock,
                        "Start Year": int(form_year),
                        "Verification Date": datetime.now().strftime("%Y-%m-%d")
                    }
                    
                    # Run secure memory injection loops across variables
                    st.session_state.production_db = pd.concat([st.session_state.production_db, pd.DataFrame([validated_record])], ignore_index=True)
                    st.session_state.pending_queue.pop(0)
                    
                    st.success(f"Log asset system record '{form_name}' committed to production data architectures. Live components updated.")
                    time.sleep(0.5)
                    st.rerun()

    # Direct spreadsheet compilation export pipeline
    st.markdown("---")
    st.markdown("### 📥 Package Current Delivery Artifact Data Structures")
    
    timestamp_export = datetime.now().strftime("%Y%m%d_%H%M")
    export_filename_string = f"Brazil_{len(st.session_state.production_db)}_Projects_{timestamp_export}_FinalReport.csv"
    csv_payload = st.session_state.production_db[["Plant Name", "Company", "Parent Group", "State", "Status", "Capacity", "Feedstock", "Verification Date"]].to_csv(index=False)
    
    st.download_button(
        label="Download Processed Delivery Matrix Spreadsheet (.CSV Document Target)", 
        data=csv_payload, 
        file_name=export_filename_string, 
        mime="text/csv"
    )
    st.caption(f"Configured Client Template Format Delivery Hook Target: `{export_filename_string}`")

# ==========================================
# PAGE 5: MAINTENANCE & LIFECYCLE ALERTS
# ==========================================
elif page == "🔔 Maintenance Alerts & Lifecycle":
    render_executive_header("🔔 Continuous Baseline Asset Lifecycle Maintenance Engine", "Dynamic Asset Configuration Monitoring & Delta Tracking Anomalies Notifications")
    
    if st.session_state.alerts_active == 0:
        st.success("✅ **Continuous monitoring systems clean.** All production variables line up smoothly against real-time text assets over the active 3-year timeline framework.")
    else:
        st.error("""
        ⚠️ **Active Production Configuration Delta Anomalous Flag (Alert Reference Key: #AL-90182)**
        * **Context Facility:** Unid. Gasa Biorefinery Layout (Operating Owner: Raízen)
        * **Incident Trigger Matrix:** Production output variation (+15%) caught inside a newly cataloged Corporate Annual Financial Release Statement.
        * **System Status:** Live database fields out-of-sync with real-time extracted data streams. Action required.
        """)
        
        col_align, col_dismiss = st.columns(2)
        with col_align:
            resolve_incident = st.button("Authorize Automated Override System Alignment Re-Calibration", use_container_width=True, type="primary")
            if resolve_incident:
                st.session_state.alerts_active = 0
                st.success("Production database elements re-calibrated. Systems checked.")
                time.sleep(0.5)
                st.rerun()
        with col_dismiss:
            if st.button("Dismiss Incident Warning Flag Alert Cache", use_container_width=True):
                st.info("System alarm warning dismissed from tracking dashboard logs.")
