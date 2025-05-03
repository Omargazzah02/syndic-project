from django.db import models
from residences_app.models import Residence
from properties_app.models import Property
from choices import CHARGE_CATEGORIES

# Create your models here.
class Charge (models.Model) : 
    residence = models.ForeignKey(Residence, on_delete=models.CASCADE, related_name='charges')
    title = models.CharField(max_length=100)
    category= models.CharField(max_length=50, choices=CHARGE_CATEGORIES)
    date_creation = models.DateTimeField(auto_now_add=True)
    price = models.FloatField()


    def __str__(self):
       
        return self.title
    def save(self , *args, **kwargs)  :
         is_new = self.pk is None  # On vérifie si c'est une création
         super().save(*args, **kwargs)  # D'abord on sauvegarde la Charge elle-même

         if not is_new:
           self.properties.all().delete()
         properties = self.residence.properties.all()
         for property in properties :
             part_percentage = property.category_shares.get(self.category, 0.0)

             PropertyCharge.objects.create(charge = self , property = property , part = (part_percentage /100 ) * float(self.price) )

class PropertyCharge (models.Model) :
    
    charge = models.ForeignKey(Charge, on_delete=models.CASCADE, related_name='properties' )
    property = models.ForeignKey(Property , on_delete=models.CASCADE , related_name='charges' )
    part = models.FloatField()
    def __str__(self):
        return self.charge.title+ " - "+self.property.property_type + " " + str(self.property.property_number)











    