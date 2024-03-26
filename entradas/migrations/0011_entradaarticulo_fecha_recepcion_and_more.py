# Generated by Django 5.0.1 on 2024-02-14 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entradas', '0010_alter_resultado_evaluacion_nombre'),
    ]

    operations = [
        migrations.AddField(
            model_name='entradaarticulo',
            name='fecha_recepcion',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='entradaarticulo',
            name='recepcion',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalentradaarticulo',
            name='fecha_recepcion',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='historicalentradaarticulo',
            name='recepcion',
            field=models.BooleanField(default=False),
        ),
    ]
