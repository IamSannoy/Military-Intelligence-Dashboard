# AI-Based Military Intelligence Dashboard

An interactive AI-powered military intelligence dashboard built with **Streamlit**, **Machine Learning**, and the **Global Terrorism Database (GTD)**. The application enables users to explore global terrorism incidents, analyze trends, predict attack types, forecast future incidents, and generate intelligence reports through a modern analytical interface.

---

## Features

- Interactive Dashboard
- Global Threat Map
- Country-wise Intelligence Analysis
- Attack Type Prediction using Machine Learning
- Threat Level Prediction
- Terrorism Forecasting
- AI Intelligence Report Generator
- Advanced Data Explorer
- Dashboard Settings

---

## Technologies Used

- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- Scikit-learn
- Joblib

---

## Machine Learning Models

The dashboard includes:

- Random Forest Classifier for Attack Type Prediction
- Random Forest Classifier for Threat Level Prediction
- Linear Regression for Attack Forecasting

---

## Dataset

This project uses the **Global Terrorism Database (GTD)**.

The dataset is **not included** in this repository due to its size.

Download it from the official GTD website and place it inside:

```
data/
```

Expected file:

```
data/globalterrorism.csv
```

---

## Project Structure

```
AI-Military-Intelligence-Dashboard
│
├── app.py
├── pages/
│   ├── Home.py
│   ├── Global_Threat_Map.py
│   ├── Country_Analysis.py
│   ├── Attack_Prediction.py
│   ├── Threat_Level_Prediction.py
│   ├── Forecasting.py
│   ├── AI_Intelligence_Report.py
│   ├── Data_Explorer.py
│   └── Settings.py
│
├── utils/
├── assets/
├── .streamlit/
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/your-username/AI-Military-Intelligence-Dashboard.git
```

Go to the project folder:

```bash
cd AI-Military-Intelligence-Dashboard
```

Create a virtual environment(If needed):

```bash
python -m venv .venv
```

Activate it.

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Run the Application

```bash
streamlit run app.py
```

---

## Required Files

Before running the project, place the following files in the appropriate folders:

### Dataset

```
data/globalterrorism.csv
```

### Trained Models

```
models/
├── attack_prediction_model.pkl
├── feature_encoders.pkl
├── target_encoder.pkl
```

These files are excluded from the repository using `.gitignore`.

---

## 📷 Dashboard Modules

- Home Dashboard
- Global Threat Map
- Country Analysis
- Attack Prediction
- Threat Level Prediction
- Forecasting
- AI Intelligence Report
- Data Explorer
- Settings

---

## Future Improvements

- Deep Learning Models
- LSTM Time-Series Forecasting
- Real-time Intelligence Feeds
- GIS Heat Maps
- User Authentication
- Report Export (PDF)
- Interactive Alert System

---

## License

This project is developed for educational and research purposes.

The Global Terrorism Database (GTD) is maintained by the National Consortium for the Study of Terrorism and Responses to Terrorism (START). Please follow their licensing and usage terms when using the dataset.

---

## Author

**Sannoy Jana**

Computer Science & Engineering Student

AI • Machine Learning • Data Analytics • Full Stack Development
