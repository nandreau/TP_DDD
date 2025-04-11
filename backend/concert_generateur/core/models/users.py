from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUser(AbstractUser):
    USER_ROLE_CHOICES = (
        ('admin', "Admin"),
        ('organizer', "Directeur de concert"),
        ('artist', "Artiste"),
    )

    role = models.CharField(max_length=20, choices=USER_ROLE_CHOICES, default='artist')

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = 'admin'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

    class Meta:
        permissions = (
            ('can_view_dashboard', 'Peut accéder au dashboard'),
        )

@receiver(post_save, sender=CustomUser)
def assign_user_group(sender, instance, created, **kwargs):
    if created:
        group_map = {
            'admin': 'Admin Group',
            'organizer': 'Organizer Group',
            'artist': 'Artist Group',
        }
        group_name = group_map.get(instance.role)
        if group_name:
            group = Group.objects.get(name=group_name)
            instance.groups.add(group)
