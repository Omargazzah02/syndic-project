# Generated by Django 5.1.6 on 2025-04-15 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='phone',
            field=models.CharField(default=0, max_length=30),
            preserve_default=False,
        ),
    ]
