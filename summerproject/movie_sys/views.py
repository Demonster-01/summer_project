import csv
import json
from datetime import timezone, datetime
import pytz
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView)
from pyexpat.errors import messages
from django.utils import timezone
from .models import Movie, Theater, Upcomming, Booking, Ott, Booking2, Booking3
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from users.models import Profile, User


class MovieListView(ListView):
    model = Theater
    template_name = 'movie_sys/home.html'
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

    def check_screening_time(self):
        current_time = timezone.localtime()
        screening_time = timezone.localtime(self.object.screening_datetime)

        screening_time = screening_time.replace(second=0, microsecond=0)

        if current_time >= screening_time:
            # Perform actions when screening time has passed
            print("The screening time has passed.")
            self.export_to_csv('old_booking_data.csv')
            Booking.objects.all().delete()
        else:
            # Perform actions when screening time has not passed
            print("The screening time has not passed yet.")
    def export_to_csv(self, filename):
        bookings = Booking.objects.all()
        field_names = ['id', 'movie', 'seat_row', 'seat_column', 'user']
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            writer.writeheader()
            for booking in bookings:
                writer.writerow({
                    'id': booking.id,
                    'movie': booking.movie.title,
                    'seat_row': booking.seat_row,
                    'seat_column': booking.seat_column,
                    'user': booking.user,
                })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rows'] = range(1, self.object.theater.no_of_seat_rows + 1)
        context['cols'] = range(1, self.object.theater.num_of_seats_column + 1)
        context['bookings'] = Booking.objects.all()
        context['current_time'] = timezone.localtime().strftime('%H:%M:%S')


        self.check_screening_time()  # Call the method to check screening time

        return context



class MovieDetailView2(DetailView):
    model = Movie
    template_name = 'movie_sys/movie_detail_2.html'

    def check_screening_time(self):
        current_time = timezone.localtime()
        screening_time = timezone.localtime(self.object.screening_datetime2)

        screening_time = screening_time.replace(second=0, microsecond=0)

        if current_time >= screening_time:
            # Perform actions when screening time has passed
            print("The screening time has passed.")
            self.export_to_csv('old_booking_data.csv')
            Booking2.objects.all().delete()
        else:
            # Perform actions when screening time has not passed
            print("The screening time has not passed yet.")
    def export_to_csv(self, filename):
        bookings2 = Booking2.objects.all()
        field_names = ['id', 'movie', 'seat_row', 'seat_column', 'user']
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            writer.writeheader()
            for booking in bookings2:
                writer.writerow({
                    'id': booking.id,
                    'movie': booking.movie.title,
                    'seat_row': booking.seat_row,
                    'seat_column': booking.seat_column,
                    'user': booking.user,
                })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rows'] = range(1, self.object.theater.no_of_seat_rows + 1)
        context['cols'] = range(1, self.object.theater.num_of_seats_column + 1)
        context['bookings2'] = Booking2.objects.all()
        context['current_time'] = timezone.localtime().strftime('%H:%M:%S')


        self.check_screening_time()  # Call the method to check screening time

        return context

class MovieDetailView3(DetailView):
    model = Movie
    template_name = 'movie_sys/movie_detail_3.html'

    def check_screening_time(self):
        current_time = timezone.localtime()
        screening_time = timezone.localtime(self.object.screening_datetime3)

        screening_time = screening_time.replace(second=0, microsecond=0)

        if current_time >= screening_time:
            # Perform actions when screening time has passed
            print("The screening time has passed.")
            self.export_to_csv('old_booking_data.csv')
            Booking3.objects.all().delete()
        else:
            # Perform actions when screening time has not passed
            print("The screening time has not passed yet.")
    def export_to_csv(self, filename):
        bookings = Booking.objects.all()
        field_names = ['id', 'movie', 'seat_row', 'seat_column', 'user']
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            writer.writeheader()
            for booking in bookings:
                writer.writerow({
                    'id': booking.id,
                    'movie': booking.movie.title,
                    'seat_row': booking.seat_row,
                    'seat_column': booking.seat_column,
                    'user': booking.user,
                })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rows'] = range(1, self.object.theater.no_of_seat_rows + 1)
        context['cols'] = range(1, self.object.theater.num_of_seats_column + 1)
        context['bookings3'] = Booking3.objects.all()
        context['current_time'] = timezone.localtime().strftime('%H:%M:%S')


        self.check_screening_time()  # Call the method to check screening time

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

class BookingDetailView2(DetailView):
    model = Booking2
    template_name = 'booking_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        booking = self.get_object()
        ticket_price = booking.ticket_price
        context['ticket_price'] = ticket_price
        print(booking)
        return context

class BookingDetailView3(DetailView):
    model = Booking3
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


class OttListView( ListView):
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



from django.contrib import messages


@login_required(login_url='login')  # Add this decorator to require authentication
def process_bookings(request, pk):
    if request.method == 'POST':
        selected_seats = request.POST.getlist('seat')
        movie = get_object_or_404(Movie, pk=pk)
        user = request.user

        if user is None:
            # User is not logged in, redirect to the login page
            messages.warning(request, 'Please login to proceed with the booking.')
            return redirect('login')

        current_datetime = datetime.now(pytz.utc)  # Make current_datetime offset-aware with UTC timezone
        screening_datetime = movie.screening_datetime.astimezone(pytz.utc)  # Make screening_datetime offset-aware with UTC timezone

        if current_datetime >= screening_datetime:
            messages.warning(request, 'The screening time has passed. Booking is not available.')
            return redirect('movie_detail', pk=pk)

        for seat in selected_seats:
            row = seat[0]
            col = seat[1]
            booking = Booking(movie=movie, seat_row=row, seat_column=col, user=user)
            booking.save()
            # Save the booking data to a CSV file
            save_booking_data(movie, row, col, user)

        messages.success(request, 'Booking successful! Enjoy the movie.')

    return redirect('movie_detail', pk=pk)


def is_screening_time_passed(current_datetime, screening_datetime):
    current_date = current_datetime.date()
    screening_date = screening_datetime.date()
    current_time = current_datetime.time()
    screening_time = screening_datetime.time()

    if current_date > screening_date:
        return True
    elif current_date == screening_date and current_time >= screening_time:
        return True
    else:
        return False


def save_booking_data(movie, row, col, user):
    # Define the file path where the booking data will be saved
    file_path = 'booking_data.csv'

    # Create a new row with the booking data
    booking_data = [str(movie.pk), movie.title, row, col, str(user.pk), user.username]

    # Write the booking data to the CSV file
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(booking_data)



@login_required(login_url='login')  # Add this decorator to require authentication
def process_bookings2(request, pk):
    if request.method == 'POST':
        selected_seats = request.POST.getlist('seat')
        movie = get_object_or_404(Movie, pk=pk)
        user = request.user

        if user is None:
            # User is not logged in, redirect to the login page
            messages.warning(request, 'Please login to proceed with the booking.')
            return redirect('login')

        current_datetime = datetime.now(pytz.utc)  # Make current_datetime offset-aware with UTC timezone
        screening_datetime = movie.screening_datetime.astimezone(pytz.utc)  # Make screening_datetime offset-aware with UTC timezone

        if current_datetime >= screening_datetime:
            messages.warning(request, 'The screening time has passed. Booking is not available.')
            return redirect('movie_detail', pk=pk)

        for seat in selected_seats:
            row = seat[0]
            col = seat[1]
            booking2 = Booking2(movie=movie, seat_row=row, seat_column=col, user=user)
            booking2.save()
            # Save the booking data to a CSV file
            save_booking_data(movie, row, col, user)

        messages.success(request, 'Booking successful! Enjoy the movie.')

    return redirect('movie_detail_2', pk=pk)



@login_required(login_url='login')  # Add this decorator to require authentication
def process_bookings3(request, pk):
    if request.method == 'POST':
        selected_seats = request.POST.getlist('seat')
        movie = get_object_or_404(Movie, pk=pk)
        user = request.user

        if user is None:
            # User is not logged in, redirect to the login page
            messages.warning(request, 'Please login to proceed with the booking.')
            return redirect('login')

        current_datetime = datetime.now(pytz.utc)  # Make current_datetime offset-aware with UTC timezone
        screening_datetime = movie.screening_datetime.astimezone(pytz.utc)  # Make screening_datetime offset-aware with UTC timezone

        if current_datetime >= screening_datetime:
            messages.warning(request, 'The screening time has passed. Booking is not available.')
            return redirect('movie_detail', pk=pk)

        for seat in selected_seats:
            row = seat[0]
            col = seat[1]
            booking3 = Booking3(movie=movie, seat_row=row, seat_column=col, user=user)
            booking3.save()
            # Save the booking data to a CSV file
            save_booking_data(movie, row, col, user)

        messages.success(request, 'Booking successful! Enjoy the movie.')

    return redirect('movie_detail_3', pk=pk)




#
# from datetime import datetime
# from .models import Screening, Dataset
# from .utils import is_screening_time_passed
#
# def reset_or_create_dataset(request):
#     screenings = Screening.objects.all()
#
#     for screening in screenings:
#         if is_screening_time_passed(screening.screening_time):
#             # Reset or create new dataset for this screening
#             # Perform the necessary actions based on your requirements
#             # Example:
#             screening.dataset_set.all().delete()  # Delete existing related datasets
#
#             # Create new dataset instances
#             new_dataset1 = Dataset(screening=screening, ...)
#             new_dataset1.save()
#             new_dataset2 = Dataset(screening=screening, ...)
#             new_dataset2.save()
#
#     # Perform any other necessary actions or return a response
#     return HttpResponse("Dataset reset/creation completed.")
#


