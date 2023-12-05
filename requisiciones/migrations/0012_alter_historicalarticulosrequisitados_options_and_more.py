# Generated by Django 4.2.4 on 2023-09-05 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requisiciones', '0011_auto_20230808_1359'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='historicalarticulosrequisitados',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical articulos requisitados', 'verbose_name_plural': 'historical articulos requisitadoss'},
        ),
        migrations.AlterModelOptions(
            name='historicaldevolucion_articulos',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical devolucion_ articulos', 'verbose_name_plural': 'historical devolucion_ articuloss'},
        ),
        migrations.AlterModelOptions(
            name='historicalrequis',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical requis', 'verbose_name_plural': 'historical requiss'},
        ),
        migrations.AlterModelOptions(
            name='historicalsalidas',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical salidas', 'verbose_name_plural': 'historical salidass'},
        ),
        migrations.AlterField(
            model_name='historicalarticulosrequisitados',
            name='history_date',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='historicaldevolucion_articulos',
            name='history_date',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='historicalrequis',
            name='history_date',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='historicalsalidas',
            name='history_date',
            field=models.DateTimeField(db_index=True),
        ),
    ]