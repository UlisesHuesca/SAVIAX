# Generated by Django 3.2.5 on 2022-07-21 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0060_auto_20220719_1825'),
    ]

    operations = [
        migrations.AddField(
            model_name='articulocomprado',
            name='seleccionado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalarticulocomprado',
            name='seleccionado',
            field=models.BooleanField(default=False),
        ),
    ]
