from rest_framework import generics, filters, viewsets
from core.models import Artist
from core.serializers.artists import ArtistSerializer
from core.permission import HasPermissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser

class ArtistListCreateView(generics.ListCreateAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [HasPermissions]
    required_permissions = ['core.view_artist']
    permission_logic = 'all'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name', 'genre__name', 'genre__family__name']
    ordering_fields = ['name', 'followers', 'spotify_popularity', 'longevity', 'top_chart_presence', 'spotify_streams_total']
    ordering = ['name']

class PublicArtistListView(generics.ListAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [HasPermissions]
    required_permissions = ['core.view_artist']
    permission_logic = 'all'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name', 'genre__name', 'genre__family__name']
    ordering_fields = ['name', 'followers', 'spotify_popularity', 'longevity', 'top_chart_presence', 'spotify_streams_total']
    ordering = ['name']

    def get_queryset(self):
        return Artist.objects.all()

class PublicArtistDetailView(generics.ListAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [HasPermissions]
    required_permissions = ['core.view_artist']
    permission_logic = 'all'
    lookup_field = 'name'


class AdminArtistDetailView(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [IsAdminUser]
    required_permissions = ['core.view_artist']
    permission_logic = 'all'
    lookup_field = 'name'
