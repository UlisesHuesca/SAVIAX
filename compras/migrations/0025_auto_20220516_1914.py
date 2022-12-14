# Generated by Django 3.2.5 on 2022-05-17 00:14

from django.db import migrations
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0024_auto_20220516_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compra',
            name='otros_pagos',
            field=djmoney.models.fields.MoneyField(blank=True, decimal_places=2, max_digits=14, null=True),
        ),
        migrations.AlterField(
            model_name='compra',
            name='tipo_de_cambio',
            field=djmoney.models.fields.MoneyField(blank=True, decimal_places=2, default_currency='MXN', max_digits=14, null=True),
        ),
        migrations.AlterField(
            model_name='historicalcompra',
            name='otros_pagos',
            field=djmoney.models.fields.MoneyField(blank=True, decimal_places=2, max_digits=14, null=True),
        ),
        migrations.AlterField(
            model_name='historicalcompra',
            name='tipo_de_cambio',
            field=djmoney.models.fields.MoneyField(blank=True, decimal_places=2, default_currency='MXN', max_digits=14, null=True),
        ),
    ]
