# Generated by Django 4.2.8 on 2024-02-07 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0029_alter_historicalproveedor_direcciones_telefono_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estatus_proveedor',
            name='nombre',
            field=models.CharField(max_length=15, null=True, unique=True),
        ),
    ]
