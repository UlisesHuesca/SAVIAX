# Generated by Django 3.2.5 on 2023-07-11 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0018_auto_20230705_2049'),
    ]

    operations = [
        migrations.AddField(
            model_name='compra',
            name='comentarios',
            field=models.TextField(max_length=400, null=True),
        ),
        migrations.AddField(
            model_name='historicalcompra',
            name='comentarios',
            field=models.TextField(max_length=400, null=True),
        ),
    ]
