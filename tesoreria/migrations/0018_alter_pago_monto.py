# Generated by Django 3.2.5 on 2022-06-10 15:26

from django.db import migrations
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tesoreria', '0017_auto_20220610_1008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pago',
            name='monto',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default_currency='MXN', max_digits=14),
        ),
    ]
