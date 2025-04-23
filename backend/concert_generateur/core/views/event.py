from rest_framework import viewsets, generics, filters
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from core.models.event import Event
from core.serializers.event import EventSerializer
from core.permission import HasPermissions
from core.views.base import BaseSafeModelViewSet, BaseSafeRetrieveAPIView, BaseSafeListAPIView

# CRUD admin via ViewSet
class EventAdminViewSet(BaseSafeModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [HasPermissions]
    required_permissions = ['core.change_event']
    permission_logic = 'all'

    def destroy(self, request, *args, **kwargs):
        if request.user.role == "organizer":
            raise PermissionDenied("Seul un administrateur peut supprimer un événement.")
        return super().destroy(request, *args, **kwargs)


# Vue publique pour la liste complète
class EventListView(BaseSafeListAPIView):
    serializer_class = EventSerializer
    permission_classes = [HasPermissions]
    required_permissions = ['core.view_event']
    permission_logic = 'all'

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Filtres par champ (via query params)
    filterset_fields = ['concert_hall__city', 'concert_hall__country_code', 'event_start']

    # Recherche textuelle
    search_fields = ['title', 'concert_hall__name', 'concert_hall__city']

    # Tri Dynamique
    ordering_fields = ['event_start', 'event_end', 'title']
    ordering = ['event_start'] # tri par défaut

    def get_queryset(self):
        user = self.request.user

        # Si l'utilisateur est un artiste, on ne lui montre que ses événements
        if hasattr(user, 'role') and user.role == 'artist':
            return Event.objects.filter(artists=user)

        return Event.objects.all()

# Read-only pour les autres utilisateurs
class EventReadOnlyView(BaseSafeRetrieveAPIView):
    serializer_class = EventSerializer
    permission_classes = [HasPermissions]
    required_permissions = ['core.view_event']
    permission_logic = 'all'
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        if user.role == "artist":
            return Event.objects.filter(artists=user)
        return Event.objects.all()

# Vue par country_code
class EventByCountryView(BaseSafeListAPIView):
    serializer_class = EventSerializer
    permission_classes = [HasPermissions]
    required_permissions = ['core.view_event']
    permission_logic = 'all'

    def get_queryset(self):
        code = self.kwargs['country_code'].upper()
        base_queryset = Event.objects.filter(concert_hall__country_code=code)

        if self.request.user.role == "artist":
            return base_queryset.filter(artists=self.request.user)

        return base_queryset


class OrganizerEventUpdateView(generics.UpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [HasPermissions]
    required_permissions = ['core.change_event']
    permission_logic = 'all'

    def get_object(self):
        obj = super().get_object()
        if self.request.user.role != "organizer":
            raise PermissionDenied("Accès réservé aux organizers.")
        if obj.organizer != self.request.user:
            raise PermissionDenied("Vous n'êtes pas l'organisateur de cet event.")
        return obj

class OrganizerEventCreateView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [HasPermissions]
    required_permissions = ['core.add_event']
    permission_logic = 'all'

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != "organizer":
            raise PermissionDenied("Seul un organizer peut créer un événement.")
        serializer.save(organizer=user)
