# Generated by Django 3.2.5 on 2022-05-17 21:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0034_auto_20220517_1424'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cond_credito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='compra',
            name='cond_de_pago',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='compras.cond_credito'),
        ),
        migrations.AlterField(
            model_name='historicalcompra',
            name='cond_de_pago',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='compras.cond_credito'),
        ),
    ]
