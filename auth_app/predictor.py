import pandas as pd
from .models import UserLoginHistory, UserLoginPrediction
from django.utils.timezone import localtime

def update_user_prediction(user):
    # Fetch all login timestamps for the user
    logs = UserLoginHistory.objects.filter(user=user).order_by('-timestamp')

    if logs.count() < 3:
        # Not enough data to make a reliable prediction
        return

    # Extract day names from timestamps (e.g., "Monday", "Tuesday")
    days = [localtime(log.timestamp).strftime("%A") for log in logs]
    df = pd.DataFrame(days, columns=["day"])

    # Find the most common login day
    predicted_day = df["day"].mode()[0]

    # Update or create prediction entry for this user
    prediction, _ = UserLoginPrediction.objects.get_or_create(user=user)
    prediction.predicted_day = predicted_day
    prediction.save()
