# Generated by Django 3.2.3 on 2023-08-17 02:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movie_sys', '0033_alter_movie_trailer_video'),
    ]

    operations = [
        migrations.CreateModel(
            name='WatchLater',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie_title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie_sys.ott')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
