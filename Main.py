import streamlit as st

st.set_page_config(
    page_title="AI Military Intelligence Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("""
<div class="hero">

<h1>Military Intelligence Dashboard</h1>

<p>
Advanced AI-powered intelligence platform for analyzing
global terrorism patterns, threat assessment,
predictive analytics, and strategic decision support.
</p>

</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
<div class="card">

<h3>Mission Overview</h3>

This platform integrates machine learning,
data visualization, forecasting,
and intelligence reporting using the
Global Terrorism Database (GTD).

</div>
""", unsafe_allow_html=True)

with col2:
    st.markdown("""
<div class="card">

<h3>Available Modules</h3>

✔ Home<br>
✔ Global Threat Map<br>
✔ Country Analysis<br>
✔ Attack Prediction<br>
✔ Threat Level Prediction<br>
✔ Forecasting<br>
✔ AI Intelligence Report<br>
✔ Data Explorer<br>
✔ Settings

</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="bottom-banner">

👈 Select a module from the sidebar to begin intelligence analysis.

</div>
""", unsafe_allow_html=True)