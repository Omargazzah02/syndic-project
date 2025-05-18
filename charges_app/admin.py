from django.contrib import admin
from .models import Charge , PropertyCharge , ChargePrediction

# Register your models here.

@admin.register(Charge)
class ChargeAdmin(admin.ModelAdmin):
    list_display = ('id', 'residence', 'title', 'category', 'date_creation', 'price')
    list_filter = (
        'residence',          # filter by residence
        'category',           # filter by category
        'date_creation',      # filter by creation date (will show by day, month, year)
    )
    search_fields = ('title',)  # optional: add a search box on titles
    ordering = ('-date_creation',)  # optional: newest first

admin.site.register(PropertyCharge)


@admin.register(ChargePrediction)
class ChargePredictionAdmin(admin.ModelAdmin):
    list_display = ('residence', 'category', 'year', 'month', 'predicted_price')
