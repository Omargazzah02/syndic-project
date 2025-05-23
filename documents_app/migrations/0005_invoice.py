# Generated by Django 5.1.6 on 2025-04-21 19:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charges_app', '0002_alter_charge_category'),
        ('documents_app', '0004_remove_document_part_percentage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('document_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='documents_app.document')),
                ('visibility', models.BooleanField(default=False)),
                ('charge', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='invoice', to='charges_app.charge')),
            ],
            bases=('documents_app.document',),
        ),
    ]
