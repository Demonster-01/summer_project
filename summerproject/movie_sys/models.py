from PIL.Image import Image
from django.core.validators import MinValueValidator
from django.db import models
from django_resized import ResizedImageField
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

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

    def __str__(self):
        return self.title

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
            self.upload_by = self._meta.model.upload_by.field.related_model.objects.get(pk=1)  # replace 1 with the id of the desired user
        super().save(*args, **kwargs)


class Ott(models.Model):
    title = models.CharField(max_length=50, null=False)
    poster = models.ImageField(default="default.jpg", upload_to='Ott_poster')
    genre = models.CharField(max_length=50, null=True)
    cast = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=500)

# class Booking(models.Model):
#     pass

# class Booking(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
#     date = models.DateField()
#     time = models.TimeField()
#     seats = models.ManyToManyField(Seat)

class Booking(models.Model):
    promo_code = models.CharField(max_length=50, blank=True, null=True)
    offer = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    no_of_rows = models.IntegerField(default=1) #no of seat to be
    ticket_price = models.IntegerField(validators=[MinValueValidator(1)], default=1)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='booking', default=" ")
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f'Booking - {self.pk}'


class Seat(models.Model):
    theater = models.ForeignKey('Theater', on_delete=models.CASCADE, related_name='seats')
    row = models.PositiveIntegerField(_('Row Number'))
    column = models.PositiveIntegerField(_('Column Number'))
    is_booked = models.BooleanField(_('Is Booked'), default=False)

    def __str__(self):
        return f'{self.theater} - Row {self.row}, Column {self.column}'
