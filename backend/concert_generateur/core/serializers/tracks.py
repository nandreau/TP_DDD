from rest_framework import serializers
from core.models import Track

class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = '__all__'

class TrackDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = '__all__'

class TrackListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['id', 'title', 'artist', 'artist_2', 'artist_3', 'artist_others', 'release_date', 'entry_date', 'entry_rank', 'current_rank', 'peak_rank', 'peak_date', 'appearances', 'consecutive_appearances', 'streams', 'source_date']

class TrackByArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['id', 'title', 'artist', 'artist_2', 'artist_3', 'artist_others', 'release_date', 'entry_date', 'entry_rank', 'current_rank', 'peak_rank', 'peak_date', 'appearances', 'consecutive_appearances', 'streams', 'source_date']

