# Generated by Django 3.2.3 on 2023-08-17 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_sys', '0037_auto_20230817_1606'),
        ('users', '0012_alter_profile_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='watch_later',
            field=models.ManyToManyField(to='movie_sys.Ott'),
        ),
    ]
