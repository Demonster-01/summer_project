# Generated by Django 3.2.3 on 2023-05-27 02:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie_sys', '0007_booking_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='email',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='name',
        ),
    ]