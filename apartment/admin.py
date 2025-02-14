from django.contrib import admin
from apartment.models import Apartment, Booking, DataBooking

admin.site.register(Apartment)
admin.site.register(Booking)
admin.site.register(DataBooking)
