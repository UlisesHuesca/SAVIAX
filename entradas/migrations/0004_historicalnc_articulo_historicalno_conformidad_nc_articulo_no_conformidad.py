# Generated by Django 3.2.5 on 2023-05-31 18:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('compras', '0008_auto_20230529_1914'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('entradas', '0003_auto_20230511_1432'),
    ]

    operations = [
        migrations.CreateModel(
            name='No_Conformidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.TextField(max_length=250, null=True)),
                ('nc_date', models.DateField(blank=True, null=True)),
                ('nc_hora', models.TimeField(blank=True, null=True)),
                ('completo', models.BooleanField(default=False)),
                ('almacenista', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.profile')),
                ('oc', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='compras.compra')),
            ],
        ),
        migrations.CreateModel(
            name='NC_Articulo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('articulo_comprado', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='compras.articulocomprado')),
                ('nc', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='entradas.no_conformidad')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalNo_Conformidad',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('comentario', models.TextField(max_length=250, null=True)),
                ('nc_date', models.DateField(blank=True, null=True)),
                ('nc_hora', models.TimeField(blank=True, null=True)),
                ('history_change_reason', models.TextField(null=True)),
                ('completo', models.BooleanField(default=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('almacenista', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='user.profile')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('oc', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='compras.compra')),
            ],
            options={
                'verbose_name': 'historical no_ conformidad',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalNC_Articulo',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('cantidad', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ('history_change_reason', models.TextField(null=True)),
                ('created_at', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('articulo_comprado', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='compras.articulocomprado')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('nc', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='entradas.no_conformidad')),
            ],
            options={
                'verbose_name': 'historical n c_ articulo',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
