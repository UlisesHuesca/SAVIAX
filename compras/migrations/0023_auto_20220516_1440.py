# Generated by Django 3.2.5 on 2022-05-16 19:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_tipo_perfil_crear_sol'),
        ('compras', '0022_auto_20220513_1838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compra',
            name='oc_autorizada_por',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Aprobacion', to='user.profile'),
        ),
        migrations.AlterField(
            model_name='compra',
            name='oc_autorizada_por2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Aprobacion2', to='user.profile'),
        ),
    ]
