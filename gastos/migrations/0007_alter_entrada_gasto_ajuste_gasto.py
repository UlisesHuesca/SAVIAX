# Generated by Django 3.2.5 on 2023-06-14 17:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gastos', '0006_auto_20230613_1741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrada_gasto_ajuste',
            name='gasto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gastos.articulo_gasto'),
        ),
    ]
