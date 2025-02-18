# Generated by Django 5.1.6 on 2025-02-17 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartment', '0003_booking_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Итоговая стоимость'),
        ),
    ]
