# Generated by Django 4.1.3 on 2022-12-16 04:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workspace', '0001_initial'),
        ('chat_channel', '0003_alter_chatchannel_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatchannel',
            name='workspace',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='chat_channel', to='workspace.workspace'),
            preserve_default=False,
        ),
    ]
