from django.urls import path
from . import views
from .views import (
    MovieListView, MovieDetailView, BookingDetailView,
    occupiedSeats, MovieCreateView, MovieUpdateView,
    MovieDeleteView, OttCreateView, OttDetailView, OttListView)


urlpatterns = [
    # path('', views.home, name='movie_sys-home'),
    path('', MovieListView.as_view(), name='movie_sys-home'),
    path('about/', views.about, name='movie_sys-about'),
    path('movie_coll/<str:theater_name>/movies/', views.movie_coll, name='movie_sys-movie_coll'),
    path('movie_detail/<int:pk>/',MovieDetailView.as_view(), name='movie_detail'),
    # path('seat_booking/', seat_booking, name='seat_booking'),
    # path('movie_detail/<int:pk>/', BookingDetailView.as_view(), name='seat_detail'),
    path('occupied/',occupiedSeats,name="occupied_seat"),
    path('movie/new/', MovieCreateView.as_view(), name='movie-create'),
    path('movie/<int:pk>/update/', MovieUpdateView.as_view(), name='movie-update'),
    path('movie/<int:pk>/delete/', MovieDeleteView.as_view(), name='movie-delete'),
    path("ott/collection/",OttListView.as_view(),name='movie_sys-ott_collection'),
    path('ott/<int:pk>/',OttDetailView.as_view(), name='ott_detail'),
    path('ott/new/', OttCreateView.as_view(), name='movie-create'),
]


