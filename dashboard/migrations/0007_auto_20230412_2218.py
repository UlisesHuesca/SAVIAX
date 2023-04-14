# Generated by Django 3.2.5 on 2023-04-13 03:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_almacen'),
        ('dashboard', '0006_auto_20230331_1823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalinventario',
            name='almacen',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='user.almacen'),
        ),
        migrations.AlterField(
            model_name='inventario',
            name='almacen',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.almacen'),
        ),
        migrations.DeleteModel(
            name='Almacen',
        ),
    ]
