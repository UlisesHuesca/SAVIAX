# Generated by Django 4.2.4 on 2023-09-08 03:49

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gastos', '0007_alter_entrada_gasto_ajuste_gasto'),
    ]

    operations = [
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo_pdf', models.FileField(upload_to='facturas', validators=[django.core.validators.FileExtensionValidator(['pdf'])])),
                ('archivo_xml', models.FileField(upload_to='xml', validators=[django.core.validators.FileExtensionValidator(['xml'])])),
                ('fecha_subida', models.DateTimeField(blank=True, null=True)),
                ('solicitud_gasto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='facturas', to='gastos.solicitud_gasto')),
            ],
        ),
    ]
