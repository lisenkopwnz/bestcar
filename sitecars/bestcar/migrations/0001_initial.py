# Generated by Django 5.0.7 on 2024-11-28 19:15

import bestcar.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Категории',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Publishing_a_trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departure', models.CharField(max_length=100, validators=[bestcar.validators.Validators_language_model()], verbose_name='отправление')),
                ('arrival', models.CharField(max_length=100, validators=[bestcar.validators.Validators_language_model()], verbose_name='прибытие')),
                ('departure_time', models.DateTimeField(validators=[bestcar.validators.Validators_date_model()], verbose_name='время отправления')),
                ('arrival_time', models.DateTimeField(default=None, validators=[bestcar.validators.Validators_date_model()], verbose_name='время прибытия')),
                ('free_seating', models.PositiveSmallIntegerField(default=1, verbose_name='количество мест')),
                ('reserved_seats', models.PositiveIntegerField(default=0, verbose_name='количество бронированных мест')),
                ('price', models.PositiveSmallIntegerField(verbose_name='цена')),
                ('slug', models.SlugField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'Опубликованные поездки',
                'verbose_name_plural': 'Опубликованные поездки',
                'ordering': ('departure_time',),
            },
        ),
    ]
