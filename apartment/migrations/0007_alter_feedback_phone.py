# Generated by Django 5.1.6 on 2025-02-19 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartment', '0006_alter_feedback_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='phone',
            field=models.CharField(max_length=11, verbose_name='Телефон'),
        ),
    ]
