from django.db import migrations
from django.contrib.auth.models import Group

def create_user_groups(apps, schema_editor):
    group_names = ['Admin Group', 'Organizer Group', 'Artist Group']
    for name in group_names:
        Group.objects.get_or_create(name=name)

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_concerthall_country_countrydemographics'),
    ]

    operations = [
        migrations.RunPython(create_user_groups),
    ]
