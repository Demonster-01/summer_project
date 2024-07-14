# Generated by Django 3.2.3 on 2023-08-23 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_sys', '0039_alter_movie_releasing_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='offer',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='releasing_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='trailer_video',
            field=models.FileField(blank=True, default='404Error.png', null=True, upload_to='movie_trailer_video/'),
        ),
    ]
