# Customer Churn Prediction (Financial Services)

Flask web app that predicts customer churn risk using a trained `CatBoostClassifier`.

## What Was Kept Same

- Existing UI flow (`/` form -> `/predict` result page)
- Existing model artifact usage
- Existing churn probability + risk band output

## Deployment-Ready Improvements

- Added robust model loading (supports `MODEL_PATH`, `selectedCatBoostClassifier.pkl`, and `CatBoostClassifier.pkl`)
- Added production runtime config (`HOST`, `PORT`, `FLASK_DEBUG`)
- Added health check endpoint: `GET /health`
- Added `wsgi.py` for WSGI servers
- Added `Procfile` (`web: gunicorn wsgi:app`)
- Updated dependencies to runtime-required packages
- Updated onboarding year/tenure logic to use dynamic current year

## Project Structure

```
Customer_Churn_predicrion_financial/
├── app.py
├── wsgi.py
├── Procfile
├── requirements.txt
├── CatBoostClassifier.pkl
├── templates/
│   └── index.html
└── static/
    └── style.css
```

## Run Locally

1. Create and activate virtual environment:

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

Linux/Mac:
```bash
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start app:

```bash
python app.py
```

Open: `http://127.0.0.1:5000`

## Environment Variables (Optional)

- `MODEL_PATH` -> absolute or relative path to model file
- `HOST` -> defaults to `0.0.0.0`
- `PORT` -> defaults to `5000`
- `FLASK_DEBUG` -> `true` or `false` (default `false`)

## Deploy (Render/Heroku-like Platforms)

- Build command:
```bash
pip install -r requirements.txt
```
- Start command:
```bash
gunicorn wsgi:app
```

## Health Check

- Endpoint: `GET /health`
- Sample response:

```json
{
  "status": "ok",
  "model_loaded": true
}
```
