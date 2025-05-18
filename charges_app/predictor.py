# charges_app/predictor.py

import joblib
import pandas as pd
import os
from datetime import datetime, timedelta
from django.conf import settings

MODEL_PATH = os.path.join(settings.BASE_DIR, 'models', 'charge_predictor.pkl')

def predict_next_month_charges(residence_id, categories):
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Modèle non trouvé. Veuillez l'entraîner d'abord.")

    model = joblib.load(MODEL_PATH)
    today = datetime.today()
    next_month = today.replace(day=1) + timedelta(days=32)
    year, month = next_month.year, next_month.month

    data = pd.DataFrame([{
        'residence__id': residence_id,
        'category': cat,
        'year': year,
        'month': month
    } for cat in categories])

    predictions = model.predict(data)
    return dict(zip(categories, predictions.round(2)))
