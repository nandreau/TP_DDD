from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_ROLE_CHOICES = (
        ('admin', "Admin"),
        ('organizer', "Directeur de concert"),
        ('artist', "Artiste"),
    )

    role = models.CharField(max_length=20, choices=USER_ROLE_CHOICES, default='artist')

    def __str__(self):
        return self.username

    class Meta:
        permissions = (
            ('can_view_dashboard', 'Peut accéder au dashboard'),
        )
