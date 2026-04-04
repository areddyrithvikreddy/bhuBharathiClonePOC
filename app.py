import streamlit as st
from src.data.dummy_data import land_data
from src.models.land_data_key import LandDataKey
from src.enums.land_dropdowns import District, Mandal, Village, SurveyNumber, KhataNumber


st.set_page_config(
    page_title="Bhu Bharathi | Telangana Land Records",
    page_icon="🌾",
    layout="centered",
    initial_sidebar_state="collapsed",
)


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tiro+Devanagari+Hindi&family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

/* ── Root tokens ── */
:root {
    --green-700: #15803d;
    --green-600: #16a34a;
    --green-500: #22c55e;
    --green-100: #dcfce7;
    --green-50:  #f0fdf4;
    --amber-500: #f59e0b;
    --amber-100: #fef3c7;
    --red-500:   #ef4444;
    --red-100:   #fee2e2;
    --radius:    12px;
    --radius-sm: 8px;
    --shadow:    0 4px 24px rgba(0,0,0,.08);
    --shadow-lg: 0 8px 40px rgba(0,0,0,.12);
}

/* ── Light mode surface tokens ── */
[data-theme="light"], .stApp {
    --bg:        #f8fafc;
    --surface:   #ffffff;
    --surface-2: #f1f5f9;
    --border:    #e2e8f0;
    --border-2:  #cbd5e1;
    --text-1:    #0f172a;
    --text-2:    #475569;
    --text-3:    #94a3b8;
    --accent:    var(--green-600);
    --accent-bg: var(--green-50);
    --th-bg:     #f1f5f9;
    --tr-alt:    #f8fafc;
    --tr-hover:  #ecfdf5;
    --badge-bg:  var(--green-100);
    --badge-txt: var(--green-700);
}

/* ── Dark mode surface tokens ── */
@media (prefers-color-scheme: dark) {
    .stApp {
        --bg:        #0d1117;
        --surface:   #161b22;
        --surface-2: #21262d;
        --border:    #30363d;
        --border-2:  #484f58;
        --text-1:    #e6edf3;
        --text-2:    #8b949e;
        --text-3:    #6e7681;
        --accent:    var(--green-500);
        --accent-bg: #0d2818;
        --th-bg:     #21262d;
        --tr-alt:    #1a1f27;
        --tr-hover:  #0d2818;
        --badge-bg:  #0d2818;
        --badge-txt: var(--green-500);
    }
}

/* ── Reset & base ── */
* { box-sizing: border-box; }

.stApp {
    background: var(--bg) !important;
    font-family: 'DM Sans', sans-serif !important;
    color: var(--text-1) !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 2.5rem 1.5rem 4rem !important;
    max-width: 780px !important;
}

/* ── Hero banner ── */
.hero-banner {
    background: linear-gradient(135deg, #15803d 0%, #166534 50%, #14532d 100%);
    border-radius: var(--radius);
    padding: 2.5rem 2rem;
    text-align: center;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    box-shadow: var(--shadow-lg);
}
.hero-banner::before {
    content: '';
    position: absolute; inset: 0;
    background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.04'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
}
.hero-title {
    font-family: 'Tiro Devanagari Hindi', serif;
    font-size: 2.2rem;
    color: #ffffff;
    margin: 0 0 0.25rem;
    letter-spacing: -0.5px;
    position: relative;
}
.hero-subtitle {
    font-family: 'DM Sans', sans-serif;
    font-size: 1rem;
    color: rgba(255,255,255,0.78);
    margin: 0;
    font-weight: 400;
    position: relative;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 999px;
    padding: 4px 14px;
    font-size: 0.75rem;
    color: rgba(255,255,255,0.9);
    margin-bottom: 1rem;
    position: relative;
}

/* ── Card container ── */
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.75rem;
    margin-bottom: 1.25rem;
    box-shadow: var(--shadow);
}
.card-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 1.25rem;
    padding-bottom: 0.875rem;
    border-bottom: 1px solid var(--border);
}
.card-icon {
    width: 36px; height: 36px;
    background: var(--accent-bg);
    border-radius: var(--radius-sm);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
}
.card-title {
    font-size: 1rem;
    font-weight: 600;
    color: var(--text-1);
    margin: 0;
    letter-spacing: -0.2px;
}

/* ── Data table ── */
.data-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.875rem;
    font-family: 'DM Sans', sans-serif;
}
.data-table th {
    background: var(--th-bg);
    color: var(--text-2);
    font-weight: 600;
    font-size: 0.775rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    padding: 10px 14px;
    text-align: left;
    width: 38%;
    border: 1px solid var(--border);
}
.data-table td {
    padding: 10px 14px;
    color: var(--text-1);
    border: 1px solid var(--border);
    font-weight: 500;
}
.data-table tr:nth-child(even) td { background: var(--tr-alt); }
.data-table tr:hover td { background: var(--tr-hover); transition: background .15s; }

/* Value emphasis */
.val-currency {
    font-family: 'DM Mono', monospace;
    font-weight: 600;
    color: var(--accent);
    font-size: 0.9rem;
}
.val-badge {
    display: inline-block;
    background: var(--badge-bg);
    color: var(--badge-txt);
    border-radius: 6px;
    padding: 2px 10px;
    font-size: 0.78rem;
    font-weight: 600;
}

/* ── Info panel ── */
.info-panel {
    background: var(--accent-bg);
    border: 1px solid var(--border);
    border-left: 4px solid var(--accent);
    border-radius: var(--radius-sm);
    padding: 1rem 1.25rem;
    margin-bottom: 1.5rem;
    color: var(--text-2);
    font-size: 0.875rem;
    line-height: 1.5;
}

/* ── Error box ── */
.error-box {
    background: var(--red-100);
    border: 1px solid #fecaca;
    border-left: 4px solid var(--red-500);
    border-radius: var(--radius-sm);
    padding: 1rem 1.25rem;
    color: #991b1b;
    font-size: 0.875rem;
    display: flex; align-items: center; gap: 10px;
}
@media (prefers-color-scheme: dark) {
    .error-box { background: #2d0f0f; border-color: #7f1d1d; color: #fca5a5; }
}

/* ── Section divider ── */
.section-label {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text-3);
    margin: 1.75rem 0 0.75rem;
}

/* ── Streamlit widget overrides ── */
div[data-testid="stSelectbox"] label,
div[data-testid="stTextInput"] label {
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    color: var(--text-2) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    margin-bottom: 4px !important;
}
div[data-testid="stSelectbox"] > div > div {
    background: var(--surface) !important;
    border: 1.5px solid var(--border-2) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-1) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
}
div[data-testid="stSelectbox"] > div > div:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(34,197,94,.15) !important;
}

/* ── Buttons ── */
.stButton > button {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    border-radius: var(--radius-sm) !important;
    border: none !important;
    padding: 0.6rem 1.6rem !important;
    transition: all .2s !important;
    cursor: pointer !important;
}
/* Primary CTA */
.stButton > button[kind="primary"],
.stButton > button:not([kind="secondary"]) {
    background: linear-gradient(135deg, #16a34a, #15803d) !important;
    color: #fff !important;
    box-shadow: 0 2px 8px rgba(21,128,61,.35) !important;
}
.stButton > button:not([kind="secondary"]):hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(21,128,61,.45) !important;
}
/* Back button */
.stButton > button[kind="secondary"] {
    background: var(--surface-2) !important;
    color: var(--text-2) !important;
    border: 1.5px solid var(--border-2) !important;
}
.stButton > button[kind="secondary"]:hover {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
}

/* ── Form grid helper ── */
.form-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0 1rem;
}

/* ── Footer ── */
.portal-footer {
    text-align: center;
    font-size: 0.75rem;
    color: var(--text-3);
    margin-top: 3rem;
    padding-top: 1rem;
    border-top: 1px solid var(--border);
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Dropdown Options
# -----------------------------
districts      = [d.value for d in District]
mandals        = [m.value for m in Mandal]
villages       = [v.value for v in Village]
survey_numbers = [s.value for s in SurveyNumber]
khata_numbers  = [k.value for k in KhataNumber]

# -----------------------------
# App State
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

# ════════════════════════════════════════════
# HOME PAGE
# ════════════════════════════════════════════
if st.session_state.page == "home":

    st.markdown("""
    <div class="hero-banner">
        <div class="hero-badge">🌐 Government of Telangana</div>
        <h1 class="hero-title">🌾 Bhu Bharathi</h1>
        <p class="hero-subtitle">Telangana Land Records Portal — Transparent · Accessible · Reliable</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-panel">
        <strong>About this portal:</strong> Bhu Bharathi provides instant access to land ownership records,
        pattadar details, and property valuations across all districts of Telangana.
        Records are updated as per the latest ROR (Rights of Record) data.
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔍  Check Land Details", use_container_width=True):
            st.session_state.page = "form"
            st.rerun()

    st.markdown("""
    <div class="portal-footer">
        Revenue Department · Government of Telangana &nbsp;|&nbsp; For support: 1800-599-4788
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════
# FORM PAGE
# ════════════════════════════════════════════
elif st.session_state.page == "form":

    st.markdown("""
    <div class="hero-banner" style="padding:1.75rem 2rem;">
        <h1 class="hero-title" style="font-size:1.6rem;">🔍 Land Record Search</h1>
        <p class="hero-subtitle">Select location details to retrieve land records</p>
    </div>
    """, unsafe_allow_html=True)

    # --- Location selectors ---
    st.markdown('<div class="section-label">📍 Location Details</div>', unsafe_allow_html=True)
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            district = st.selectbox("District", districts)
        with col2:
            mandal = st.selectbox("Mandal", mandals)

        col3, col4 = st.columns(2)
        with col3:
            village = st.selectbox("Village", villages)
        with col4:
            survey_no = st.selectbox("Survey No. / Sub-division", survey_numbers)

        khata_no = st.selectbox("Khata Number", khata_numbers)

    st.markdown("<br>", unsafe_allow_html=True)

    col_back, col_spacer, col_submit = st.columns([1, 0.2, 2])
    with col_back:
        if st.button("⬅ Back", key="back_btn", type="secondary"):
            st.session_state.page = "home"
            st.rerun()
    with col_submit:
        submit = st.button("🔍  Search Records", key="submit_btn", use_container_width=True)

    # --- Results ---
    if submit:
        key = LandDataKey(
            District(district),
            Mandal(mandal),
            Village(village),
            SurveyNumber(survey_no),
            KhataNumber(khata_no)
        )

        if key in land_data:
            data = land_data[key]

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="section-label">📋 Search Results</div>', unsafe_allow_html=True)

            # ── Pattadar Card ──
            st.markdown(f"""
            <div class="card">
                <div class="card-header">
                    <div class="card-icon">👤</div>
                    <span class="card-title">Pattadar Details</span>
                </div>
                <table class="data-table">
                    <tr><th>District</th>          <td>{district}</td></tr>
                    <tr><th>Mandal</th>             <td>{mandal}</td></tr>
                    <tr><th>Village</th>            <td>{village}</td></tr>
                    <tr><th>Survey No.</th>         <td><span class="val-badge">{survey_no}</span></td></tr>
                    <tr><th>Khata No.</th>          <td><span class="val-badge">{khata_no}</span></td></tr>
                    <tr><th>Pattadar Name</th>      <td><strong>{data.pattadar_name}</strong></td></tr>
                    <tr><th>Father's Name</th>      <td>{data.father_name}</td></tr>
                </table>
            </div>
            """, unsafe_allow_html=True)

            # ── Land Details Card ──
            nature_label = data.nature.name.replace('_', ' ').title()
            classification_label = data.classification.name.title()

            st.markdown(f"""
            <div class="card">
                <div class="card-header">
                    <div class="card-icon">🌱</div>
                    <span class="card-title">Land Details</span>
                </div>
                <table class="data-table">
                    <tr><th>Land Size</th>          <td><strong>{data.land_size}</strong></td></tr>
                    <tr><th>Nature of Land</th>     <td><span class="val-badge">{nature_label}</span></td></tr>
                    <tr><th>Classification</th>     <td><span class="val-badge">{classification_label}</span></td></tr>
                    <tr><th>Market Value</th>        <td><span class="val-currency">₹{data.market_value:,.0f}</span></td></tr>
                </table>
            </div>
            """, unsafe_allow_html=True)

        else:
            st.markdown("""
            <div class="error-box">
                ⚠️ <span><strong>No records found</strong> — The selected combination did not match any land records. Please verify your inputs and try again.</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div class="portal-footer">
        Revenue Department · Government of Telangana &nbsp;|&nbsp; For support: 1800-599-4788
    </div>
    """, unsafe_allow_html=True)
