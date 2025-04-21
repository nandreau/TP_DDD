from django.db import models

class Track(models.Model):
    title = models.CharField(max_length=255)
    artist = models.ForeignKey("Artist", on_delete=models.CASCADE, related_name="tracks")  # main_artist

    artist_2 = models.CharField(max_length=255, null=True, blank=True)
    artist_3 = models.CharField(max_length=255, null=True, blank=True)
    artist_others = models.TextField(null=True, blank=True)

    release_date = models.DateField(null=True, blank=True)
    entry_date = models.DateField(null=True, blank=True)
    entry_rank = models.IntegerField(null=True, blank=True)
    current_rank = models.IntegerField(null=True, blank=True)
    peak_rank = models.IntegerField(null=True, blank=True)
    peak_date = models.DateField(null=True, blank=True)

    appearances = models.IntegerField(null=True, blank=True)
    consecutive_appearances = models.IntegerField(null=True, blank=True)
    streams = models.BigIntegerField(null=True, blank=True)
    source_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.artist.name}"

