# 💼 Customer Churn Prediction — Financial Services

A production-ready Flask web application that predicts whether a financial-services customer is likely to churn, using a trained **CatBoost** classifier. Users enter customer attributes through an intuitive web form and instantly receive a churn probability score along with a color-coded risk level.

---

## 📌 Table of Contents

- [Features](#-features)
- [Demo](#-demo)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Clone the Repository](#1-clone-the-repository)
  - [Create Virtual Environment](#2-create-a-virtual-environment)
  - [Install Dependencies](#3-install-dependencies)
  - [Run the Application](#4-run-the-application)
- [How It Works](#-how-it-works)
- [Input Features](#-input-features)
- [API Endpoints](#-api-endpoints)
- [Environment Variables](#-environment-variables)
- [Deployment](#-deployment)
  - [Render](#deploy-on-render)
  - [Heroku](#deploy-on-heroku)
  - [Railway](#deploy-on-railway)
- [Model Training](#-model-training)
- [License](#-license)

---

## ✨ Features

- **Instant Predictions** — Submit a form and get churn probability in real-time
- **Risk Classification** — Results are categorized as Low / Medium / High risk with color coding
- **Visual Risk Meter** — Progress bar and needle indicator for churn probability
- **Auto-calculated Tenure** — Customer tenure is computed automatically from the onboarding year
- **Health Check Endpoint** — `/health` returns model load status (useful for monitoring)
- **Production-Ready** — Gunicorn + WSGI, environment variable configuration, structured logging

---

## 🖥️ Demo

| Form Input | Prediction Result |
|---|---|
| Fill in customer attributes (logins, tickets, loans, etc.) | See churn probability %, risk level badge, and visual risk meter |

Once running locally, open **http://127.0.0.1:5000** in your browser.

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| **Backend** | Python 3.10+, Flask 3.x |
| **ML Model** | CatBoost Classifier (serialized with joblib) |
| **Frontend** | HTML5, Bootstrap 5.3, Jinja2 templates |
| **WSGI Server** | Gunicorn 22.x |
| **Data Processing** | NumPy, Pandas, scikit-learn |

---

## 📁 Project Structure

```
Customer_Churn_predicrion_financial/
│
├── app.py                              # Main Flask application
├── wsgi.py                             # WSGI entry point for Gunicorn
├── Procfile                            # Process file for Render/Heroku
├── requirements.txt                    # Python dependencies
│
├── CatBoostClassifier.pkl              # Trained model (serialized)
├── customer_churn_data.csv             # Raw dataset
├── Cleaned_Churn_Dataset.csv           # Cleaned dataset
├── Selected_features.csv              # Feature-selected dataset
│
├── 1_Train_model_Churn Prediction.ipynb   # Full EDA + model training notebook
├── 2.train selected dataset.ipynb         # Training on selected features
│
├── templates/
│   └── index.html                      # Main web page (form + results)
│
├── static/
│   └── style.css                       # Custom styles
│
└── README.md                           # This file
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10** or higher
- **pip** (comes with Python)
- **Git**

### 1. Clone the Repository

```bash
git clone https://github.com/Tanmay-Master/Customer_Churn_predicrion_financial.git
cd Customer_Churn_predicrion_financial
```

### 2. Create a Virtual Environment

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs: Flask, Gunicorn, joblib, NumPy, Pandas, scikit-learn, and CatBoost.

### 4. Run the Application

```bash
python app.py
```

The app starts at **http://127.0.0.1:5000**. Open this URL in your browser.

> **Note:** To run with Gunicorn (Linux/macOS only):
> ```bash
> gunicorn wsgi:app
> ```

---

## ⚙️ How It Works

```
┌──────────────┐     POST /predict     ┌──────────────┐     predict()     ┌─────────────────┐
│              │ ──────────────────────►│              │ ─────────────────►│                 │
│   Browser    │   8 form features     │  Flask App   │   feature array   │  CatBoost Model │
│  (index.html)│ ◄──────────────────── │  (app.py)    │ ◄───────────────  │  (.pkl file)    │
│              │   prediction result   │              │   probability     │                 │
└──────────────┘                       └──────────────┘                   └─────────────────┘
```

1. **User** fills in 8 customer attributes on the web form
2. **Flask** receives the form data via `POST /predict`
3. The data is converted to a feature array and passed to the **CatBoost model**
4. The model returns a churn probability (0–100%)
5. The probability is classified into a **risk level** (Low / Medium / High)
6. The result is rendered back on the same page with a visual risk meter

---

## 📊 Input Features

The model expects these **8 features** (in order):

| # | Feature | Type | Description | Validation |
|---|---|---|---|---|
| 1 | **Total Logins** | Float | Number of times the customer logged in | ≥ 0 |
| 2 | **Tickets Raised** | Integer | Support tickets submitted by the customer | ≥ 0 |
| 3 | **Onboarding Year** | Integer | Year the customer joined | 2000 – current year |
| 4 | **Customer Tenure** | Float | Years since onboarding (auto-calculated) | Read-only |
| 5 | **Sentiment Score** | Float | Customer satisfaction score | 0.0 – 1.0 |
| 6 | **Loans Accessed** | Float | Number of loan products viewed | ≥ 0 |
| 7 | **Loans Taken** | Float | Number of loans actually taken | ≥ 0 |
| 8 | **Monthly Avg Balance** | Float | Average monthly account balance | ≥ 0 |

### Risk Classification

| Churn Probability | Risk Level | Color |
|---|---|---|
| < 30% | 🟢 Low Risk | Green |
| 30% – 69% | 🟠 Medium Risk | Orange |
| ≥ 70% | 🔴 High Risk | Red |

---

## 🔌 API Endpoints

| Method | Route | Description |
|---|---|---|
| `GET` | `/` | Renders the home page with the prediction form |
| `POST` | `/predict` | Accepts form data, runs the model, returns results |
| `GET` | `/health` | Returns JSON health status |

### Health Check Response

```json
{
  "status": "ok",
  "model_loaded": true
}
```

---

## 🔐 Environment Variables

All are optional — sensible defaults are provided:

| Variable | Default | Description |
|---|---|---|
| `SECRET_KEY` | Random (auto-generated) | Flask session secret key. **Set this in production!** |
| `MODEL_PATH` | *(not set)* | Path to a custom model `.pkl` file |
| `HOST` | `0.0.0.0` | Server bind address |
| `PORT` | `5000` | Server port |
| `FLASK_DEBUG` | `false` | Enable Flask debug mode (`true` / `false`) |

### Model Loading Priority

The app searches for the model file in this order:
1. Path specified in `MODEL_PATH` env variable
2. `selectedCatBoostClassifier.pkl` (in project root)
3. `CatBoostClassifier.pkl` (in project root)

---

## ☁️ Deployment

### Deploy on Render

1. Push this repo to GitHub
2. Go to [render.com](https://render.com) → **New Web Service**
3. Connect your GitHub repository
4. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn wsgi:app`
   - **Environment:** Python 3
5. Add environment variable: `SECRET_KEY` = *(any random string)*
6. Click **Deploy**

### Deploy on Heroku

```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Set environment variable
heroku config:set SECRET_KEY=your-secret-key-here

# Deploy
git push heroku main
```

The `Procfile` (`web: gunicorn wsgi:app`) is already configured.

### Deploy on Railway

1. Push to GitHub
2. Go to [railway.app](https://railway.app) → **New Project** → **Deploy from GitHub**
3. Railway auto-detects the `Procfile`
4. Add environment variable: `SECRET_KEY` = *(any random string)*
5. Deploy

---

## 🧪 Model Training

The model was trained using the Jupyter notebooks included in this repository:

| Notebook | Purpose |
|---|---|
| `1_Train_model_Churn Prediction.ipynb` | Full EDA, data cleaning, feature engineering, and model comparison |
| `2.train selected dataset.ipynb` | Training on the selected feature subset |

### Dataset

- **Raw data:** `customer_churn_data.csv` (10 columns, ~10k records)
- **Cleaned data:** `Cleaned_Churn_Dataset.csv`
- **Selected features:** `Selected_features.csv` (8 features + target)

### Target Variable

- `Churned` — Binary (0 = Retained, 1 = Churned)

### Algorithm

- **CatBoost Classifier** — A gradient boosting algorithm optimized for categorical features
- Serialized using `joblib` → `CatBoostClassifier.pkl`

---

## 📄 License

This project is open source and available for educational and commercial use.

---

> **Built with** ❤️ using Flask + CatBoost
