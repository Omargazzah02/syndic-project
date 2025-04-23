from django.db import models
from choices import CHARGE_CATEGORIES
from django.core.exceptions import ValidationError


class Residence (models.Model):
    residence_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zip_code = models.IntegerField()
    country = models.CharField(max_length=100)
    floor_count = models.CharField(max_length=100)
    has_parking = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)  # Champ créé à la création de l'objet
    updated_at = models.DateTimeField(auto_now=True) 


    def __str__(self):
        return self.residence_name
    



