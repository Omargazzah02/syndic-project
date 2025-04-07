# urls.py
from django.urls import path
from .views import ResidenceListView

urlpatterns = [
    path('get_residences/', ResidenceListView.as_view(), name='get_residences'),
]
