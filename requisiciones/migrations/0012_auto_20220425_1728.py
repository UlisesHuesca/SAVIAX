# Generated by Django 3.2.5 on 2022-04-25 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requisiciones', '0011_auto_20220425_1619'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalsalidas',
            name='salida_firmada',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='salidas',
            name='salida_firmada',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
