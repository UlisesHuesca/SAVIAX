# Generated by Django 3.2.5 on 2022-06-10 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tesoreria', '0018_alter_pago_monto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pago',
            name='comentario',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
