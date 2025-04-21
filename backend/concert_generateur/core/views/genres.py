from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from core.models import Genre, GenreFamily
from core.serializers.genres import GenreSerializer, GenreFamilySerializer
from core.permission import HasPermissions

# Admins only
class GenreAdminViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminUser]

class GenreFamilyAdminViewSet(viewsets.ModelViewSet):
    queryset = GenreFamily.objects.all()
    serializer_class = GenreFamilySerializer
    permission_classes = [IsAdminUser]

# Public lecture seule
class GenreListView(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [HasPermissions]
    required_permissions = ['core.view_genre']
    permission_logic = 'all'

class GenreFamilyListView(viewsets.ReadOnlyModelViewSet):
    queryset = GenreFamily.objects.all()
    serializer_class = GenreFamilySerializer
    permission_classes = [HasPermissions]
    required_permissions = ['core.view_genrefamily']
    permission_logic = 'all'
