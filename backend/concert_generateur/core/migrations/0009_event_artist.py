# Generated by Django 5.2 on 2025-04-13 15:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0008_assign_event_permissions"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="artist",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="events",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
