# Generated by Django 5.0.7 on 2024-09-17 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bestcar', '0003_alter_publishing_a_trip_free_seating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publishing_a_trip',
            name='free_seating',
            field=models.PositiveSmallIntegerField(choices=[(1, '1')], default=1, verbose_name='количество мест'),
        ),
    ]
