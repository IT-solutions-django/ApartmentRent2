from django.contrib import admin
from apartment.models import Apartment, Booking, DataBooking, Feedback, ApartmentPhoto

admin.site.register(Apartment)
admin.site.register(Booking)
admin.site.register(DataBooking)
admin.site.register(Feedback)
admin.site.register(ApartmentPhoto)
