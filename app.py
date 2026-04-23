import os
from pathlib import Path
from datetime import datetime, timezone

import joblib
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', os.urandom(24))
BASE_DIR = Path(__file__).resolve().parent

# Initialize model as None
model = None


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
    return render_template('index.html', current_year=_current_year())

@app.route('/predict', methods=['POST'])
def predict():
    # Check if model is loaded
    if model is None:
        return render_template('index.html', error="Model not loaded. Please contact administrator.")
    
    try:
        # Get form data
        data = request.form.to_dict()
        
        # Convert to appropriate data types and prepare for prediction
        features = [
            float(data['total_logins']),
            float(data['tickets_raised']),
            int(data['onboarding_year']),
            float(data['customer_tenure']),
            float(data['sentiment_score']),
            float(data['loans_accessed']),
            float(data['loans_taken']),
            float(data['monthly_avg_balance'])
        ]
        
        # Make prediction
        prediction = model.predict([features])
        probability = model.predict_proba([features])
        
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
            'risk_color': risk_color
        }
        
        return render_template(
            'index.html',
            prediction=result,
            form_data=data,
            current_year=_current_year(),
        )
    
    except Exception as e:
        app.logger.exception("Prediction error")
        return render_template(
            'index.html',
            error="An unexpected error occurred. Please check your inputs and try again.",
            form_data=request.form.to_dict(),
            current_year=_current_year(),
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
