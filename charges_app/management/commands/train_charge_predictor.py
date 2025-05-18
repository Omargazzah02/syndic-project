# charges_app/management/commands/train_charge_predictor.py

import pandas as pd
import os
import joblib
from django.core.management.base import BaseCommand
from charges_app.models import Charge
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

class Command(BaseCommand):
    help = "Train AI model to predict next month's charges per category"

    def handle(self, *args, **kwargs):
        charges = Charge.objects.all().values('residence__id', 'category', 'price', 'date_creation')
        df = pd.DataFrame(charges)

        if df.empty:
            self.stdout.write(self.style.ERROR("Pas assez de données pour entraîner le modèle."))
            return

        df['year'] = pd.to_datetime(df['date_creation']).dt.year
        df['month'] = pd.to_datetime(df['date_creation']).dt.month

        X = df[['residence__id', 'category', 'year', 'month']]
        y = df['price']

        preprocessor = ColumnTransformer(transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), ['residence__id', 'category']),
        ], remainder='passthrough')

        model = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('regressor', LinearRegression())
        ])

        model.fit(X, y)

        os.makedirs('models', exist_ok=True)
        joblib.dump(model, 'models/charge_predictor.pkl')

        self.stdout.write(self.style.SUCCESS("Modèle entraîné et sauvegardé avec succès."))
