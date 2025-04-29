# core/migrations/0008_assign_event_permissions.py
from django.db import migrations

def assign_event_and_hall_permissions(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    group_permissions = {
        "Artist Group": [
            "view_event",
            "view_concerthall",
        ],
        "Organizer Group": [
            "view_event",
            "add_event"
            "change_event"
            "view_concerthall",
        ],
        "Admin Group": [
            "view_event",
            "change_event"
            "add_event"
            "delete_event"
            "change_concerthall"
            "add_concerthall"
            "delete_concerthall"
            "view_concerthall",
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
        ('core', '0007_concerthall_concert_hall_id_concerthall_image_url_and_more'),
    ]

    operations = [
        migrations.RunPython(assign_event_and_hall_permissions, reverse_code=migrations.RunPython.noop),
    ]
