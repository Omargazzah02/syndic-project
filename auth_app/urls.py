from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import LoginView,ModifyPasswordView ,UserProfileView


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('modify-password/',ModifyPasswordView.as_view(), name='modify-password'),
    path("profile/", UserProfileView.as_view(), name="user-profile"),





  

]