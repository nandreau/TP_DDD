# core/models/event.py
from django.db import models
from django.conf import settings
from core.models.concerthall import ConcertHall
from core.models.artists import Artist

class Event(models.Model):
    id = models.AutoField(primary_key=True)
    event_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    title = models.CharField(max_length=200)  # EventName
    event_start = models.DateTimeField(null=True, blank=True)
    event_end = models.DateTimeField(null=True, blank=True)
    image_url = models.URLField(max_length=500, blank=True, default='')

    concert_hall = models.ForeignKey(
        ConcertHall,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='events'
    )

    artists = models.ManyToManyField(
        Artist,
        blank=True,
        related_name='events'
    )

    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='organized_events'
    )

    def __str__(self):
        return str(self.title) if self.title else "Event sans titre"
