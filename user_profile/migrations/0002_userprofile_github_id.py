# Generated by Django 4.1 on 2022-08-08 14:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='github_id',
            field=models.CharField(default='0', max_length=20),
        ),
    ]
