from rest_framework import serializers
from core.models.demographics import CountryDemographics

class CountryDemographicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryDemographics
        fields = '__all__'

    def validate_country(self, value):
        # Un seul bloc démographique par pays autorisé
        if self.instance is None and CountryDemographics.objects.filter(country=value).exists():
            raise serializers.ValidationError("Les données démographiques pour ce pays existent déjà.")
        return value

    def validate(self, attrs):
        if not attrs.get('country'):
            raise serializers.ValidationError({'country': "Le pays est requis."})
        return attrs
