# Generated by Django 3.2.5 on 2022-05-06 23:03

from django.db import migrations
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0007_auto_20220506_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compra',
            name='costo_fletes',
            field=djmoney.models.fields.MoneyField(decimal_places=2, max_digits=14, null=True),
        ),
        migrations.AlterField(
            model_name='compra',
            name='impuestos_adicionales',
            field=djmoney.models.fields.MoneyField(decimal_places=2, max_digits=14, null=True),
        ),
        migrations.AlterField(
            model_name='historicalcompra',
            name='costo_fletes',
            field=djmoney.models.fields.MoneyField(decimal_places=2, max_digits=14, null=True),
        ),
        migrations.AlterField(
            model_name='historicalcompra',
            name='impuestos_adicionales',
            field=djmoney.models.fields.MoneyField(decimal_places=2, max_digits=14, null=True),
        ),
    ]
