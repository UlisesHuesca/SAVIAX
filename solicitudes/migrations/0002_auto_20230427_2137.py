# Generated by Django 3.2.5 on 2023-04-28 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitudes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proyecto',
            name='monto_total',
        ),
        migrations.AddField(
            model_name='subproyecto',
            name='descripcion',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]