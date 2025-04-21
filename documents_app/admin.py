from django.contrib import admin
from .models import Document, Invoice
# Register your models here.

admin.site.register(Document)

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    exclude = ('residence','category', )  # ne pas l'afficher dans l'admin