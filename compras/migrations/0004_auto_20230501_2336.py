# Generated by Django 3.2.5 on 2023-05-02 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0003_alter_proveedor_nombre_comercial'),
    ]

    operations = [
        migrations.AddField(
            model_name='compra',
            name='facturas_completas',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalcompra',
            name='facturas_completas',
            field=models.BooleanField(default=False),
        ),
    ]
