# Generated by Django 4.2.9 on 2024-01-29 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entradas', '0007_alter_historicalentrada_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resultado_Evaluacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
            ],
        ),
        migrations.RemoveField(
            model_name='reporte_calidad',
            name='autorizado',
        ),
        migrations.AddField(
            model_name='reporte_calidad',
            name='evaluacion',
            field=models.BooleanField(default=None, null=True),
        ),
    ]
