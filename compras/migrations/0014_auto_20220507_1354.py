# Generated by Django 3.2.5 on 2022-05-07 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0013_auto_20220506_2005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compra',
            name='flete',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='historicalcompra',
            name='flete',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
