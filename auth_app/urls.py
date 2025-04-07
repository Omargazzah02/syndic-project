from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import LoginView,ModifyPasswordView


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('modify-password/',ModifyPasswordView.as_view(), name='modify-password')




  

]