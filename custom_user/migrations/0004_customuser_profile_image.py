# Generated by Django 4.1.4 on 2022-12-23 01:29

import custom_user.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_user', '0003_alter_customuser_display_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to=custom_user.models.upload_img),
        ),
    ]
