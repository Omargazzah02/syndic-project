# Generated by Django 5.1.7 on 2025-05-07 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charges_app', '0004_alter_charge_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='charge',
            name='category',
            field=models.CharField(max_length=50),
        ),
    ]
