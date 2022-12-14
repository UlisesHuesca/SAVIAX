# Generated by Django 3.2.5 on 2022-04-18 18:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_profile_image'),
        ('dashboard', '0021_auto_20220415_1113'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='sol_autorizada_por',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Autoriza', to='user.profile'),
        ),
        migrations.AlterField(
            model_name='order',
            name='staff',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Crea', to='user.profile'),
        ),
    ]
