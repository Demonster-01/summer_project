# Generated by Django 3.2.3 on 2023-05-16 08:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movie_sys', '0003_ott_date_posted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='theater',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movies', to='movie_sys.theater'),
        ),
    ]
