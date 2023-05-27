from movie_sys.models import Theater
from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    theater_name = models.ForeignKey(Theater, on_delete=models.CASCADE, null=True, blank=True)
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('client', 'Client'),
        ('manager', 'Manager'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')
    contact = models.IntegerField(unique=True, blank=False,null=False)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

from django.contrib.auth.models import User
User._meta.get_field('email')._unique = True
