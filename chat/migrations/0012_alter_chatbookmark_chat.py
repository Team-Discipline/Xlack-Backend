# Generated by Django 4.1.4 on 2023-01-06 10:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0011_chatbookmark'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatbookmark',
            name='chat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmarks', to='chat.chat'),
        ),
    ]
