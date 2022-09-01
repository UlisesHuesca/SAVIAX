# Generated by Django 3.2.5 on 2022-06-03 22:20

from django.db import migrations, models
import django.db.models.deletion
import djmoney.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('compras', '0046_auto_20220602_1929'),
        ('user', '0007_tipo_perfil_crear_sol'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cuenta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cuenta', models.CharField(max_length=13, null=True)),
                ('clabe', models.CharField(max_length=22, null=True)),
                ('monto_inicial_currency', djmoney.models.fields.CurrencyField(choices=[('MXN', 'Peso mexicano'), ('USD', 'US Dollar')], default='MXN', editable=False, max_length=3)),
                ('monto_inicial', djmoney.models.fields.MoneyField(blank=True, decimal_places=2, default_currency='MXN', max_digits=14, null=True)),
                ('saldo_currency', djmoney.models.fields.CurrencyField(choices=[('MXN', 'Peso mexicano'), ('USD', 'US Dollar')], default='MXN', editable=False, max_length=3)),
                ('saldo', djmoney.models.fields.MoneyField(blank=True, decimal_places=2, default_currency='MXN', max_digits=14, null=True)),
                ('banco', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='compras.banco')),
                ('distrito', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.distrito')),
                ('encargado', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.profile')),
                ('moneda', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='compras.moneda')),
            ],
        ),
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('saldo_currency', djmoney.models.fields.CurrencyField(choices=[('MXN', 'Peso mexicano'), ('USD', 'US Dollar')], default='MXN', editable=False, max_length=3)),
                ('saldo', djmoney.models.fields.MoneyField(blank=True, decimal_places=2, default_currency='MXN', max_digits=14, null=True)),
                ('pagada', models.BooleanField(default=False)),
                ('cuenta', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tesoreria.cuenta')),
                ('hecho_por', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Tesorero', to='user.profile')),
                ('oc', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='compras.compra')),
            ],
        ),
    ]
