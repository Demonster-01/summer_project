# Generated by Django 3.2.3 on 2023-05-27 10:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_sys', '0008_auto_20230527_0838'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='screening_time',
            field=models.TimeField(default=datetime.time(12, 0)),
        ),
    ]
