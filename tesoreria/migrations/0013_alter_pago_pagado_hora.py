# Generated by Django 3.2.5 on 2022-06-06 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tesoreria', '0012_pago_hecho'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pago',
            name='pagado_hora',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
