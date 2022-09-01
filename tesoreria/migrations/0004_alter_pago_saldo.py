# Generated by Django 3.2.5 on 2022-06-03 23:19

from decimal import Decimal
from django.db import migrations
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tesoreria', '0003_pago_distrito'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pago',
            name='saldo',
            field=djmoney.models.fields.MoneyField(blank=True, decimal_places=2, default=Decimal('0'), default_currency='MXN', max_digits=14, null=True),
        ),
    ]
