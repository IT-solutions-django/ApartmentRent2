# Generated by Django 5.1.6 on 2025-02-16 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartment', '0002_databooking_alter_booking_apartment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('P', 'Ожидает'), ('C', 'Подтверждено'), ('X', 'Отменено'), ('D', 'Завершено')], default='P', max_length=1, verbose_name='Статус'),
        ),
    ]
