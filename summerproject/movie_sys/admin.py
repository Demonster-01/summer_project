from django.contrib import admin
from .models import Movie,Theater,Upcomming,Booking,Seat
# Register your models here.
# admin.site.unregister(Movie)
admin.site.register(Movie)
admin.site.register(Theater)
admin.site.register(Upcomming)

admin.site.register(Seat)
admin.site.register(Booking)