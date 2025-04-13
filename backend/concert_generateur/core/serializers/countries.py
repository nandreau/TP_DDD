from rest_framework import serializers
from core.models.countries import Country
from core.serializers.demographics import CountryDemographicsSerializer

class CountrySerializer(serializers.ModelSerializer):
    demographics = CountryDemographicsSerializer(read_only=True)

    class Meta:
        model = Country
        fields = ['code', 'name', 'demographics']
