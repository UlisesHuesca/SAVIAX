# Generated by Django 3.2.5 on 2023-03-23 00:14

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dashboard', '0001_initial'),
        ('user', '0001_initial'),
        ('solicitudes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tipo_Gasto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=15, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Solicitud_Gasto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('folio', models.CharField(max_length=6, null=True, unique=True)),
                ('complete', models.BooleanField(null=True)),
                ('autorizar', models.BooleanField(default=None, null=True)),
                ('created_at', models.DateField(null=True)),
                ('created_at_time', models.TimeField(null=True)),
                ('approved_at', models.DateField(null=True)),
                ('approbado_fecha2', models.DateField(null=True)),
                ('approved_at_time', models.TimeField(null=True)),
                ('aprobado_hora2', models.TimeField(null=True)),
                ('area', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='solicitudes.operacion')),
                ('proyecto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='solicitudes.proyecto')),
                ('staff', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Crea_gasto', to='user.profile')),
                ('subproyecto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='solicitudes.subproyecto')),
                ('superintendente', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='superintendente', to='user.profile')),
                ('tipo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='gastos.tipo_gasto')),
            ],
        ),
        migrations.CreateModel(
            name='Articulo_Gasto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clase', models.BooleanField(default=False, null=True)),
                ('concepto', models.CharField(max_length=25, null=True)),
                ('cantidad', models.IntegerField(blank=True, default=0, null=True)),
                ('precio_unitario', models.DecimalField(blank=True, decimal_places=2, max_digits=14, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('factura_pdf', models.FileField(blank=True, null=True, upload_to='facturas', validators=[django.core.validators.FileExtensionValidator(['pdf'])])),
                ('factura_xml', models.FileField(blank=True, null=True, upload_to='xml', validators=[django.core.validators.FileExtensionValidator(['xml'])])),
                ('gasto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='gastos.solicitud_gasto')),
                ('producto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.inventario')),
            ],
        ),
    ]
