# Generated by Django 4.1.4 on 2022-12-20 14:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0003_userprofile_display_name_userprofile_phone_number_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
