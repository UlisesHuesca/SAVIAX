# Generated by Django 4.2.4 on 2023-09-09 00:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gastos', '0010_remove_solicitud_gasto_proyecto_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='archivo_xml',
            field=models.FileField(blank=True, null=True, upload_to='xml', validators=[django.core.validators.FileExtensionValidator(['xml'])]),
        ),
    ]
