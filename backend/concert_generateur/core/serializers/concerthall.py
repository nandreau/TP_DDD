from rest_framework import serializers
from core.models.concerthall import ConcertHall

class ConcertHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConcertHall
        fields = '__all__'
