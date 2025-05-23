# urls.py
from django.urls import path
from .views import ResidenceListView, ResidenceDetailsView, GetContactManagers ,IsManagerView

urlpatterns = [
    path('get_residences/', ResidenceListView.as_view(), name='get_residences'),
    path('get_residence_details/<int:residence_id>/' , ResidenceDetailsView.as_view() ,name='get_residence_details'),
    path ('get_contact_managers/<residence_id>/' , GetContactManagers.as_view() , name='get_contact_managers'),
    path ('is_manager/<int:residence_id>/' , IsManagerView.as_view() , name= "is_manager")
]
