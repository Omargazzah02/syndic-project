from django.db import models
from residences_app.models import Residence
from django.core.validators import FileExtensionValidator


# Create your models here.
class Document (models.Model) : 
    CATEGORY_CHOICES = [
        ('Documents administratifs' , 'Documents administratifs'),
        ('Documents financiers' , 'Documents financiers'),
        ('Documents techniques' , 'Documents techniques') , 
        ('Documents relatifs à la gestion des travaux' , 'Documents relatifs à la gestion des travaux'),
        ('Documents relatifs aux assurances' , 'Documents relatifs aux assurances') ,
        ('Documents juridiques' , 'Documents juridiques')
    ]
    residence = models.ForeignKey(Residence, on_delete=models.CASCADE, related_name='documents')
    category = models.CharField(max_length=100 , choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=100)
    pdf_file = models.FileField(upload_to='pdfs/',  validators=[FileExtensionValidator(allowed_extensions=['pdf'])] ,)

