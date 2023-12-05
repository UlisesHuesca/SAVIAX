# Generated by Django 4.2.4 on 2023-10-18 19:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gastos', '0011_alter_factura_archivo_xml'),
        ('tesoreria', '0007_alter_pago_tipo_de_cambio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pago',
            name='gasto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='articulos', to='gastos.solicitud_gasto'),
        ),
    ]