# Generated by Django 3.2.5 on 2022-06-03 00:44

from decimal import Decimal
from django.db import migrations
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('solicitudes', '0004_auto_20220602_1326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subproyecto',
            name='gastado',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='MXN', max_digits=14),
        ),
    ]
