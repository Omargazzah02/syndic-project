# charges_app/management/commands/generate_fake_charges.py

from django.core.management.base import BaseCommand
from charges_app.models import Charge, Residence
from faker import Faker
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = "Génère des charges fictives sur 12 mois pour entraîner le modèle"

    def handle(self, *args, **kwargs):
        fake = Faker('fr_FR')
        categories = ['charges_generales', 'ascenseur', 'jardinage', 'plomberie', 'électricité', 'nettoyage']
        residences = Residence.objects.all()

        if not residences.exists():
            self.stdout.write(self.style.ERROR("Aucune résidence trouvée. Ajoutez des résidences avant."))
            return

        for residence in residences:
            self.stdout.write(f"Génération pour résidence : {residence.residence_name}")
            for months_ago in range(1, 13):  # les 12 derniers mois
                for category in categories:
                    random_day = random.randint(1, 28)
                    date_creation = (datetime.now() - timedelta(days=30 * months_ago)).replace(day=random_day)
                    price = random.randint(50, 300)

                    Charge.objects.create(
                        residence=residence,
                        category=category,
                        title=f"{category.capitalize()} - {date_creation.strftime('%B %Y')}",
                        date_creation=date_creation,
                        price=price,
                    )

        self.stdout.write(self.style.SUCCESS("✅ Données fictives générées avec succès."))
