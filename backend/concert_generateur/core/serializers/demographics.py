from rest_framework import serializers
from core.models.demographics import CountryDemographics

class CountryDemographicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryDemographics
        fields = '__all__'
