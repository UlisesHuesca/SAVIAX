# Generated by Django 4.2.4 on 2023-09-05 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entradas', '0006_auto_20230825_0835'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='historicalentrada',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical entrada', 'verbose_name_plural': 'historical entradas'},
        ),
        migrations.AlterModelOptions(
            name='historicalentradaarticulo',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical entrada articulo', 'verbose_name_plural': 'historical entrada articulos'},
        ),
        migrations.AlterModelOptions(
            name='historicalnc_articulo',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical n c_ articulo', 'verbose_name_plural': 'historical n c_ articulos'},
        ),
        migrations.AlterModelOptions(
            name='historicalno_conformidad',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical no_ conformidad', 'verbose_name_plural': 'historical no_ conformidads'},
        ),
        migrations.AlterField(
            model_name='historicalentrada',
            name='history_date',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='historicalentradaarticulo',
            name='history_date',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='historicalnc_articulo',
            name='history_date',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='historicalno_conformidad',
            name='history_date',
            field=models.DateTimeField(db_index=True),
        ),
    ]
