🏦 Customer Churn Prediction — Web Application
This repository contains a Flask-based web application for predicting customer churn in the financial services domain.
It integrates Machine Learning (CatBoostClassifier) with a user-friendly HTML/Bootstrap frontend to help businesses identify customers at risk of churn and proactively design retention strategies.

📂 Repository Structure
/Churn Prediction
│
├── templates/
│   └── index.html                # Main web interface (HTML + JavaScript)
│
├── static/
│   └── Style.css                 # Custom CSS & Bootstrap overrides
│
├── selectedCatBoostClassifier.pkl # Final trained CatBoost model (production-ready)
├── app.py                        # Flask backend (application logic & API endpoints)
└── README.md                     # Project documentation

🚀 Features

Frontend: Clean Bootstrap interface with JS interactivity.

Backend: Flask handles requests and serves predictions.

Model: CatBoostClassifier (high-accuracy, production-selected model).

Prediction Output: Probability of churn + churn label (0 = Retained, 1 = Churned).

Custom Styling: Style.css to override default Bootstrap theme.

🧠 Machine Learning Model

Model Used: CatBoostClassifier

Training Data: Processed banking customer dataset (10k customers → balanced to 15,288 rows with SMOTE).

Final Metrics:

Accuracy: 0.9235

F1 Score: 0.9230

ROC AUC: 0.9772

Selected Features:
Total Logins, Tickets Raised, Customer Tenure Year, Sentiment Score,
Onboarding Year, Loans Accessed, Loans Taken, Monthly Avg Balance

⚙️ How to Run Locally
1. Clone the repository
git clone https://github.com/<your-username>/churn-prediction.git
cd "Churn Prediction"

2. Set up virtual environment & install dependencies
python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows

pip install -r requirements.txt


If requirements.txt is missing, install core dependencies manually:

pip install flask pandas numpy scikit-learn catboost imbalanced-learn shap matplotlib seaborn

3. Run the Flask app
python app.py


Then open your browser at http://127.0.0.1:5000/

🌐 Application Workflow

User enters customer details (or uploads dataset) via index.html.

Flask backend (app.py) loads selectedCatBoostClassifier.pkl.

Model predicts churn probability and returns risk classification.

Results displayed on the web interface with intuitive styling.

🛠️ Tech Stack

Frontend: HTML, CSS (Bootstrap customized) + JavaScript

Backend: Flask (Python)

Machine Learning: CatBoost, Scikit-learn, Pandas, NumPy

Visualization & Explainability (dev phase): SHAP, Matplotlib, Seaborn

📈 Business Impact

Early detection of at-risk customers.

Enables data-driven retention campaigns.

Improves Customer Lifetime Value (CLV) and reduces churn rate.
