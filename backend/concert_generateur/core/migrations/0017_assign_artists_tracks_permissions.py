# core/migrations/0008_assign_event_permissions.py
from django.db import migrations

def assign_event_and_hall_permissions(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    group_permissions = {
        "Artist Group": [
            "view_track",
            "view_artist",
        ],
        "Organizer Group": [
            "view_track",
            "view_artist",
        ],
        "Admin Group": [
            "view_track",
            "view_artist",
            "change_track",
            "add_track",
            "delete_track",
            "change_artist",
            "add_artist",
            "delete_artist",
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
        ('core', '0016_track_artist_2_track_artist_3_track_artist_others'),
    ]

    operations = [
        migrations.RunPython(assign_event_and_hall_permissions, reverse_code=migrations.RunPython.noop),
    ]
