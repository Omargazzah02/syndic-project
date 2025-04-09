from django.urls import path
from .views import PropertiesListView, PropertyDetailsView


urlpatterns = [

    path('get_properties_by_residence/<int:residence_id>/',PropertiesListView.as_view(), name='get_properties_by_residence'),
    path('get_property_details/<int:property_id>/',PropertyDetailsView.as_view(), name='get_property_details')
    
    
    
    
    


]