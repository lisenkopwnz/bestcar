# Generated by Django 5.0.7 on 2024-12-09 18:20

import bestcar.validators
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departure', models.CharField(max_length=100, validators=[django.core.validators.RegexValidator(message='Поле должно содержать только русские буквы и символы \\-,./.', regex='^[а-яА-ЯёЁ0-9\\-,./ ]+$')], verbose_name='отправление')),
                ('arrival', models.CharField(max_length=100, validators=[django.core.validators.RegexValidator(message='Поле должно содержать только русские буквы и символы \\-,./.', regex='^[а-яА-ЯёЁ0-9\\-,./ ]+$')], verbose_name='прибытие')),
                ('departure_time', models.DateTimeField(validators=[bestcar.validators.Validators_date_model()], verbose_name='время отправления')),
                ('arrival_time', models.DateTimeField(validators=[bestcar.validators.Validators_date_model()], verbose_name='время прибытия')),
                ('price', models.PositiveSmallIntegerField(verbose_name='цена')),
                ('slug', models.SlugField(max_length=100)),
            ],
            options={
                'verbose_name': 'зарезервированные поездки',
                'verbose_name_plural': 'зарезервированные поездки',
            },
        ),
    ]
