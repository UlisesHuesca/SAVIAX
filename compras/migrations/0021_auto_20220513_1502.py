# Generated by Django 3.2.5 on 2022-05-13 20:02

from django.db import migrations, models
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0020_auto_20220511_1930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compra',
            name='costo_fletes',
            field=djmoney.models.fields.MoneyField(blank=True, decimal_places=2, max_digits=14, null=True),
        ),
        migrations.AlterField(
            model_name='compra',
            name='dias_de_credito',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='compra',
            name='impuestos_adicionales',
            field=djmoney.models.fields.MoneyField(blank=True, decimal_places=2, max_digits=14, null=True),
        ),
        migrations.AlterField(
            model_name='historicalcompra',
            name='costo_fletes',
            field=djmoney.models.fields.MoneyField(blank=True, decimal_places=2, max_digits=14, null=True),
        ),
        migrations.AlterField(
            model_name='historicalcompra',
            name='dias_de_credito',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='historicalcompra',
            name='impuestos_adicionales',
            field=djmoney.models.fields.MoneyField(blank=True, decimal_places=2, max_digits=14, null=True),
        ),
        migrations.AlterField(
            model_name='historicalproveedor_completo',
            name='dias_credito',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='proveedor_completo',
            name='dias_credito',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
