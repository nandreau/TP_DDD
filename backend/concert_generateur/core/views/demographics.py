# core/views/demographics.py
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.generics import RetrieveAPIView
from core.models.demographics import CountryDemographics
from core.serializers.demographics import CountryDemographicsSerializer
from core.permission import HasPermissions
from core.views.base import BaseSafeModelViewSet, BaseSafeRetrieveAPIView

class CountryDemographicsViewSet(BaseSafeModelViewSet):
    queryset = CountryDemographics.objects.all()
    serializer_class = CountryDemographicsSerializer
    permission_classes = [IsAdminUser]

class CountryDemographicsReadOnlyView(BaseSafeRetrieveAPIView):
    queryset = CountryDemographics.objects.all()
    serializer_class = CountryDemographicsSerializer
    permission_classes = [HasPermissions]
    allowed_roles = ['admin', 'organizer']
    required_permissions = ['core.view_countrydemographics']
    permission_logic = 'all'
    lookup_field = 'country'
