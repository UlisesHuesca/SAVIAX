# Generated by Django 5.0.1 on 2024-02-13 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0033_historicalpreevaluacion_comparativo_model_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalpreevaluacion',
            name='modified_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='preevaluacion',
            name='modified_at',
            field=models.DateTimeField(null=True),
        ),
    ]