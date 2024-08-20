from django.db import transaction

from bestcar.models import Publishing_a_trip
from booking.decorators import booking_decorator
from booking.exeption import SeatingError
from booking.models import Booking


class Confirmation:
    """
    Берем из модели Publishing_a_trip необходимые данные для создания записи в таблице
    Booking ,предварительно проверяя наличие свободных мест.
    """

    @staticmethod
    @booking_decorator
    def confirmation(trip_slug, request, trip):
        try:
            with transaction.atomic():
                booking = Booking(departure=trip.departure,
                                  arrival=trip.arrival,
                                  departure_time=trip.departure_time,
                                  arrival_time=trip.arrival_time,
                                  price=trip.price,
                                  cat=trip.cat,
                                  author_trip=trip.author,
                                  name_companion=request.user,
                                  slug=trip.slug
                                  )
                booking.save()
        except SeatingError as e:
            return str(e)
