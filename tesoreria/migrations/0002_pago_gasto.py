# Generated by Django 3.2.5 on 2023-03-27 18:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gastos', '0009_solicitud_gasto_pagada'),
        ('tesoreria', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pago',
            name='gasto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gastos.solicitud_gasto'),
        ),
    ]
