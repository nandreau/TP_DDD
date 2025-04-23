from rest_framework import serializers
from core.models import Artist

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = '__all__'

    def validate_name(self, value):
        if self.instance is None and Artist.objects.filter(name=value).exists():
            raise serializers.ValidationError("Un artiste avec ce nom existe déjà.")
        return value

    def validate(self, attrs):
        if not attrs.get('name'):
            raise serializers.ValidationError({'name': "Le nom de l'artiste est requis."})
        return attrs
