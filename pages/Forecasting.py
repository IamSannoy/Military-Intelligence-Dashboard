import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from sklearn.linear_model import LinearRegression

from utils.ui import load_css

# =====================================================
# Page Configuration
# =====================================================

st.set_page_config(
    page_title="AI Forecasting",
    page_icon="📈",
    layout="wide"
)

load_css()

# =====================================================
# Premium Header
# =====================================================

st.markdown("""
<div class="page-header">

<h1>📈 AI Terrorism Forecasting</h1>

<p>
Predict future terrorism trends using machine learning
trained on historical records from the Global Terrorism
Database (GTD). This module provides long-term trend
analysis, growth estimation and intelligence support
for strategic planning.
</p>

</div>
""", unsafe_allow_html=True)

# =====================================================
# Load Dataset
# =====================================================

@st.cache_data
def load_data():

    df = pd.read_csv(
        "data/globalterrorism.csv",
        encoding="latin1",
        low_memory=False
    )

    return df


with st.spinner("Loading intelligence database..."):
    df = load_data()

# =====================================================
# Sidebar
# =====================================================

st.sidebar.header("⚙ Forecast Settings")

countries = sorted(
    df["country_txt"]
    .dropna()
    .unique()
)

country = st.sidebar.selectbox(
    "Country",
    countries,
    label_visibility="collapsed",
    placeholder="Select Country"
)

forecast_years = st.sidebar.slider(
    "📅 Forecast Period (Years)",
    min_value=1,
    max_value=10,
    value=5
)

# =====================================================
# Prepare Historical Data
# =====================================================

with st.spinner("Preparing historical intelligence..."):

    country_df = df[
        df["country_txt"] == country
    ]

    yearly = (
        country_df
        .groupby("iyear")
        .size()
        .reset_index(name="Attacks")
    )

    yearly = yearly.sort_values("iyear")

# =====================================================
# Validate Dataset
# =====================================================

if yearly.empty:

    st.error(
        "No historical records are available for the selected country."
    )

    st.stop()

if len(yearly) < 5:

    st.warning(
        "Not enough historical data is available to build a reliable forecasting model."
    )

    st.stop()

# =====================================================
# Train Machine Learning Model
# =====================================================

with st.spinner("Training forecasting model..."):

    X = yearly[["iyear"]]

    y = yearly["Attacks"]

    model = LinearRegression()

    model.fit(
        X,
        y
    )

# =====================================================
# Future Forecast
# =====================================================

with st.spinner("Generating future predictions..."):

    last_year = yearly["iyear"].max()

    future_years = np.arange(
        last_year + 1,
        last_year + forecast_years + 1
    )

    future_df = pd.DataFrame({
        "iyear": future_years
    })

    predictions = model.predict(
        future_df
    )

    predictions = np.maximum(
        predictions,
        0
    )

    forecast = pd.DataFrame({

        "Year": future_years,

        "Forecasted Attacks":
        predictions.astype(int)

    })

# =====================================================
# Intelligence Statistics
# =====================================================

historical_last = int(
    yearly.iloc[-1]["Attacks"]
)

forecast_last = int(
    forecast.iloc[-1]["Forecasted Attacks"]
)

growth = (
    (forecast_last - historical_last)
    / max(historical_last, 1)
) * 100

average_attacks = int(
    yearly["Attacks"].mean()
)

maximum_attacks = int(
    yearly["Attacks"].max()
)

minimum_attacks = int(
    yearly["Attacks"].min()
)

# =====================================================
# AI Forecast Summary
# =====================================================

st.markdown("## 🧠 AI Forecast Summary")

trend = (
    "Increasing"
    if growth > 15
    else "Stable"
    if growth >= 0
    else "Decreasing"
)

st.markdown(f"""
<div class="report-card">

<h3>📄 Executive Forecast Report</h3>

<b>Country:</b> {country}<br><br>

<b>Historical Records:</b> {len(yearly)} Years<br><br>

<b>Average Annual Attacks:</b> {average_attacks}<br><br>

<b>Highest Recorded Attacks:</b> {maximum_attacks}<br><br>

<b>Lowest Recorded Attacks:</b> {minimum_attacks}<br><br>

<b>Current Annual Attacks:</b> {historical_last}<br><br>

<b>Predicted Attacks ({forecast_years} Years):</b> {forecast_last}<br><br>

<b>Estimated Growth:</b> {growth:.2f}%<br><br>

<b>AI Assessment:</b><br>
The forecasting model predicts an <b>{trend}</b> trend in terrorist
activity for <b>{country}</b>. These projections are generated using
historical GTD records and should be considered decision-support
information rather than definitive intelligence.

</div>
""", unsafe_allow_html=True)

# =====================================================
# KPI Dashboard
# =====================================================

st.markdown("## 📊 Forecast Indicators")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Current",
        historical_last
    )

with c2:
    st.metric(
        "Forecast",
        forecast_last
    )

with c3:
    st.metric(
        "Growth",
        f"{growth:.2f}%"
    )

with c4:
    st.metric(
        "Forecast Years",
        forecast_years
    )

# =====================================================
# Forecast Chart
# =====================================================

st.markdown("## 📈 Forecast Visualization")

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=yearly["iyear"],
        y=yearly["Attacks"],
        mode="lines+markers",
        name="Historical",
        line=dict(width=3)
    )
)

fig.add_trace(
    go.Scatter(
        x=forecast["Year"],
        y=forecast["Forecasted Attacks"],
        mode="lines+markers",
        name="Forecast",
        line=dict(width=3, dash="dash")
    )
)

fig.update_layout(

    title=f"Forecast for {country}",

    xaxis_title="Year",

    yaxis_title="Number of Attacks",

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="rgba(0,0,0,0)",

    font_color="white",

    height=600,

    legend=dict(
        bgcolor="rgba(0,0,0,0)"
    )
)

with st.spinner("Rendering forecast visualization..."):

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
# Forecast Table
# =====================================================

st.markdown("## 📋 Forecast Results")

st.dataframe(
    forecast,
    use_container_width=True,
    hide_index=True
)

# =====================================================
# Growth Analysis
# =====================================================

st.markdown("## 📊 Growth Analysis")

g1, g2, g3 = st.columns(3)

g1.metric(
    "Historical",
    historical_last
)

g2.metric(
    "Forecast",
    forecast_last
)

g3.metric(
    "Growth %",
    f"{growth:.2f}%"
)

# =====================================================
# Risk Assessment
# =====================================================

st.markdown("## 🚨 Threat Assessment")

if growth < 0:

    st.success("""
### 🟢 Low Risk Outlook

The model forecasts a decline in terrorist activity.
Continue monitoring while maintaining intelligence
operations.
""")

elif growth < 15:

    st.warning("""
### 🟡 Moderate Risk Outlook

The projected activity remains relatively stable.
Maintain surveillance and periodic reassessment.
""")

else:

    st.error("""
### 🔴 High Risk Outlook

The model predicts increasing terrorist activity.
Strengthen intelligence gathering and preparedness.
""")

# =====================================================
# Download Forecast
# =====================================================

st.markdown("## 📥 Export Forecast")

csv = forecast.to_csv(
    index=False
).encode()

st.download_button(
    "📄 Download Forecast Report",
    data=csv,
    file_name=f"{country}_forecast.csv",
    mime="text/csv",
    use_container_width=True
)

# =====================================================
# Footer
# =====================================================

st.caption(
    "Forecasts are generated using Linear Regression on historical GTD data and are intended for analytical purposes only."
)