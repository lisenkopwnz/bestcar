# Generated by Django 5.0.7 on 2024-11-28 19:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bestcar', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='publishing_a_trip',
            name='author',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddIndex(
            model_name='publishing_a_trip',
            index=models.Index(fields=['departure', 'arrival', 'free_seating', 'departure_time'], name='trip_filter_idx'),
        ),
    ]
