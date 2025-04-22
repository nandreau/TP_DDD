from django.db import models

class GenreFamily(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    age_group_streams = models.JSONField(default=dict, blank=True)

    def __str__(self) -> str:
        return str(self.name) if self.name else "Genre Family sans nom"

    class Meta:
        verbose_name_plural = "Genre Families"

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True, db_column='genre_name', default='(unknown)')
    family = models.ForeignKey(GenreFamily, on_delete=models.SET_NULL, null=True, blank=True, related_name='genres')

    def __str__(self) -> str:
        return str(self.name) if self.name else "Genre sans nom"
