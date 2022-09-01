# Generated by Django 3.2.5 on 2022-08-22 23:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0064_auto_20220822_1154'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tipo_Orden',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=15, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='historicalorder',
            name='tipo',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='dashboard.tipo_orden'),
        ),
        migrations.AddField(
            model_name='order',
            name='tipo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.tipo_orden'),
        ),
    ]
