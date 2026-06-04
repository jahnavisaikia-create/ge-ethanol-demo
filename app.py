import streamlit as st
import pandas as pd

# --- STAGE LAYER CONFIGURATION ---
st.set_page_config(page_title="GEA Navigator", layout="wide", initial_sidebar_state="expanded")

# --- EXECUTIVE PREMIUM DESIGN LANGUAGE (CSS) ---
# Hard-locks font consistency, container padding, metric card symmetry, and form alignments
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Base Reset & Consistent Typography */
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; color: #1e293b; }
    
    /* Symmetrical Information Banners (Left Column of Login) */
    .brand-hero-card {
        background-color: #fff1f2;
        border: 1px solid #ffe4e6;
        padding: 2.25rem;
        border-radius: 12px;
        margin-bottom: 1.25rem;
    }
    .brand-system-tag { color: #e11d48; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem; }
    .brand-main-title { font-size: 2.25rem; font-weight: 800; color: #0f172a; margin-bottom: 1rem; letter-spacing: -0.03em; }
    .brand-description { font-size: 1rem; color: #475569; line-height: 1.6; }
    
    .product-info-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 1.75rem;
        border-radius: 12px;
        box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.05);
    }
    .product-info-title { font-size: 1.15rem; font-weight: 700; color: #0f172a; margin-bottom: 0.5rem; }
    .product-info-body { font-size: 0.95rem; color: #475569; line-height: 1.6; }

    /* Performance Grid Metrics (Replaces raw text numbers in image 30) */
    .kpi-container-card {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 2px 0 rgb(0 0 0 / 0.05);
        margin-bottom: 1rem;
    }
    .kpi-label { font-size: 0.85rem; font-weight: 500; color: #64748b; margin-bottom: 0.25rem; }
    .kpi-value { font-size: 2.5rem; font-weight: 700; color: #0f172a; letter-spacing: -0.03em; line-height: 1; }

    /* Global Content Alignment Titles */
    .workspace-header-title { font-size: 1.75rem; font-weight: 700; color: #0f172a; margin-top: 1.5rem; margin-bottom: 1rem; letter-spacing: -0.02em; }
    
    /* Clean Login & Workspace Forms Design */
    div[data-testid="stForm"] {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 14px !important;
        padding: 2.5rem !important;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05) !important;
    }
    
    /* Scope indicator card spacing adjustments */
    .scope-box {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        padding: 1.25rem;
        border-radius: 8px;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# --- TRACK DATA AND WORKSPACE INITIALIZATION ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ==========================================
# 🔓 VIEW LAYER 1: PREMIUM SECURITY GATEWAY (FIXES image 28 / 29)
# ==========================================
if not st.session_state.logged_in:
    st.markdown('<div style="padding-top:2rem;"></div>', unsafe_allow_html=True)
    
    # 50/50 Symmetrical Split Layout Layout
    col_left, col_right = st.columns([1, 1], gap="large")
    
    with col_left:
        st.markdown("""
        <div class="brand-hero-card">
            <div class="brand-system-tag">SG Analytics Research Workspace</div>
            <div class="brand-main-title">Research, review, and reporting in one place.</div>
            <div class="brand-description">This workflow turns country-specific source tracking into reviewed project records and downloadable Excel reports aligned to the GEA template.</div>
        </div>
        <div class="product-info-card">
            <div class="product-info-title">What the product does</div>
            <div class="product-info-body">Analysts select one or more countries, trigger research, review extracted project fields in an editable side-by-side workspace, and generate report-ready outputs with traceable history.</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col_right:
        with st.form("login_gateway"):
            st.markdown("<h2 style='margin-top:0; margin-bottom:1.5rem; font-weight:700; color:#0f172a;'>Login</h2>", unsafe_allow_html=True)
            username = st.text_input("Username", value="Sneha")
            password = st.text_input("Password", type="password", value="••••••••")
            st.markdown("<div style='padding-top:1rem;'></div>", unsafe_allow_html=True)
            submit_auth = st.form_submit_button("Sign in", use_container_width=True)
            
            if submit_auth:
                st.session_state.logged_in = True
                st.rerun()

# ==========================================
# 🔒 VIEW LAYER 2: WORKSPACE CONTROL INTERFACE (FIXES image 30)
# ==========================================
else:
    # Navigation Sidebar Panel
    with st.sidebar:
        st.markdown("<h2 style='font-weight:700; margin-bottom:0.25rem;'>GEA Navigator</h2>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:0.9rem; color:#64748b; line-height:1.4;'>Country-led research, guided review, and report generation.</p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:0.8rem; color:#94a3b8; margin-top:2rem;'>Signed in as <span style='color:#475569; font-weight:600;'>Sneha</span></p>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("<p style='font-size:0.85rem; font-weight:600; color:#e11d48; margin-bottom:0.5rem;'>Research</p>", unsafe_allow_html=True)
        
        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()
            
    # Main Page Layout Content Flow
    st.markdown("<p style='font-size:0.95rem; color:#64748b; margin-top:0.5rem; margin-bottom:1.5rem;'>Select a country scope, start research, and review extracted projects before generating a report.</p>", unsafe_allow_html=True)
    
    # Ingestion Trigger Box Container
    with st.container(border=True):
        col_inputs, col_actions = st.columns([3, 2], gap="medium")
        with col_inputs:
            st.checkbox("Select all countries", value=False)
            st.multiselect("Country", ["Brazil", "United States", "India"], default=["Brazil"])
        with col_actions:
            st.markdown("<p style='font-size:1.1rem; font-weight:700; color:#0f172a; margin-bottom:0.75rem;'>Action</p>", unsafe_allow_html=True)
            st.button("Start Research", use_container_width=True)
            
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Grid Metric Block Alignments (Resolves raw layout numbers from image 30)
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    with col_kpi1:
        st.markdown("""<div class="kpi-container-card"><div class="kpi-label">Countries in scope</div><div class="kpi-value">1</div></div>""", unsafe_allow_html=True)
    with col_kpi2:
        st.markdown("""<div class="kpi-container-card"><div class="kpi-label">Projects found</div><div class="kpi-value">5</div></div>""", unsafe_allow_html=True)
    with col_kpi3:
        st.markdown("""<div class="kpi-container-card"><div class="kpi-label">Pending review</div><div class="kpi-value">5</div></div>""", unsafe_allow_html=True)
        
    # Table Summary Blocks
    st.markdown('<div class="workspace-header-title">Research summary</div>', unsafe_allow_html=True)
    mock_summary_data = pd.DataFrame({
        "Country": ["Brazil", "Brazil", "Brazil", "Brazil"],
        "Company": ["Be8", "CB Bioenergia", "FS Indústria de Etanol S.A.", "Raízen"],
        "#Projects": [1, 1, 2, 1],
        "# Review pending": [1, 1, 2, 1]
    })
    st.dataframe(mock_summary_data, use_container_width=True, hide_index=True)
    
    # Action Operations Footer Symmetries
    st.markdown("<br>", unsafe_allow_html=True)
    col_rep, col_scp = st.columns([3, 2], gap="medium")
    with col_rep:
        st.button("Generate Report", use_container_width=True)
    with col_scp:
        st.markdown("""<div class="scope-box"><p style='font-size:0.85rem; font-weight:600; color:#0f172a; margin:0;'>Current country scope</p><p style='font-size:0.9rem; color:#475569; margin:4px 0 0 0;'>Brazil</p></div>""", unsafe_allow_html=True)
        
    # Detail Drilldowns Section
    st.markdown('<div class="workspace-header-title">Company drilldown</div>', unsafe_allow_html=True)
    with st.expander("Be8 | Brazil | 1 project(s) | 1 pending", expanded=True):
        st.markdown("<div style='padding:0.5rem 0;'></div>", unsafe_allow_html=True)
        d_col1, d_col2 = st.columns([3, 1])
        with d_col1:
            st.button("Be8 Passo Fundo Cereal Ethanol Plant", use_container_width=True)
        with d_col2:
            st.markdown("<p style='font-size:0.9rem; color:#64748b; margin-top:8px; text-align:center;'>Pending Review</p>", unsafe_allow_html=True)
