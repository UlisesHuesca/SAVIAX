# Generated by Django 3.2.5 on 2022-07-14 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0054_auto_20220707_1831'),
    ]

    operations = [
        migrations.AddField(
            model_name='articulocomprado',
            name='cantidad_entradas_pendientes',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='historicalarticulocomprado',
            name='cantidad_entradas_pendientes',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
