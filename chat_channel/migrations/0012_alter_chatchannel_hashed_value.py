# Generated by Django 4.1.5 on 2023-02-18 02:07

import Hasher.Hasher
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chat_channel", "0011_alter_chatchannel_hashed_value"),
    ]

    operations = [
        migrations.AlterField(
            model_name="chatchannel",
            name="hashed_value",
            field=models.CharField(
                db_index=True,
                default=Hasher.Hasher.Hasher.hash,
                max_length=10,
                unique=True,
            ),
        ),
    ]
