# Generated by Django 3.2.5 on 2023-04-03 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='compra',
            name='referencia',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='historicalcompra',
            name='referencia',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
