# Generated by Django 3.2.3 on 2023-05-04 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_sys', '0017_auto_20230504_2119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ott',
            name='trailer_video',
            field=models.FileField(blank=True, null=True, upload_to='ott_movie_trailer/'),
        ),
    ]