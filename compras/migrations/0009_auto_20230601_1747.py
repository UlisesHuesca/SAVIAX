# Generated by Django 3.2.5 on 2023-06-01 22:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('compras', '0008_auto_20230529_1914'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalproveedor_direcciones',
            name='completo',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalproveedor_direcciones',
            name='creado_por',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='user.profile'),
        ),
        migrations.AddField(
            model_name='proveedor',
            name='creado_por',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.profile'),
        ),
        migrations.AddField(
            model_name='proveedor_direcciones',
            name='completo',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='proveedor_direcciones',
            name='creado_por',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.profile'),
        ),
        migrations.CreateModel(
            name='HistoricalProveedor',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('razon_social', models.CharField(db_index=True, max_length=100, null=True)),
                ('nombre_comercial', models.CharField(blank=True, max_length=100, null=True)),
                ('rfc', models.CharField(db_index=True, max_length=13, null=True)),
                ('history_change_reason', models.TextField(null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('creado_por', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='user.profile')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical proveedor',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
