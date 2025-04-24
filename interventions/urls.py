from django.urls import path
from .views import InterventionListByResidenceAPIView, CreateInterventionAPIView , InterventionDetail  , AcceptInterventionView , RefuseInterventionView , TerminateInterventionView

urlpatterns = [
    path('interventions/<int:residence_id>/', InterventionListByResidenceAPIView.as_view(), name='intervention-list-by-residence'),
    path('interventions/create/', CreateInterventionAPIView.as_view(), name='intervention-create'),
    path('interventions/accept/<int:intervention_id>/', AcceptInterventionView.as_view(), name='accept-intervention'),
    path('interventions/delete/<int:pk>/', InterventionDetail.as_view(), name='intervention-detail'),  # Uncomment if needed
    path('interventions/refuse/<int:intervention_id>/', RefuseInterventionView.as_view(), name='refuse-intervention'),  # Uncomment if needed
    path('interventions/terminate/<int:intervention_id>/', TerminateInterventionView.as_view(), name='terminate-intervention'),  # Uncomment if needed




]
