# Generated by Django 3.2.3 on 2023-08-23 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_sys', '0038_alter_movie_screening_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='releasing_date',
            field=models.DateField(null=True),
        ),
    ]
