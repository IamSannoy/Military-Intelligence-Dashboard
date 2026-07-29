# Military Intelligence Dashboard

A comprehensive **Streamlit-based Military Intelligence Dashboard** for exploring, analyzing, and predicting terrorist incident patterns using the **Global Terrorism Database (GTD)** or user-uploaded datasets.

The platform combines interactive visualizations, machine learning, forecasting, and automated intelligence reporting into a single application. It supports both the default GTD dataset with pre-trained models and custom CSV datasets with automatic model training.

---

## Features

### Interactive Data Analysis

* Global Threat Map
* Country-wise Analysis
* Data Explorer
* Dynamic statistics and visualizations

### Machine Learning

* Attack Type Prediction
* Threat Level Prediction
* Automatic training for custom datasets
* Pre-trained models for the default GTD dataset

### Forecasting

* Historical trend analysis
* Future incident forecasting
* Time-series visualizations

### AI Intelligence Report

* Automatically generated intelligence summaries
* Country-level insights
* Threat assessment reports

### Smart Dataset Management

* Supports the default Global Terrorism Database (GTD)
* Upload custom CSV datasets
* Automatic column mapping
* Dataset compatibility detection
* Temporary dataset storage
* Automatic cleanup of uploaded datasets

---

## Technologies Used

* Python
* Streamlit
* Pandas
* NumPy
* Scikit-learn
* Plotly
* Joblib

---

## Project Structure

```text
Military_Intelligence_Dashboard/
│
├── main.py
├── pages/
│   ├── Global_Threat_Map.py
│   ├── Country_Analysis.py
│   ├── Attack_Prediction.py
│   ├── Threat_Level_Prediction.py
│   ├── Forecasting.py
│   ├── AI_Intelligence_Report.py
│   └── Data_Explorer.py
│
├── utils/
│   ├── data_loader.py
│   ├── dataset.py
│   └── style.py
│
├── models/
│
├── data/
│
├── temp_uploads/
│
├── train_custom_model.py
├── threat_model.py
├── clean_up.py
├── requirements.txt
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/<your-username>/<repository-name>.git
cd <repository-name>
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment:

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run main.py
```

---

## How It Works

### Default Dataset Mode

When no dataset is uploaded:

* Uses the default Global Terrorism Database (GTD)
* Loads pre-trained machine learning models
* No additional model training is required
* Faster startup and prediction

### Custom Dataset Mode

When a compatible CSV dataset is uploaded:

* Automatically detects supported columns
* Allows manual column mapping
* Enables only compatible analysis pages
* Trains custom machine learning models when required
* Stores the uploaded dataset temporarily during the session

---

## Supported Dataset Fields

The application recognizes the following standard fields:

* Country
* Region
* Year
* Attack Type
* Weapon Type
* Target Type
* Terrorist Group
* Latitude
* Longitude
* Fatalities
* Injuries

Datasets containing these fields can automatically use the supported analysis modules.

---

## Machine Learning Models

### Attack Type Prediction

Predicts the likely attack type using incident attributes such as:

* Country
* Region
* Weapon Type
* Target Type
* Terrorist Group
* Fatalities
* Injuries

### Threat Level Prediction

Calculates an incident's threat level based on its impact:

* LOW
* MEDIUM
* HIGH

The model uses:

* Country
* Region
* Attack Type
* Weapon Type
* Target Type
* Fatalities
* Injuries

---

## Highlights

* Responsive Streamlit interface
* Automatic dataset adaptation
* Dynamic model training
* Interactive visualizations
* Modular architecture
* Clean and maintainable codebase
* Easy extension for future intelligence modules

---

## Future Improvements

* Deep learning-based threat prediction
* Natural language intelligence summaries using large language models
* Real-time incident feeds
* Advanced geospatial analytics
* User authentication and role management
* Cloud deployment
* Exportable intelligence reports
