from django.urls import path
from . import views
from .views import (
    MovieListView, MovieDetailView, BookingDetailView,
    MovieCreateView, MovieUpdateView,
    MovieDeleteView, OttCreateView, OttDetailView, OttListView, TheaterCreateView, MoviecollListView, process_bookings,
    MovieDetailView2, MovieDetailView3, process_bookings2, process_bookings3, TrailerView)


urlpatterns = [
    # path('', views.home, name='movie_sys-home'),
    path('', MovieListView.as_view(), name='movie_sys-home'),
    path('about/', views.about, name='movie_sys-about'),
    # path('occupied/',occupiedSeats,name="occupied_seat"),

    path('movie_coll/<int:theater_id>/movies/', MoviecollListView.as_view(), name='movie_sys-movie_coll'),
    path('movie_detail/<int:pk>/',MovieDetailView.as_view(), name='movie_detail'),
    path('movie_detail_2/<int:pk>/',MovieDetailView2.as_view(), name='movie_detail_2'),
    path('movie_detail_3/<int:pk>/',MovieDetailView3.as_view(), name='movie_detail_3'),
    path('trailer/<int:pk>/',TrailerView.as_view(), name='Trailerpage'),
    path('movie/new/', MovieCreateView.as_view(), name='movie-create'),
    path('movie/<int:pk>/update/', MovieUpdateView.as_view(), name='movie-update'),
    path('movie/<int:pk>/delete/', MovieDeleteView.as_view(), name='movie-delete'),

    path("ott/collection/",OttListView.as_view(),name='movie_sys-ott_collection'),
    path('ott/<int:pk>/', OttDetailView.as_view(), name='ott_detail'),
    path('ott/new/', OttCreateView.as_view(), name='ott-create'),
    path('my-booking/', views.my_booking, name='my_booking'),
    path('ott/<int:pk>/add_watch_later/', views.add_to_watch_later, name='add_watch_later'),

    path('theater/new/', TheaterCreateView.as_view(), name='theater-create'),
    path('movie/new/<int:user_id>/', MovieCreateView.as_view(), name='movie-create'),

    # path('occupied/', views.occupiedSeats, name='occupied_seats'),
    path('movie_detail/<int:pk>/process_bookings/', process_bookings, name='process_bookings'),
    path('movie_detail_2/<int:pk>/process_bookings2/', process_bookings2, name='process_bookings2'),
    path('movie_detail_3/<int:pk>/process_bookings3/', process_bookings3, name='process_bookings3'),
    path('search/', views.search_theater, name='search_theater'),
    path('cancel_booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('remove_watch_later/<int:pk>/', views.remove_from_watch_later, name='remove_watch_later'),
]

