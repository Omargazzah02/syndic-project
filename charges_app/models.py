from django.db import models
from residences_app.models import Residence
from properties_app.models import Property

# Create your models here.
class Charge (models.Model) : 
    residence = models.ForeignKey(Residence, on_delete=models.CASCADE, related_name='charges')
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=100)

    price = models.FloatField()

    def __str__(self):
       
        return self.title
    def save(self , *args, **kwargs)  :
         is_new = self.pk is None  # On vérifie si c'est une création
         super().save(*args, **kwargs)  # D'abord on sauvegarde la Charge elle-même
         properties = self.residence.properties.all()
         for property in properties :
             PropertyCharge.objects.create(charge = self , property = property , part = (property.part_percentage /100 ) * self.price )

class PropertyCharge (models.Model) :
    
    charge = models.ForeignKey(Charge, on_delete=models.CASCADE, related_name='properties' )
    property = models.ForeignKey(Property , on_delete=models.CASCADE , related_name='charges' )
    part = models.FloatField()
    def __str__(self):
        return self.charge.title+ " - "+self.property.property_type + " " + str(self.property.property_number)










    