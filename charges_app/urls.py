
from django.urls import path 
from .views import ChargesListView

urlpatterns = [
    path("get_charges/<int:residence_id>/" ,ChargesListView.as_view() , name="get_charges" )
    
]