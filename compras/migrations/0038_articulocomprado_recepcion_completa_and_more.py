# Generated by Django 4.2.9 on 2024-02-20 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0037_compra_recepcion_completa_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='articulocomprado',
            name='recepcion_completa',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalarticulocomprado',
            name='recepcion_completa',
            field=models.BooleanField(default=False),
        ),
    ]