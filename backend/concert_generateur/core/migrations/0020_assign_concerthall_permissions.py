from django.db import migrations

def assign_concerthall_permissions(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    ConcertHall = apps.get_model('core', 'ConcertHall')

    # Récupérer le groupe Organizer
    organizer_group = Group.objects.get(name='Organizer Group')

    # Récupérer la permission view_concerthall
    content_type = ContentType.objects.get_for_model(ConcertHall)
    view_permission = Permission.objects.get(
        content_type=content_type,
        codename='view_concerthall'
    )

    # Ajouter la permission au groupe
    organizer_group.permissions.add(view_permission)

def remove_concerthall_permissions(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    ConcertHall = apps.get_model('core', 'ConcertHall')

    # Récupérer le groupe Organizer
    organizer_group = Group.objects.get(name='Organizer Group')

    # Récupérer la permission view_concerthall
    content_type = ContentType.objects.get_for_model(ConcertHall)
    view_permission = Permission.objects.get(
        content_type=content_type,
        codename='view_concerthall'
    )

    # Retirer la permission du groupe
    organizer_group.permissions.remove(view_permission)

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0019_alter_event_options'),
    ]

    operations = [
        migrations.RunPython(assign_concerthall_permissions, remove_concerthall_permissions),
    ]
