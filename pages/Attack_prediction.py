import streamlit as st
import pandas as pd
import joblib
from utils.ui import load_css

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------

st.set_page_config(
    page_title="Attack Prediction",
    page_icon="🤖",
    layout="wide"
)

load_css()

# -------------------------------------------------
# Header
# -------------------------------------------------

st.markdown("""
<div class="page-header">
<h1>🤖 AI Attack Type Prediction</h1>

<p>
Predict the most probable terrorist attack type using
machine learning trained on the Global Terrorism Database (GTD).
Provide incident details below and let the AI generate its prediction.
</p>

</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Load Models
# -------------------------------------------------

@st.cache_resource
def load_models():

    

        model = joblib.load(
            "models/attack_prediction_model.pkl"
        )

        encoders = joblib.load(
            "models/feature_encoders.pkl"
        )

        target_encoder = joblib.load(
            "models/target_encoder.pkl"
        )

        return model, encoders, target_encoder


model, encoders, target_encoder = load_models()

# -------------------------------------------------
# Load Dataset
# -------------------------------------------------

@st.cache_data
def load_data():

    with st.spinner("Loading intelligence database..."):

        df = pd.read_csv(
            "data/globalterrorism.csv",
            encoding="latin1",
            low_memory=False
        )

        df = df.dropna(subset=[
            "country_txt",
            "region_txt",
            "weaptype1_txt",
            "targtype1_txt",
            "gname"
        ])

    return df


df = load_data()

# -------------------------------------------------
# Input Form
# -------------------------------------------------

st.markdown("""
<div class="card">
<h2>🎯 Incident Information</h2>
<p>Enter the available intelligence to predict the likely attack type.</p>
</div>
""", unsafe_allow_html=True)

with st.form("prediction_form"):

    left, right = st.columns(2)

    with left:

        country = st.selectbox(
    "",
          sorted(df["country_txt"].unique()),
          label_visibility="collapsed",
          placeholder="Select Country"
)

        region = st.selectbox(
            "🌎 Region",
            sorted(df["region_txt"].unique())
        )

        weapon = st.selectbox(
            "🔫 Weapon Type",
            sorted(df["weaptype1_txt"].unique())
        )

        target = st.selectbox(
            "🎯 Target Type",
            sorted(df["targtype1_txt"].unique())
        )

    with right:

        group = st.selectbox(
            "👥 Terrorist Organization",
            sorted(df["gname"].unique())
        )

        success = st.selectbox(
            "✅ Successful Attack",
            [0, 1],
            format_func=lambda x: "Yes" if x else "No"
        )

        suicide = st.selectbox(
            "💣 Suicide Attack",
            [0, 1],
            format_func=lambda x: "Yes" if x else "No"
        )

        nkill = st.number_input(
            "☠ Fatalities",
            min_value=0,
            value=0
        )

        nwound = st.number_input(
            "🏥 Injuries",
            min_value=0,
            value=0
        )

    predict = st.form_submit_button(
        "🚀 Predict Attack Type",
        use_container_width=True
    )

# -------------------------------------------------
# Prediction
# -------------------------------------------------

if predict:

    with st.spinner("Analyzing intelligence and generating prediction..."):

        country_encoded = encoders["country_txt"].transform([country])[0]
        region_encoded = encoders["region_txt"].transform([region])[0]
        weapon_encoded = encoders["weaptype1_txt"].transform([weapon])[0]
        target_encoded = encoders["targtype1_txt"].transform([target])[0]
        group_encoded = encoders["gname"].transform([group])[0]

        input_df = pd.DataFrame({

            "country_txt":[country_encoded],
            "region_txt":[region_encoded],
            "weaptype1_txt":[weapon_encoded],
            "targtype1_txt":[target_encoded],
            "gname":[group_encoded],
            "success":[success],
            "suicide":[suicide],
            "nkill":[nkill],
            "nwound":[nwound]

        })

        prediction = model.predict(input_df)

        attack_type = target_encoder.inverse_transform(
            prediction
        )[0]

        probabilities = model.predict_proba(input_df)

        confidence = probabilities.max()*100

    # -------------------------
    # Results
    # -------------------------

    st.markdown("---")

    st.markdown("""
    <div class="report-card">
    <h2>🧠 AI Prediction Result</h2>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2,1])

    with col1:

        st.success(
            f"### Predicted Attack Type\n\n**{attack_type}**"
        )

        st.progress(confidence/100)

        st.write(
            f"**Prediction Confidence:** {confidence:.2f}%"
        )

    with col2:

        st.metric(
            "Confidence",
            f"{confidence:.2f}%"
        )

        st.metric(
            "Fatalities",
            nkill
        )

        st.metric(
            "Injuries",
            nwound
        )

    st.markdown("## 📋 AI Assessment")

    st.info(f"""
**Predicted Attack Type:** {attack_type}

**Threat Assessment**

- The model predicts that the incident most closely matches **{attack_type}**.
- Estimated confidence is **{confidence:.2f}%**.
- Analysts should combine this prediction with field intelligence before making operational decisions.
- The prediction is based on historical GTD patterns and should be treated as decision support rather than definitive intelligence.
""")