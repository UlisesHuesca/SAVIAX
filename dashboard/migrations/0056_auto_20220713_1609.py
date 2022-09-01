# Generated by Django 3.2.5 on 2022-07-13 21:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_tipo_perfil_crear_sol'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('solicitudes', '0005_alter_subproyecto_gastado'),
        ('dashboard', '0055_auto_20220711_1831'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='folio',
            field=models.CharField(max_length=6, null=True, unique=True),
        ),
        migrations.CreateModel(
            name='HistoricalOrder',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('folio', models.CharField(db_index=True, max_length=6, null=True)),
                ('requisitar', models.BooleanField(default=False, null=True)),
                ('complete', models.BooleanField(null=True)),
                ('autorizar', models.BooleanField(default=None, null=True)),
                ('created_at', models.DateField(blank=True, editable=False)),
                ('created_at_time', models.TimeField(blank=True, editable=False)),
                ('approved_at', models.DateField(null=True)),
                ('approved_at_time', models.TimeField(null=True)),
                ('history_change_reason', models.TextField(null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('activo', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='solicitudes.activo')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('operacion', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='solicitudes.operacion')),
                ('proyecto', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='solicitudes.proyecto')),
                ('sector', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='solicitudes.sector')),
                ('sol_autorizada_por', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='user.profile')),
                ('staff', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='user.profile')),
                ('subproyecto', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='solicitudes.subproyecto')),
            ],
            options={
                'verbose_name': 'historical order',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
