# Generated by Django 3.2.5 on 2022-08-20 01:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_distrito_abreviado'),
        ('requisiciones', '0022_auto_20220721_1856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articulosrequisitados',
            name='almacenista',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Almacen2', to='user.profile'),
        ),
    ]
