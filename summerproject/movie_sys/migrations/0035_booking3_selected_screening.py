# Generated by Django 3.2.3 on 2023-08-17 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_sys', '0034_watchlater'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking3',
            name='selected_screening',
            field=models.DateTimeField(null=True),
        ),
    ]