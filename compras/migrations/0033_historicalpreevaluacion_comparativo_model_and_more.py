# Generated by Django 5.0.1 on 2024-02-13 00:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0032_historicalpreevaluacion_completo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalpreevaluacion',
            name='comparativo_model',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='compras.comparativo'),
        ),
        migrations.AddField(
            model_name='preevaluacion',
            name='comparativo_model',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='compras.comparativo'),
        ),
    ]