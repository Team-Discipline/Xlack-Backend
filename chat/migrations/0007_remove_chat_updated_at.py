# Generated by Django 4.1 on 2022-08-07 16:52

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('chat', '0006_alter_chat_channel_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='updated_at',
        ),
    ]
