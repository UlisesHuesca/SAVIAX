# Generated by Django 3.2.5 on 2022-03-24 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='avatar.jpg', upload_to='profile_images'),
        ),
    ]
