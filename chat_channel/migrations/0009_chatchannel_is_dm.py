# Generated by Django 4.1.4 on 2023-01-08 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat_channel', '0008_chatchannel_hashed_value_alter_chatchannel_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatchannel',
            name='is_dm',
            field=models.BooleanField(default=False),
        ),
    ]
