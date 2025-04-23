from rest_framework import serializers
from core.models import Genre, GenreFamily

class GenreFamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = GenreFamily
        fields = '__all__'

    def validate_name(self, value):
        if self.instance is None and GenreFamily.objects.filter(name=value).exists():
            raise serializers.ValidationError("Cette famille de genre existe déjà.")
        return value

    def validate(self, attrs):
        if not attrs.get('name'):
            raise serializers.ValidationError({'name': "Le nom de la famille de genre est requis."})
        return attrs


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

    def validate_name(self, value):
        if self.instance is None and Genre.objects.filter(name=value).exists():
            raise serializers.ValidationError("Ce nom de genre existe déjà.")
        return value

    def validate(self, attrs):
        if not attrs.get('name'):
            raise serializers.ValidationError({'name': "Le nom du genre est requis."})
        return attrs
