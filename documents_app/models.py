from django.db import models
from residences_app.models import Residence
from django.core.validators import FileExtensionValidator
from charges_app.models import Charge


# Create your models here.
class Document (models.Model) : 
    CATEGORY_CHOICES = [
        ('Documents administratifs' , 'Documents administratifs'),
        ('Documents financiers' , 'Documents financiers'),
        ('Documents techniques' , 'Documents techniques') , 
        ('Documents relatifs à la gestion des travaux' , 'Documents relatifs à la gestion des travaux'),
        ('Documents relatifs aux assurances' , 'Documents relatifs aux assurances') ,
        ('Documents juridiques' , 'Documents juridiques'),
        ('Factures' , 'Factures'),
    ]
    residence = models.ForeignKey(Residence, on_delete=models.CASCADE, related_name='documents')
    category = models.CharField(max_length=100 , choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=100)
    pdf_file = models.FileField(upload_to='pdfs/',  validators=[FileExtensionValidator(allowed_extensions=['pdf'])] ,)
    date_creation = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title




class Invoice (Document) : 

        charge = models.OneToOneField(
        Charge,
        on_delete=models.CASCADE,
        related_name='invoice',

    )
        def save(self , *args, **kwargs):
             if self.charge:
                  self.residence = self.charge.residence
                  self.category = "Factures"
             super().save(*args, **kwargs)

    