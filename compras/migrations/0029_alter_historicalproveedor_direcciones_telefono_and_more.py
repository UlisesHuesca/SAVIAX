# Generated by Django 4.2.4 on 2023-10-11 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0028_alter_historicalarticulocomprado_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalproveedor_direcciones',
            name='telefono',
            field=models.CharField(max_length=14, null=True),
        ),
        migrations.AlterField(
            model_name='proveedor_direcciones',
            name='telefono',
            field=models.CharField(max_length=14, null=True),
        ),
    ]
