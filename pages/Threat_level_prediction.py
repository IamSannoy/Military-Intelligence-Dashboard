import streamlit as st
import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from utils.ui import load_css
# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="Threat Level Prediction",
    page_icon="🚨",
    layout="wide"
)
load_css()
st.markdown("""
<div class="page-header">

<h1>🚨 AI Threat Level Prediction</h1>

<p>
Estimate the operational threat level of a terrorism incident
using machine learning trained on the Global Terrorism Database.
</p>

</div>
""", unsafe_allow_html=True)

# -------------------------------
# Load Dataset
# -------------------------------
@st.cache_data
def load_data():
    return pd.read_csv(
        "data/globalterrorism.csv",
        encoding="latin1",
        low_memory=False
    )

with st.spinner("Loading intelligence database..."):
    df = load_data()

df = df[[
    "country_txt",
    "region_txt",
    "attacktype1_txt",
    "weaptype1_txt",
    "targtype1_txt",
    "nkill",
    "nwound"
]]

df = df.dropna()

# -------------------------------
# Create Threat Level
# -------------------------------
df["impact"] = df["nkill"] + df["nwound"]

def classify_threat(x):
    if x <= 2:
        return "LOW"
    elif x <= 10:
        return "MEDIUM"
    else:
        return "HIGH"

df["threat_level"] = df["impact"].apply(classify_threat)

# -------------------------------
# Encode Categorical Data
# -------------------------------
encoders = {}

for col in [
    "country_txt",
    "region_txt",
    "attacktype1_txt",
    "weaptype1_txt",
    "targtype1_txt"
]:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le

# Encode target
target_encoder = LabelEncoder()
df["threat_level"] = target_encoder.fit_transform(df["threat_level"])

# -------------------------------
# Train Model
# -------------------------------

X = df.drop(columns=["threat_level", "impact"])
y = df["threat_level"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

# -------------------------------
# Sidebar Inputs
# -------------------------------
st.sidebar.header("Input Parameters")

country = st.sidebar.selectbox("Country", df["country_txt"].unique())
region = st.sidebar.selectbox("Region", df["region_txt"].unique())
attack = st.sidebar.selectbox("Attack Type", df["attacktype1_txt"].unique())
weapon = st.sidebar.selectbox("Weapon Type", df["weaptype1_txt"].unique())
target = st.sidebar.selectbox("Target Type", df["targtype1_txt"].unique())

nkill = st.sidebar.number_input("Number Killed", 0, 1000, 0)
nwound = st.sidebar.number_input("Number Wounded", 0, 1000, 0)

# -------------------------------
# Prediction Button
# -------------------------------
if st.button(
    "🚨 Predict Threat Level",
    use_container_width=True
):

    with st.spinner("Running AI threat assessment..."):

    # Encode inputs
     input_data = np.array([[
        country,
        region,
        attack,
        weapon,
        target,
        nkill,
        nwound
    ]])

    prediction = model.predict(input_data)
    probability = model.predict_proba(input_data)

    result = target_encoder.inverse_transform(prediction)[0]
    confidence = np.max(probability) * 100

    # -------------------------------
    # Output
    # -------------------------------
    st.markdown("## 🧠 AI Threat Assessment")
    if result == "LOW":
        st.success("""
### 🟢 LOW THREAT

Minimal operational impact detected.

Routine monitoring is recommended.
""")
    elif result == "MEDIUM":
        st.warning("""
### 🟡 MEDIUM THREAT

Moderate operational impact detected.

Enhanced surveillance is recommended.
""")
    else:
        st.error("""
### 🔴 HIGH THREAT

High operational impact detected.

Immediate response and intelligence coordination
are recommended.
""")

    st.metric("Confidence Score", f"{confidence:.2f}%")

    st.write("### Probability Distribution")
    prob_df = pd.DataFrame({
    "Threat Level": target_encoder.classes_,
    "Probability": probability[0]
})

st.markdown('<div class="chart-card">', unsafe_allow_html=True)

st.bar_chart(
    prob_df.set_index("Threat Level")
)

st.markdown("</div>", unsafe_allow_html=True)