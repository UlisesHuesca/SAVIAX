# Generated by Django 3.2.5 on 2022-06-13 14:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_tipo_perfil_crear_sol'),
        ('entradas', '0002_historicalentradaarticulo'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrada',
            name='almacenista',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.profile'),
        ),
        migrations.AddField(
            model_name='entrada',
            name='completo',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalentrada',
            name='almacenista',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='user.profile'),
        ),
        migrations.AddField(
            model_name='historicalentrada',
            name='completo',
            field=models.BooleanField(default=False),
        ),
    ]
