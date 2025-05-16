from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from auth_app.models import UserLoginPrediction
from django.utils import timezone

class Command(BaseCommand):
    help = 'Send email reminders for users predicted to log in today'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        #tomorrow = today + datetime.timedelta(days=1)
        #day_name = tomorrow.strftime('%A') 
        day_name = today.strftime('%A')  # ✅ Today’s day name (e.g., 'Wednesday')

        users_to_notify = UserLoginPrediction.objects.filter(predicted_day=day_name)

        for prediction in users_to_notify:
            user = prediction.user
            if not user.email:
                continue  # Skip if no email

            send_mail(
                subject='🕒 Connexion prévue aujourd\'hui',
                message=f"Bonjour {user.username}, vous êtes censé vous connecter aujourd'hui ({day_name}).",
                from_email=None,  # Uses DEFAULT_FROM_EMAIL from settings.py
                recipient_list=[user.email],
                fail_silently=False
            )
            self.stdout.write(f"✅ Email sent to {user.username} ({user.email}) for {day_name}")

        self.stdout.write("📩 Tous les rappels ont été envoyés pour aujourd'hui.")
