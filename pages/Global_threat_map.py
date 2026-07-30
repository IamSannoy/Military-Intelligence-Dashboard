import streamlit as st
import plotly.express as px

from utils.data_loader import load_data
from utils.ui import load_css

# =====================================================
# Page Configuration
# =====================================================

st.set_page_config(
    page_title="Global Threat Map",
    page_icon="🌍",
    layout="wide"
)

load_css()

# =====================================================
# Premium Header
# =====================================================

st.markdown("""
<div class="page-header">

<h1>🌍 Global Threat Intelligence Map</h1>

<p>
Visualize worldwide terrorist incidents from the Global Terrorism
Database (GTD). Explore geographic patterns, historical events,
and intelligence insights through an interactive global map.
</p>

</div>
""", unsafe_allow_html=True)

# =====================================================
# Load Dataset
# =====================================================

with st.spinner("Loading global intelligence database..."):
    df = load_data()

# =====================================================
# Sidebar
# =====================================================

st.sidebar.header("⚙ Map Filters")

years = sorted(df["iyear"].dropna().unique())

year = st.sidebar.selectbox(
    "",
    ["All"] + sorted(df["iyear"].unique().tolist()),
    label_visibility="collapsed",
    placeholder="Select Year"
)

# =====================================================
# Apply Filters
# =====================================================

with st.spinner("Filtering intelligence records..."):

    filtered_df = df.copy()

    if year != "All":
        filtered_df = filtered_df[
            filtered_df["iyear"] == year
        ]

    filtered_df = filtered_df.dropna(
        subset=["latitude", "longitude"]
    )

# =====================================================
# Validate Data
# =====================================================

if filtered_df.empty:

    st.warning(
        "No incidents are available for the selected filter."
    )

    st.stop()

# =====================================================
# Intelligence Statistics
# =====================================================

total_incidents = len(filtered_df)

countries = filtered_df["country_txt"].nunique()

fatalities = int(
    filtered_df["nkill"].fillna(0).sum()
)

attack_types = filtered_df[
    "attacktype1_txt"
].nunique()

# =====================================================
# KPI Dashboard
# =====================================================

st.markdown("## 📊 Global Threat Overview")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Incidents",
        f"{total_incidents:,}"
    )

with c2:
    st.metric(
        "Countries",
        countries
    )

with c3:
    st.metric(
        "Fatalities",
        f"{fatalities:,}"
    )

with c4:
    st.metric(
        "Attack Types",
        attack_types
    )

# =====================================================
# AI Intelligence Summary
# =====================================================

top_country = (
    filtered_df["country_txt"]
    .value_counts()
    .idxmax()
)

top_attack = (
    filtered_df["attacktype1_txt"]
    .value_counts()
    .idxmax()
)

top_group = (
    filtered_df["gname"]
    .value_counts()
    .idxmax()
)

st.markdown("## 🧠 AI Intelligence Summary")

st.markdown(f"""
<div class="report-card">

<h3>📄 Executive Threat Assessment</h3>

<b>Total Incidents:</b> {total_incidents:,}<br><br>

<b>Countries Affected:</b> {countries}<br><br>

<b>Total Fatalities:</b> {fatalities:,}<br><br>

<b>Highest Activity Country:</b> {top_country}<br><br>

<b>Most Common Attack:</b> {top_attack}<br><br>

<b>Most Active Organization:</b> {top_group}<br><br>

<b>Assessment:</b><br>

The available intelligence indicates that
<b>{top_country}</b> experienced the greatest concentration
of recorded terrorist activity. The dominant attack method
was <b>{top_attack}</b>, while
<b>{top_group}</b> appears most frequently in the
selected dataset.

</div>
""", unsafe_allow_html=True)

# =====================================================
# Global Map
# =====================================================

st.markdown("## 🌍 Interactive Threat Map")

with st.spinner("Rendering global threat map..."):

    fig = px.scatter_geo(

        filtered_df,

        lat="latitude",

        lon="longitude",

        color="attacktype1_txt",

        hover_name="country_txt",

        hover_data={
            "city": True,
            "gname": True,
            "iyear": True,
            "nkill": True,
            "latitude": False,
            "longitude": False
        },

        projection="natural earth",

        height=700
    )

    fig.update_layout(

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        font_color="white",

        margin=dict(
            l=0,
            r=0,
            t=20,
            b=0
        ),

        legend=dict(
            bgcolor="rgba(0,0,0,0)"
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
# Intelligence Table
# =====================================================

st.markdown("## 📋 Incident Records")

columns = [

    "iyear",

    "country_txt",

    "city",

    "attacktype1_txt",

    "weaptype1_txt",

    "gname",

    "nkill"

]

st.dataframe(

    filtered_df[columns],

    use_container_width=True,

    hide_index=True
)

# =====================================================
# Download
# =====================================================

st.markdown("## 📥 Export Intelligence")

csv = filtered_df.to_csv(
    index=False
).encode()

st.download_button(

    "📄 Download Filtered Intelligence",

    data=csv,

    file_name="Global_Threat_Map_Data.csv",

    mime="text/csv",

    use_container_width=True
)

# =====================================================
# Footer
# =====================================================

st.caption(
    "Interactive visualization based on the Global Terrorism Database (GTD). Use the sidebar filters to refine the displayed intelligence."
)