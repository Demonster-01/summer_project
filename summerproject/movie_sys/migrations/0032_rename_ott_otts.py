# Generated by Django 3.2.3 on 2023-05-05 12:00

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movie_sys', '0031_alter_ott_upload_by'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Ott',
            new_name='Otts',
        ),
    ]