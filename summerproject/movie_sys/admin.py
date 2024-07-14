from django.contrib import admin
from .models import Movie, Theater, Upcomming, Booking, Ott, Booking2, Booking3, WatchLater

class MovieModelAdmin(admin.ModelAdmin):
    def has_add_permission(self, request,obj= None):
        return False

    def has_delete_permission(self, request,obj= None):
        return False

    def has_module_permission(self, request,obj= None):
        return False
# Register your models here.
admin.site.register(Movie,MovieModelAdmin)
admin.site.register(Theater)
admin.site.register(Upcomming,MovieModelAdmin)
admin.site.register(Ott)

admin.site.register(Booking)
admin.site.register(Booking2)
admin.site.register(Booking3)
admin.site.register(WatchLater,MovieModelAdmin)
