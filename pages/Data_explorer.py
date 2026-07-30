import streamlit as st
import pandas as pd
import plotly.express as px
from utils.ui import load_css
# --------------------------------------------------------
# Page Configuration
# --------------------------------------------------------

st.set_page_config(
    page_title="Data Explorer",
    page_icon="📊",
    layout="wide"
)
load_css()
st.title("📊 Global Terrorism Data Explorer")

st.markdown("Explore, filter, visualize and download the GTD dataset.")

# --------------------------------------------------------
# Load Dataset
# --------------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv(
        "data/globalterrorism.csv",
        encoding="latin1",
        low_memory=False
    )
    return df

with st.spinner("Loading Global Terrorism Database..."):
    df = load_data()

# --------------------------------------------------------
# Sidebar Filters
# --------------------------------------------------------

st.sidebar.header("Filter Dataset")

# Year
years = sorted(df["iyear"].dropna().unique())
selected_year = st.sidebar.multiselect(
    "Select Year",
    years,
    default=[]
)

# Country
countries = sorted(df["country_txt"].dropna().unique())
selected_country = st.sidebar.multiselect(
    "Select Country",
    countries,
    default=[]
)

# Region
regions = sorted(df["region_txt"].dropna().unique())
selected_region = st.sidebar.multiselect(
    "Select Region",
    regions,
    default=[]
)

# Attack Type
attack_types = sorted(df["attacktype1_txt"].dropna().unique())
selected_attack = st.sidebar.multiselect(
    "Attack Type",
    attack_types,
    default=[]
)

# Weapon Type
weapons = sorted(df["weaptype1_txt"].dropna().unique())
selected_weapon = st.sidebar.multiselect(
    "Weapon Type",
    weapons,
    default=[]
)

# Terrorist Group
groups = sorted(df["gname"].dropna().unique())
selected_group = st.sidebar.multiselect(
    "Terrorist Group",
    groups,
    default=[]
)

# --------------------------------------------------------
# Apply Filters
# --------------------------------------------------------
with st.spinner("Applying filters..."):
 filtered_df = df.copy()

 if selected_year:
    filtered_df = filtered_df[
        filtered_df["iyear"].isin(selected_year)
    ]

 if selected_country:
    filtered_df = filtered_df[
        filtered_df["country_txt"].isin(selected_country)
    ]

 if selected_region:
    filtered_df = filtered_df[
        filtered_df["region_txt"].isin(selected_region)
    ]

 if selected_attack:
    filtered_df = filtered_df[
        filtered_df["attacktype1_txt"].isin(selected_attack)
    ]

 if selected_weapon:
    filtered_df = filtered_df[
        filtered_df["weaptype1_txt"].isin(selected_weapon)
    ]

 if selected_group:
    filtered_df = filtered_df[
        filtered_df["gname"].isin(selected_group)
    ]

# --------------------------------------------------------
# Search Box
# --------------------------------------------------------

search = st.text_input(
    "🔍 Search by City or Country"
)

if search:

    filtered_df = filtered_df[
        filtered_df["city"].fillna("").str.contains(
            search,
            case=False
        )
        |
        filtered_df["country_txt"].fillna("").str.contains(
            search,
            case=False
        )
    ]

# --------------------------------------------------------
# KPIs
# --------------------------------------------------------

st.subheader("Dataset Summary")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Incidents",
    len(filtered_df)
)

c2.metric(
    "Countries",
    filtered_df["country_txt"].nunique()
)

c3.metric(
    "Fatalities",
    int(filtered_df["nkill"].fillna(0).sum())
)

c4.metric(
    "Injuries",
    int(filtered_df["nwound"].fillna(0).sum())
)

# --------------------------------------------------------
# AI Dataset Summary
# --------------------------------------------------------

st.markdown("## 🧠 AI Intelligence Summary")

if filtered_df.empty:

    st.warning("No records match the selected filters.")

else:

    primary_region = (
        filtered_df["region_txt"].mode().iloc[0]
        if not filtered_df["region_txt"].mode().empty
        else "N/A"
    )

    common_attack = (
        filtered_df["attacktype1_txt"].mode().iloc[0]
        if not filtered_df["attacktype1_txt"].mode().empty
        else "N/A"
    )

    common_weapon = (
        filtered_df["weaptype1_txt"].mode().iloc[0]
        if not filtered_df["weaptype1_txt"].mode().empty
        else "N/A"
    )

    top_country = (
        filtered_df["country_txt"].value_counts().idxmax()
    )

    st.markdown(f"""
<div class="report-card">

<h3>📄 Executive Intelligence Summary</h3>

<b>Records Selected:</b> {len(filtered_df):,}<br><br>

<b>Countries Covered:</b> {filtered_df['country_txt'].nunique()}<br><br>

<b>Total Fatalities:</b> {int(filtered_df['nkill'].fillna(0).sum()):,}<br><br>

<b>Total Injuries:</b> {int(filtered_df['nwound'].fillna(0).sum()):,}<br><br>

<b>Highest Activity Country:</b> {top_country}<br><br>

<b>Primary Region:</b> {primary_region}<br><br>

<b>Most Common Attack Type:</b> {common_attack}<br><br>

<b>Most Frequently Used Weapon:</b> {common_weapon}<br><br>

<b>AI Assessment:</b><br>
Historical incident patterns indicate that the selected dataset
is primarily concentrated in <b>{primary_region}</b>, with
<b>{common_attack}</b> emerging as the dominant attack method.
Resource allocation and intelligence monitoring should prioritize
high-risk regions and recurring operational patterns.

</div>
""", unsafe_allow_html=True)

# --------------------------------------------------------
# Dataset Preview
# --------------------------------------------------------

st.subheader("Filtered Dataset")

columns = [
    "iyear",
    "country_txt",
    "city",
    "attacktype1_txt",
    "gname",
    "nkill",
    "nwound"
]

st.dataframe(filtered_df[columns])
# --------------------------------------------------------
# Charts
# --------------------------------------------------------

st.subheader("Visual Analytics")

tab1, tab2, tab3 = st.tabs([
    "Country",
    "Attack Type",
    "Weapon Type"
])

# ---------------- Country ----------------

with tab1:

    country_chart = (
        filtered_df["country_txt"]
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
        title="Top 10 Countries"
    )
    fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="white",
    height=450
)
    with st.spinner("Generating visual analytics..."):
     st.markdown('<div class="chart-card">', unsafe_allow_html=True)

     st.plotly_chart(
     fig,
     use_container_width=True
)

     st.markdown("</div>", unsafe_allow_html=True)

# ---------------- Attack ----------------

with tab2:

    attack_chart = (
        filtered_df["attacktype1_txt"]
        .value_counts()
        .reset_index()
    )

    attack_chart.columns = [
        "Attack Type",
        "Count"
    ]

    fig = px.pie(
        attack_chart,
        names="Attack Type",
        values="Count",
        title="Attack Type Distribution"
    )
    fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="white",
    height=450
)
    with st.spinner("Generating visual analytics..."):
         st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    
         st.plotly_chart(
         fig,
         use_container_width=True
    )
    
         st.markdown("</div>", unsafe_allow_html=True)

# ---------------- Weapon ----------------

with tab3:

    weapon_chart = (
        filtered_df["weaptype1_txt"]
        .value_counts()
        .reset_index()
    )

    weapon_chart.columns = [
        "Weapon",
        "Count"
    ]

    fig = px.bar(
        weapon_chart,
        x="Weapon",
        y="Count",
        color="Count",
        title="Weapon Type Distribution"
    )
    fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="white",
    height=450
)
    with st.spinner("Generating visual analytics..."):
         st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    
         st.plotly_chart(
         fig,
         use_container_width=True
    )
    
         st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------------
# Missing Values
# --------------------------------------------------------

st.subheader("Missing Values")
with st.spinner("Analyzing dataset quality..."):
    missing = (
        filtered_df.isnull()
        .sum()
        .sort_values(ascending=False)
    )

missing = missing.reset_index()

missing.columns = [
    "Column",
    "Missing Values"
]

st.dataframe(
    missing,
    use_container_width=True
)

# --------------------------------------------------------
# Dataset Information
# --------------------------------------------------------

st.subheader("Dataset Information")

st.write("Rows :", filtered_df.shape[0])

st.write("Columns :", filtered_df.shape[1])

st.write("Memory Usage (MB):",
         round(filtered_df.memory_usage(deep=True).sum()/1024**2,2))

st.write("Column Names")

st.write(filtered_df.columns.tolist())

csv = filtered_df.to_csv(index=False)

st.markdown("## 📥 Export Dataset")

st.download_button(
    "📄 Download Filtered GTD Dataset",
    csv,
    file_name="Filtered_GTD_Data.csv",
    mime="text/csv",
    use_container_width=True
)