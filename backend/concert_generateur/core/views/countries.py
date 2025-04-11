# core/views/countries.py
from rest_framework import viewsets
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAdminUser
from core.models.countries import Country
from core.serializers.countries import CountrySerializer
from core.permission import HasPermissions


class CountryAdminViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [IsAdminUser]

class CountryReadOnlyView(RetrieveAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [HasPermissions]
    required_permissions = ['core.view_country']
    permission_logic = 'all'
    lookup_field = 'code'
