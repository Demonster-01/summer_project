import json
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView)
from .models import Movie, Theater, Upcomming, Booking, Ott
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages


class MovieListView(ListView):
    model = Theater
    template_name = 'movie_sys/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'theaters'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['upcommings'] = Upcomming.objects.all()
        context['ott_list'] = Ott.objects.all()
        return context


def about(request):
    return render(request, 'movie_sys/about.html')


def movie_coll(request, theater_name):
    movies = Movie.objects.filter(theater=theater_name)
    theaters = Theater.objects.all()
    upcommings = Upcomming.objects.filter(upload_by=theater_name)
    context = {
        'movies': movies,
        'theaters': theaters,
        'upcommings': upcommings,
    }

    return render(request, 'movie_sys/movie_coll.html', context)


class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movie_sys/movie_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rows'] = range(1, self.object.theater.no_of_seat_rows + 1)
        context['cols'] = range(1, self.object.theater.num_of_seats_column + 1)
        return context


class BookingDetailView(DetailView):
    model = Booking
    template_name = 'booking_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        booking = self.get_object()
        ticket_price = booking.ticket_price
        context['ticket_price'] = ticket_price
        print(booking)
        return context

def occupiedSeats(request):
    data = json.loads(request.body)
    movie = Movie.object.get(title=data["movie_title"])
    occupied = movie.booked_seats.all()
    occupied_seats = list(map(lambda seat: seat.seat_no - 1, occupied))

    return JsonResponse({
        "occupied_seats":occupied_seats,
        "movies":str(Movie)
    })

class MovieCreateView(LoginRequiredMixin, CreateView):
    model = Movie
    fields = ['title', 'poster','releasing_date','genre','cast','directed_by','description','promo_code','offer','ticket_price']
    template_name = 'movie_sys/movie_form.html'
    def form_valid(self, form):
        form.instance.theater_name = get_object_or_404(Theater, user=self.request.user)
        return super().form_valid(form)


class MovieUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Movie
    fields = ['title', 'poster','releasing_date','genre','cast','directed_by','description','promo_code','offer','ticket_price']
    template_name = 'movie_sys/movie_form.html'

    def form_valid(self, form):
        form.instance.theater_name = get_object_or_404(Theater, user=self.request.user)
        return super().form_valid(form)

    def test_func(self):
        movie = self.get_object()
        if self.request.user == movie.theater.user:
            return True
        return False



class MovieDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Movie
    success_url = '/'

    def test_func(self):
        movie = self.get_object()
        if self.request.user == movie.theater.user:
            return True
        return False


class OttListView(ListView):
    model = Ott
    template_name = 'movie_sys/ott_coll.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ott_list'] = Ott.objects.all()
        return context


class OttDetailView(DetailView):
    model = Ott
    template_name = 'movie_sys/ott_detail.html'  # replace with your actual template name
    context_object_name = 'ott'


class OttCreateView(LoginRequiredMixin, CreateView):
    model = Ott
    fields = ['title','poster', 'genre', 'cast', 'description', 'movie_video', 'trailer_video']
    success_url = '/'
    template_name = 'movie_sys/movie_form.html'

    def form_valid(self, form):
        form.instance.upload_by = self.request.user
        return super().form_valid(form)
