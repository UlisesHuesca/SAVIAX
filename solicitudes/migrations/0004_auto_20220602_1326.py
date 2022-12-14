# Generated by Django 3.2.5 on 2022-06-02 18:26

from django.db import migrations
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('solicitudes', '0003_alter_subproyecto_presupuesto_currency'),
    ]

    operations = [
        migrations.AddField(
            model_name='subproyecto',
            name='gastado',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default_currency='MXN', max_digits=14, null=True),
        ),
        migrations.AddField(
            model_name='subproyecto',
            name='gastado_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('MXN', 'Peso mexicano'), ('USD', 'US Dollar')], default='MXN', editable=False, max_length=3),
        ),
    ]
