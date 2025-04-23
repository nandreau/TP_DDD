from rest_framework import serializers
from core.models.event import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError("Le titre de l’événement est requis.")
        return value

    def validate(self, attrs):
        start = attrs.get("event_start")
        end = attrs.get("event_end")

        if start and end and start > end:
            raise serializers.ValidationError({
                "event_end": "La date de fin doit être postérieure à la date de début."
            })

        if not attrs.get("concert_hall"):
            raise serializers.ValidationError({
                "concert_hall": "Une salle de concert doit être spécifiée."
            })

        return attrs
