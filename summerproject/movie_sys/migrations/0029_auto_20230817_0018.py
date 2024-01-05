# Generated by Django 3.2.3 on 2023-08-16 18:33

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('movie_sys', '0028_alter_booking3_seat_column'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='trailer_video',
            field=models.FileField(default='404Error.png', upload_to='movie_trailer/'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='screening_datetime',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 17, 7, 15, tzinfo=utc)),
        ),
    ]