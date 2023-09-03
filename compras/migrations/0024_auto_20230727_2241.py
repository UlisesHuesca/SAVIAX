# Generated by Django 3.2.5 on 2023-07-28 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0023_auto_20230717_1752'),
    ]

    operations = [
        migrations.AddField(
            model_name='compra',
            name='saldo_a_favor',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=14),
        ),
        migrations.AddField(
            model_name='historicalcompra',
            name='saldo_a_favor',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=14),
        ),
    ]