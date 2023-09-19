from datetime import time, datetime

from PIL.Image import Image
from django.core.validators import MinValueValidator
from django.db import models
from django_resized import ResizedImageField
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
import datetime

# Create your models here.

class Theater(models.Model):
    theater_name = models.CharField(max_length=50, null=True)
    location = models.CharField(max_length=50, null=True)
    logo = ResizedImageField(size=[400, 400], quality=100, upload_to='theater_logos', default='default.jpg')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    no_of_seat_rows = models.IntegerField(default=10)
    num_of_seats_column = models.IntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)
    contact = models.IntegerField(default=9807654321, blank=False,null=False)

    class Meta:
        unique_together = ('theater_name', 'location')

    def __str__(self):
        return self.theater_name


class Movie(models.Model):
    # id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, null=False)
    poster = models.ImageField(default="default.jpg", upload_to='movie_poster')
    trailer_video = models.FileField(default="404Error.png",upload_to='movie_trailer_video/',null=True,blank=True)
    releasing_date = models.DateField( null=True,blank=True)
    screening_datetime = models.DateTimeField(
        default=timezone.localtime(timezone.now()).replace(hour=13, minute=0, second=0, microsecond=0))
    screening_datetime2 = models.DateTimeField(null=True,blank=True)
    screening_datetime3 = models.DateTimeField(null=True,blank=True)
    genre = models.CharField(max_length=50, null=True)
    cast = models.CharField(max_length=200, null=True)
    directed_by = models.CharField(max_length=50, null=True)
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE, null=False, related_name='movies')
    description = models.CharField(max_length=500, null=True)
    # booked_seats = models.ManyToManyField('Booking', blank=True)
    promo_code = models.CharField(max_length=50, blank=True, null=True)
    offer = models.DecimalField(max_digits=5, decimal_places=2, null=True,blank=True)
    ticket_price = models.IntegerField(validators=[MinValueValidator(1)], default=1)
    reserved_seats = models.JSONField(blank=True, null=True)
    # ... other fields and methods ...

    def reserve_seat(self, row, col):
        if self.reserved_seats is None:
            self.reserved_seats = []
        self.reserved_seats.append((row, col))
        self.save()
    def get_reserved_seats(self):
        return self.reserved_seats if self.reserved_seats else []
    def get_formatted_screening_time(self):
        return self.screening_time.strftime("%H:%M")

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



class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    purchase_time = models.DateTimeField(auto_now_add=True, null=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, default=1)
    seat_row = models.CharField(max_length=10, default=0)
    seat_column = models.CharField(max_length=1, default=0)
    is_booked = models.BooleanField(default=False)
    version = models.IntegerField(default=0)
    selected_screening = models.DateTimeField(null=True)
    is_canceled = models.BooleanField(default=False)

    class Meta:
        unique_together = ('movie', 'seat_row', 'seat_column')

    def __str__(self):
        return f"Booking {self.movie.title} - Seat {self.seat_row}-{self.seat_column}"

class Booking2(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    purchase_time = models.DateTimeField(auto_now_add=True, null=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, default=1)
    seat_row = models.CharField(max_length=10, default=0)
    seat_column = models.CharField(max_length=1, default=0)
    is_booked = models.BooleanField(default=False)
    version = models.IntegerField(default=0)
    selected_screening = models.DateTimeField(null=True)
    is_canceled = models.BooleanField(default=False)

    class Meta:
        unique_together = ('movie', 'seat_row', 'seat_column')

    def __str__(self):
        return f"Booking for 2nd {self.movie.title} - Seat {self.seat_row}-{self.seat_column}"


class Booking3(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    purchase_time = models.DateTimeField(auto_now_add=True, null=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, default=1)
    seat_row = models.CharField(max_length=10, default=0)
    seat_column = models.CharField(max_length=1, default=0)
    is_booked = models.BooleanField(default=False)
    version = models.IntegerField(default=0)
    selected_screening = models.DateTimeField(null=True)
    is_canceled = models.BooleanField(default=False)

    class Meta:
        unique_together = ('movie', 'seat_row', 'seat_column')

    def __str__(self):
        return f"Booking for 3rd {self.movie.title} - Seat {self.seat_row}-{self.seat_column}"








class Ott(models.Model):
    title = models.CharField(max_length=50, null=False)
    poster = models.ImageField(default="default.jpg", upload_to='Ott_poster')
    genre = models.CharField(max_length=50, null=True, blank=True)
    cast = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=500, blank=True)
    movie_video = models.FileField(upload_to='ott_movie_videos/', null=False)
    trailer_video = models.FileField(upload_to='ott_movie_trailer/', null=True, blank=True)
    upload_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('ott_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class WatchLater(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_title = models.ForeignKey(Ott,on_delete=models.CASCADE)

def is_screening_time_passed(screening_time):
    current_time = datetime.now().time()
    return current_time > screening_time
