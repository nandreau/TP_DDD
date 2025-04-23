from rest_framework import generics, filters
from rest_framework.exceptions import PermissionDenied
from core.models import Track
from core.serializers.tracks import TrackSerializer, TrackDetailSerializer, TrackListSerializer, TrackByArtistSerializer
from core.permission import HasPermissions
from django_filters.rest_framework import DjangoFilterBackend
from core.views.base import BaseSafeModelViewSet, BaseSafeRetrieveAPIView, BaseSafeListAPIView, BaseSafeListCreateAPIView

class TrackListCreateView(BaseSafeListCreateAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = [HasPermissions]
    required_permissions = ['core.view_track']
    permission_logic = 'all'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['title', 'artist__name']
    ordering_fields = ['title', 'artist__name', 'release_date', 'entry_date', 'entry_rank', 'current_rank', 'peak_rank', 'peak_date', 'appearances', 'consecutive_appearances', 'streams', 'source_date']
    ordering = ['title']

class TrackDetailView(BaseSafeRetrieveAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackDetailSerializer
    permission_classes = [HasPermissions]
    required_permissions = ['core.view_track']
    permission_logic = 'all'
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied("Seul un admin peut supprimer un morceau.")
        return super().delete(request, *args, **kwargs)

class TrackByArtistView(BaseSafeListAPIView):
    serializer_class = TrackByArtistSerializer
    permission_classes = [HasPermissions]
    required_permissions = ['core.view_track']
    permission_logic = 'all'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['title', 'artist__name']
    ordering_fields = ['title', 'artist__name', 'release_date', 'entry_date', 'entry_rank', 'current_rank', 'peak_rank', 'peak_date', 'appearances', 'consecutive_appearances', 'streams', 'source_date']
    ordering = ['title']

    def get_queryset(self):
        artist_name = self.kwargs['name']
        return Track.objects.filter(artist__name=artist_name)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['artist_name'] = self.kwargs['name']
        return context

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

class TrackListView(BaseSafeListAPIView):
    serializer_class = TrackListSerializer
    permission_classes = [HasPermissions]
    required_permissions = ['core.view_track']
    permission_logic = 'all'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['title', 'artist__name']
    ordering_fields = ['title', 'artist__name', 'release_date', 'entry_date', 'entry_rank', 'current_rank', 'peak_rank', 'peak_date', 'appearances', 'consecutive_appearances', 'streams', 'source_date']
    ordering = ['title']

    def get_queryset(self):
        return Track.objects.all()
