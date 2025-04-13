# core/models/concerthall.py
from django.db import models

class ConcertHall(models.Model):
    name = models.CharField(max_length=150)  # Nom de la salle de concert
    capacity = models.PositiveIntegerField(null=True, blank=True)
    city = models.CharField(max_length=100)
    country_code = models.CharField(max_length=3)  # Champ non relationnel, stocke le CountryCode

    def __str__(self):
        return self.name
