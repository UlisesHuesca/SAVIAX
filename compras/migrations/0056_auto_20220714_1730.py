# Generated by Django 3.2.5 on 2022-07-14 22:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0055_auto_20220714_1712'),
    ]

    operations = [
        migrations.RenameField(
            model_name='articulocomprado',
            old_name='cantidad_entradas_pendientes',
            new_name='entradas_pendientes',
        ),
        migrations.RenameField(
            model_name='historicalarticulocomprado',
            old_name='cantidad_entradas_pendientes',
            new_name='entradas_pendientes',
        ),
    ]
