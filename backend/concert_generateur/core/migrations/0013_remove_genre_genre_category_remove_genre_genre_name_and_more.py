# Generated by Django 5.2 on 2025-04-15 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0012_genrefamily_genre"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="genre",
            name="genre_category",
        ),
        migrations.RemoveField(
            model_name="genre",
            name="genre_name",
        ),
        migrations.AddField(
            model_name="genre",
            name="name",
            field=models.CharField(
                db_column="genre_name", default="(unknown)", max_length=100, unique=True
            ),
        ),
        migrations.AddField(
            model_name="genrefamily",
            name="audience_stats",
            field=models.JSONField(blank=True, default=dict),
        ),
    ]
