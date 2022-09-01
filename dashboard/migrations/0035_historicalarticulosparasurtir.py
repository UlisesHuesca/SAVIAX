# Generated by Django 3.2.5 on 2022-04-23 00:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0034_articulosparasurtir_cantidad_salida'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalArticulosparaSurtir',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('cantidad', models.IntegerField(blank=True, default=0, null=True)),
                ('surtir', models.BooleanField(default=False, null=True)),
                ('cantidad_requisitar', models.IntegerField(blank=True, default=0, null=True)),
                ('requisitar', models.BooleanField(default=False, null=True)),
                ('cantidad_salida', models.IntegerField(blank=True, default=0, null=True)),
                ('salida', models.BooleanField(default=False, null=True)),
                ('history_change_reason', models.TextField(null=True)),
                ('created_at', models.DateTimeField(blank=True, editable=False)),
                ('modified_at', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('articulos', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='dashboard.articulosordenados')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical articulospara surtir',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
