# Generated by Django 3.2.3 on 2023-05-27 10:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_sys', '0009_movie_screening_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='screening_time',
            field=models.TimeField(default=datetime.time(1, 20)),
        ),
    ]
