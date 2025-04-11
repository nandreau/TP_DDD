from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from core.views import (
    UserRegistrationView,
    UserAdminViewSet,
    UserProfileView,
    DashboardView
)
from core.views.demographics import CountryDemographicsViewSet, CountryDemographicsReadOnlyView
from core.views.countries import CountryAdminViewSet, CountryReadOnlyView
# from core.views.concerthall import ConcertHallReadOnlyView
from core.views.groups import GroupAdminViewSet
from core.views.tokens import TokenProxyView


# ROUTER pour les ViewSets (CRUD admin)
router = DefaultRouter()
router.register(r'admin/demographics', CountryDemographicsViewSet, basename='demographics')
router.register(r'admin/countries', CountryAdminViewSet, basename='countries')
router.register(r'admin/users', UserAdminViewSet, basename='admin-users')
router.register(r'admin/groups', GroupAdminViewSet, basename='admin-groups')


urlpatterns = [
    # Auth et dashboard
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', obtain_auth_token, name='api_token_auth'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    # Endpoint read-only : pays + données démographiques combinées
    path('country/<str:code>/', CountryReadOnlyView.as_view(), name='country-detail'),

    path('demographics/<str:country>/', CountryDemographicsReadOnlyView.as_view(), name='countrydemographics-detail'),

    # Endpoints CRUD admin via DRF router
    path('', include(router.urls)),

    # Endpoint pour récupérer/mettre à jour les infos de l'utilisateur connecté
    path('profile/', UserProfileView.as_view(), name='user-profile'),

    # Endpoint pour le token proxy (admin)
    path('token-proxy/', TokenProxyView.as_view(), name='token-proxy'),

]
