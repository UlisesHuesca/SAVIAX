# Generated by Django 3.2.5 on 2022-04-23 01:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0035_historicalarticulosparasurtir'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articulosparasurtir',
            name='cantidad_salida',
        ),
        migrations.RemoveField(
            model_name='historicalarticulosparasurtir',
            name='cantidad_salida',
        ),
    ]
