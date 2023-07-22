from django.contrib import admin
from .models import Movie, Theater, Upcomming, Booking, Ott, Booking2, Booking3

# Register your models here.
# admin.site.unregister(Movie)
admin.site.register(Movie)
admin.site.register(Theater)
admin.site.register(Upcomming)
admin.site.register(Ott)

admin.site.register(Booking)
admin.site.register(Booking2)
admin.site.register(Booking3)
