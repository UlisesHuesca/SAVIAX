# Generated by Django 3.2.5 on 2022-05-17 02:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0032_auto_20220516_2056'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='compra',
            name='otros_pagos',
        ),
        migrations.RemoveField(
            model_name='compra',
            name='otros_pagos_currency',
        ),
        migrations.RemoveField(
            model_name='historicalcompra',
            name='otros_pagos',
        ),
        migrations.RemoveField(
            model_name='historicalcompra',
            name='otros_pagos_currency',
        ),
    ]
