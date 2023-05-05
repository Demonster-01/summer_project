from django.contrib import admin
from .models import Movie,Theater,Upcomming,Booking,Ott
# Register your models here.
# admin.site.unregister(Movie)
admin.site.register(Movie)
admin.site.register(Theater)
admin.site.register(Upcomming)
admin.site.register(Ott)

admin.site.register(Booking)