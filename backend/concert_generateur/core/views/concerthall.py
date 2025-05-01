from rest_framework import viewsets, generics, filters, status
from rest_framework.permissions import IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from core.models.concerthall import ConcertHall
from core.serializers.concerthall import ConcertHallSerializer
from core.permission import HasPermissions
from core.exceptions import handle_api_error, APIException

# Base filter config
CONCERTHALL_FILTERS = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
CONCERTHALL_FILTERSET_FIELDS = ['city', 'country_code', 'capacity']
CONCERTHALL_SEARCH_FIELDS = ['name', 'city']
CONCERTHALL_ORDERING_FIELDS = ['name', 'capacity']
CONCERTHALL_DEFAULT_ORDER = ['name']


class ConcertHallAdminViewSet(viewsets.ModelViewSet):
    queryset = ConcertHall.objects.all()
    serializer_class = ConcertHallSerializer
    permission_classes = [IsAdminUser]

    @handle_api_error
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @handle_api_error
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @handle_api_error
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @handle_api_error
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class ConcertHallReadOnlyView(generics.RetrieveAPIView):
    queryset = ConcertHall.objects.all()
    serializer_class = ConcertHallSerializer
    permission_classes = [HasPermissions]
    allowed_roles = ['admin', 'organizer']
    required_permissions = ['core.view_concerthall']
    permission_logic = 'all'
    lookup_field = 'id'

    @handle_api_error
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ConcertHallListView(generics.ListAPIView):
    queryset = ConcertHall.objects.all()
    serializer_class = ConcertHallSerializer
    permission_classes = [HasPermissions]
    allowed_roles = ['admin', 'organizer']
    required_permissions = ['core.view_concerthall']
    permission_logic = 'all'
    filter_backends = CONCERTHALL_FILTERS
    filterset_fields = CONCERTHALL_FILTERSET_FIELDS
    search_fields = CONCERTHALL_SEARCH_FIELDS
    ordering_fields = CONCERTHALL_ORDERING_FIELDS
    ordering = CONCERTHALL_DEFAULT_ORDER

    @handle_api_error
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ConcertHallByCountryView(generics.ListAPIView):
    serializer_class = ConcertHallSerializer
    permission_classes = [HasPermissions]
    allowed_roles = ['admin', 'organizer']
    required_permissions = ['core.view_concerthall']
    permission_logic = 'all'

    @handle_api_error
    def get_queryset(self):
        code = self.kwargs.get('country_code')
        if not code:
            raise APIException("Champ requis", "Le code pays est requis dans l'URL", status.HTTP_400_BAD_REQUEST)

        return ConcertHall.objects.filter(country_code=code.upper())

    @handle_api_error
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
