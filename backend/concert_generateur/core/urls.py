from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from core.views import UserRegistrationView
from core.views.dashboard import DashboardView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', obtain_auth_token, name='api_token_auth'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

]
