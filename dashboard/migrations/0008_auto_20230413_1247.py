# Generated by Django 3.2.5 on 2023-04-13 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_auto_20230412_2218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalinventario',
            name='cantidad',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=14),
        ),
        migrations.AlterField(
            model_name='historicalinventario',
            name='cantidad_apartada',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=14),
        ),
        migrations.AlterField(
            model_name='historicalinventario',
            name='cantidad_entradas',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=14),
        ),
        migrations.AlterField(
            model_name='inventario',
            name='cantidad',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=14),
        ),
        migrations.AlterField(
            model_name='inventario',
            name='cantidad_apartada',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=14),
        ),
        migrations.AlterField(
            model_name='inventario',
            name='cantidad_entradas',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=14),
        ),
    ]
