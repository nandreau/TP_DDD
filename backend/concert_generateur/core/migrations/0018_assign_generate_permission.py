# core/migrations/0018_assign_generate_permission.py
from django.db import migrations, models

def assign_event_and_hall_permissions(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    group_permissions = {
        "Organizer Group": [
            "core.generate_event",
            "core.validate_event",
            "core.view_concerthall",
        ],
        "Admin Group": [
            "core.generate_event",
            "core.validate_event",
            "core.view_concerthall",
        ],
    }

    for group_name, perm_codenames in group_permissions.items():
        try:
            group = Group.objects.get(name=group_name)
        except Group.DoesNotExist:
            continue

        for codename in perm_codenames:
            try:
                perm = Permission.objects.get(codename=codename, content_type__app_label='core')
                group.permissions.add(perm)
            except Permission.DoesNotExist:
                continue

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_assign_artists_tracks_permissions'),
    ]

    operations = [
        migrations.RunPython(assign_event_and_hall_permissions, reverse_code=migrations.RunPython.noop),
        migrations.AlterField(
            model_name="event",
            name="artists",
            field=models.ManyToManyField(
                blank=True, related_name="events", to="core.artist"
            ),
        ),
    ]
