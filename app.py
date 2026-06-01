import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import time

# --- ENTERPRISE LAYOUT SYSTEM ---
st.set_page_config(
    page_title="GE Global Ethanol Intelligence Command Center", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- UNIFIED BRANDING & SYMMETRICAL DESIGN ARCHITECTURE ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; color: #1e293b; }
    
    .executive-header-box {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 2.5rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    }
    .executive-title { font-size: 2.25rem; font-weight: 800; color: #ffffff; margin-bottom: 0.5rem; letter-spacing: -0.025em; }
    .executive-subtitle { font-size: 1.1rem; color: #94a3b8; font-weight: 400; }
    
    .section-title { font-size: 1.35rem; font-weight: 700; color: #0f172a; margin-top: 1.5rem; margin-bottom: 1rem; letter-spacing: -0.01em; border-left: 4px solid #0284c7; padding-left: 0.75rem; }
    
    .metric-card-box {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
        text-align: center;
        height: 100%;
    }
    .metric-label { font-size: 0.85rem; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem; }
    .metric-val-green { font-size: 2rem; font-weight: 800; color: #16a34a; }
    .metric-val-amber { font-size: 2rem; font-weight: 800; color: #d97706; }
    .metric-val-blue { font-size: 2rem; font-weight: 800; color: #2563eb; }
    .metric-val-red { font-size: 2rem; font-weight: 800; color: #dc2626; }
    .metric-caption { font-size: 0.8rem; color: #94a3b8; margin-top: 0.25rem; }

    .pipeline-step-container {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        margin-bottom: 1rem;
    }
    .pipeline-step-header { font-size: 1.05rem; font-weight: 700; color: #1e293b; margin-bottom: 0.5rem; display: flex; align-items: center; }
    .pipeline-step-body { font-size: 0.95rem; color: #475569; line-height: 1.6; text-align: justify; }
    
    div[data-testid="stForm"] {
        border: 1px solid #e2e8f0 !important;
        padding: 2rem !important;
        border-radius: 12px !important;
        background: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# --- GLOBAL DATABASE MEMORY INITIALIZATION ---
if "production_db" not in st.session_state:
    st.session_state.production_db = pd.DataFrame([
        {"Plant Name": "Unid. Barra", "Company": "Raízen", "Parent Group": "Cosan & Shell", "State": "São Paulo", "City": "Barra Bonita", "lat": -22.4042, "lon": -48.5564, "Status": "Operating", "Capacity": 180, "Feedstock": "Sugarcane Bagasse", "Start Year": 2004, "Verification Date": "2026-05-15"},
        {"Plant Name": "Unid. Maracaí", "Company": "Raízen", "Parent Group": "Cosan & Shell", "State": "São Paulo", "City": "Maracaí", "lat": -22.6124, "lon": -50.6345, "Status": "Operating", "Capacity": 120, "Feedstock": "Sugarcane Bagasse", "Start Year": 2008, "Verification Date": "2026-05-20"},
        {"Plant Name": "Boa Vista Biorefinery", "Company": "São Martinho", "Parent Group": "São Martinho Group", "State": "Goiás", "City": "Quirinópolis", "lat": -18.4483, "lon": -50.4514, "Status": "Closed", "Capacity": 50, "Feedstock": "Sugarcane Bagasse", "Start Year": 2012, "Verification Date": "2026-05-28"}
    ])

if "pending_queue" not in st.session_state:
    st.session_state.pending_queue = [
        {"Plant Name": "Unid. Gasa", "Company": "Raízen", "Parent Group": "Cosan & Shell", "State": "São Paulo", "City": "Andradina", "lat": -20.8961, "lon": -51.3794, "Status": "Capacity Expanded (+15%)", "Capacity": 95, "Feedstock": "Sugarcane Bagasse", "Start Year": 2003, "Confidence": 94.2, "Source": "Bloomberg Industrial Index", "ExtractDate": "2026-06-01"},
        {"Plant Name": "Sinop Biofuel Plant", "Company": "Inpasa", "Parent Group": "Inpasa Brasil", "State": "Mato Grosso", "City": "Sinop", "lat": -11.8541, "lon": -55.5085, "Status": "Planned/Under Construction", "Capacity": 400, "Feedstock": "Corn", "Start Year": 2026, "Confidence": 89.7, "Source": "Mato Grosso Regional Registry", "ExtractDate": "2026-06-01"}
    ]

if "scraper_triggered" not in st.session_state:
    st.session_state.scraper_triggered = False

if "alerts_active" not in st.session_state:
    st.session_state.alerts_active = 1

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🧭 Navigation Hub")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Go To Module:",
    [
        "🏠 Home / Workflow Overview",
        "🗺️ Geospatial Intelligence Map",
        "📊 Global Portfolio Analytics",  # Added 6th View Page
        "🔍 Automated Research & Extraction Hub",
        "🖥️ Human-in-the-Loop Review Queue",
        "🔔 Maintenance Alerts & Lifecycle"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎛️ Simulation Controls")
if st.sidebar.button("Reset Global Environment Cache", use_container_width=True):
    st.session_state.clear()
    st.rerun()

def render_executive_panel(title, subtitle):
    st.markdown(f"""
    <div class="executive-header-box">
        <div class="executive-title">{title}</div>
        <div class="executive-subtitle">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# PAGE 1: HOME
# ==========================================
if page == "🏠 Home / Workflow Overview":
    render_executive_panel("Global Ethanol Production Intelligence Hub", "Enterprise Asset Tracking, Automated NLP Data Extraction & Verification System")
    
    st.markdown('<div class="section-title">Platform Metrics & Processing Performance Queue</div>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""<div class="metric-card-box"><div class="metric-label">Verified Master Data</div><div class="metric-val-green">{len(st.session_state.production_db)} Plants</div><div class="metric-caption">Phase 1 Brazil Footprint Scope</div></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="metric-card-box"><div class="metric-label">Staging Area Pending</div><div class="metric-val-amber">{len(st.session_state.pending_queue)} Plants</div><div class="metric-caption">Awaiting Human Analyst Cross-Check</div></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="metric-card-box"><div class="metric-label">Total Pipeline Located</div><div class="metric-val-blue">{len(st.session_state.production_db) + len(st.session_state.pending_queue)} Assets</div><div class="metric-caption">Machine Learning Scraping Matches</div></div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""<div class="metric-card-box"><div class="metric-label">Operational Anomalies</div><div class="metric-val-red">{st.session_state.alerts_active} Flagged</div><div class="metric-caption">Requires Immediate Verification Lifecycle</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_left, col_right = st.columns([1, 1])
    with col_left:
        st.markdown('<div class="section-title">Data Pipeline Functional Blueprint</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="pipeline-step-container">
            <div class="pipeline-step-header">🤖 1. Automated Machine Learning Discovery</div>
            <div class="pipeline-step-body">Background parsing networks crawl decentralized public documents, enterprise filings, and sector indices to isolate production facilities tracking within the 2003–2026 parameters.</div>
        </div>
        <div class="pipeline-step-container">
            <div class="pipeline-step-header">🖥️ 2. Human-In-The-Loop Verification Matrix</div>
            <div class="pipeline-step-body">To satisfy absolute 100% fidelity constraints, data engineers evaluate multi-category entities using high-density interface grids matching against unedited source documentation streams.</div>
        </div>
        <div class="pipeline-step-container">
            <div class="pipeline-step-header">🔔 3. Continuous 3-Year Lifecycle Audits</div>
            <div class="pipeline-step-body">Post-verification records stay monitored. System rules run continuous checks against production profiles to issue immediate flags regarding expansion alerts or plant closure closures.</div>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="section-title">Verification Horizon Progress Target</div>', unsafe_allow_html=True)
        total_scope = len(st.session_state.production_db) + len(st.session_state.pending_queue)
        progress_val = int((len(st.session_state.production_db) / total_scope) * 100) if total_scope > 0 else 100
        
        roadmap_data = pd.DataFrame({
            "Market Horizon Target": ["Phase 1: Brazil Context Scope", "Phase 2: United States Pipeline", "Phase 3: Global Expansion Base"],
            "Operational Progress (%)": [progress_val, 0, 0]
        })
        
        fig = px.bar(roadmap_data, y="Market Horizon Target", x="Operational Progress (%)", orientation="h", color_discrete_sequence=["#0284c7"], text="Operational Progress (%)")
        fig.update_layout(xaxis_range=[0, 100], height=230, margin=dict(t=10, b=10, l=10, r=10), xaxis=dict(title=None, showticklabels=False, showgrid=False), yaxis=dict(title=None))
        st.plotly_chart(fig, use_container_width=True)

# ==========================================
# PAGE 2: GEOSPATIAL INTELLIGENCE MAP
# ==========================================
elif page == "🗺️ Geospatial Intelligence Map":
    render_executive_panel("Geospatial Intelligence Engine Map", "Phase 1 High-Density Production Asset Clusters Location Mapping")
    
    map_df = st.session_state.production_db.copy()
    if map_df.empty:
        st.warning("No validated records currently present in production data structures. Route to the HITL Queue to commit entries.")
    else:
        map_df["Hover Details"] = (
            "🏭 Plant: " + map_df["Plant Name"] + "<br>" +
            "🏢 Company: " + map_df["Company"] + "<br>" +
            "⚡ Capacity: " + map_df["Capacity"].astype(str) + " M Liters/Yr"
        )
        
        fig_map = px.scatter_mapbox(
            map_df, lat="lat", lon="lon", color="Status", size="Capacity", size_max=35,
            color_discrete_map={"Operating": "#2ecc71", "Closed": "#e74c3c", "Capacity Expanded (+15%)": "#f1c40f"},
            hover_name="Plant Name", hover_data={"lat": False, "lon": False, "Status": True, "Capacity": False, "Hover Details": True},
            zoom=4.2
        )
        fig_map.update_layout(mapbox_style="open-street-map", margin=dict(r=0, t=0, l=0, b=0), height=500, showlegend=True)
        st.plotly_chart(fig_map, use_container_width=True)
        
        st.markdown('<div class="section-title">Active Master Production Registry</div>', unsafe_allow_html=True)
        st.dataframe(map_df[["Plant Name", "Company", "Parent Group", "State", "Status", "Capacity", "Feedstock", "Verification Date"]], use_container_width=True)

# ==========================================
# NEW PAGE 3: GLOBAL PORTFOLIO ANALYTICS (EXECUTIVE MACRO-INTELLIGENCE)
# ==========================================
elif page == "📊 Global Portfolio Analytics":
    render_executive_panel("Global Portfolio Analytics Dashboard", "Strategic Macro Intelligence Metrics & Aggregated Field Insights")
    
    # Compile complete combined database profile dynamically
    all_assets_df = pd.concat([st.session_state.production_db, pd.DataFrame(st.session_state.pending_queue)], ignore_index=True)
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown('<div class="section-title">Production Capacity Distribution by Operating Entity</div>', unsafe_allow_html=True)
        fig_company = px.bar(all_assets_df, x="Company", y="Capacity", color="Status", title="Capacity Share (Million Liters/Year)", color_discrete_sequence=px.colors.qualitative.Dark2)
        st.plotly_chart(fig_company, use_container_width=True)
        
    with col_chart2:
        st.markdown('<div class="section-title">Feedstock Biomass Market Share</div>', unsafe_allow_html=True)
        fig_pie = px.pie(all_assets_df, names="Feedstock", values="Capacity", title="Asset Resource Breakdown Matrix", hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)
        
    st.markdown('---')
    st.markdown('<div class="section-title">Asset Horizon Tracking Constraints Checklist (2003 - 2026 Timeline)</div>', unsafe_allow_html=True)
    fig_trend = px.scatter(all_assets_df, x="Start Year", y="Capacity", size="Capacity", color="Status", hover_name="Plant Name", title="Asset Inception Matrix Filters Validation Loop View")
    fig_trend.update_layout(xaxis_range=[2002, 2027])
    st.plotly_chart(fig_trend, use_container_width=True)

# ==========================================
# PAGE 4: AUTOMATED RESEARCH HUB
# ==========================================
elif page == "🔍 Automated Research & Extraction Hub":
    render_executive_panel("Automated AI Discovery & NLP Extraction Center", "Machine Learning Web Scraping Processing Interfaces & Raw Telemetry Output")
    
    col_control, col_console = st.columns([1, 2])
    with col_control:
        st.markdown('<div class="section-title">Execution Controls</div>', unsafe_allow_html=True)
        country_sel = st.selectbox("Select Target Deployment Market Context:", ["Brazil Regional Scope (Phase 1)", "India Regional Scope", "United States Scope"])
        source_filter = st.multiselect("Allowed Scraping Protocols:", ["Enterprise Websites", "Regulatory Registries", "Bloomberg RSS Directories", "Government Gazettes"], default=["Enterprise Websites", "Bloomberg RSS Directories"])
        
        trigger_btn = st.button("Launch Extraction Sequence Pipeline", use_container_width=True, type="primary")
        if trigger_btn:
            st.session_state.scraper_triggered = True
            
    with col_console:
        st.markdown('<div class="section-title">Pipeline Operations Logs</div>', unsafe_allow_html=True)
        if st.session_state.scraper_triggered:
            with st.status("Running active extraction protocols...", expanded=True) as status:
                st.write("Initializing secure background data routing daemons... OK")
                time.sleep(0.4)
                st.write("Handshake established with target investor registries. Querying indexes... OK")
                time.sleep(0.4)
                st.write("Payload located via RSS Match ID #81023. Running unstructured text NLP mapping rules... OK")
                time.sleep(0.4)
                status.update(label="Scraping cycle successfully completed! Record transferred to staging.", state="complete", expanded=True)
            st.code("NLP Entity Resolution Match Output:\n -> Plant: Unid. Gasa\n -> Mapped Metric Fields: 33/33 Attributes Found\n -> Core Parsing Engine Confidence Scale: 94.2%")
        else:
            st.info("System Engine idling. Execute 'Launch Extraction Sequence Pipeline' to begin processing live web scrapers.")

    st.markdown("---")
    st.markdown('<div class="section-title">Extracted Pipeline Payload Fields (Staged for HITL Validation)</div>', unsafe_allow_html=True)
    if len(st.session_state.pending_queue) == 0:
        st.success("🎉 Staging environment clear. All discovered records successfully verified and pushed to production database layouts.")
    else:
        pending_df = pd.DataFrame(st.session_state.pending_queue)
        st.dataframe(pending_df[["Plant Name", "Company", "Source", "Confidence", "Status", "Capacity", "ExtractDate"]], use_container_width=True)

# ==========================================
# PAGE 5: HUMAN-IN-THE-LOOP (HITL) QUEUE
# ==========================================
elif page == "🖥️ Human-in-the-Loop Review Queue":
    render_executive_panel("Human-In-The-Loop Data Verification Interface", "100% Data Fidelity Verification Environment for Senior Corporate Leadership Validation")
    
    if len(st.session_state.pending_queue) == 0:
        st.balloons()
        st.success("🎉 **Validation Queue Completely Clear!** All discovered industrial assets are safely logged to production layouts.")
    else:
        current_target = st.session_state.pending_queue[0]
        st.warning(f"👉 **Awaiting Action:** Evaluating Extraction Target Record **1 of {len(st.session_state.pending_queue)}**: **{current_target['Plant Name']}** (AI Engine Match Confidence Scale: {current_target['Confidence']}%)")
        
        left_pane, right_pane = st.columns([2, 3])
        with left_pane:
            st.markdown('<div class="section-title">Original Source Text Fragment</div>', unsafe_allow_html=True)
            st.info(f"""**Document Excerpt Source Reference ({current_target['Source']}):** "{st.session_state.pending_queue[0]['Company']}'s infrastructure details logged major expansions. The operating management firm has approved capital layouts. Metrics confirm an immediate modification to spatial design criteria, increasing active nameplate production capacity metrics to achieve an effective annual baseline yield capability of {current_target['Capacity']} Million Liters per annum..." """)
            st.caption("Primary Reference Source Track URL String: https://www.bloomberg.com/news/articles/brazil-biofuel-expansion-raizen")
            
            st.markdown('<div class="section-title">Capacity Verification Methodology Standard Logic</div>', unsafe_allow_html=True)
            st.latex(r"Capacity_{Effective} = Capacity_{Design} \times \text{Energy Density Scale Factor}")
            
        with right_pane:
            st.markdown('<div class="section-title">Verified Enterprise Data Field Form</div>', unsafe_allow_html=True)
            with st.form("hitl_interactive_form"):
                st.markdown("##### 📋 Core Asset Profile & Identification")
                f_col1, f_col2 = st.columns(2)
                with f_col1:
                    form_name = st.text_input("Project Factory Registration Name", value=current_target["Plant Name"])
                    form_parent = st.text_input("Parent Corporate Umbrella Group", value=current_target["Parent Group"])
                with f_col2:
                    form_company = st.text_input("Primary Operating Management Entity", value=current_target["Company"])
                    form_status = st.selectbox("Active Operational Pipeline Status", ["Operating", "Planned/Under Construction", "Capacity Expanded (+15%)", "Closed"], index=2)
                
                st.markdown("##### 🗺️ Geographic Location Data (Google Maps Sync)")
                f_col3, f_col4 = st.columns(2)
                with f_col3:
                    form_lat = st.text_input("Verified Latitude Node", value=str(current_target["lat"]))
                    form_city = st.text_input("Target City Boundaries", value=current_target["City"])
                with f_col4:
                    form_lon = st.text_input("Verified Longitude Node", value=str(current_target["lon"]))
                    form_state = st.text_input("Regional State Classification", value=current_target["State"])
                
                st.markdown("##### ⚙️ Production Metrics, Feedstocks & Byproducts")
                f_col5, f_col6 = st.columns(2)
                with f_col5:
                    form_capacity = st.number_input("Standardized Capacity Volume [M Liters/Yr]", value=current_target["Capacity"])
                    form_feedstock = st.text_input("Feedstock Biomass Input Mix Profile", value=current_target["Feedstock"])
                with f_col6:
                    form_year = st.number_input("Operational Asset Construction Launch Year", value=current_target["Start Year"])
                    form_byprod = st.text_input("Primary Coproduct/Byproduct Stream Profile", value="Vinasse Bio-Compost Base")
                
                st.markdown("<br>", unsafe_allow_html=True)
                submit_verification = st.form_submit_button("Commit Checked Attributes to Master Database Schema", use_container_width=True)
                if submit_verification:
                    validated_record = {
                        "Plant Name": form_name, "Company": form_company, "Parent Group": form_parent, "State": form_state, "City": form_city,
                        "lat": float(form_lat), "lon": float(form_lon), "Status": form_status, "Capacity": int(form_capacity),
                        "Feedstock": form_feedstock, "Start Year": int(form_year), "Verification Date": datetime.now().strftime("%Y-%m-%d")
                    }
                    st.session_state.production_db = pd.concat([st.session_state.production_db, pd.DataFrame([validated_record])], ignore_index=True)
                    st.session_state.pending_queue.pop(0)
                    st.success("Log asset system record successfully committed.")
                    time.sleep(0.5)
                    st.rerun()

    st.markdown("---")
    st.markdown('<div class="section-title">Package Current Delivery Artifact Data Structures</div>', unsafe_allow_html=True)
    timestamp_export = datetime.now().strftime("%Y%m%d_%H%M")
    export_filename_string = f"Brazil_{len(st.session_state.production_db)}_Projects_{timestamp_export}_FinalReport.csv"
    csv_payload = st.session_state.production_db[["Plant Name", "Company", "Parent Group", "State", "Status", "Capacity", "Feedstock", "Verification Date"]].to_csv(index=False)
    st.download_button(label="Download Processed Delivery Matrix Spreadsheet (.CSV Document Target)", data=csv_payload, file_name=export_filename_string, mime="text/csv")

# ==========================================
# PAGE 6: MAINTENANCE & LIFECYCLE ALERTS
# ==========================================
elif page == "🔔 Maintenance Alerts & Lifecycle":
    render_executive_panel("Continuous Baseline Asset Lifecycle Maintenance Engine", "Dynamic Asset Configuration Monitoring & Delta Tracking Anomalies Notifications")
    
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
