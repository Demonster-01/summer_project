# Generated by Django 3.2.3 on 2023-04-27 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_sys', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='seat',
            name='reserved',
            field=models.BooleanField(default=False, verbose_name='Reserved'),
        ),
    ]
