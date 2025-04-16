from django.urls import path
from .views import InterventionListByResidenceAPIView, CreateInterventionAPIView

urlpatterns = [
    path('interventions/<int:residence_id>/', InterventionListByResidenceAPIView.as_view(), name='intervention-list-by-residence'),
    path('interventions/create/', CreateInterventionAPIView.as_view(), name='intervention-create'),
]
