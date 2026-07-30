import streamlit as st
import pandas as pd

from utils.ui import load_css

# =====================================================
# Page Configuration
# =====================================================

st.set_page_config(
    page_title="Dashboard Settings",
    page_icon="⚙️",
    layout="wide"
)

load_css()

# =====================================================
# Header
# =====================================================

st.markdown("""
<div class="page-header">

<h1>⚙️ Dashboard Settings</h1>

<p>
Configure the AI Military Intelligence Dashboard. Customize
visualization preferences, prediction settings, report options,
and review dataset information.
</p>

</div>
""", unsafe_allow_html=True)

# =====================================================
# Load Dataset
# =====================================================

@st.cache_data
def load_dataset():

    return pd.read_csv(
        "data/globalterrorism.csv",
        encoding="latin1",
        low_memory=False
    )


with st.spinner("Loading dashboard configuration..."):

    try:
        df = load_dataset()
        dataset_loaded = True
    except Exception:
        dataset_loaded = False

# =====================================================
# Dashboard Preferences
# =====================================================

st.markdown("## 🎛 Dashboard Preferences")

left, right = st.columns(2)

with left:

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)

    theme = st.selectbox(
        "Theme",
        [
            "Dark (Recommended)",
            "Light"
        ],
        label_visibility="collapsed",
        placeholder="..."
    )

    layout = st.selectbox(
        "Layout",
        [
            "Wide",
            "Centered"
        ]
    )

    default_country = st.text_input(
        "Default Country",
        "India"
    )

    forecast_years = st.slider(
        "Default Forecast Years",
        1,
        10,
        5
    )

    st.markdown("</div>", unsafe_allow_html=True)

with right:

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)

    confidence = st.slider(
        "Minimum Prediction Confidence (%)",
        50,
        100,
        80
    )

    show_probability = st.checkbox(
        "Show Prediction Confidence",
        True
    )

    show_ai_summary = st.checkbox(
        "Show AI Executive Summary",
        True
    )

    animations = st.checkbox(
        "Enable Animations",
        True
    )

    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# Report Settings
# =====================================================

st.markdown("## 📄 Intelligence Report Settings")

st.markdown('<div class="chart-card">', unsafe_allow_html=True)

report_format = st.selectbox(
    "Report Format",
    [
        "PDF",
        "Text",
        "Word"
    ],
    label_visibility="collapsed",
    placeholder="..."
)

include_charts = st.checkbox(
    "Include Charts",
    True
)

include_tables = st.checkbox(
    "Include Tables",
    True
)

include_recommendations = st.checkbox(
    "Include AI Recommendations",
    True
)

st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# Forecast Settings
# =====================================================

st.markdown("## 📈 Forecast Configuration")

st.markdown('<div class="chart-card">', unsafe_allow_html=True)

forecast_model = st.selectbox (
    "Forecasting Model",
    [
        "Linear Regression",
        "ARIMA",
        "Prophet"
    ],
    label_visibility="collapsed",
    placeholder="..."
)

forecast_period = st.slider(
    "Forecast Horizon (Years)",
    1,
    10,
    5
)

st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# Dataset Status
# =====================================================

st.markdown("## 📊 Dataset Information")

if dataset_loaded:

    rows = df.shape[0]
    cols = df.shape[1]
    countries = df["country_txt"].nunique()

    memory = round(
        df.memory_usage(deep=True).sum() / 1024**2,
        2
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Rows", f"{rows:,}")
    c2.metric("Columns", cols)
    c3.metric("Countries", countries)
    c4.metric("Memory", f"{memory} MB")

    st.success("Global Terrorism Database loaded successfully.")

else:

    st.error(
        "Unable to load the Global Terrorism Database."
    )

# =====================================================
# About Dashboard
# =====================================================

st.markdown("## 🛡 Dashboard Information")

st.markdown("""
<div class="report-card">

<h3>AI Military Intelligence Dashboard</h3>

<b>Version:</b> 1.0<br><br>

<b>Dataset:</b> Global Terrorism Database (GTD)<br><br>

<b>Modules:</b>

<ul>
<li>Global Threat Map</li>
<li>Country Analysis</li>
<li>Attack Prediction</li>
<li>Threat Level Prediction</li>
<li>Forecasting</li>
<li>AI Intelligence Report</li>
<li>Data Explorer</li>
</ul>

This dashboard combines historical terrorism data,
interactive analytics, and machine learning models
to support intelligence analysis and decision-making.

</div>
""", unsafe_allow_html=True)

# =====================================================
# Save Settings
# =====================================================

st.markdown("## 💾 Configuration")

left, right = st.columns(2)

with left:

    if st.button(
        "💾 Save Settings",
        use_container_width=True
    ):

        st.success(
            "Settings saved successfully."
        )

        st.balloons()

with right:

    if st.button(
        "🔄 Restore Defaults",
        use_container_width=True
    ):

        st.info(
            "Default settings restored."
        )

# =====================================================
# Footer
# =====================================================

st.caption(
    "AI Military Intelligence Dashboard • Configuration Panel"
)