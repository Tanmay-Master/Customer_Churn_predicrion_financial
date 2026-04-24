# 💼 Customer Churn Prediction — Financial Services

A Flask web app that predicts customer churn using a trained CatBoost ML model. Users enter customer data and get instant churn probability with risk classification.

---

## � Quick Start

### Prerequisites
- Python 3.10+
- pip

### Setup (3 steps)

```bash
# 1. Clone & navigate
git clone https://github.com/Tanmay-Master/Customer_Churn_predicrion_financial.git
cd Customer_Churn_predicrion_financial

# 2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux

# 3. Install & run
pip install -r requirements.txt
python app.py
```

Open **http://127.0.0.1:5000** in your browser.

---

## 📁 Coding Files Explained

### **app.py** — Main Application
The Flask backend that handles everything.

**Key Functions:**
- `load_model()` — Loads the trained CatBoost model from `.pkl` file
- `home()` — Renders the prediction form page
- `predict()` — Processes form data, runs ML model, returns churn probability
- `health()` — API endpoint for monitoring (returns `{"status": "ok", "model_loaded": true/false}`)

**How it works:**
1. User submits 8 customer features via HTML form
2. Flask validates & converts data types (int/float)
3. Creates pandas DataFrame with correct column order
4. CatBoost model predicts churn probability (0-100%)
5. Classifies risk level: Low (<30%) | Medium (30-69%) | High (≥70%)
6. Returns result with color-coded risk badge

**Key Features:**
- Automatic model path detection (checks env variable, then `.pkl` files)
- Error handling with user-friendly messages
- Logging for debugging
- Environment variable support (SECRET_KEY, MODEL_PATH, HOST, PORT, FLASK_DEBUG)

---

### **wsgi.py** — Production Server Entry Point
Minimal file for Gunicorn (production WSGI server).

```python
from app import app
```

**Usage:** `gunicorn wsgi:app` (Linux/macOS only)

---

### **requirements.txt** — Dependencies
Lists all Python packages needed.

```
Flask>=3.0          # Web framework
gunicorn>=22.0      # Production server
joblib>=1.3         # Model serialization
pandas>=2.0         # Data processing
numpy>=1.26         # Numerical computing
scikit-learn>=1.4   # ML utilities
catboost>=1.2       # ML model library
seaborn>=0.12       # Data visualization (for notebooks)
xgboost>=2.0        # Alternative ML (for notebooks)
lightgbm>=4.0       # Alternative ML (for notebooks)
```

**Install:** `pip install -r requirements.txt`

---

### **Procfile** — Deployment Configuration
Tells cloud platforms (Render, Heroku) how to run the app.

```
web: gunicorn wsgi:app
```

---

## 📊 Data & Model Files

| File | Purpose | Size |
|---|---|---|
| `CatBoostClassifier.pkl` | Trained ML model (primary) | ~50MB |
| `selectedCatBoostClassifier.pkl` | Trained ML model (backup) | ~50MB |
| `customer_churn_data.csv` | Raw dataset (10 columns, ~10k rows) | ~2MB |
| `Cleaned_Churn_Dataset.csv` | Cleaned dataset | ~2MB |
| `Selected_features.csv` | Final 8 features + target | ~1MB |

---

## 📓 Jupyter Notebooks (Training)

### **1_Train_model_Churn Prediction.ipynb**
Complete ML pipeline:
- Data exploration & visualization
- Data cleaning & preprocessing
- Feature engineering
- Model comparison (CatBoost, XGBoost, LightGBM)
- Hyperparameter tuning
- Final model evaluation

### **2.train selected dataset.ipynb**
Simplified training on selected 8 features:
- Loads cleaned data
- Trains CatBoost on best features
- Saves model as `.pkl`

---

## 🎨 Frontend Files

### **templates/index.html**
Single-page form with:
- 8 input fields for customer data
- Auto-calculated tenure (from onboarding year)
- Form validation (client-side)
- Results display with risk meter & color coding
- Responsive Bootstrap 5 design

### **static/style.css**
Custom styling:
- Risk meter visualization
- Color-coded badges (green/orange/red)
- Form styling & animations
- Mobile responsive layout

---

## 🔌 API Endpoints

| Method | Route | Input | Output |
|---|---|---|---|
| `GET` | `/` | — | HTML form page |
| `POST` | `/predict` | Form data (8 fields) | Prediction result + form |
| `GET` | `/health` | — | `{"status": "ok", "model_loaded": bool}` |

---

## 📥 Input Features (8 Required)

| # | Feature | Type | Range | Example |
|---|---|---|---|---|
| 1 | Total Logins | Float | ≥0 | 45.5 |
| 2 | Tickets Raised | Integer | ≥0 | 3 |
| 3 | Customer Tenure | Float | Auto-calculated | — |
| 4 | Sentiment Score | Float | 0.0–1.0 | 0.75 |
| 5 | Onboarding Year | Integer | 2000–current | 2020 |
| 6 | Loans Accessed | Float | ≥0 | 2.0 |
| 7 | Loans Taken | Float | ≥0 | 1.0 |
| 8 | Monthly Avg Balance | Float | ≥0 | 5000.0 |

---

## 📈 Output Format

```json
{
  "prediction": "Will Churn" or "Will Not Churn",
  "probability": 65.42,
  "risk_level": "Medium Risk",
  "risk_color": "orange"
}
```

**Risk Classification:**
- 🟢 **Low Risk** — <30% churn probability
- 🟠 **Medium Risk** — 30–69% churn probability
- 🔴 **High Risk** — ≥70% churn probability

---

## � Environment Variables

| Variable | Default | Purpose |
|---|---|---|
| `SECRET_KEY` | Auto-generated | Flask session encryption (set in production!) |
| `MODEL_PATH` | Not set | Custom model file path |
| `HOST` | `0.0.0.0` | Server bind address |
| `PORT` | `5000` | Server port |
| `FLASK_DEBUG` | `false` | Debug mode (`true`/`false`) |

**Example `.env` file:**
```
SECRET_KEY=your-secret-key-here
FLASK_DEBUG=false
PORT=5000
```

---

## ☁️ Deployment

### **Render**
1. Push to GitHub
2. Go to render.com → New Web Service
3. Connect repo
4. Build: `pip install -r requirements.txt`
5. Start: `gunicorn wsgi:app`
6. Add env var: `SECRET_KEY=your-key`

### **Heroku**
```bash
heroku login
heroku create your-app-name
heroku config:set SECRET_KEY=your-key
git push heroku main
```

### **Railway**
1. Go to railway.app → New Project
2. Connect GitHub repo
3. Add env var: `SECRET_KEY=your-key`
4. Deploy (auto-detects Procfile)

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.10+, Flask 3.x |
| **ML Model** | CatBoost Classifier |
| **Frontend** | HTML5, Bootstrap 5, Jinja2 |
| **Server** | Gunicorn (production) |
| **Data** | Pandas, NumPy, scikit-learn |

---

## 📂 Project Structure

```
Customer_Churn_predicrion_financial/
├── app.py                          # Main Flask app
├── wsgi.py                         # Gunicorn entry point
├── requirements.txt                # Dependencies
├── Procfile                        # Deployment config
├── .gitignore                      # Git ignore rules
│
├── CatBoostClassifier.pkl          # Trained model
├── selectedCatBoostClassifier.pkl  # Backup model
│
├── customer_churn_data.csv         # Raw data
├── Cleaned_Churn_Dataset.csv       # Cleaned data
├── Selected_features.csv           # Final features
│
├── 1_Train_model_Churn Prediction.ipynb    # Full training
├── 2.train selected dataset.ipynb          # Feature training
│
├── templates/
│   └── index.html                  # Web form & results
├── static/
│   └── style.css                   # Styling
└── README.md                       # This file
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|---|---|
| Model not loading | Check `.pkl` file exists in project root or set `MODEL_PATH` env var |
| Port 5000 in use | Change `PORT` env var: `set PORT=8000` (Windows) or `export PORT=8000` (Linux) |
| Import errors | Run `pip install -r requirements.txt` again |
| Form validation fails | Check input types match (int vs float) and ranges are valid |

---

## 📝 License

Open source — free for educational & commercial use.

---

**Built with** ❤️ **using Flask + CatBoost**
