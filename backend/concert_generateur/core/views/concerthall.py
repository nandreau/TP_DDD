from rest_framework import viewsets, generics, filters
from rest_framework.permissions import IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from core.models.concerthall import ConcertHall
from core.serializers.concerthall import ConcertHallSerializer
from core.permission import HasPermissions

# CRUD admin via ViewSet
class ConcertHallAdminViewSet(viewsets.ModelViewSet):
    queryset = ConcertHall.objects.all()
    serializer_class = ConcertHallSerializer
    permission_classes = [IsAdminUser]

# Read-only pour les autres utilisateurs
class ConcertHallReadOnlyView(generics.RetrieveAPIView):
    queryset = ConcertHall.objects.all()
    serializer_class = ConcertHallSerializer
    permission_classes = [HasPermissions]
    required_permissions = ['core.view_concerthall']
    permission_logic = 'all'
    lookup_field = 'id'

# Liste publique filtrable
class ConcertHallListView(generics.ListAPIView):
    queryset = ConcertHall.objects.all()
    serializer_class = ConcertHallSerializer
    permission_classes = [HasPermissions]
    required_permissions = ['core.view_concerthall']
    permission_logic = 'all'

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['city', 'country_code', 'capacity']
    search_fields = ['name', 'city']
    ordering_fields = ['name', 'capacity']
    ordering = ['name']

class ConcertHallByCountryView(generics.ListAPIView):
    serializer_class = ConcertHallSerializer
    permission_classes = [HasPermissions]
    required_permissions = ['core.view_concerthall']
    permission_logic = 'all'

    def get_queryset(self):
        code = self.kwargs['country_code'].upper()
        return ConcertHall.objects.filter(country_code=code)
