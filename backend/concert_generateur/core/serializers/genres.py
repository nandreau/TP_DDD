from rest_framework import serializers
from core.models import Genre, GenreFamily

class GenreFamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = GenreFamily
        fields = '__all__'

class GenreSerializer(serializers.ModelSerializer):
    family = GenreFamilySerializer(read_only=True)

    class Meta:
        model = Genre
        fields = '__all__'
