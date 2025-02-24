from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from django.db.models import Q
from apartment.forms import BookingForm, FeedbackForm
from apartment.models import Apartment, Booking
from django.http import JsonResponse
from .utils.send_tg import send_telegram_message
import json
from rent.tasks import send_telegram_message, send_telegram_feedback


def main(request):
    if request.POST:
        if request.POST.get('check-in-date'):
            start_date = datetime.strptime(request.POST['check-in-date'], '%Y-%m-%d').date()
            end_date = datetime.strptime(request.POST['check-out-date'], '%Y-%m-%d').date()
            count_people = request.POST['count-people']

            return redirect(
                f"/catalog/?check-in-date={start_date}&check-out-date={end_date}&people-count={count_people}")
        else:
            form = FeedbackForm(request.POST)
            if form.is_valid():
                form.save()

                message = (f'💬 <b>Новое сообщение!</b>\n\n'
                           f'👤 Имя: <b>{form.cleaned_data.get("name")}</b>\n'
                           f'📱 Телефон: <b>{form.cleaned_data.get("phone")}</b>\n'
                           f'💬 Сообщение: <b>{form.cleaned_data.get("comment")}</b>'
                           )
                send_telegram_feedback.delay(message)

                return JsonResponse({'success': 'Ваша заявка отправлена, менеджер свяжется с вами в ближайшее время',
                                     'redirect_url': f'{request.path}'})
            else:
                errors = [error for field in form for error in field.errors]
                return JsonResponse({'errors': errors}, status=400)

    if request.user.is_authenticated:
        active_bookings = Booking.objects.filter(user=request.user, status='C')
    else:
        active_bookings = []

    aparts_popular = Apartment.objects.all()

    date_now = datetime.now().date()
    date_tomorrow = date_now + timedelta(days=1)

    form = FeedbackForm()

    return render(request, 'main.html', {'aparts_popular': aparts_popular, 'active_bookings': active_bookings,
                                         'date_now': date_now.isoformat(),
                                         'date_tomorrow': date_tomorrow.isoformat(), 'form': form})


def catalog(request):
    people_options = list(range(1, 7))

    date_in = request.GET.get('check-in-date')
    date_out = request.GET.get('check-out-date')
    people_count = request.GET.get('people-count')
    if date_in and date_out and people_count:
        try:
            date_in = datetime.strptime(date_in, '%Y-%m-%d').date()
            date_out = datetime.strptime(date_out, '%Y-%m-%d').date()
            if date_in < datetime.now().date() or date_out <= date_in:
                raise ValueError
            people_count = int(people_count)
        except ValueError:
            return redirect('catalog')

        unavailable_apartments = Booking.objects.filter(
            Q(start_date__lt=date_out, end_date__gt=date_in)
        ).values_list('apartment_id', flat=True)

        aparts = Apartment.objects.filter(
            quantity_people__gte=people_count,
            available=True
        ).exclude(id__in=unavailable_apartments)

    else:
        aparts = Apartment.objects.all()

    date_now = datetime.now().date()
    date_tomorrow = date_now + timedelta(days=1)

    if request.user.is_authenticated:
        active_bookings = Booking.objects.filter(user=request.user, status='C')
    else:
        active_bookings = []

    form = FeedbackForm()

    if date_in and date_out and people_count:
        return render(request, 'catalog.html',
                      {'aparts': aparts, 'date_start': date_in.isoformat(), 'date_end': date_out.isoformat(),
                       'people_count': people_count, 'people_options': people_options,
                       'active_bookings': active_bookings, 'form': form})

    return render(request, 'catalog.html',
                  {'aparts': aparts, 'people_options': people_options, 'date_now': date_now.isoformat(),
                   'date_tomorrow': date_tomorrow.isoformat(), 'active_bookings': active_bookings, 'form': form})


def card(request, card_id):
    if request.user.is_authenticated:
        active_bookings = Booking.objects.filter(user=request.user, status='C')
    else:
        active_bookings = []

    form = FeedbackForm()

    card_info = Apartment.objects.get(id=card_id)
    return render(request, 'card.html', {'card_info': card_info, 'active_bookings': active_bookings, 'form': form})


@login_required
def reservation(request, card_id):
    if request.POST:
        form_data_booking = BookingForm(request.POST)

        if form_data_booking.is_valid():
            date_start = datetime.strptime(request.POST['check-in-date'], '%Y-%m-%d').date()
            date_end = datetime.strptime(request.POST['check-out-date'], '%Y-%m-%d').date()

            if date_start < datetime.now().date() or date_end <= date_start:
                return JsonResponse({'error': 'Неверный формат даты.'}, status=400)

            existing_booking = Booking.objects.filter(
                apartment_id=card_id,
                start_date__lt=date_end,
                end_date__gt=date_start
            )

            if existing_booking.exists():
                return JsonResponse({'error': 'Квартира уже забронирована на эти даты.'}, status=400)

            data_booking = form_data_booking.save()

            apart_booking = Booking(
                user=request.user,
                apartment_id=card_id,
                start_date=date_start,
                end_date=date_end,
                data_booking=data_booking
            )
            apart_booking.save()

            message = (f"🏠 <b>Новое бронирование!</b>\n"
                       f"📍 Квартира: <b>{apart_booking.apartment.name}</b>\n"
                       f"👤 Пользователь: <b>{request.user.username}</b>\n"
                       f"📅 Даты: <b>{date_start} - {date_end}</b>")
            send_telegram_message.delay(message)

            return JsonResponse({'success': 'Бронирование успешно!', 'redirect_url': '/catalog'})

    date_in = request.GET.get('check-in-date')
    date_out = request.GET.get('check-out-date')

    if date_in and date_out:
        try:
            date_start = datetime.strptime(date_in, '%Y-%m-%d').date()
            date_end = datetime.strptime(date_out, '%Y-%m-%d').date()
        except ValueError:
            return redirect('reservation')

    form_data_booking = BookingForm()

    card_info = Apartment.objects.get(id=card_id)

    date_now = datetime.now().date()
    date_tomorrow = date_now + timedelta(days=1)

    if request.user.is_authenticated:
        active_bookings = Booking.objects.filter(user=request.user, status='C')
    else:
        active_bookings = []

    bookings = Booking.objects.filter(apartment=card_info)

    booked_dates = []
    for booking in bookings:
        current_date = booking.start_date
        while current_date <= booking.end_date:
            booked_dates.append(current_date.strftime("%Y-%m-%d"))
            current_date += timedelta(days=1)

    form_2 = FeedbackForm()

    if date_in and date_out:
        return render(request, 'reservation.html',
                      {'date_now': date_now.isoformat(),
                       'date_tomorrow': (date_start + timedelta(days=1)).isoformat(),
                       'form': form_data_booking, 'card_info': card_info, 'active_bookings': active_bookings,
                       "booked_dates": json.dumps(booked_dates), 'date_in': date_start.isoformat(),
                       'date_out': date_end.isoformat(), 'form_2': form_2})

    return render(request, 'reservation.html',
                  {'date_now': date_now.isoformat(), 'date_tomorrow': date_tomorrow.isoformat(),
                   'form': form_data_booking, 'card_info': card_info, 'active_bookings': active_bookings,
                   "booked_dates": json.dumps(booked_dates), 'form_2': form_2})
