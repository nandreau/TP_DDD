from django.db import models
from .genres import Genre, GenreFamily

class Artist(models.Model):
    name = models.CharField(max_length=100, unique=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True, related_name='artists')
    genre_family = models.ForeignKey(GenreFamily, on_delete=models.SET_NULL, null=True, blank=True, related_name='artists')
    spotify_popularity = models.IntegerField(null=True, blank=True)
    followers = models.BigIntegerField(null=True, blank=True)
    longevity = models.IntegerField(null=True, blank=True)
    top_chart_presence = models.IntegerField(null=True, blank=True)
    spotify_streams_total = models.BigIntegerField(null=True, blank=True)

    # Stats par pays
    stats_FR = models.IntegerField(null=True, blank=True)
    stats_GB = models.IntegerField(null=True, blank=True)
    stats_DE = models.IntegerField(null=True, blank=True)
    stats_IT = models.IntegerField(null=True, blank=True)
    stats_ES = models.IntegerField(null=True, blank=True)
    stats_BE = models.IntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return str(self.name) if self.name else "Artiste sans nom"
