import os
from pathlib import Path
from datetime import datetime, timezone

import joblib
import pandas as pd
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', os.urandom(24))
BASE_DIR = Path(__file__).resolve().parent

# Initialize model as None
model = None

# Label encoding mappings (from training notebook - alphabetically sorted by LabelEncoder)
LABEL_ENCODINGS = {
    'Gender':          {'Female': 0, 'Male': 1, 'Other': 2},
    'Location':        {'East': 0, 'North': 1, 'South': 2, 'West': 3},
    'Occupation':      {'Retired': 0, 'Salaried': 1, 'Self-employed': 2, 'Student': 3},
    'Income Bracket':  {'High': 0, 'Low': 1, 'Medium': 2},
    'Channel':         {'Agent': 0, 'Branch': 1, 'Online': 2},
    'Device Type':     {'Android': 0, 'Web': 1, 'iOS': 2},
    'Current Plan':    {'Basic': 0, 'Gold': 1, 'Platinum': 2, 'Silver': 3},
    'Payment Mode':    {'Auto': 0, 'Manual': 1},
    'Survey Feedback': {'Bad': 0, 'Good': 1, 'Neutral': 2},
}

# Feature names in the exact order the model expects
FEATURE_NAMES = [
    'Age', 'Gender', 'Location', 'Occupation', 'Income Bracket',
    'Credit Score', 'Channel', 'Device Type', 'Loans Accessed',
    'Savings Accessed', 'Monthly Avg Balance', 'Loans Taken',
    'Repayment Misses', 'Overdraft Events', 'Failed Payments',
    'Current Plan', 'Payment Mode', 'Tickets Raised',
    'Resolution Time (hrs)', 'Sentiment Score', 'Survey Feedback',
    'Onboarding Year', 'Onboarding Month', 'Customer Tenuer Year',
    'Total Logins', 'Support Intensity',
]

# Form field name -> model feature name mapping
FORM_TO_FEATURE = {
    'age':                  'Age',
    'gender':               'Gender',
    'location':             'Location',
    'occupation':           'Occupation',
    'income_bracket':       'Income Bracket',
    'credit_score':         'Credit Score',
    'channel':              'Channel',
    'device_type':          'Device Type',
    'loans_accessed':       'Loans Accessed',
    'savings_accessed':     'Savings Accessed',
    'monthly_avg_balance':  'Monthly Avg Balance',
    'loans_taken':          'Loans Taken',
    'repayment_misses':     'Repayment Misses',
    'overdraft_events':     'Overdraft Events',
    'failed_payments':      'Failed Payments',
    'current_plan':         'Current Plan',
    'payment_mode':         'Payment Mode',
    'tickets_raised':       'Tickets Raised',
    'resolution_time':      'Resolution Time (hrs)',
    'sentiment_score':      'Sentiment Score',
    'survey_feedback':      'Survey Feedback',
    'onboarding_year':      'Onboarding Year',
    'onboarding_month':     'Onboarding Month',
    'customer_tenure':      'Customer Tenuer Year',
    'total_logins':         'Total Logins',
    'support_intensity':    'Support Intensity',
}


def _model_paths():
    env_model = os.getenv("MODEL_PATH")
    candidates = [
        env_model,
        "selectedCatBoostClassifier.pkl",
        "CatBoostClassifier.pkl",
    ]
    return [BASE_DIR / p for p in candidates if p]


def load_model():
    global model

    try:
        for path in _model_paths():
            if path.exists():
                model = joblib.load(path)
                app.logger.info(f"Model loaded successfully from: {path}")
                return

        app.logger.error("Error: Could not find model file. Checked paths:")
        for path in _model_paths():
            app.logger.error(f"  - {path}")
    except Exception as e:
        app.logger.exception(f"Error loading model: {str(e)}")


load_model()


def _current_year():
    return datetime.now(timezone.utc).year


@app.route('/')
def home():
    return render_template(
        'index.html',
        current_year=_current_year(),
        label_encodings=LABEL_ENCODINGS,
    )


@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return render_template(
            'index.html',
            error="Model not loaded. Please contact administrator.",
            current_year=_current_year(),
            label_encodings=LABEL_ENCODINGS,
        )

    try:
        data = request.form.to_dict()

        # Build feature dict with proper types and label encoding
        feature_dict = {}
        for form_field, feature_name in FORM_TO_FEATURE.items():
            raw_value = data.get(form_field, '')

            if feature_name in LABEL_ENCODINGS:
                # Apply label encoding for categorical features
                feature_dict[feature_name] = LABEL_ENCODINGS[feature_name][raw_value]
            elif feature_name in ('Age', 'Credit Score', 'Loans Accessed', 'Savings Accessed',
                                  'Loans Taken', 'Repayment Misses', 'Overdraft Events',
                                  'Failed Payments', 'Onboarding Year', 'Onboarding Month'):
                feature_dict[feature_name] = int(raw_value)
            else:
                feature_dict[feature_name] = float(raw_value)

        # Create DataFrame with correct column order
        input_df = pd.DataFrame([feature_dict])[FEATURE_NAMES]

        # Make prediction
        prediction = model.predict(input_df)
        probability = model.predict_proba(input_df)

        # Calculate risk percentage
        churn_probability = probability[0][1] * 100

        # Determine risk level
        if churn_probability < 30:
            risk_level = "Low Risk"
            risk_color = "green"
        elif churn_probability < 70:
            risk_level = "Medium Risk"
            risk_color = "orange"
        else:
            risk_level = "High Risk"
            risk_color = "red"

        result = {
            'prediction': 'Will Churn' if prediction[0] == 1 else 'Will Not Churn',
            'probability': round(churn_probability, 2),
            'risk_level': risk_level,
            'risk_color': risk_color,
        }

        return render_template(
            'index.html',
            prediction=result,
            form_data=data,
            current_year=_current_year(),
            label_encodings=LABEL_ENCODINGS,
        )

    except Exception as e:
        app.logger.exception("Prediction error")
        return render_template(
            'index.html',
            error="An unexpected error occurred. Please check your inputs and try again.",
            form_data=request.form.to_dict(),
            current_year=_current_year(),
            label_encodings=LABEL_ENCODINGS,
        )


@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "model_loaded": model is not None}), 200


if __name__ == '__main__':
    app.run(
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "5000")),
        debug=os.getenv("FLASK_DEBUG", "false").lower() == "true",
    )
