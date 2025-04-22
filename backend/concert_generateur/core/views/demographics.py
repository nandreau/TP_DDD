# core/views/demographics.py
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.generics import RetrieveAPIView
from core.models.demographics import CountryDemographics
from core.serializers.demographics import CountryDemographicsSerializer
from core.permission import HasPermissions


class CountryDemographicsViewSet(viewsets.ModelViewSet):
    queryset = CountryDemographics.objects.all()
    serializer_class = CountryDemographicsSerializer
    permission_classes = [IsAdminUser]

class CountryDemographicsReadOnlyView(RetrieveAPIView):
    queryset = CountryDemographics.objects.all()
    serializer_class = CountryDemographicsSerializer
    permission_classes = [HasPermissions]
    required_permissions = ['core.view_countrydemographics']
    permission_logic = 'all'
    lookup_field = 'country'
