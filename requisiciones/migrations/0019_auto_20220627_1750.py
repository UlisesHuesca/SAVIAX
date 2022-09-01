# Generated by Django 3.2.5 on 2022-06-27 22:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('requisiciones', '0018_alter_requis_colocada'),
    ]

    operations = [
        migrations.AddField(
            model_name='requis',
            name='approved_at_time',
            field=models.TimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='requis',
            name='approved_at',
            field=models.DateField(),
        ),
    ]
