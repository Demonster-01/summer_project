# Generated by Django 3.2.3 on 2023-08-16 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_sys', '0024_alter_movie_screening_datetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking2',
            name='is_booked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='booking2',
            name='version',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='booking3',
            name='is_booked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='booking3',
            name='version',
            field=models.IntegerField(default=0),
        ),
    ]