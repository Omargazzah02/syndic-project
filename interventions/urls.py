from django.urls import path
from .views import InterventionListByResidenceAPIView, CreateInterventionAPIView ,UpdateInterventionStatus, InterventionDetail  

urlpatterns = [
    path('interventions/<int:residence_id>/', InterventionListByResidenceAPIView.as_view(), name='intervention-list-by-residence'),
    path('interventions/create/', CreateInterventionAPIView.as_view(), name='intervention-create'),
    path('interventions/update-status/<int:intervention_id>/', UpdateInterventionStatus.as_view(), name='update-intervention-status'),
    path('interventions/delete/<int:pk>/', InterventionDetail.as_view(), name='intervention-detail'),  # Uncomment if needed


]
