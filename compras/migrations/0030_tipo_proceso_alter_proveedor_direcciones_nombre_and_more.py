# Generated by Django 5.0.1 on 2024-02-07 01:23

import django.db.models.deletion
import simple_history.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0029_alter_historicalproveedor_direcciones_telefono_and_more'),
        ('dashboard', '0017_merge_20240204_1331'),
        ('user', '0004_alter_banco_nombre'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tipo_Proceso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Preevaluacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField()),
                ('requisitos_sgc_ver', models.CharField(blank=True, max_length=255, null=True)),
                ('sgc_b', models.BooleanField(default=False)),
                ('especs_ver', models.CharField(blank=True, max_length=255, null=True)),
                ('especs_b', models.BooleanField(default=False)),
                ('precios_ver', models.CharField(blank=True, max_length=255, null=True)),
                ('precios_b', models.BooleanField(default=False)),
                ('control_cadena_suministro', models.CharField(blank=True, max_length=255, null=True)),
                ('control_cadena_b', models.BooleanField(default=False)),
                ('resultado', models.BooleanField(default=False)),
                ('capacidad_proveedor', models.CharField(blank=True, max_length=255, null=True)),
                ('capacidad_proveedor_b', models.BooleanField(default=False)),
                ('areas_exito', models.CharField(blank=True, max_length=255, null=True)),
                ('areas_oportunidad', models.CharField(blank=True, max_length=255, null=True)),
                ('creado_por', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.profile')),
                ('criticidad', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.criticidad')),
                ('nombre', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='preevaluacion', to='compras.proveedor')),
                ('tipo_proceso', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='compras.tipo_proceso')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalPreevaluacion',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('creado_at', models.DateTimeField(blank=True, editable=False)),
                ('modified_at', models.DateTimeField()),
                ('requisitos_sgc_ver', models.CharField(blank=True, max_length=255, null=True)),
                ('sgc_b', models.BooleanField(default=False)),
                ('especs_ver', models.CharField(blank=True, max_length=255, null=True)),
                ('especs_b', models.BooleanField(default=False)),
                ('precios_ver', models.CharField(blank=True, max_length=255, null=True)),
                ('precios_b', models.BooleanField(default=False)),
                ('control_cadena_suministro', models.CharField(blank=True, max_length=255, null=True)),
                ('control_cadena_b', models.BooleanField(default=False)),
                ('resultado', models.BooleanField(default=False)),
                ('capacidad_proveedor', models.CharField(blank=True, max_length=255, null=True)),
                ('capacidad_proveedor_b', models.BooleanField(default=False)),
                ('areas_exito', models.CharField(blank=True, max_length=255, null=True)),
                ('areas_oportunidad', models.CharField(blank=True, max_length=255, null=True)),
                ('history_change_reason', models.TextField(null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('creado_por', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='user.profile')),
                ('criticidad', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='dashboard.criticidad')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('nombre', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='compras.proveedor')),
                ('tipo_proceso', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='compras.tipo_proceso')),
            ],
            options={
                'verbose_name': 'historical preevaluacion',
                'verbose_name_plural': 'historical preevaluacions',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
