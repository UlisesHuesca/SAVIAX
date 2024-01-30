# Generated by Django 3.2.5 on 2023-08-08 19:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('activos', '0002_auto_20230808_1349'),
        ('requisiciones', '0010_auto_20230804_2231'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalsalidas',
            name='activo',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='activos.activo'),
        ),
        migrations.AddField(
            model_name='historicalsalidas',
            name='seleccionado',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='historicalsalidas',
            name='validacion_activos',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='salidas',
            name='activo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='activos.activo'),
        ),
        migrations.AddField(
            model_name='salidas',
            name='seleccionado',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='salidas',
            name='validacion_activos',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
