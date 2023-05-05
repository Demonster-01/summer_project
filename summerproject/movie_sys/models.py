from PIL.Image import Image
from django.core.validators import MinValueValidator
from django.db import models
from django_resized import ResizedImageField
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


# Create your models here.

class Theater(models.Model):
    theater_name = models.CharField(max_length=50, null=True)
    location = models.CharField(max_length=50, null=True)
    logo = ResizedImageField(size=[400, 400], quality=100, upload_to='theater_logos', default='default.jpg')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    no_of_seat_rows = models.IntegerField(default=10)
    num_of_seats_column = models.IntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('theater_name', 'location')

    def __str__(self):
        return self.theater_name


class Movie(models.Model):
    # id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, null=False)
    poster = models.ImageField(default="default.jpg", upload_to='movie_poster')
    releasing_date = models.DateField()
    genre = models.CharField(max_length=50, null=True)
    cast = models.CharField(max_length=200, null=True)
    directed_by = models.CharField(max_length=50, null=True)
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE, null=True, related_name='movies')
    description = models.CharField(max_length=500, null=True)
    booked_seats = models.ManyToManyField('Booking', blank=True)
    promo_code = models.CharField(max_length=50, blank=True, null=True)
    offer = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    ticket_price = models.IntegerField(validators=[MinValueValidator(1)], default=1)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('movie_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if not self.id:
            try:
                last_movie = Movie.objects.latest('id')
                self.id = last_movie.id + 1
            except Movie.DoesNotExist:
                self.id = 1
        super().save(*args, **kwargs)


class Upcomming(models.Model):
    title = models.CharField(max_length=50, null=False)
    poster = models.ImageField(default="default.jpg", upload_to='upcomming_poster')
    genre = models.CharField(max_length=50, null=True)
    cast = models.CharField(max_length=200, null=True)
    directed_by = models.CharField(max_length=50, null=True)
    upload_by = models.ForeignKey(Theater, on_delete=models.CASCADE, null=True, related_name='upcoming_movies')

    def save(self, *args, **kwargs):
        if not self.pk:  # object is being created
            self.upload_by = self._meta.model.upload_by.field.related_model.objects.get(
                pk=1)  # replace 1 with the id of the desired user
        super().save(*args, **kwargs)


class Ott(models.Model):
    title = models.CharField(max_length=50, null=False)
    poster = models.ImageField(default="default.jpg", upload_to='Ott_poster')
    genre = models.CharField(max_length=50, null=True, blank=True)
    cast = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=500, blank=True)
    movie_video = models.FileField(upload_to='ott_movie_videos/', null=False)
    trailer_video = models.FileField(upload_to='ott_movie_trailer/', null=True, blank=True)
    upload_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('ott_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title




    # def is_admin_user(self):
    #     return self.user == User.objects.get(position='admin')
    #
    # class Meta:
    #     permissions = [('can_view_ott', 'Can view Ott')]

    # def save(self, *args, **kwargs):
    #     if self.is_admin_user():
    #         super().save(*args, **kwargs)
    #     else:
    #         raise Exception("You don't have permission to save this model.")


class Booking(models.Model):
    seat_no = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    purchase_time = models.DateTimeField(auto_now_add=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.user:
            self.name = self.user.get_full_name()
            self.email = self.user.email
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.email} purchased oon  {self.purchase_time}"
