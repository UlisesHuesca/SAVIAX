# Generated by Django 3.2.5 on 2022-05-06 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0002_auto_20220506_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalproveedor_completo',
            name='dias_credito',
            field=models.PositiveIntegerField(db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='proveedor_completo',
            name='dias_credito',
            field=models.PositiveIntegerField(null=True, unique=True),
        ),
    ]
