from django.contrib import admin
from .models import Property

# Register your models here.

@admin.register(Property)
class Property (admin.ModelAdmin) :
    exclude = ("part_percentage",)