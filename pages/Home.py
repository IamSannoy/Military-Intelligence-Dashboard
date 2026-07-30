import streamlit as st
import plotly.express as px

from utils.data_loader import load_data
from utils.ui import load_css

# =====================================================
# Page Configuration
# =====================================================

st.set_page_config(
    page_title="Military Intelligence Dashboard",
    page_icon="🛡️",
    layout="wide"
)

load_css()

# =====================================================
# Premium Header
# =====================================================

st.markdown("""
<div class="page-header">

<h1>🛡 AI Military Intelligence Dashboard</h1>

<p>
Welcome to the AI-powered Military Intelligence Dashboard.
This platform analyzes historical terrorism incidents from the
Global Terrorism Database (GTD) to provide interactive
visualizations, predictive analytics, and intelligence-driven
decision support.
</p>

</div>
""", unsafe_allow_html=True)

# =====================================================
# Load Dataset
# =====================================================

with st.spinner("Loading intelligence database..."):
    df = load_data()

# =====================================================
# Dashboard Statistics
# =====================================================

total_incidents = len(df)

fatalities = int(df["nkill"].fillna(0).sum())

injuries = int(df["nwound"].fillna(0).sum())

countries = df["country_txt"].nunique()

attack_types = df["attacktype1_txt"].nunique()

groups = df["gname"].nunique()

# =====================================================
# KPI Dashboard
# =====================================================

st.markdown("## 📊 Global Intelligence Overview")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Total Incidents",
        f"{total_incidents:,}"
    )

with c2:
    st.metric(
        "Fatalities",
        f"{fatalities:,}"
    )

with c3:
    st.metric(
        "Injuries",
        f"{injuries:,}"
    )

c4, c5, c6 = st.columns(3)

with c4:
    st.metric(
        "Countries",
        countries
    )

with c5:
    st.metric(
        "Attack Types",
        attack_types
    )

with c6:
    st.metric(
        "Organizations",
        groups
    )

# =====================================================
# AI Intelligence Summary
# =====================================================

top_country = df["country_txt"].value_counts().idxmax()

top_attack = df["attacktype1_txt"].value_counts().idxmax()

top_group = df["gname"].value_counts().idxmax()

top_weapon = df["weaptype1_txt"].value_counts().idxmax()

st.markdown("## 🧠 AI Executive Summary")

st.markdown(f"""
<div class="report-card">

<h3>📄 Global Intelligence Assessment</h3>

<b>Total Recorded Incidents:</b> {total_incidents:,}<br><br>

<b>Countries Monitored:</b> {countries}<br><br>

<b>Total Fatalities:</b> {fatalities:,}<br><br>

<b>Total Injuries:</b> {injuries:,}<br><br>

<b>Highest Activity Country:</b> {top_country}<br><br>

<b>Most Common Attack Type:</b> {top_attack}<br><br>

<b>Most Frequently Used Weapon:</b> {top_weapon}<br><br>

<b>Most Active Organization:</b> {top_group}<br><br>

<b>Assessment:</b><br>

Historical GTD intelligence indicates persistent terrorist
activity across multiple regions. The dashboard provides
decision-support capabilities through trend analysis,
interactive mapping, machine learning predictions,
forecasting, and intelligence reporting.

</div>
""", unsafe_allow_html=True)

# =====================================================
# Attack Trend
# =====================================================

st.markdown("## 📈 Terrorism Trend Over Time")

with st.spinner("Generating historical trend..."):

    yearly = (
        df.groupby("iyear")
        .size()
        .reset_index(name="Attacks")
    )

    fig = px.line(
        yearly,
        x="iyear",
        y="Attacks",
        markers=True,
        title="Historical Terrorism Activity"
    )

    fig.update_layout(

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        font_color="white",

        height=500,

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        )
    )

    st.markdown(
        '<div class="chart-card">',
        unsafe_allow_html=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

# =====================================================
# Top 10 Countries
# =====================================================

st.markdown("## 🌍 Top 10 Most Affected Countries")

country_chart = (
    df["country_txt"]
    .value_counts()
    .head(10)
    .reset_index()
)

country_chart.columns = [
    "Country",
    "Incidents"
]

fig = px.bar(
    country_chart,
    x="Country",
    y="Incidents",
    color="Incidents",
    color_continuous_scale="Reds"
)

fig.update_layout(

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="rgba(0,0,0,0)",

    font_color="white",

    height=500
)

st.markdown(
    '<div class="chart-card">',
    unsafe_allow_html=True
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown(
    "</div>",
    unsafe_allow_html=True
)

# =====================================================
# Quick Navigation
# =====================================================

st.markdown("## 🚀 Intelligence Modules")

st.info("""
### Available Modules

🗺 **Global Threat Map**
- Explore incidents geographically.

🌎 **Country Analysis**
- Analyze terrorism trends for individual countries.

🤖 **Attack Prediction**
- Predict attack types using machine learning.

🚨 **Threat Level Prediction**
- Estimate threat severity from incident information.

📈 **Forecasting**
- Forecast future terrorism trends.

🧠 **AI Intelligence Report**
- Generate executive intelligence summaries.

📊 **Data Explorer**
- Search, filter, visualize, and export GTD data.
""")

# =====================================================
# Footer
# =====================================================

st.caption(
    "AI Military Intelligence Dashboard • Powered by the Global Terrorism Database (GTD)"
)