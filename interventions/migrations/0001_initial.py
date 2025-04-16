# Generated by Django 5.1.7 on 2025-04-16 00:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('residences_app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Intervention',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('plomberie', 'Plomberie'), ('électricité', 'Électricité'), ('jardinage', 'Jardinage'), ('nettoyage', 'Nettoyage')], max_length=50)),
                ('status', models.CharField(choices=[('en_attente', 'En attente'), ('en_cours', 'En cours'), ('terminée', 'Terminée'), ('refusée', 'Refusée')], default='en_attente', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('residence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='residences_app.residence')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
