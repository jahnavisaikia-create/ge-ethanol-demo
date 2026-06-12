import streamlit as st
import pandas as pd

# --- CXO ENTERPRISE THEMING & CONFIGURATION ---
st.set_page_config(
    page_title="Optum Intelligent Operations Platform",
    page_icon="🧡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# FIXED: Explicit, granular initialization of every single state key individually to stop KeyError bugs
if "auth_executed" not in st.session_state:
    st.session_state["auth_executed"] = False
if "auth_repaired" not in st.session_state:
    st.session_state["auth_repaired"] = False
if "claims_executed" not in st.session_state:
    st.session_state["claims_executed"] = False
if "claims_settled" not in st.session_state:
    st.session_state["claims_settled"] = False
if "twin_executed" not in st.session_state:
    st.session_state["twin_executed"] = False
if "pharmacy_ok" not in st.session_state:
    st.session_state["pharmacy_ok"] = False
if "ride_ok" not in st.session_state:
    st.session_state["ride_ok"] = False
if "pcp_ok" not in st.session_state:
    st.session_state["pcp_ok"] = False
if "coach_ok" not in st.session_state:
    st.session_state["coach_ok"] = False

# High-Fidelity CSS Styling Engine with fixed sidebar contrast parameters
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background-color: #F8FAFC !important;
    }
    
    /* FIXED: Force clean contrast inside the sidebar radio selection block */
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
        color: #1E293B !important;
        font-weight: 600 !important;
    }
    [data-testid="stSidebar"] label p {
        color: #334155 !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
    }
    
    h1 { font-weight: 700 !important; color: #1E293B !important; font-size: 2.2rem !important; letter-spacing: -0.02em; }
    h2 { font-weight: 600 !important; color: #334155 !important; font-size: 1.5rem !important; margin-top: 1.5rem !important; }
    h3 { font-weight: 600 !important; color: #475569 !important; font-size: 1.2rem !important; }
    
    .metric-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05);
    }
    .metric-val { font-size: 1.8rem; font-weight: 700; color: #EF5A24; margin-bottom: 2px; }
    .metric-lbl { font-size: 0.85rem; font-weight: 500; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em; }
    .metric-delta { font-size: 0.8rem; font-weight: 600; color: #10B981; margin-top: 4px; }
    
    .agent-box {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 14px;
        box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
    }
    .agent-header-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
    .agent-title { font-weight: 600; font-size: 1.05rem; color: #0F172A; }
    .agent-badge { font-size: 0.75rem; font-weight: 600; padding: 4px 10px; border-radius: 9999px; text-transform: uppercase; }
    
    .badge-active { background-color: #CCFBF1; color: #0D9488; border: 1px solid #99F6E4; }
    .badge-alert { background-color: #FEF3C7; color: #D97706; border: 1px solid #FDE68A; }
    .badge-critical { background-color: #FEE2E2; color: #DC2626; border: 1px solid #FCA5A5; }
    .badge-twin { background-color: #E0E7FF; color: #4F46E5; border: 1px solid #C7D2FE; }
    .badge-idle { background-color: #F1F5F9; color: #64748B; border: 1px solid #E2E8F0; }
    
    .narrative-banner {
        background: linear-gradient(90deg, #1E293B 0%, #334155 100%);
        color: #FFFFFF;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 25px;
    }
    .red-team-panel { background-color: #FFF5F5; border: 1px solid #FCA5A5; border-radius: 10px; padding: 16px; margin-top: 15px; }
    .negotiation-panel { background-color: #F0FDF4; border: 1px solid #BBF7D0; border-radius: 10px; padding: 20px; margin-top: 15px; }
    </style>
    """, unsafe_allow_html=True)

# System Master Case Data
case_data = {
    "text": "Patient presents with severe L4-L5 disc degeneration. History indicates completion of 12+ weeks of conservative physical therapy without meaningful improvement. Requesting authorization approval for single-level lumbar fusion inpatient stay (3 days standard duration).",
    "codes": [
        {"Type": "ICD-10", "Code": "M51.36", "Match": "99%"},
        {"Type": "CPT", "Code": "22612", "Match": "97%"},
        {"Type": "DRG", "Code": "460", "Match": "94%"}
    ],
    "repair_text": "Pre-operative imaging analytics confirm severe L4-L5 disc space narrowing exceeding 25% boundary with structural mechanical instability.",
    "red_team_alert": "Human Payer Reviewer or automated rules engine will likely trigger an automatic denial due to incomplete documentation of precise interspace narrowing thresholds under regional InterQual policy criterion #4.",
    "billing_total": 24500.00,
    "corrected_total": 18450.00,
    "integrity_issue": "High-cost specialty infusion billed as an independent item without localized diagnostic history markers in master logs.",
    "risk_score": "78%",
    "risk_drivers": "Medication Non-Adherence (42%) | Absentee Preventative Primary Care Tracking (35%) | Regional Social Gaps (23%)"
}

# --- SIDEBAR INTERFACE ---
st.sidebar.image("https://www.optum.com/content/dam/optum4/images/logo/optum-logo.svg", width=140)
st.sidebar.markdown("<br>", unsafe_allow_html=True)

st.sidebar.markdown("### **Platform Portfolio**")
app_selection = st.sidebar.radio(
    "Navigate Strategic Portfolios:",
    [
        "Prior Authorization Copilot",
        "Claims Integrity War Room",
        "Care Navigation Digital Twin"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### **Active Stream Context**")
st.sidebar.info("👤 **Member Profile:** Marcus Vance (Age 64)\n\n🏢 **Facility:** Mercy General Health System")

# ==============================================================================
# DEMO 1: PRIOR AUTHORIZATION COPILOT
# ==============================================================================
if "Prior Authorization" in app_selection:
    st.markdown("""
        <div class="narrative-banner">
            <span style="text-transform: uppercase; font-size: 0.75rem; font-weight: 700; color: #EF5A24; letter-spacing: 0.1em;">Phase 1: Pre-Submission Operational Defense</span>
            <h1 style="color: #FFFFFF !important; margin-top: 5px; margin-bottom: 10px;">Zero-Touch Prior Authorization Copilot</h1>
            <p style="margin: 0; font-size: 0.95rem; opacity: 0.9; line-height: 1.5;">
                <strong>The Strategic Problem:</strong> Payer environments face systemic litigation risks from provider-side startups weaponizing AI to challenge routine coverage denials.<br>
                <strong>The Value Proposition:</strong> This EHR-native multi-agent engine intercepts messy provider intent data streams and auto-repairs missing configuration vectors <em>before</em> submission—guaranteeing 96%+ first-pass alignment.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    k1, k2, k3 = st.columns(3)
    k1.markdown('<div class="metric-card"><div class="metric-lbl">First-Pass Approval</div><div class="metric-val">96.4%</div><div class="metric-delta">▲ +18.2% vs Baseline</div></div>', unsafe_allow_html=True)
    k2.markdown('<div class="metric-card"><div class="metric-lbl">Manual Touch Reduction</div><div class="metric-val">65%</div><div class="metric-delta">▼ Structural Drop</div></div>', unsafe_allow_html=True)
    k3.markdown('<div class="metric-card"><div class="metric-lbl">Missing Info Denials</div><div class="metric-val">-80%</div><div class="metric-delta">Blocked Upstream</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    c1, c2, c3 = st.columns([3, 4.5, 3.5])
    
    with c1:
        st.markdown("<h3>📥 Ingestion & Mapping</h3>", unsafe_allow_html=True)
        st.text_area("Raw Provider EHR Context Extract", value=case_data["text"], height=150)
        st.dataframe(pd.DataFrame(case_data["codes"]), use_container_width=True, hide_index=True)

    with c2:
        st.markdown("<h3>⚙️ Agent Orchestration Core</h3>", unsafe_allow_html=True)
        if st.button("⚡ Execute Autonomous Copilot Validation Pipeline", type="primary", use_container_width=True):
            st.session_state["auth_executed"] = True
            
        a_status = "active" if st.session_state["auth_executed"] else "idle"
        badge_cls = "badge-active" if st.session_state["auth_executed"] else "badge-idle"
        alert_cls = "badge-alert" if st.session_state["auth_executed"] else "badge-idle"
        
        st.markdown(f'<div class="agent-box"><div class="agent-header-row"><span class="agent-title">🧠 Clinical Reasoning Agent</span><span class="agent-badge {badge_cls}">{a_status}</span></div><div style="font-size:0.88rem; color:#475569;">{"Parsed narrative text patterns and cross-verified historical conservative line lengths (>12 weeks)." if st.session_state["auth_executed"] else "Awaiting invocation..."}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="agent-box"><div class="agent-header-row"><span class="agent-title">🔍 Evidence Validator Agent</span><span class="agent-badge {alert_cls}">{"ALERT" if st.session_state["auth_executed"] else "IDLE"}</span></div><div style="font-size:0.88rem; color:#475569;">{"Configuration Exception: Found missing numeric evaluation thresholds for specific space narrowing targets." if st.session_state["auth_executed"] else "Awaiting invocation..."}</div></div>', unsafe_allow_html=True)

        if st.session_state["auth_executed"]:
            st.markdown(f'<div class="red-team-panel"><span style="color:#DC2626; font-weight:700; font-size:0.85rem; text-transform:uppercase;">⚠️ Adversarial Red-Team Simulation Output</span><p style="font-size:0.88rem; color:#991B1B; margin-top:4px;">{case_data["red_team_alert"]}</p></div>', unsafe_allow_html=True)
            st.text_input("AI Formulated Narrative Payload Enrichment Injection:", value=case_data["repair_text"])
            if st.button("🛡️ Inject Repair & Secure Adjudication Guarantee", type="secondary", use_container_width=True):
                st.session_state["auth_repaired"] = True
            if st.session_state["auth_repaired"]:
                st.toast("✅ Submission payload successfully fortified against denial logic maps.")
                st.success("Airtight configuration parameters applied. Clean claim path validated.")
                st.session_state["auth_repaired"] = False

    with c3:
        st.markdown("<h3>🔒 Traceable Audit Ledger</h3>", unsafe_allow_html=True)
        st.dataframe(pd.DataFrame([
            {"Lifecycle Node": "Entity Extractor", "Evidence Base": "EHR Progress Notes", "Human Trigger": "No"},
            {"Lifecycle Node": "Criteria Validation", "Evidence Base": "Staged PT Logs", "Human Trigger": "No"},
            {"Lifecycle Node": "Adversarial Repair", "Evidence Base": "Imaging Patch", "Human Trigger": "Yes"}
        ]), use_container_width=True, hide_index=True)

# ==============================================================================
# DEMO 2: CLAIMS INTEGRITY WAR ROOM
# ==============================================================================
elif "Claims Integrity" in app_selection:
    st.markdown("""
        <div class="narrative-banner">
            <span style="text-transform: uppercase; font-size: 0.75rem; font-weight: 700; color: #EF5A24; letter-spacing: 0.1em;">Phase 2: Real-Time Transaction Adjudication</span>
            <h1 style="color: #FFFFFF !important; margin-top: 5px; margin-bottom: 10px;">Claims Integrity War Room</h1>
            <p style="margin: 0; font-size: 0.95rem; opacity: 0.9; line-height: 1.5;">
                <strong>The Strategic Problem:</strong> Traditional retrospective 'pay-and-chase' Fraud, Waste, and Abuse (FWA) detection causes significant administrative friction and severe payment leakage.<br>
                <strong>The Value Proposition:</strong> Shifting security upstream, this framework builds a live relational <em>Clinical Truth Graph</em> before checkout, replacing blunt den-and-appeal workflows with proactive AI-guided settlement adjustments.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    k1, k2, k3 = st.columns(3)
    k1.markdown('<div class="metric-card"><div class="metric-lbl">Leakage Prevention</div><div class="metric-val">34.2%</div><div class="metric-delta">▲ $4.2M Saved YTD</div></div>', unsafe_allow_html=True)
    k2.markdown('<div class="metric-card"><div class="metric-lbl">Downstream Appeals</div><div class="metric-val">-58.0%</div><div class="metric-delta">Upstream Mitigation</div></div>', unsafe_allow_html=True)
    k3.markdown('<div class="metric-card"><div class="metric-lbl">Scanning Latency</div><div class="metric-val">1.4 min</div><div class="metric-delta">Real-Time Engine</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    c1, c2 = st.columns([5, 5])
    
    with c1:
        st.markdown("<h3>🕸️ Clinical Truth Journey Reconciliation</h3>", unsafe_allow_html=True)
        if st.button("🔍 Execute Upstream Integrity Matrix Scan", type="primary", use_container_width=True):
            st.session_state["claims_executed"] = True
            
        c_status = "critical" if st.session_state["claims_executed"] else "idle"
        c_badge = "badge-critical" if st.session_state["claims_executed"] else "badge-idle"
        
        st.markdown(f'<div class="agent-box"><div class="agent-header-row"><span class="agent-title">⛓️ Clinical Consistency Verification Swarm</span><span class="agent-badge {c_badge}">{c_status}</span></div><div style="font-size:0.88rem; color:#475569;">{"Anomaly Triggered: High-cost specialty infusion billed as an independent item without localized diagnostic history markers in master logs." if st.session_state["claims_executed"] else "Awaiting tracking initiation..."}</div></div>', unsafe_allow_html=True)

    with c2:
        st.markdown("<h3>🤝 Real-Time Peer Resolution Matrix</h3>", unsafe_allow_html=True)
        if st.session_state["claims_executed"]:
            st.markdown(f"""
                <div class="negotiation-panel">
                    <h4 style="color:#1E40AF; margin-top:0;">Interactive Remittance Adjustment Alternative</h4>
                    <p style="font-size:0.9rem; color:#1E40AF;">Anomalous lines flag structural validation risk patterns under CMS Code Manual Section 12.</p>
                    <table style="width:100%; font-size:0.9rem; margin:15px 0; color:#1E40AF;">
                        <tr><td><b>Original Submission Target:</b></td><td style="text-align:right; color:#DC2626; font-weight:700;">${case_data["billing_total"]:,.2f}</td></tr>
                        <tr><td><b>AI Calibrated Adjustment:</b></td><td style="text-align:right; color:#16A34A; font-weight:700;">${case_data["corrected_total"]:,.2f}</td></tr>
                    </table>
                </div>
            """, unsafe_allow_html=True)
            if st.button("🤝 Accept Aligned Remittance Adjustments", type="primary", use_container_width=True):
                st.session_state["claims_settled"] = True
            if st.session_state["claims_settled"]:
                st.success("Remittance updated and cleared at optimized tier of $18,450.00. Transaction finalized.")
                st.session_state["claims_settled"] = False
        else:
            st.info("Execute upstream data check to run automated audits and populate settlement options.")

# ==============================================================================
# DEMO 3: AI CARE NAVIGATION DIGITAL TWIN
# ==============================================================================
else:
    st.markdown("""
        <div class="narrative-banner">
            <span style="text-transform: uppercase; font-size: 0.75rem; font-weight: 700; color: #EF5A24; letter-spacing: 0.1em;">Phase 3: Proactive Trajectory Management</span>
            <h1 style="color: #FFFFFF !important; margin-top: 5px; margin-bottom: 10px;">AI Care Navigation Digital Twin</h1>
            <p style="margin: 0; font-size: 0.95rem; opacity: 0.9; line-height: 1.5;">
                <strong>The Strategic Problem:</strong> Healthcare plans lose millions on high-risk multi-chronic cohorts because care management is reactive, relying on passive chatbots that fail to connect realities.<br>
                <strong>The Value Proposition:</strong> This orchestration engine synthesizes datasets into a predictive <em>Digital Twin</em> trajectory timeline, deploying targeted operational micro-agents to resolve clinical gaps before an expensive ER event occurs.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    k1, k2, k3 = st.columns(3)
    k1.markdown('<div class="metric-card"><div class="metric-lbl">Avoidable ER Utilization</div><div class="metric-val">-32.4%</div><div class="metric-delta">▲ Preventative Shift</div></div>', unsafe_allow_html=True)
    k2.markdown('<div class="metric-card"><div class="metric-lbl">Chronic Cohort PMPM Savings</div><div class="metric-val">$142.50</div><div class="metric-delta">Per Member/Month</div></div>', unsafe_allow_html=True)
    k3.markdown('<div class="metric-card"><div class="metric-lbl">STAR Index Metrics</div><div class="metric-val">+0.45</div><div class="metric-delta">Quality Tier Gained</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    c1_twin, c2_twin = st.columns([4.5, 5.5])
    
    with c1_twin:
        st.markdown("<h3>📊 Trajectory Analytics Core</h3>", unsafe_allow_html=True)
        if st.button("🧬 Compile Predictive Patient Trajectory Map", type="primary", use_container_width=True):
            st.session_state["twin_executed"] = True
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.metric(label="90-Day Unplanned Escalation Risk Index", value="78%" if st.session_state["twin_executed"] else "0%", delta="CRITICAL RISK TIER" if st.session_state["twin_executed"] else "Awaiting Run")
        
        if st.session_state["twin_executed"]:
            st.error(f"**Primary Underlying Structural Risk Drivers:**\n\n{case_data['risk_drivers']}")

    with c2_twin:
        st.markdown("<h3>🚀 Micro-Agent Proactive Interventions</h3>", unsafe_allow_html=True)
        twin_status = "twin" if st.session_state["twin_executed"] else "idle"
        twin_cls = "badge-twin" if st.session_state["twin_executed"] else "badge-idle"
        
        ta, tb = st.columns(2)
        with ta:
            st.markdown(f'<div class="agent-box"><div class="agent-header-row"><span class="agent-title">💊 Pharmacy Optimizer</span><span class="agent-badge {twin_cls}">{twin_status}</span></div><div style="font-size:0.85rem; color:#475569;">Rerouting patient to Tier-1 generic alternatives to eliminate out-of-pocket barriers.</div></div>', unsafe_allow_html=True)
            if st.session_state["twin_executed"] and st.button("Confirm Generic Rx Swaps", key="nav_rx"):
                st.session_state["pharmacy_ok"] = True
            if st.session_state["pharmacy_ok"]:
                st.toast("✅ Optimized pharmaceutical script routed to network loops.")
                st.session_state["pharmacy_ok"] = False
                
            st.markdown(f'<div class="agent-box"><div class="agent-header-row"><span class="agent-title">🚗 SDOH Transport Dispatch</span><span class="agent-badge {twin_cls}">{twin_status}</span></div><div style="font-size:0.85rem; color:#475569;">Dispatching medical transit resource vouchers to handle clinical attendance gaps.</div></div>', unsafe_allow_html=True)
            if st.session_state["twin_executed"] and st.button("Dispatch Ride Vouchers", key="nav_ride"):
                st.session_state["ride_ok"] = True
            if st.session_state["ride_ok"]:
                st.toast("✅ Lyft/Uber Healthcare transit parameters deployed.")
                st.session_state["ride_ok"] = False

        with tb:
            st.markdown(f'<div class="agent-box"><div class="agent-header-row"><span class="agent-title">📅 Scheduling Coordinator</span><span class="agent-badge {twin_cls}">{twin_status}</span></div><div style="font-size:0.85rem; color:#475569;">Staging an immediate tracking preventative follow-up window inside the network.</div></div>', unsafe_allow_html=True)
            if st.session_state["twin_executed"] and st.button("Lock Provider Block", key="nav_pcp"):
                st.session_state["pcp_ok"] = True
            if st.session_state["pcp_ok"]:
                st.toast("✅ Preventative care appointment slot locked on network calendar.")
                st.session_state["pcp_ok"] = False
                
            st.markdown(f'<div class="agent-box"><div class="agent-header-row"><span class="agent-title">🗣️ Engagement Core</span><span class="agent-badge {twin_cls}">{twin_status}</span></div><div style="font-size:0.85rem; color:#475569;">Translating priorities into crisp behavioral coaching paths for care manager outreach.</div></div>', unsafe_allow_html=True)
            if st.session_state["twin_executed"] and st.button("Deploy Coaching Script", key="nav_coach"):
                st.session_state["coach_ok"] = True
            if st.session_state["coach_ok"]:
                st.toast("✅ Customized script synchronized to care management console.")
                st.session_state["coach_ok"] = False
