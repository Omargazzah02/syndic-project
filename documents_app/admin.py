from django.contrib import admin
from .models import Document, Invoice
# Register your models here.

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'date_creation', 'summary')  # Add 'summary' here if needed
admin.site.register(Document, DocumentAdmin)


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    exclude = ('residence','category', )  # ne pas l'afficher dans l'admin