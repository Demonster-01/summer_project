from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Movie, Theater, Upcomming,Booking, Seat
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect




class MovieListView(ListView):
    model = Theater
    template_name = 'movie_sys/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'theaters'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['upcommings'] = Upcomming.objects.all()
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



# class MovieDetailView(DetailView):
#     model = Movie
#     template_name = 'movie_sys/movie_detail.html'



class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movie_sys/movie_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rows'] = range(1, self.object.theater.no_of_seat_rows+1)
        context['cols'] = range(1, self.object.theater.num_of_seats_column+1)
        # context['bookings'] = self.object.booking_set.all()
        return context

def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        booking.selected_seats = request.POST.get('selected_seats', '')
        booking.save()
    context = {'booking': booking}
    return render(request, 'movie_sys/booking_detail.html', context)








def reserve_seats(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    rows = range(1, movie.theater.rows + 1)
    cols = range(1, movie.theater.columns + 1)

    if request.method == 'POST':
        selected_seats = request.POST.getlist('seat')
        for seat in movie.seats.all():
            seat_id = f"{seat.row}-{seat.column}"
            if seat_id in selected_seats:
                seat.is_booked = True
                seat.reserved = True
            else:
                seat.is_booked = False
                seat.reserved = False
            seat.save()

        return HttpResponseRedirect('/thankyou/')

    context = {
        'movie': movie,
        'rows': rows,
        'cols': cols,
    }
    return render(request, 'movie_sys/movie_detail.html', context)
