# Generated by Django 3.2.5 on 2023-05-11 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0005_auto_20230504_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articulocomprado',
            name='cantidad',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=14),
        ),
        migrations.AlterField(
            model_name='articulocomprado',
            name='cantidad_pendiente',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=14),
        ),
        migrations.AlterField(
            model_name='historicalarticulocomprado',
            name='cantidad',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=14),
        ),
        migrations.AlterField(
            model_name='historicalarticulocomprado',
            name='cantidad_pendiente',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=14),
        ),
    ]
