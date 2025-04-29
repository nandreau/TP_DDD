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
from django.core.exceptions import PermissionDenied


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

class ArtistUpdateView(BaseSafeModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [HasPermissions]
    required_permissions = ['core.change_artist']
    permission_logic = 'all'
    lookup_field = 'id'
    http_method_names = ['get', 'put', 'patch', 'delete']

    def get_queryset(self):
        # Un artiste ne peut voir/modifier que ses propres informations
        if not self.request.user.is_staff:
            return Artist.objects.filter(id=self.request.user.artist.id)
        return Artist.objects.all()

    def update(self, request, *args, **kwargs):
        if not request.user.is_staff and request.user.artist.id != int(kwargs['id']):
            raise PermissionDenied("Vous ne pouvez modifier que vos propres informations.")
        return super().update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if not request.user.is_staff and request.user.artist.id != int(kwargs['id']):
            raise PermissionDenied("Vous ne pouvez supprimer que votre propre compte.")
        return super().delete(request, *args, **kwargs)
