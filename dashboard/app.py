from pathlib import Path
import pandas as pd
import streamlit as st

# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Olive Dating — M&E Platform",
    page_icon="🫒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# 2. CUSTOM CSS & UI SYSTEM
# ============================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Main App Background */
    .stApp {
        background-color: #FAFAF9;
    }

    /* ---------------- SIDEBAR REDESIGN ---------------- */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E7E5E4 !important;
        padding-top: 1.2rem;
    }

    /* Brand Header */
    .brand-box {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 8px 6px 18px 6px;
        border-bottom: 1px solid #F5F5F4;
        margin-bottom: 20px;
    }

    .brand-title {
        font-size: 1.15rem;
        font-weight: 800;
        color: #1C1917;
        line-height: 1.1;
        letter-spacing: -0.02em;
    }

    .brand-badge {
        font-size: 0.65rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #556B2F;
        background-color: #F4F6F0;
        padding: 2px 7px;
        border-radius: 4px;
        display: inline-block;
        margin-top: 4px;
    }

    /* --- TURN RADIO BUTTONS INTO ELEVATED BUTTON TILES --- */
    div[data-testid="stRadio"] > label {
        display: none !important;
    }

    div[data-testid="stRadio"] div[role="radiogroup"] {
        gap: 8px;
        display: flex;
        flex-direction: column;
    }

    /* Unselected Button Style */
    div[data-testid="stRadio"] div[role="radiogroup"] > label {
        background-color: #FBFBFA !important;
        border: 1px solid #E7E5E4 !important;
        border-radius: 10px !important;
        padding: 12px 14px !important;
        margin: 0 !important;
        cursor: pointer !important;
        transition: all 0.18s ease-in-out !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02) !important;
    }

    /* Hide standard radio dot circle */
    div[data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child {
        display: none !important;
    }

    /* Label text typography */
    div[data-testid="stRadio"] div[role="radiogroup"] > label p {
        font-size: 0.88rem !important;
        font-weight: 600 !important;
        color: #44403C !important;
        margin: 0 !important;
    }

    /* Hover State */
    div[data-testid="stRadio"] div[role="radiogroup"] > label:hover {
        background-color: #F4F6F0 !important;
        border-color: #556B2F !important;
        transform: translateX(3px);
    }

    div[data-testid="stRadio"] div[role="radiogroup"] > label:hover p {
        color: #556B2F !important;
    }

    /* Active / Selected Button State */
    div[data-testid="stRadio"] div[role="radiogroup"] > label[data-checked="true"],
    div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) {
        background-color: #556B2F !important;
        border-color: #556B2F !important;
        box-shadow: 0 4px 10px rgba(85, 107, 47, 0.25) !important;
    }

    div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) p {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }

    /* Sidebar Footer Info Card */
    .sidebar-footer {
        background-color: #FAFAF9;
        border: 1px solid #E7E5E4;
        border-radius: 10px;
        padding: 12px;
        margin-top: 36px;
    }

    .pulse-dot {
        height: 8px;
        width: 8px;
        background-color: #10B981;
        border-radius: 50%;
        display: inline-block;
        margin-right: 6px;
    }

    /* ---------------- MAIN DASHBOARD COMPONENTS ---------------- */
    /* Metric KPI Tiles */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E7E5E4;
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
        transition: transform 0.15s ease-in-out, border-color 0.15s ease-in-out;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        border-color: #556B2F;
        box-shadow: 0 6px 12px -2px rgba(85, 107, 47, 0.08);
    }

    div[data-testid="stMetricLabel"] {
        font-size: 0.8rem !important;
        font-weight: 700 !important;
        color: #78716C !important;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    div[data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: 800 !important;
        color: #1C1917 !important;
    }

    /* Custom Qualitative Cards */
    .eval-card {
        background-color: #FFFFFF;
        border: 1px solid #E7E5E4;
        border-left: 4px solid #556B2F;
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }

    .pill-target {
        display: inline-block;
        padding: 3px 9px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        background-color: #F5F5F4;
        color: #44403C;
        margin-right: 6px;
    }

    .pill-gap {
        display: inline-block;
        padding: 3px 9px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        background-color: #FEF2F2;
        color: #DC2626;
    }

    hr {
        border: 0;
        height: 1px;
        background: #E7E5E4;
        margin: 24px 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# 3. PATHS & DATA INGESTION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

EXECUTIVE_FILE = PROCESSED_DIR / "executive_metrics.csv"
ME_FILE = PROCESSED_DIR / "me_evaluation.csv"

@st.cache_data
def load_data():
    if not EXECUTIVE_FILE.exists() or not ME_FILE.exists():
        st.error(
            "Processed metrics files not found. From the project root, "
            "run `python src/generate_metrics.py` after generating and cleaning the data."
        )
        st.stop()

    executive = pd.read_csv(EXECUTIVE_FILE)
    me = pd.read_csv(ME_FILE)
    return executive, me

df, me = load_data()

if df.empty:
    st.error("Executive metrics contain no rows. Regenerate the processed metrics.")
    st.stop()

# Data normalization and sanitization
numeric_columns = [
    "new_users", "profile_completion", "active_users", "sessions",
    "matches", "messages", "retention_7_day_pct", "retention_30_day_pct",
    "churn_rate_pct", "sessions_per_active_user", "matches_per_active_user",
    "messages_per_active_user"
]

for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

cohort_metrics = df.dropna(
    subset=[
        "profile_completion",
        "retention_7_day_pct",
        "retention_30_day_pct",
    ]
)
activity_metrics = df[df["active_users"] > 0]

if cohort_metrics.empty or activity_metrics.empty:
    st.error("Executive metrics do not contain a complete user cohort and activity month.")
    st.stop()

latest_cohort = cohort_metrics.iloc[-1]
latest_activity = activity_metrics.iloc[-1]

# ============================================================
# 4. SIDEBAR NAVIGATION
# ============================================================

with st.sidebar:
    # Logo & Brand
    st.markdown(
        """
        <div class="brand-box">
            <svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect width="40" height="40" rx="10" fill="#556B2F"/>
                <ellipse cx="20" cy="23" rx="9" ry="11" fill="#E8F0E6"/>
                <circle cx="20" cy="23" r="4.5" fill="#556B2F"/>
                <path d="M20 12C20 8 25 6 27 8" stroke="#E8F0E6" stroke-width="2.5" stroke-linecap="round"/>
                <path d="M22 10C25 10 28 12 29 14" stroke="#A3B18A" stroke-width="2" stroke-linecap="round"/>
            </svg>
            <div>
                <div class="brand-title">Olive Dating</div>
                <div class="brand-badge">M&E Data Platform</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        "<p style='font-size: 0.72rem; font-weight: 700; color: #A8A29E; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px;'>Navigation</p>",
        unsafe_allow_html=True,
    )

    nav_selection = st.radio(
        "Navigation",
        [
            "📊  Executive Overview",
            "💬  Engagement Monitoring",
            "📉  Retention & Churn",
            "🎯  Evaluation & Matrix",
        ],
        label_visibility="collapsed",
    )

    # Normalize selection string for clean routing
    current_page = nav_selection.split("  ")[-1].strip()

    st.markdown(
        """
        <div class="sidebar-footer">
            <div style="font-size: 0.75rem; font-weight: 700; color: #292524; margin-bottom: 4px;">
                <span class="pulse-dot"></span>Pipeline Operational
            </div>
            <div style="font-size: 0.72rem; color: #78716C;">Environment: <strong>Synthetic Prod</strong></div>
            <div style="font-size: 0.72rem; color: #78716C;">Markets: <strong>MENA & USA</strong></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# 5. VIEW ROUTER & PAGES
# ============================================================

st.title("Olive Dating — M&E Analytics Platform")
st.caption("Strategic cross-functional data monitoring user lifecycle, active engagement, and program targets.")
st.write("")

# ------------------------------------------------------------
# PAGE 1: EXECUTIVE OVERVIEW
# ------------------------------------------------------------
if current_page == "Executive Overview":
    st.markdown(
        f"#### 📊 Monthly Performance Summary &nbsp;•&nbsp; "
        f"`Cohort: {latest_cohort['month']} | Activity: {latest_activity['month']}`"
    )
    st.write("")

    # KPI Topline Cards
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("New Signups", f"{latest_cohort['new_users']:,.0f}")
    k2.metric("Active Users", f"{latest_activity['active_users']:,.0f}")
    k3.metric("Profile Setup", f"{latest_cohort['profile_completion']:.1f}%")
    k4.metric("7-Day Retention", f"{latest_cohort['retention_7_day_pct']:.1f}%")
    k5.metric("30-Day Retention", f"{latest_cohort['retention_30_day_pct']:.1f}%")

    st.divider()

    # Trend Charts
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("##### 📈 Growth & User Activity Volume")
        engagement = df[["month", "active_users", "sessions", "matches", "messages"]].set_index("month")
        st.line_chart(engagement, color=["#556B2F", "#A3B18A", "#D4A373", "#78716C"])

    with c2:
        st.markdown("##### 🔄 Cohort Retention Curves (%)")
        retention = df[["month", "retention_7_day_pct", "retention_30_day_pct"]].set_index("month")
        st.line_chart(retention, color=["#556B2F", "#D4A373"])

# ------------------------------------------------------------
# PAGE 2: ENGAGEMENT MONITORING
# ------------------------------------------------------------
elif current_page == "Engagement Monitoring":
    st.markdown("#### 💬 User Activity & Behavioral Touchpoints")
    st.write("")

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Monthly Active Users", f"{latest_activity['active_users']:,.0f}")
    k2.metric("Total Sessions", f"{latest_activity['sessions']:,.0f}")
    k3.metric("Matches Formed", f"{latest_activity['matches']:,.0f}")
    k4.metric("Messages Sent", f"{latest_activity['messages']:,.0f}")

    st.divider()

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("##### App Sessions Volume")
        st.line_chart(df[["month", "sessions"]].set_index("month"), color="#556B2F")
        st.markdown("##### Matches Created")
        st.line_chart(df[["month", "matches"]].set_index("month"), color="#A3B18A")

    with c2:
        st.markdown("##### Messages Exchanged")
        st.line_chart(df[["month", "messages"]].set_index("month"), color="#D4A373")
        st.markdown("##### Profile Completion Rate (%)")
        st.line_chart(df[["month", "profile_completion"]].set_index("month"), color="#606C38")

# ------------------------------------------------------------
# PAGE 3: RETENTION & CHURN
# ------------------------------------------------------------
elif current_page == "Retention & Churn":
    st.markdown("#### 📉 Cohort Decay & Churn Tracking")
    st.write("")

    k1, k2, k3 = st.columns(3)
    k1.metric("7-Day Retention", f"{latest_cohort['retention_7_day_pct']:.1f}%")
    k2.metric("30-Day Retention", f"{latest_cohort['retention_30_day_pct']:.1f}%")
    k3.metric(
        "30-Day Cohort Churn",
        f"{latest_cohort['churn_rate_pct']:.1f}%",
        delta_color="inverse",
    )

    st.divider()

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("##### Retention Cohort Stability")
        st.line_chart(df[["month", "retention_7_day_pct", "retention_30_day_pct"]].set_index("month"), color=["#556B2F", "#D4A373"])

    with c2:
        st.markdown("##### 30-Day Churn by Signup Cohort (%)")
        st.line_chart(df[["month", "churn_rate_pct"]].set_index("month"), color="#DC2626")

    st.markdown("##### Touchpoint Frequency per Active User")
    freq = df[["month", "sessions_per_active_user", "matches_per_active_user", "messages_per_active_user"]].set_index("month")
    st.line_chart(freq, color=["#556B2F", "#A3B18A", "#D4A373"])

# ------------------------------------------------------------
# PAGE 4: EVALUATION & MATRIX
# ------------------------------------------------------------
elif current_page == "Evaluation & Matrix":
    st.markdown("#### 🎯 Monitoring & Evaluation (M&E) Target Matrix")
    st.caption("Qualitative benchmarks and performance indicators evaluated against operational targets.")
    st.write("")

    # Structured Table
    perf_table = me[["indicator", "target", "actual", "gap", "finding"]].copy()
    perf_table.columns = ["Strategic Indicator", "Target", "Actual", "Variance / Gap", "Key Finding"]

    st.dataframe(
        perf_table,
        use_container_width=True,
        hide_index=True,
    )

    st.divider()
    st.markdown("#### 📋 Findings & Strategic Interventions")

    for _, row in me.iterrows():
        st.markdown(
            f"""
            <div class="eval-card">
                <div style="font-size: 1.05rem; font-weight: 700; color: #1C1917; margin-bottom: 8px;">
                    📌 {row['indicator']}
                </div>
                <div style="margin-bottom: 12px;">
                    <span class="pill-target">🎯 Target: {row['target']}</span>
                    <span class="pill-target">📊 Actual: {row['actual']}</span>
                    <span class="pill-gap">Variance: {row['gap']}</span>
                </div>
                <p style="margin: 4px 0; font-size: 0.9rem;"><strong>Observed Finding:</strong> {row['finding']}</p>
                <p style="margin: 4px 0; font-size: 0.9rem;"><strong>Recommendation:</strong> {row['recommendation']}</p>
                <p style="margin: 4px 0; font-size: 0.9rem;"><strong>Product Intervention:</strong> {row['intervention']}</p>
                <p style="margin: 4px 0; font-size: 0.9rem; color: #78716C;"><strong>Follow-up Cycle:</strong> {row['follow_up']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )