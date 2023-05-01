from django.urls import path
from . import views
from .views import MovieListView, MovieDetailView




urlpatterns = [
    # path('', views.home, name='movie_sys-home'),
    path('', MovieListView.as_view(), name='movie_sys-home'),
    path('about/', views.about, name='movie_sys-about'),
    path('movie_coll/<str:theater_name>/movies/', views.movie_coll, name='movie_sys-movie_coll'),
    path('movie_detail/<int:pk>/', views.MovieDetailView.as_view(), name='movie_detail'),
]
