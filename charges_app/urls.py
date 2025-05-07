
from django.urls import path 
from .views import ChargesListView,AddChargeView , ChargesManagingListView , DeleteChargeView , UpdateChargeView

urlpatterns = [
    path("get_charges/<int:residence_id>/" ,ChargesListView.as_view() , name="get_charges" ),
    path("add_charge/<int:residence_id>/" ,AddChargeView.as_view()  , name="add_charge" ),
    path("get_charges_managing/<int:residence_id>/" ,ChargesManagingListView.as_view() , name='get_charges_managing'),
    path("delete_charge/<int:charge_id>/" ,DeleteChargeView.as_view() , name='delete_charge'),
    path("update_charge/<int:residence_id>/<int:charge_id>/" ,UpdateChargeView.as_view() , name='update_charge'),

    
]