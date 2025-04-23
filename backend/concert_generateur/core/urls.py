from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from core.views import (
    UserRegistrationView,
    UserAdminViewSet,
    UserProfileView,
    DashboardView
)
from core.views.demographics import CountryDemographicsViewSet, CountryDemographicsReadOnlyView
from core.views.concerthall import ConcertHallReadOnlyView, ConcertHallAdminViewSet, ConcertHallListView, ConcertHallByCountryView
from core.views.countries import CountryAdminViewSet, CountryReadOnlyView
from core.views.event import EventAdminViewSet, EventReadOnlyView, EventListView, EventByCountryView, OrganizerEventUpdateView, OrganizerEventCreateView
from core.views.groups import GroupAdminViewSet
from core.views.tokens import TokenProxyView
from core.views.artists import ArtistListCreateView, AdminArtistDetailView, PublicArtistListView, PublicArtistDetailView
from core.views.tracks import TrackListView, TrackDetailView, TrackByArtistView
from core.views.genres import GenreAdminViewSet, GenreFamilyAdminViewSet, GenreListView, GenreFamilyListView
from core.views.generate import GenerateEventView, ValidateEventView
from core.views.login import CustomLoginView

schema_view = get_schema_view(
    openapi.Info(
        title="Concert Generator API",
        default_version='v1',
        description="Explore et teste toutes les routes de ton API ici 🔥",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@concertgen.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

# ROUTER pour les ViewSets (CRUD admin)
router = DefaultRouter()
router.register(r'admin/demographics', CountryDemographicsViewSet, basename='demographics')
router.register(r'admin/countries', CountryAdminViewSet, basename='countries')
router.register(r'admin/users', UserAdminViewSet, basename='admin-users')
router.register(r'admin/groups', GroupAdminViewSet, basename='admin-groups')
router.register(r'admin/concerthalls', ConcertHallAdminViewSet, basename='admin-concerthalls')
router.register(r'admin/events', EventAdminViewSet, basename='admin-events')
router.register(r'admin/artists', AdminArtistDetailView, basename='admin-artists')
router.register(r'admin/genres', GenreAdminViewSet, basename='admin-genres')
router.register(r'admin/genrefamilies', GenreFamilyAdminViewSet, basename='admin-genrefamilies')


urlpatterns = [
    # Swagger
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # Auth et dashboard
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', CustomLoginView.as_view(), name='custom-login'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    # Endpoint read-only : pays + données démographiques combinées
    path('country/<str:code>/', CountryReadOnlyView.as_view(), name='country-detail'),
    path('demographics/<str:country>/', CountryDemographicsReadOnlyView.as_view(), name='countrydemographics-detail'),

    # Endpoints CRUD admin via DRF router
    path('', include(router.urls)),

    # Endpoint pour les artistes
    # Routes publiques
    path('artists/', PublicArtistListView.as_view(), name='artist-list'),
    path('artists/<str:name>/', PublicArtistDetailView.as_view(), name='artist-detail'),

    # Endpoint pour récupérer/mettre à jour les infos de l'utilisateur connecté
    path('profile/', UserProfileView.as_view(), name='user-profile'),

    # Events publics
    path('events/', EventListView.as_view(), name='event-list'),
    path('events/<int:id>/', EventReadOnlyView.as_view(), name='event-detail'),
    path('events/by-country/<str:country_code>/', EventByCountryView.as_view(), name='event-by-country'),
    path('events/organizer/<int:pk>/', OrganizerEventUpdateView.as_view(), name='organizer-event-update'),
    path('events/organizer/', OrganizerEventCreateView.as_view(), name='organizer-event-create'),

    # ConcertHalls publics
    path('concerthalls/', ConcertHallListView.as_view(), name='concerthall-list'),
    path('concerthalls/<int:id>/', ConcertHallReadOnlyView.as_view(), name='concerthall-detail'),
    path('concerthalls/by-country/<str:country_code>/', ConcertHallByCountryView.as_view(), name='concerthall-by-country'),

    # Genres publics
    path('genres/', GenreListView.as_view({'get': 'list'}), name='genre-list'),
    path('genrefamilies/', GenreFamilyListView.as_view({'get': 'list'}), name='genrefamily-list'),

    # Endpoint pour générer un événement
    path('generate-event/', GenerateEventView.as_view(), name='generate-event'),
    path('validate-event/', ValidateEventView.as_view(), name='validate-event'),
    # Endpoint pour le token proxy (admin)
    path('token-proxy/', TokenProxyView.as_view(), name='token-proxy'),

    # Endpoint pour les tracks
    path('tracks/', TrackListView.as_view(), name='track-list'),
    path('tracks/<int:id>/', TrackDetailView.as_view(), name='track-detail'),
    path('tracks/by-artist/<str:name>/', TrackByArtistView.as_view(), name='track-by-artist'),
]
