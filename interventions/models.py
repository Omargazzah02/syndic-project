from django.db import models
from django.conf import settings
from residences_app.models import Residence  # Assuming you have this app

class Intervention(models.Model):
    INTERVENTION_CHOICES = [
        ('plomberie', 'Plomberie'),
        ('électricité', 'Électricité'),
        ('jardinage', 'Jardinage'),
        ('nettoyage', 'Nettoyage'),
    ]

    STATUS_CHOICES = [
        ('en_attente', 'En attente'),
        ('en_cours', 'En cours'),
        ('terminée', 'Terminée'),
        ('refusée', 'Refusée'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    residence = models.ForeignKey(Residence, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=INTERVENTION_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='en_attente')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} - {self.user.username} - {self.status}"


