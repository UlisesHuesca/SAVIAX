# Generated by Django 3.2.5 on 2023-07-06 02:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0017_auto_20230705_2048'),
    ]

    operations = [
        migrations.AddField(
            model_name='compra',
            name='comparativo_model',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='compras.comparativo'),
        ),
        migrations.AddField(
            model_name='historicalcompra',
            name='comparativo_model',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='compras.comparativo'),
        ),
    ]