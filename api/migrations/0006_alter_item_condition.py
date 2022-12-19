# Generated by Django 4.1.4 on 2022-12-17 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_batch_options_alter_brand_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='condition',
            field=models.CharField(choices=[('NEW', 'Новый'), ('USED', 'Б/у'), ('DISCOUNT', 'Уценка')], default='NEW', max_length=10, verbose_name='Состояние'),
        ),
    ]