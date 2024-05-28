import django_filters
from .models import *

class Bookingfilter(django_filters.filterset):
    class Meta:
        model = Booking
        fields = '__all__'