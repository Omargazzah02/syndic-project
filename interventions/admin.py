from django.contrib import admin
from .models import Intervention

@admin.register(Intervention)
class InterventionAdmin(admin.ModelAdmin):
    list_display = ('user', 'residence', 'type', 'status', 'created_at')
    list_filter = ('type', 'status', 'residence')
    search_fields = ('user__username',)
