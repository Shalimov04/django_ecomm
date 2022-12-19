# Generated by Django 4.1.4 on 2022-12-18 13:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_pickupaddress_delete_paymentdetails'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True, verbose_name='Имя клиента')),
                ('phone', models.CharField(blank=True, max_length=12, null=True, validators=[django.core.validators.RegexValidator(message='Формат ввода: +7XXXXXXXXXX. Введённое значение не соответствует формату.', regex='^\\+?1?\\d{10,11}$')], verbose_name='Номер телефона')),
                ('device', models.CharField(blank=True, max_length=200, null=True, verbose_name='ID устройства')),
            ],
            options={
                'verbose_name': 'Покупатель',
                'verbose_name_plural': 'Покупатели',
            },
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]