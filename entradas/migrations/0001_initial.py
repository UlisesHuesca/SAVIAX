# Generated by Django 3.2.5 on 2022-06-11 18:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('compras', '0050_auto_20220608_1122'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Entrada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.CharField(blank=True, max_length=250, null=True)),
                ('oc', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='compras.compra')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalEntrada',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('comentario', models.CharField(blank=True, max_length=250, null=True)),
                ('history_change_reason', models.TextField(null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('oc', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='compras.compra')),
            ],
            options={
                'verbose_name': 'historical entrada',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='EntradaArticulo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField(blank=True, null=True)),
                ('articulo_comprado', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='compras.articulocomprado')),
                ('entrada', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='entradas.entrada')),
            ],
        ),
    ]
