from django.shortcuts import render
from datetime import datetime, timedelta
from apartment.forms import BookingForm
from apartment.models import Apartment


def main(request):
    aparts_popular = Apartment.objects.all()
    return render(request, 'main.html', {'aparts_popular': aparts_popular})


def catalog(request):
    aparts = Apartment.objects.all()
    return render(request, 'catalog.html', {'aparts': aparts})


def card(request, card_id):
    card_info = Apartment.objects.get(id=card_id)
    return render(request, 'card.html', {'card_info': card_info})


def reservation(request, card_id):
    form_data_booking = BookingForm()

    card_info = Apartment.objects.get(id=card_id)

    date_now = datetime.now().date()
    date_tomorrow = date_now + timedelta(days=1)
    return render(request, 'reservation.html',
                  {'date_now': date_now.isoformat(), 'date_tomorrow': date_tomorrow.isoformat(),
                   'form': form_data_booking, 'card_info': card_info})
