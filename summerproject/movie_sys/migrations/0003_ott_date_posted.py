# Generated by Django 3.2.3 on 2023-05-16 06:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('movie_sys', '0002_theater_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='ott',
            name='date_posted',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
