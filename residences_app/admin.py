from django.contrib import admin
from django import forms
from .models import Residence
from properties_app.models import Property

class PropertyInline(admin.TabularInline):
    model = Property
    fields = ('part_percentage',)
    extra = 0
    def has_add_permission(self, request, obj=None):
        return False  # Cela supprime le bouton "Add another Property"

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)

        class CleanedFormset(formset):
            def clean(self_inner):
                super().clean()
                total = 0
                for form in self_inner.forms:
                    if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                        total += form.cleaned_data.get('part_percentage', 0)

                if round(total, 2) != 100.00:
                    raise forms.ValidationError("Le total des parts doit être exactement égal à 100 %.")

        return CleanedFormset

class ResidenceAdmin(admin.ModelAdmin):
    inlines = [PropertyInline]

admin.site.register(Residence, ResidenceAdmin)
