# Generated by Django 4.2 on 2024-02-16 08:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("iGEMResearcher", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Reference",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("authors", models.TextField()),
                ("title", models.CharField(max_length=255)),
                ("journal", models.CharField(max_length=255)),
                ("links", models.URLField()),
                (
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="references",
                        to="iGEMResearcher.team",
                    ),
                ),
            ],
        ),
    ]
