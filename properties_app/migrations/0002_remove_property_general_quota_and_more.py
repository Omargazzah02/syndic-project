# Generated by Django 5.1.6 on 2025-04-17 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='general_quota',
        ),
        migrations.AddField(
            model_name='property',
            name='part_percentage',
            field=models.FloatField(default=0.0),
        ),
    ]
