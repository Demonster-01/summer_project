# Generated by Django 3.2.3 on 2023-05-06 05:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movie_sys', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='theater_name',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='movie_sys.theater'),
        ),
    ]
