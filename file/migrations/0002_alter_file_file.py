# Generated by Django 4.1.4 on 2022-12-24 13:29

from django.db import migrations, models
import file.models


class Migration(migrations.Migration):

    dependencies = [
        ('file', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(upload_to=file.models.upload_file),
        ),
    ]
