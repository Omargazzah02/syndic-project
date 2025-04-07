from django.urls import path
from .views import PropertiesListView


urlpatterns = [

    path('get_properties_by_residence/<int:residence_id>/',PropertiesListView.as_view(), name='get_properties_by_residence')




  

]