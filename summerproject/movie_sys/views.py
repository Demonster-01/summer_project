import csv
from datetime import timezone, datetime, timedelta
from django.db import transaction, IntegrityError

import pytz
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView)
from pyexpat.errors import messages
from django.utils import timezone
from .models import Movie, Theater, Upcomming, Booking, Ott, Booking2, Booking3, WatchLater
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.utils import IntegrityError
from django.contrib import messages
from users.models import Profile, User


# def movie_deta(request):
#     return render(request,'movie_sys/movie_deta.html')


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


        self.check_screening_time()

        return context



class MovieDetailView2(DetailView):
    model = Movie
    template_name = 'movie_sys/movie_detail_2.html'

    def check_screening_time(self):
        current_time = timezone.localtime()
        screening_time = timezone.localtime(self.object.screening_datetime2)

        screening_time = screening_time.replace(second=0, microsecond=0)

        if current_time >= screening_time:
            print("The screening time has passed.")
            self.export_to_csv('old_booking_data.csv')
            Booking2.objects.all().delete()
        else:
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


        self.check_screening_time() 

        return context

class MovieDetailView3(DetailView):
    model = Movie
    template_name = 'movie_sys/movie_detail_3.html'

    def check_screening_time(self):
        current_time = timezone.localtime()
        screening_time = timezone.localtime(self.object.screening_datetime3)

        screening_time = screening_time.replace(second=0, microsecond=0)

        if current_time >= screening_time:
            print("The screening time has passed.")
            self.export_to_csv('old_booking_data.csv')
            Booking3.objects.all().delete()
        else:
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


        self.check_screening_time() 

        return context

class TrailerView(DetailView):
    model = Movie
    template_name = 'movie_sys/trailer_play.html' 
    context_object_name = 'trailer'


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


class MovieCreateView(LoginRequiredMixin, CreateView):
    model = Movie
    fields = ['title','trailer_video', 'poster','screening_datetime','screening_datetime2','screening_datetime3','genre','cast','directed_by','description','promo_code','offer','ticket_price']
    template_name = 'movie_sys/movie_form.html'
    success_url = '/'
    def form_valid(self, form):
        theater = get_object_or_404(Theater, user=self.request.user)
        form.instance.theater = theater
        return super().form_valid(form)


class MovieUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Movie
    fields = ['title','trailer_video', 'poster','releasing_date','genre','cast','directed_by','description','promo_code','offer','ticket_price']
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


class OttDetailView(LoginRequiredMixin,DetailView):
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





@login_required(login_url='login')
def process_bookings(request, pk):
    if request.method == 'POST':
        selected_seats = request.POST.getlist('seat')
        movie = get_object_or_404(Movie, pk=pk)
        user = request.user
        selected_screening = movie.screening_datetime  # Adjust as needed

        if user is None:
            messages.warning(request, 'Please log in to proceed with the booking.')
            return redirect('login')

        max_allowed_bookings_total = 10
        existing_bookings_total = Booking.objects.filter(user=user).count()

        if existing_bookings_total >= max_allowed_bookings_total:
            messages.warning(request, 'You have already booked the maximum allowed seats (10 in total).')
        else:
            current_datetime = timezone.now()
            screening_datetime = movie.screening_datetime  # Adjust as needed

            time_difference = screening_datetime - current_datetime

            if time_difference <= timedelta(minutes=40):
                messages.warning(request, 'The screening time is too close. Booking is not available.')
            else:
                with transaction.atomic():
                    bookings_for_screening = Booking.objects.filter(movie=movie, user=user).count()

                    if bookings_for_screening >= max_allowed_bookings_total:
                        messages.warning(request, 'You have already booked the maximum allowed seats for this screening.')
                    else:
                        # Calculate the number of seats left to book for this screening
                        seats_left_for_screening = max_allowed_bookings_total - bookings_for_screening

                        # Check if the user is trying to book more seats than are available for this screening
                        if len(selected_seats) > seats_left_for_screening:
                            messages.warning(request, f'You can only book {seats_left_for_screening} seats for this screening.')
                        else:
                            for seat in selected_seats:
                                row = seat[0]
                                col = seat[1]

                                try:
                                    # Attempt to create a booking while acquiring a row-level lock
                                    booking = Booking(
                                        movie=movie,
                                        seat_row=row,
                                        seat_column=col,
                                        user=user,
                                        selected_screening=selected_screening,
                                    )
                                    booking.save()
                                    # Save additional booking data if needed
                                    messages.success(request, f'Seat {row}{col} booking successful! Enjoy the movie.')
                                except IntegrityError:
                                    # The seat is already booked, handle gracefully
                                    messages.warning(request, f'Seat {row}{col} is already booked. Please select another seat.')

    return redirect('movie_detail', pk=pk)




@login_required(login_url='login')
def process_bookings2(request, pk):
    if request.method == 'POST':
        selected_seats = request.POST.getlist('seat')
        movie = get_object_or_404(Movie, pk=pk)
        user = request.user
        selected_screening = movie.screening_datetime2  # Adjust as needed

        if user is None:
            messages.warning(request, 'Please log in to proceed with the booking.')
            return redirect('login')

        max_allowed_bookings_total = 10
        existing_bookings_total = Booking2.objects.filter(user=user).count()

        if existing_bookings_total >= max_allowed_bookings_total:
            messages.warning(request, 'You have already booked the maximum allowed seats (10 in total).')
        else:
            current_datetime = timezone.now()
            screening_datetime = movie.screening_datetime2  # Adjust as needed

            time_difference = screening_datetime - current_datetime

            if time_difference <= timedelta(minutes=40):
                messages.warning(request, 'The screening time is too close. Booking is not available.')
            else:
                with transaction.atomic():
                    bookings_for_screening = Booking2.objects.filter(movie=movie, user=user).count()

                    if bookings_for_screening >= max_allowed_bookings_total:
                        messages.warning(request, 'You have already booked the maximum allowed seats for this screening.')
                    else:
                        # Calculate the number of seats left to book for this screening
                        seats_left_for_screening = max_allowed_bookings_total - bookings_for_screening

                        # Check if the user is trying to book more seats than are available for this screening
                        if len(selected_seats) > seats_left_for_screening:
                            messages.warning(request, f'You can only book {seats_left_for_screening} seats for this screening.')
                        else:
                            for seat in selected_seats:
                                row = seat[0]
                                col = seat[1]

                                try:
                                    # Attempt to create a booking while acquiring a row-level lock
                                    booking2 = Booking2(
                                        movie=movie,
                                        seat_row=row,
                                        seat_column=col,
                                        user=user,
                                        selected_screening=selected_screening,
                                    )
                                    booking2.save()
                                    # Save additional booking data if needed
                                    messages.success(request, f'Seat {row}{col} booking successful! Enjoy the movie.')
                                except IntegrityError:
                                    # The seat is already booked, handle gracefully
                                    messages.warning(request, f'Seat {row}{col} is already booked. Please select another seat.')

    return redirect('movie_detail_2', pk=pk)



@login_required(login_url='login')
def process_bookings3(request, pk):
    if request.method == 'POST':
        selected_seats = request.POST.getlist('seat')
        movie = get_object_or_404(Movie, pk=pk)
        user = request.user
        selected_screening = movie.screening_datetime3  # Adjust as needed

        if user is None:
            messages.warning(request, 'Please log in to proceed with the booking.')
            return redirect('login')

        max_allowed_bookings_per_screening = 10
        existing_bookings_for_screening = Booking3.objects.filter(movie=movie, user=user).count()

        if existing_bookings_for_screening >= max_allowed_bookings_per_screening:
            messages.warning(request, 'You have already booked the maximum allowed seats for this screening.')
        else:
            current_datetime = timezone.now()
            screening_datetime = movie.screening_datetime3  # Adjust as needed

            time_difference = screening_datetime - current_datetime

            if time_difference <= timedelta(minutes=40):
                messages.warning(request, 'The screening time is too close. Booking is not available.')
            else:
                with transaction.atomic():
                    for seat in selected_seats:
                        row = seat[0]
                        col = seat[1]

                        try:
                            # Attempt to create a booking while acquiring a row-level lock
                            booking3 = Booking3(
                                movie=movie,
                                seat_row=row,
                                seat_column=col,
                                user=user,
                                selected_screening=selected_screening,
                            )
                            booking3.save()
                            # Save additional booking data if needed
                            messages.success(request, f'Seat {row}{col} booking successful! Enjoy the movie.')
                        except IntegrityError:
                            # The seat is already booked, handle gracefully
                            messages.warning(request, f'Seat {row}{col} is already booked. Please select another seat.')

    return redirect('movie_detail_3', pk=pk)




def search_theater(request):
    if 'query' in request.GET:
        query = request.GET['query']
        theaters = Theater.objects.filter(location__icontains=query)
        params = {'theaters': theaters}
        return render(request, 'movie_sys/search.html', params)
    return render(request, 'movie_sys/search.html')




@login_required(login_url='login')
def my_booking(request):
    user = request.user

    if user.is_authenticated:
        profile = get_object_or_404(Profile, user=user)
        watch_later_ott = profile.watch_later.all()

        # Fetch bookings from all three models
        bookings1 = Booking.objects.filter(user=user)
        bookings2 = Booking2.objects.filter(user=user)
        bookings3 = Booking3.objects.filter(user=user)

        # Combine the booking data
        all_bookings = list(bookings1) + list(bookings2) + list(bookings3)

        watch_later_movies = WatchLater.objects.filter(user=user).select_related('movie_title')
        context = {
            'all_bookings': all_bookings,
            'watch_later_movies': watch_later_movies,
            'watch_later_ott': watch_later_ott
        }
        return render(request, 'movie_sys/mybookings.html', context)
    else:
        # Handle the case where the user is not authenticated
        return redirect('login')  


login_required(login_url='login')
def add_to_watch_later(request, pk):
    user = request.user

    if user.is_authenticated:
        ott = get_object_or_404(Ott, pk=pk)
        profile = get_object_or_404(Profile, user=request.user)

        if ott in profile.watch_later.all():
            messages.warning(request, f'{ott.title} is already in your watch later list.')
        else:
            profile.watch_later.add(ott)
            messages.success(request, f'{ott.title} has been added to your watch later list.')

        return redirect('ott_detail', pk=pk)
    else:
        # Handle the case where the user is not authenticated
        return redirect('login')  





@login_required(login_url='login')
def cancel_booking(request, booking_id):
    try:
        user = request.user

        all_bookings = list(Booking.objects.filter(user=user, is_canceled=False)) + \
                       list(Booking2.objects.filter(user=user, is_canceled=False)) + \
                       list(Booking3.objects.filter(user=user, is_canceled=False))


        booking_to_cancel = next((booking for booking in all_bookings if booking.id == booking_id), None)

        # Calculate the time difference
        current_datetime = datetime.now(pytz.utc)
        screening_datetime = booking_to_cancel.selected_screening.astimezone(pytz.utc)
        time_difference = screening_datetime - current_datetime


        if time_difference <= timedelta(minutes=45):
            messages.warning(request, 'Booking cancellation is not available within 45 minutes of screening.')
        elif timedelta(minutes=45) < time_difference <= timedelta(hours=1, minutes=30):
            # 50% refund
            booking_to_cancel.is_canceled = True
            booking_to_cancel.delete()
            messages.success(request, 'Booking canceled. 50% refund applied.')
        elif timedelta(hours=1, minutes=30) < time_difference <= timedelta(hours=2):
            # 75% refund
            booking_to_cancel.is_canceled = True
            booking_to_cancel.delete()
            messages.success(request, 'Booking canceled. 75% refund applied.')
        else:
            # 90% refund
            booking_to_cancel.is_canceled = True
            booking_to_cancel.delete()
            messages.success(request, 'Booking canceled. 90% refund applied.')

        return redirect('my_booking')

    except Booking.DoesNotExist:
        messages.warning(request, 'Booking not found or already canceled.')
        return redirect('my_booking')
    except Exception as e:
        messages.error(request, f"An error occurred: {e}")
        return redirect('my_booking')





@login_required(login_url='login')
def remove_from_watch_later(request, pk):
    user = request.user

    if user.is_authenticated:
        ott = get_object_or_404(Ott, pk=pk)
        profile = get_object_or_404(Profile, user=user)

        if ott in profile.watch_later.all():
            profile.watch_later.remove(ott)
            messages.success(request, f'{ott.title} has been removed from your watch later list.')
        else:
            messages.warning(request, f'{ott.title} was not found in your watch later list.')

        return redirect('my_booking')
    else:
        return redirect('login')

