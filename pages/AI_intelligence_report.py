import streamlit as st
import pandas as pd
import plotly.express as px
from utils.ui import load_css

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------

st.set_page_config(
    page_title="AI Intelligence Report",
    page_icon="🧠",
    layout="wide"
)

load_css()

# -------------------------------------------------
# Header
# -------------------------------------------------

st.markdown("""
<div class="page-header">
    <h1>🧠 AI Intelligence Report</h1>
    <p>
    AI-powered strategic intelligence generated from the
    Global Terrorism Database (GTD). Analyze worldwide
    terrorist activity, assess risks, and support
    intelligence-driven decision making.
    </p>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Load Dataset
# -------------------------------------------------

@st.cache_data
def load_data():
    return pd.read_csv(
        "data/globalterrorism.csv",
        encoding="latin1",
        low_memory=False
    )

df = load_data()

# -------------------------------------------------
# Sidebar
# -------------------------------------------------

st.sidebar.header("⚙ Intelligence Filters")

years = sorted(df["iyear"].dropna().unique())

year = st.sidebar.selectbox(
    "",
    ["All"] + sorted(df["iyear"].unique().tolist()),
    label_visibility="collapsed",
    placeholder="Select Year"
)

if year != "All":
    df = df[df["iyear"] == year]

# -------------------------------------------------
# Statistics
# -------------------------------------------------

total_incidents = len(df)
total_killed = int(df["nkill"].fillna(0).sum())
total_wounded = int(df["nwound"].fillna(0).sum())
countries = df["country_txt"].nunique()
groups = df["gname"].nunique()

top_countries = df["country_txt"].value_counts().head(10)
top_groups = df["gname"].value_counts().head(10)
attack_types = df["attacktype1_txt"].value_counts()
weapon_types = df["weaptype1_txt"].value_counts()

avg_killed = df["nkill"].fillna(0).mean()

if avg_killed < 2:
    threat = "🟢 LOW"
elif avg_killed < 5:
    threat = "🟡 MEDIUM"
else:
    threat = "🔴 HIGH"

# -------------------------------------------------
# KPI Dashboard
# -------------------------------------------------

st.markdown("## 📊 Intelligence Overview")

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.metric("Incidents", f"{total_incidents:,}")

with c2:
    st.metric("Fatalities", f"{total_killed:,}")

with c3:
    st.metric("Injuries", f"{total_wounded:,}")

with c4:
    st.metric("Countries", countries)

with c5:
    st.metric("Threat Level", threat)

st.markdown("<br>", unsafe_allow_html=True)

# -------------------------------------------------
# Executive Summary
# -------------------------------------------------

summary = f"""
### Executive Intelligence Summary

- **{total_incidents:,}** terrorist incidents were recorded.

- Activities occurred across **{countries} countries**.

- Total fatalities reached **{total_killed:,}**.

- Total injuries reached **{total_wounded:,}**.

- Current global threat assessment is **{threat}**.

- Highest-risk country:
  **{top_countries.index[0]}**

- Most active terrorist organization:
  **{top_groups.index[0]}**

- Primary attack method:
  **{attack_types.index[0]}**

- Most commonly used weapon:
  **{weapon_types.index[0]}**
"""

st.markdown(
    f"""
<div class="report-card">
{summary}
</div>
""",
    unsafe_allow_html=True,
)

# -------------------------------------------------
# Charts
# -------------------------------------------------

left, right = st.columns(2)

with left:

    st.markdown("""
    <div class="chart-card">
    <h3>🌍 Top 10 High-Risk Countries</h3>
    """, unsafe_allow_html=True)

    fig = px.bar(
        top_countries,
        x=top_countries.values,
        y=top_countries.index,
        orientation="h",
        color=top_countries.values,
        color_continuous_scale="Blues"
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        height=450
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

with right:

    st.markdown("""
    <div class="chart-card">
    <h3>🚨 Most Active Terrorist Groups</h3>
    """, unsafe_allow_html=True)

    fig2 = px.bar(
        top_groups,
        x=top_groups.values,
        y=top_groups.index,
        orientation="h",
        color=top_groups.values,
        color_continuous_scale="Reds"
    )

    fig2.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        height=450
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------
# AI Assessment
# -------------------------------------------------

st.markdown("## 🤖 AI Intelligence Assessment")

assessment = f"""
### Strategic Recommendations

✅ Increase surveillance in **{top_countries.index[0]}**

✅ Monitor activities associated with **{top_groups.index[0]}**

✅ Strengthen protection of critical infrastructure

✅ Improve intelligence sharing among agencies

✅ Increase monitoring of explosive-based attacks

✅ Continue predictive threat modeling using AI and machine learning

✅ Allocate resources according to regional risk trends

✅ Review emergency preparedness for high-risk regions
"""

st.markdown(
    f"""
<div class="report-card">
{assessment}
</div>
""",
    unsafe_allow_html=True,
)

# -------------------------------------------------
# Intelligence Snapshot
# -------------------------------------------------

st.markdown("## 📌 Intelligence Snapshot")

col1, col2 = st.columns(2)

with col1:
    st.info(
        f"""
Highest Risk Country

**{top_countries.index[0]}**

Incidents:
**{top_countries.iloc[0]:,}**
"""
    )

with col2:
    st.warning(
        f"""
Most Active Organization

**{top_groups.index[0]}**

Recorded Attacks:
**{top_groups.iloc[0]:,}**
"""
    )

# -------------------------------------------------
# Download Report
# -------------------------------------------------

report = f"""
====================================================

AI MILITARY INTELLIGENCE REPORT

====================================================

Year Selected : {year}

Total Incidents : {total_incidents:,}

Fatalities : {total_killed:,}

Injuries : {total_wounded:,}

Countries Affected : {countries}

Threat Level : {threat}

Highest Risk Country :
{top_countries.index[0]}

Most Active Group :
{top_groups.index[0]}

Most Common Attack :
{attack_types.index[0]}

Most Common Weapon :
{weapon_types.index[0]}

====================================================

STRATEGIC RECOMMENDATIONS

Increase surveillance in {top_countries.index[0]}

Monitor {top_groups.index[0]}

Improve intelligence sharing

Protect critical infrastructure

Continue AI-based forecasting

====================================================
"""

st.markdown("<br>", unsafe_allow_html=True)

st.download_button(
    "Download Intelligence Report",
    report,
    file_name="AI_Intelligence_Report.txt",
    use_container_width=True
)