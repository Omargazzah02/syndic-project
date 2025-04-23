from django.db import models
from django.core.exceptions import ValidationError
from choices import CHARGE_CATEGORIES
from auth_app.models import CustomUser
from residences_app.models import Residence

class Property(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='properties')
    residence = models.ForeignKey(Residence, on_delete=models.CASCADE, related_name='properties')
    
    PROPERTY_TYPES = [
        ('maison', 'Maison'),
        ('appartement', 'Appartement'),
        ('cave', 'Cave'),
    ]
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPES)
    
    property_number = models.IntegerField()
    property_size = models.FloatField()
    description = models.TextField()
    status = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    number_of_rooms = models.IntegerField()
    category_shares = models.JSONField(null=True)

    def clean(self):
        expected_keys = [key for key, _ in CHARGE_CATEGORIES]
        shares = self.category_shares or {}

        missing = []
        errors = []

        for key in expected_keys:
            if key not in shares:
                missing.append(key)
            else:
                value = shares[key]
                if isinstance(value, str):
                    try:
                        shares[key] = float(value)
                    except ValueError:
                        errors.append(f"La valeur pour '{key}' doit être un nombre.")
                elif not isinstance(value, (float, int)):
                    errors.append(f"La valeur pour '{key}' doit être un nombre.")

        if missing:
            errors.append(f"Catégories manquantes : {missing}")

        if errors:
            raise ValidationError(errors)

        return super().clean()

    def __str__(self):
        return f"Property {self.property_number} - {self.property_type}"

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"
