# Generated by Django 3.2.3 on 2023-05-04 09:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie_sys', '0013_rename_theater_movie_theater_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='theater_name',
            new_name='theater',
        ),
    ]
