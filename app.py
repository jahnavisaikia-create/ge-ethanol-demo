import streamlit as st
import pandas as pd

# --- GE CORPORATE INTELLIGENCE CONFIGURATION ---
st.set_page_config(
    page_title="GEA Navigator - Global Ethanol Intelligence", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- PREMIUM GE INDUSTRIAL BRAND THEME (CSS) ---
# Enforces GE Slate (#0f172a), Industrial Cyan (#0284c7), and completely erases the pink palette
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Force Stark White Background and Global Corporate Fonts */
    html, body, [class*="css"] { 
        font-family: 'Inter', sans-serif; 
        color: #1e293b; 
        background-color: #ffffff !important;
    }
    
    /* Premium GE Industrial Header Banner */
    .ge-header-banner {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 2.5rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    }
    .ge-title { font-size: 2.25rem; font-weight: 800; color: #ffffff; margin-bottom: 0.5rem; letter-spacing: -0.025em; }
    .ge-subtitle { font-size: 1.1rem; color: #94a3b8; font-weight: 400; }
    
    /* Left Banner Box on Login Screen (Replaces Pink Card from image 28/29) */
    .ge-brand-hero-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 2.5rem;
        border-radius: 12px;
        margin-bottom: 1.25rem;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05);
    }
    .ge-system-tag { color: #0284c7; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem; }
    .ge-main-title { font-size: 2rem; font-weight: 800; color: #ffffff; margin-bottom: 1rem; letter-spacing: -0.02em; }
    .ge-description { font-size: 0.95rem; color: #cbd5e1; line-height: 1.6; }
    
    .ge-product-info-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 1.75rem;
        border-radius: 12px;
        box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.05);
    }
    .ge-info-title { font-size: 1.15rem; font-weight: 700; color: #0f172a; margin-bottom: 0.5rem; }
    .ge-info-body { font-size: 0.95rem; color: #475569; line-height: 1.6; }

    /* Symmetrical Performance Metric Cards (Replaces raw text numbers in image 30) */
    .ge-kpi-container-card {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        border-top: 4px solid #0284c7;
        border-left: 1px solid #e2e8f0;
        border-right: 1px solid #e2e8f0;
        border-bottom: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05);
        text-align: center;
        height: 100%;
    }
    .ge-kpi-label { font-size: 0.85rem; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem; }
    .ge-kpi-value { font-size: 2.75rem; font-weight: 800; color: #0f172a; letter-spacing: -0.03em; line-height: 1; }

    /* Balanced Alignment Component Titles */
    .ge-workspace-header-title { font-size: 1.35rem; font-weight: 700; color: #0f172a; margin-top: 1.5rem; margin-bottom: 1rem; letter-spacing: -0.01em; border-left: 4px solid #0284c7; padding-left: 0.75rem; }
    
    /* Clean Enterprise Input Forms Styling */
    div[data-testid="stForm"] {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 14px !important;
        padding: 2.5rem !important;
        box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.05) !important;
    }
    
    /* Bottom Scope Bar Box */
    .ge-scope-box {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        padding: 1.25rem;
        border-radius: 8px;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION CONTROLS ---
st.sidebar.title("🧭 Navigation Hub")
st.sidebar.caption("GE Brand Layout Mode Active")
st.sidebar.markdown("---")

# Direct selection view allows clicking through screens instantly without getting blocked by the gateway gate
view_page = st.sidebar.radio(
    "Select Display Mockup View:",
    [
        "🔐 Screen 28 & 29: Premium Login Interface",
        "🏠 Screen 30: Operations Management Hub"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("Signed in as: Sneha")

# ==========================================
# 🔓 VIEW MODULE: SCREENS 28 & 29 (AUTHENTICATION GATEWAY)
# ==========================================
if view_page == "🔐 Screen 28 & 29: Premium Login Interface":
    st.markdown('<div style="padding-top:1rem;"></div>', unsafe_allow_html=True)
    
    # Perfectly symmetrical 50/50 dashboard split layout
    col_left, col_right = st.columns([1, 1], gap="large")
    
    with col_left:
        # GE Brand Identity Infused Blueprint Cards
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
            st.markdown("<h2 style='margin-top:0; margin-bottom:1.5rem; font-weight:700; color:#0f172a;'>Login</h2>", unsafe_allow_html=True)
            username = st.text_input("Username", value="Sneha")
            password = st.text_input("Password", type="password", value="••••••••")
            st.markdown("<div style='padding-top:1rem;'></div>", unsafe_allow_html=True)
            submit_auth = st.form_submit_button("Sign in", use_container_width=True)
            if submit_auth:
                st.success("Authentication mock successful! Navigate to Screen 30 using the sidebar.")

# ==========================================
# 🔒 VIEW MODULE: SCREEN 30 (COMMAND WORKSPACE HUB)
# ==========================================
else:
    # Render premium GE Slate Top Block Banner Panel
    render_ge_panel("GEA Navigator: Operations Command Hub", "Target Scope Framework: Brazil Country Filters (Temporal Scope Window: 2003 - 2026)")
    st.markdown("<p style='font-size:0.95rem; color:#64748b; margin-top:-1rem; margin-bottom:1.5rem;'>Select a country scope, start research, and review extracted projects before generating a report.</p>", unsafe_allow_html=True)
    
    # Core Filter Action Ingestion Box Container Card
    with st.container(border=True):
        col_inputs, col_actions = st.columns([3, 2], gap="medium")
        with col_inputs:
            st.checkbox("Select all countries", value=False)
            st.multiselect("Country", ["Brazil", "United States", "India"], default=["Brazil"])
        with col_actions:
            st.markdown("<p style='font-size:1.1rem; font-weight:700; color:#0f172a; margin-bottom:0.75rem;'>Action</p>", unsafe_allow_html=True)
            st.button("Start Research", use_container_width=True, type="primary")
            
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Symmetrical Performance Cards (Replaces the uncontained raw floating text metrics)
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    with col_kpi1:
        st.markdown("""<div class="ge-kpi-container-card"><div class="ge-kpi-label">Countries in Scope</div><div class="ge-kpi-value">1</div></div>""", unsafe_allow_html=True)
    with col_kpi2:
        st.markdown("""<div class="ge-kpi-container-card"><div class="ge-kpi-label">Projects Discovered</div><div class="ge-kpi-value">5</div></div>""", unsafe_allow_html=True)
    with col_kpi3:
        st.markdown("""<div class="ge-kpi-container-card"><div class="ge-kpi-label">Pending Review Queue</div><div class="ge-kpi-value">5</div></div>""", unsafe_allow_html=True)
        
    # Table Summary Blocks Registry
    st.markdown('<div class="ge-workspace-header-title">Research Summary Matrix</div>', unsafe_allow_html=True)
    mock_summary_data = pd.DataFrame({
        "Country Target": ["Brazil", "Brazil", "Brazil", "Brazil"],
        "Operating Company Owner": ["Be8", "CB Bioenergia", "FS Indústria de Etanol S.A.", "Raízen"],
        "# Discovered Projects": [1, 1, 2, 1],
        "# Review Pending Flags": [1, 1, 2, 1]
    })
    st.dataframe(mock_summary_data, use_container_width=True, hide_index=True)
    
    # Symmetrical Layout Action Footer Elements
    st.markdown("<br>", unsafe_allow_html=True)
    col_rep, col_scp = st.columns([3, 2], gap="medium")
    with col_rep:
        st.button("Generate Template Report Output", use_container_width=True)
    with col_scp:
        st.markdown("""<div class="ge-scope-box"><p style='font-size:0.85rem; font-weight:600; color:#0f172a; margin:0;'>Active Country Scope Parameter</p><p style='font-size:0.9rem; color:#0284c7; font-weight:600; margin:4px 0 0 0;'>Brazil 🇧🇷</p></div>""", unsafe_allow_html=True)
        
    # Drilldowns Accordion Segment
    st.markdown('<div class="ge-workspace-header-title">Company Metric Drilldowns</div>', unsafe_allow_html=True)
    with st.expander("Be8 | Brazil | 1 project(s) | 1 pending review metric logs", expanded=True):
        st.markdown("<div style='padding:0.25rem 0;'></div>", unsafe_allow_html=True)
        d_col1, d_col2 = st.columns([3, 1])
        with d_col1:
            st.button("Be8 Passo Fundo Cereal Ethanol Plant Asset Log", use_container_width=True)
        with d_col2:
            st.markdown("<p style='font-size:0.95rem; color:#d97706; font-weight:600; margin-top:8px; text-align:center;'>⏳ Awaiting Audit Check</p>", unsafe_allow_html=True)
