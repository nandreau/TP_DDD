from rest_framework import serializers
from core.models.countries import Country
from core.serializers.demographics import CountryDemographicsSerializer

class CountrySerializer(serializers.ModelSerializer):
    demographics = CountryDemographicsSerializer(read_only=True)

    class Meta:
        model = Country
        fields = ['code', 'name', 'demographics']

    def validate_code(self, value):
        if self.instance is None and Country.objects.filter(code=value).exists():
            raise serializers.ValidationError("Un pays avec ce code existe déjà.")
        return value

    def validate(self, attrs):
        required_fields = ['code', 'name']
        errors = {}

        for field in required_fields:
            if not attrs.get(field):
                errors[field] = "Ce champ est requis."

        if errors:
            raise serializers.ValidationError(errors)

        return attrs
