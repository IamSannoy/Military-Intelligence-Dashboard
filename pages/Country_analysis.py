import streamlit as st
import plotly.express as px
from utils.data_loader import load_data
from utils.ui import load_css

# -------------------------------------------------------
# Page Configuration
# -------------------------------------------------------

st.set_page_config(
    page_title="Country Intelligence Analysis",
    page_icon="🌎",
    layout="wide"
)

load_css()

# -------------------------------------------------------
# Header
# -------------------------------------------------------

st.markdown("""
<div class="page-header">
<h1>🌎 Country Intelligence Analysis</h1>

<p>
Analyze terrorism activity for an individual country using
historical intelligence from the Global Terrorism Database.
View trends, organizations, attack methods, geographic
distribution, and AI-assisted intelligence insights.
</p>

</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# Load Dataset
# -------------------------------------------------------

with st.spinner("Loading intelligence database..."):
    df = load_data()

# -------------------------------------------------------
# Sidebar
# -------------------------------------------------------

st.sidebar.header("⚙ Intelligence Filters")

countries = sorted(df["country_txt"].dropna().unique())

country = st.sidebar.selectbox(
    "Country",
    countries,
    label_visibility="collapsed",
    placeholder="Select Country"
)
with st.spinner("Generating intelligence report..."):
    country_df = df[df["country_txt"] == country]

# -------------------------------------------------------
# Statistics
# -------------------------------------------------------

total_incidents = len(country_df)
fatalities = int(country_df["nkill"].fillna(0).sum())
injured = int(country_df["nwound"].fillna(0).sum())
groups = country_df["gname"].nunique()

# -------------------------------------------------------
# Intelligence Header
# -------------------------------------------------------

st.markdown(f"""
<div class="report-card">

<h2>📄 Intelligence Report</h2>

<b>Country:</b> {country}

</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# KPI Dashboard
# -------------------------------------------------------

st.markdown("## 📊 Key Intelligence Indicators")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Incidents", f"{total_incidents:,}")

with c2:
    st.metric("Fatalities", f"{fatalities:,}")

with c3:
    st.metric("Injuries", f"{injured:,}")

with c4:
    st.metric("Organizations", groups)

st.markdown("<br>", unsafe_allow_html=True)

# -------------------------------------------------------
# AI Summary
# -------------------------------------------------------

top_group = country_df["gname"].value_counts().idxmax()
top_attack = country_df["attacktype1_txt"].value_counts().idxmax()
top_weapon = country_df["weaptype1_txt"].value_counts().idxmax()

st.markdown("## 🧠 AI Intelligence Summary")

st.info(f"""
**Executive Assessment**

• Total recorded incidents: **{total_incidents:,}**

• Total fatalities: **{fatalities:,}**

• Most active terrorist organization:
**{top_group}**

• Most common attack method:
**{top_attack}**

• Most frequently used weapon:
**{top_weapon}**

The historical data indicates recurring operational
patterns that should be considered during strategic
planning and resource allocation.
""")

# -------------------------------------------------------
# Charts
# -------------------------------------------------------

left, right = st.columns(2)

with left:

    yearly = (
        country_df
        .groupby("iyear")
        .size()
        .reset_index(name="Attacks")
    )

    fig = px.line(
        yearly,
        x="iyear",
        y="Attacks",
        markers=True,
        title="Attacks Over Time"
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        height=430
    )

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with right:

    attack = (
        country_df
        .groupby("attacktype1_txt")
        .size()
        .reset_index(name="Count")
    )

    fig = px.pie(
        attack,
        names="attacktype1_txt",
        values="Count",
        hole=.45
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        height=430
    )

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------
# Organizations & Weapons
# -------------------------------------------------------

left, right = st.columns(2)

with left:

    groups_df = (
        country_df
        .groupby("gname")
        .size()
        .reset_index(name="Attacks")
        .sort_values("Attacks", ascending=False)
        .head(10)
    )

    fig = px.bar(
        groups_df,
        x="Attacks",
        y="gname",
        orientation="h",
        color="Attacks",
        color_continuous_scale="Reds"
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        height=450
    )

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with right:

    weapon_df = (
        country_df
        .groupby("weaptype1_txt")
        .size()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )

    fig = px.bar(
        weapon_df,
        x="weaptype1_txt",
        y="Count",
        color="Count",
        color_continuous_scale="Blues"
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        height=450
    )

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------
# Interactive Map
# -------------------------------------------------------

st.markdown("## 🌍 Incident Location Map")

map_df = country_df.dropna(
    subset=["latitude", "longitude"]
)

if len(map_df):

    with st.spinner("Rendering intelligence map..."):

        fig = px.scatter_geo(
            map_df,
            lat="latitude",
            lon="longitude",
            hover_name="city",
            hover_data={
                "country_txt":True,
                "iyear":True,
                "attacktype1_txt":True,
                "gname":True,
                "nkill":True,
                "latitude":False,
                "longitude":False
            },
            color="attacktype1_txt",
            projection="natural earth",
            height=650
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            margin=dict(l=0,r=0,t=20,b=0)
        )

        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------
# Data Table
# -------------------------------------------------------

st.markdown("## 📋 Incident Database")

cols = [
    "iyear",
    "city",
    "attacktype1_txt",
    "targtype1_txt",
    "weaptype1_txt",
    "gname",
    "nkill",
    "nwound"
]

st.dataframe(
    country_df[cols],
    use_container_width=True,
    hide_index=True
)

# -------------------------------------------------------
# Download
# -------------------------------------------------------

st.markdown("## 📥 Export Intelligence")

csv = country_df.to_csv(index=False).encode()

st.download_button(
    "📄 Download Country Intelligence Report",
    csv,
    file_name=f"{country}_intelligence.csv",
    mime="text/csv",
    use_container_width=True
)