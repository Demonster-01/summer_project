import json
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView)
from pyexpat.errors import messages

from .models import Movie, Theater, Upcomming, Booking, Ott
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

from users.models import Profile, User


class MovieListView(ListView):
    model = Theater
    template_name = 'movie_sys/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'theaters'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['upcommings'] = Upcomming.objects.all()
        context['ott_list'] = Ott.objects.all()
        context['profile'] = Profile.objects.all()
        return context


def about(request):
    return render(request, 'movie_sys/about.html')



class MoviecollListView(ListView):
    model = Movie
    template_name = 'movie_sys/movie_coll.html'
    context_object_name = 'movies'

    def get_queryset(self):
        theater_id = self.kwargs['theater_id']
        return Movie.objects.filter(theater_id=theater_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        theater_id = self.kwargs['theater_id']
        theater = get_object_or_404(Theater, pk=theater_id)
        context['theater'] = theater
        context['theaters'] = Theater.objects.all()
        context['upcommings'] = Upcomming.objects.filter(upload_by=theater)

        return context


# def movie_coll(request, theater_name):
#     theater = get_object_or_404(Theater, theater_name=theater_name)
#     movies = Movie.objects.filter(theater=theater_name)
#     theaters = Theater.objects.all()
#     upcommings = Upcomming.objects.filter(upload_by=theater_name)
#
#     context = {
#         'movies': movies,
#         'theaters': theaters,
#         'upcommings': upcommings,
#         'theater': theater,
#     }
#
#     return render(request, 'movie_sys/movie_coll.html', context)


#
# from django.http import Http404
# def movie_coll(request, theater_name):
#     try:
#         theater = Theater.objects.get(theater_name=theater_name)
#
#         if request.user == theater.user:
#             movies = Movie.objects.filter(theater=theater)
#             upcommings = Upcomming.objects.filter(upload_by=theater)
#
#             context = {
#                 'theater': theater,
#                 'movies': movies,
#                 'upcommings': upcommings,
#             }
#
#             return render(request, 'movie_sys/movie_coll.html', context)
#         else:
#             raise Http404("This theater does not belong to the current user.")
#     except Theater.DoesNotExist:
#         raise Http404("Theater matching query does not exist.")





# class MovieDetailView(DetailView):
#     model = Movie
#     template_name = 'movie_sys/movie_detail.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['rows'] = range(1, self.object.theater.no_of_seat_rows + 1)
#         context['cols'] = range(1, self.object.theater.num_of_seats_column + 1)
#         return context








class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movie_sys/movie_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rows'] = range(1, self.object.theater.no_of_seat_rows + 1)
        context['cols'] = range(1, self.object.theater.num_of_seats_column + 1)
        context['bookings'] = Booking.objects.all()
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




@csrf_exempt
def occupiedSeats(request):
    data = json.loads(request.body)
    movie_title = data["movie_title"]
    movie = Movie.objects.get(title=movie_title)
    occupied_seats = movie.booked_seats.values_list('seat_no', flat=True)

    return JsonResponse({
        "occupied_seats": list(occupied_seats),
        "movie_title": movie_title
    })

class MovieCreateView(LoginRequiredMixin, CreateView):
    model = Movie
    fields = ['title', 'poster','releasing_date','genre','cast','directed_by','description','promo_code','offer','ticket_price']
    template_name = 'movie_sys/movie_form.html'
    success_url = '/'
    def form_valid(self, form):
        theater = get_object_or_404(Theater, user=self.request.user)
        form.instance.theater = theater
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
    template_name = 'movie_sys/movie_confirm_delete.html'
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
    fields = ['title', 'poster', 'genre', 'cast', 'description', 'movie_video', 'trailer_video']
    template_name = 'movie_sys/movie_form.html'

    def form_valid(self, form):
        ott = form.save(commit=False)
        ott.upload_by = self.request.user
        ott.save()
        return super().form_valid(form)

# @method_decorator(staff_member_required, name='dispatch')
# class TheaterCreateView(LoginRequiredMixin, CreateView):
#     model = Theater
#     fields = ['theater_name', 'location', 'logo', 'user', 'no_of_seat_rows', 'num_of_seats_column', 'contact']
#     template_name = 'movie_sys/movie_form.html'
#
#     def form_valid(self, form):
#         theater = form.save(commit=False)
#         theater.upload_by = self.request.user
#         theater.save()
#         return super().form_valid(form)



class TheaterCreateView(LoginRequiredMixin, CreateView):
    model = Theater
    fields = ['theater_name', 'location', 'logo', 'user', 'no_of_seat_rows', 'num_of_seats_column', 'contact']
    template_name = 'movie_sys/movie_form.html'
    success_url = '/'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['user'].queryset = User.objects.filter(profile__role__in=['manager', 'admin'])
        return form

    def form_valid(self, form):
        theater = form.save(commit=False)
        theater.upload_by = self.request.user
        theater.save()
        return super().form_valid(form)





@login_required(login_url='login')  # Add this decorator to require authentication
def process_bookings(request, pk):
    if request.method == 'POST':
        selected_seats = request.POST.getlist('seat')
        movie = get_object_or_404(Movie, pk=pk)
        user = request.user if request.user.is_authenticated else None

        if user is None:
            # User is not logged in, redirect to the login page
            messages.warning(request, 'Please login to proceed with the booking.')
            return redirect('login')

        for seat in selected_seats:
            print(seat)
            row = seat[0]
            col = seat[1]
            booking = Booking(movie=movie, seat_row=row, seat_column=col, user=user)
            booking.save()

    return redirect('movie_detail', pk=pk)
