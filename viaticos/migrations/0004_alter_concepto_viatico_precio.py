# Generated by Django 4.2.4 on 2023-11-28 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viaticos', '0003_solicitud_viatico_facturas_completas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='concepto_viatico',
            name='precio',
            field=models.DecimalField(decimal_places=4, max_digits=10, null=True),
        ),
    ]
