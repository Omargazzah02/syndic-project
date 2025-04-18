from django.db import models
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

    part_percentage = models.FloatField(default=0.0 )

 
    def __str__(self):
        return f"Property {self.property_number} - {self.property_type}"

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"
