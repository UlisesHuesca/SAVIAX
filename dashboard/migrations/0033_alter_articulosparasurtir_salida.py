# Generated by Django 3.2.5 on 2022-04-22 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0032_articulosparasurtir_salida'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articulosparasurtir',
            name='salida',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
