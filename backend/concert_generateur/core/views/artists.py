from rest_framework import generics, filters, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from core.models import Artist
from core.serializers.artists import ArtistSerializer
from core.permission import HasPermissions
from core.exceptions import handle_api_error, APIException
from django.core.exceptions import ObjectDoesNotExist
from core.views.base import BaseSafeModelViewSet, BaseSafeRetrieveAPIView, BaseSafeListAPIView

# Base config for all list views
BASE_FILTERS = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
SEARCH_FIELDS = ['name', 'genre__name', 'genre__family__name']
ORDERING_FIELDS = ['name', 'followers', 'spotify_popularity', 'longevity', 'top_chart_presence', 'spotify_streams_total']
DEFAULT_ORDERING = ['name']


class ArtistListCreateView(BaseSafeListAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [HasPermissions]
    required_permissions = ['core.view_artist']
    permission_logic = 'all'
    filter_backends = BASE_FILTERS
    search_fields = SEARCH_FIELDS
    ordering_fields = ORDERING_FIELDS
    ordering = DEFAULT_ORDERING

    @handle_api_error
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @handle_api_error
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class PublicArtistListView(BaseSafeListAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [HasPermissions]
    required_permissions = ['core.view_artist']
    permission_logic = 'all'
    filter_backends = BASE_FILTERS
    search_fields = SEARCH_FIELDS
    ordering_fields = ORDERING_FIELDS
    ordering = DEFAULT_ORDERING

    @handle_api_error
    def get_queryset(self):
        return Artist.objects.all()


class PublicArtistDetailView(BaseSafeRetrieveAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [HasPermissions]
    required_permissions = ['core.view_artist']
    permission_logic = 'all'
    lookup_field = 'name'


class AdminArtistDetailView(BaseSafeModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [IsAdminUser]
    required_permissions = ['core.view_artist']
    permission_logic = 'all'
    lookup_field = 'name'
