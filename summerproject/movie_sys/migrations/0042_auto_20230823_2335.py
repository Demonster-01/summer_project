# Generated by Django 3.2.3 on 2023-08-23 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_sys', '0041_auto_20230823_2332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='screening_datetime2',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='screening_datetime3',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]