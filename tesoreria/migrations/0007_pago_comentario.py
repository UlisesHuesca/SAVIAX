# Generated by Django 3.2.5 on 2022-06-03 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tesoreria', '0006_alter_pago_pagado'),
    ]

    operations = [
        migrations.AddField(
            model_name='pago',
            name='comentario',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
