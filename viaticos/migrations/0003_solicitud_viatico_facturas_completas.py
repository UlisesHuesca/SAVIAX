# Generated by Django 3.2.5 on 2023-07-06 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viaticos', '0002_auto_20230501_1414'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitud_viatico',
            name='facturas_completas',
            field=models.BooleanField(default=False),
        ),
    ]
