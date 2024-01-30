# Generated by Django 3.2.5 on 2023-05-11 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entradas', '0002_auto_20230508_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entradaarticulo',
            name='cantidad',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=14),
        ),
        migrations.AlterField(
            model_name='entradaarticulo',
            name='cantidad_por_surtir',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=14),
        ),
        migrations.AlterField(
            model_name='historicalentradaarticulo',
            name='cantidad',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=14),
        ),
        migrations.AlterField(
            model_name='historicalentradaarticulo',
            name='cantidad_por_surtir',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=14),
        ),
        migrations.AlterField(
            model_name='reporte_calidad',
            name='cantidad',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=14),
        ),
    ]
