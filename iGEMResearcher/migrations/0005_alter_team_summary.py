# Generated by Django 4.2 on 2024-02-29 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("iGEMResearcher", "0004_team_summary"),
    ]

    operations = [
        migrations.AlterField(
            model_name="team",
            name="summary",
            field=models.TextField(blank=True, null=True),
        ),
    ]
