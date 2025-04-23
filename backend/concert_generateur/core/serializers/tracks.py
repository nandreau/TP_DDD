from rest_framework import serializers
from core.models import Track

from rest_framework import serializers
from core.models import Track

class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = '__all__'

    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError("Le titre du morceau est requis.")
        return value

    def validate_artist(self, value):
        if not value:
            raise serializers.ValidationError("L’artiste principal est requis.")
        return value

    def _validate_optional_int(self, field_name, value):
        if value in [None, ""]:
            return None
        try:
            return int(value)
        except (ValueError, TypeError):
            raise serializers.ValidationError({field_name: "Un nombre entier valide est requis."})

    def _validate_optional_bigint(self, field_name, value):
        return self._validate_optional_int(field_name, value)

    def validate_streams(self, value):
        return self._validate_optional_bigint("streams", value)

    def validate_appearances(self, value):
        return self._validate_optional_int("appearances", value)

    def validate_consecutive_appearances(self, value):
        return self._validate_optional_int("consecutive_appearances", value)

    def validate_entry_rank(self, value):
        return self._validate_optional_int("entry_rank", value)

    def validate_current_rank(self, value):
        return self._validate_optional_int("current_rank", value)

    def validate_peak_rank(self, value):
        return self._validate_optional_int("peak_rank", value)


class TrackDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = '__all__'

    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError("Le titre du morceau est requis.")
        return value

    def validate_artist(self, value):
        if not value:
            raise serializers.ValidationError("L’artiste principal est requis.")
        return value

class TrackListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['id', 'title', 'artist', 'artist_2', 'artist_3', 'artist_others', 'release_date', 'entry_date', 'entry_rank', 'current_rank', 'peak_rank', 'peak_date', 'appearances', 'consecutive_appearances', 'streams', 'source_date']

class TrackByArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['id', 'title', 'artist', 'artist_2', 'artist_3', 'artist_others', 'release_date', 'entry_date', 'entry_rank', 'current_rank', 'peak_rank', 'peak_date', 'appearances', 'consecutive_appearances', 'streams', 'source_date']
