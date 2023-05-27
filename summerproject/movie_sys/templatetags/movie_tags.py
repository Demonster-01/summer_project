from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def seat_reserved(context, row, col):
    movie = context['movie']
    return movie.booked_seats.filter(seat_no=row * movie.theater.num_of_seats_column + col).exists()
