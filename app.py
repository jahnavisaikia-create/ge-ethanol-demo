import streamlit as st
import pandas as pd

# --- GE CORPORATE INTELLIGENCE CONFIGURATION ---
st.set_page_config(
    page_title="GEA Navigator - Global Ethanol Intelligence", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ADVANCED ENTERPRISE CSS INDUSTRIAL STYLE SHEET ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global System Overrides */
    html, body, [class*="css"] { 
        font-family: 'Inter', sans-serif; 
        color: #1e293b;
        background-color: #f8fafc !important;
    }
    
    /* Clean, Non-Boring Header Blocks */
    .ge-header-banner {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 2.5rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1);
    }
    .ge-title { font-size: 2.25rem; font-weight: 800; color: #ffffff; margin-bottom: 0.5rem; letter-spacing: -0.025em; }
    .ge-subtitle { font-size: 1.1rem; color: #94a3b8; font-weight: 400; }
    
    /* Left Panel Hero Box on Authentication Gateway */
    .ge-brand-hero-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 3rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05);
    }
    .ge-system-tag { color: #38bdf8; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.75rem; }
    .ge-main-title { font-size: 2.25rem; font-weight: 800; color: #ffffff; margin-bottom: 125rem; letter-spacing: -0.02em; line-height: 1.2; }
    .ge-description { font-size: 1rem; color: #cbd5e1; line-height: 1.6; text-align: justify; }
    
    .ge-product-info-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05);
    }
    .ge-info-title { font-size: 1.25rem; font-weight: 700; color: #0f172a; margin-bottom: 0.75rem; letter-spacing: -0.01em; }
    .ge-info-body { font-size: 0.95rem; color: #475569; line-height: 1.6; text-align: justify; }

    /* Crisp Architectural Metrics Cards */
    .ge-kpi-container-card {
        background: #ffffff;
        padding: 1.75rem;
        border-radius: 12px;
        border-top: 4px solid #0284c7;
        border-left: 1px solid #e2e8f0;
        border-right: 1px solid #e2e8f0;
        border-bottom: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05);
        text-align: center;
        height: 100%;
    }
    .ge-kpi-label { font-size: 0.85rem; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem; }
    .ge-kpi-value { font-size: 3rem; font-weight: 800; color: #0f172a; letter-spacing: -0.04em; line-height: 1; }

    /* Aligned Grid Component Headers */
    .ge-workspace-header-title { font-size: 1.4rem; font-weight: 700; color: #0f172a; margin-top: 2rem; margin-bottom: 1.25rem; letter-spacing: -0.015em; border-left: 4px solid #0284c7; padding-left: 0.75rem; }
    
    /* Structured Layout Action Controls Outer Box */
    .ge-control-deck-container {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.75rem;
        box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.05);
        margin-bottom: 2rem;
    }

    /* Production-Grade Input Forms Border Lock */
    div[data-testid="stForm"] {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 16px !important;
        padding: 3rem !important;
        box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.05) !important;
    }
    
    /* Bottom Scope Component Block */
    .ge-scope-box {
        background-color: #f1f5f9;
        border: 1px solid #e2e8f0;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        height: 100%;
    }
</style>
""", unsafe_allow_html=True)

# --- REUSABLE PATTERN: BRANDED INDUSTRIAL BANNER ENGINE ---
# Placed globally at top context tier to eliminate all NameError gaps
def render_ge_panel(title, subtitle):
    st.markdown(f"""
    <div class="ge-header-banner">
        <div class="ge-title">{title}</div>
        <div class="ge-subtitle">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)

# --- GLOBAL DATABASE MEMORY INITIALIZATION ---
if "production_db" not in st.session_state:
    st.session_state.production_db = pd.DataFrame([
        {"Plant Name": "Unid. Barra", "Company": "Raízen", "Parent Group": "Cosan & Shell", "State": "São Paulo", "City": "Barra Bonita", "lat": -22.4042, "lon": -48.5564, "Status": "Operating", "Capacity": 180, "Feedstock": "Sugarcane Bagasse", "Start Year": 2004, "Verification Date": "2026-05-15"},
        {"Plant Name": "Unid. Maracaí", "Company": "Raízen", "Parent Group": "Cosan & Shell", "State": "São Paulo", "City": "Maracaí", "lat": -22.6124, "lon": -50.6345, "Status": "Operating", "Capacity": 120, "Feedstock": "Sugarcane Bagasse", "Start Year": 2008, "Verification Date": "2026-05-20"},
        {"Plant Name": "Passo Fundo Cereal Plant", "Company": "Be8", "Parent Group": "ECB Group", "State": "Rio Grande do Sul", "City": "Passo Fundo", "lat": -28.2624, "lon": -52.4068, "Status": "Operating", "Capacity": 210, "Feedstock": "Corn", "Start Year": 2011, "Verification Date": "2026-05-25"}
    ])

if "pending_queue" not in st.session_state:
    st.session_state.pending_queue = [
        {"Plant Name": "Unid. Gasa", "Company": "Raízen", "Parent Group": "Cosan & Shell", "State": "São Paulo", "City": "Andradina", "lat": -20.8961, "lon": -51.3794, "Status": "Capacity Expanded (+15%)", "Capacity": 95, "Feedstock": "Sugarcane Bagasse", "Start Year": 2003, "Confidence": 94.2, "Source": "Bloomberg Industrial Index", "ExtractDate": "2026-06-01"},
        {"Plant Name": "Sinop Biofuel Plant", "Company": "Inpasa", "Parent Group": "Inpasa Brasil", "State": "Mato Grosso", "City": "Sinop", "lat": -11.8541, "lon": -55.5085, "Status": "Planned/Under Construction", "Capacity": 400, "Feedstock": "Corn", "Start Year": 2026, "Confidence": 89.7, "Source": "Mato Grosso Regional Registry", "ExtractDate": "2026-06-01"}
    ]

# --- SIDEBAR NAVIGATION CONTROLS ---
st.sidebar.title("🧭 GEA Command Hub")
st.sidebar.caption("Enterprise Layout Mode Active")
st.sidebar.markdown("---")

view_page = st.sidebar.radio(
    "Select Display Mockup View:",
    [
        "🔐 Screen 28 & 29: Premium Login Interface",
        "🏠 Screen 30: Operations Management Hub"
    ]
)
st.sidebar.markdown("---")
st.sidebar.info("Authenticated Identity: Analyst Sneha")

# ==========================================
# VIEW MODULE: SCREENS 28 & 29 (AUTHENTICATION GATEWAY)
# ==========================================
if view_page == "🔐 Screen 28 & 29: Premium Login Interface":
    st.markdown('<div style="padding-top:1.5rem;"></div>', unsafe_allow_html=True)
    
    col_left, col_right = st.columns([1, 1], gap="large")
    with col_left:
        st.markdown("""
        <div class="ge-brand-hero-card">
            <div class="ge-system-tag">SG Analytics Research Workspace</div>
            <div class="ge-main-title">Research, review, and reporting in one place.</div>
            <div class="ge-description">This workflow turns country-specific source tracking into reviewed project records and downloadable Excel reports aligned to the GEA template.</div>
        </div>
        <div class="ge-product-info-card">
            <div class="ge-info-title">What the product does</div>
            <div class="ge-info-body">Analysts select one or more countries, trigger research, review extracted project fields in an editable side-by-side workspace, and generate report-ready outputs with traceable history.</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col_right:
        with st.form("login_gateway"):
            st.markdown("<h2 style='margin-top:0; margin-bottom:1.75rem; font-weight:800; color:#0f172a; letter-spacing:-0.02em;'>Login</h2>", unsafe_allow_html=True)
            username = st.text_input("Username", value="Sneha")
            password = st.text_input("Password", type="password", value="••••••••")
            st.markdown("<div style='padding-top:1.5rem;'></div>", unsafe_allow_html=True)
            submit_auth = st.form_submit_button("Sign in", use_container_width=True)
            if submit_auth:
                st.success("Authentication mockup successful! Toggle to Screen 30 via the sidebar navigation menu.")

# ==========================================
# VIEW MODULE: SCREEN 30 (COMMAND WORKSPACE HUB)
# ==========================================
else:
    render_ge_panel("GEA Navigator: Operations Command Hub", "Target Scope Framework: Brazil Country Filters (Temporal Scope Window: 2003 - 2026)")
    st.markdown("<p style='font-size:1rem; color:#475569; margin-top:-1rem; margin-bottom:2rem;'>Select a country scope, start research, and review extracted projects before generating a report.</p>", unsafe_allow_html=True)
    
    # Structural Control Deck Container
    st.markdown('<div class="ge-control-deck-container">', unsafe_allow_html=True)
    col_inputs, col_actions = st.columns([3, 2], gap="large")
    with col_inputs:
        st.checkbox("Select all countries", value=False)
        st.multiselect("Country", ["Brazil", "United States", "India"], default=["Brazil"])
    with col_actions:
        st.markdown("<p style='font-size:1.05rem; font-weight:700; color:#0f172a; margin-bottom:0.75rem; letter-spacing:-0.01em;'>Action</p>", unsafe_allow_html=True)
        st.button("Start Research", use_container_width=True, type="primary")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Balanced KPI Analytics Grid
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    with col_kpi1:
        st.markdown("""<div class="ge-kpi-container-card"><div class="ge-kpi-label">Countries in Scope</div><div class="ge-kpi-value">1</div></div>""", unsafe_allow_html=True)
    with col_kpi2:
        st.markdown("""<div class="ge-kpi-container-card"><div class="ge-kpi-label">Projects Discovered</div><div class="ge-kpi-value">5</div></div>""", unsafe_allow_html=True)
    with col_kpi3:
        st.markdown("""<div class="ge-kpi-container-card"><div class="ge-kpi-label">Pending Review Queue</div><div class="ge-kpi-value">5</div></div>""", unsafe_allow_html=True)
        
    # Table Matrix Area
    st.markdown('<div class="ge-workspace-header-title">Research Summary Matrix</div>', unsafe_allow_html=True)
    mock_summary_data = pd.DataFrame({
        "Country Target": ["Brazil", "Brazil", "Brazil", "Brazil"],
        "Operating Company Owner": ["Be8", "CB Bioenergia", "FS Indústria de Etanol S.A.", "Raízen"],
        "# Discovered Projects": [1, 1, 2, 1],
        "# Review Pending Flags": [1, 1, 2, 1]
    })
    st.dataframe(mock_summary_data, use_container_width=True, hide_index=True)
    
    # Aligned Operations Footer Elements
    st.markdown("<br>", unsafe_allow_html=True)
    col_rep, col_scp = st.columns([3, 2], gap="large")
    with col_rep:
        st.markdown("<div style='margin-top: 6px;'></div>", unsafe_allow_html=True)
        st.button("Generate Template Report Output", use_container_width=True)
    with col_scp:
        st.markdown("""
        <div class="ge-scope-box">
            <span style='font-size:0.8rem; font-weight:600; color:#64748b; text-transform:uppercase; letter-spacing:0.05em;'>Active Country Scope Parameter</span>
            <span
