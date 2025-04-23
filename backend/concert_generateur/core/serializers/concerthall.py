from rest_framework import serializers
from core.models.concerthall import ConcertHall

class ConcertHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConcertHall
        fields = '__all__'

    def validate_name(self, value):
        # Si on est en création ET qu'un nom identique existe
        if self.instance is None and ConcertHall.objects.filter(name=value).exists():
            raise serializers.ValidationError("Une salle de concert avec ce nom existe déjà.")
        return value

    def validate_capacity(self, value):
        if not isinstance(value, int):
            raise serializers.ValidationError("La capacité doit être un entier.")
        if value <= 0:
            raise serializers.ValidationError("La capacité doit être supérieure à 0.")
        return value

    def validate(self, attrs):
        required_fields = ['name', 'city', 'country_code', 'capacity', 'address']
        errors = {}

        for field in required_fields:
            if not attrs.get(field):
                errors[field] = "Ce champ est requis."

        if errors:
            raise serializers.ValidationError(errors)

        return attrs
