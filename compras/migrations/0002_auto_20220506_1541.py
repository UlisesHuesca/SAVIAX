# Generated by Django 3.2.5 on 2022-05-06 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compra',
            name='dias_de_credito',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='compra',
            name='dias_de_entrega',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='historicalcompra',
            name='dias_de_credito',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='historicalcompra',
            name='dias_de_entrega',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
