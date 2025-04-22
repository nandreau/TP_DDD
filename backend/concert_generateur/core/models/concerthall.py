# core/models/concerthall.py
from django.db import models

class ConcertHall(models.Model):
    id = models.AutoField(primary_key=True)
    concert_hall_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    name = models.CharField(max_length=150)  # ConcertHallName
    capacity = models.PositiveIntegerField(null=True, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    country_code = models.CharField(max_length=3)
    postal_code = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True, default='')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    image_url = models.URLField(max_length=500, blank=True, default='')

    def __str__(self):
        return self.name
