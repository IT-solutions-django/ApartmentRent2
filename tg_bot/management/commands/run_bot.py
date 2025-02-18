from django.core.management.base import BaseCommand
from telebot import types
import telebot
from apartment.models import Booking
import multiprocessing

bot = telebot.TeleBot("7945761248:AAEtjVm4drm3nxgcEee-r3nu9gMLjPQk0_A")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Используй /bookings чтобы посмотреть забронированные квартиры.")


@bot.message_handler(commands=['bookings'])
def list_bookings(message):
    bookings = Booking.objects.all()
    if bookings:
        for booking in bookings:
            data_booking = booking.data_booking
            messages = f'Пользователь: {booking.user.username}.\nДата бронирования: {booking.start_date} - {booking.end_date}.\nСтатус: {booking.status}\n\nДанные бронирования\nИмя - {data_booking.name}\nФамилия - {data_booking.surname}\nТелефон - {data_booking.phone}\nEmail - {data_booking.email}\nКомментарий - {data_booking.comment}'

            markup = types.InlineKeyboardMarkup()
            confirm_button = types.InlineKeyboardButton("✅ Подтвердить", callback_data=f'confirm_{booking.id}')
            cancel_button = types.InlineKeyboardButton("❌ Отменить", callback_data=f'cancel_{booking.id}')
            markup.add(confirm_button, cancel_button)

            bot.reply_to(message, messages, reply_markup=markup)
    else:
        bot.reply_to(message, 'Нет забронированных квартир.')


@bot.callback_query_handler(func=lambda call: call.data.startswith(('confirm_', 'cancel_')))
def handle_booking_action(call):
    action, booking_id = call.data.split('_')
    booking = Booking.objects.get(id=int(booking_id))

    if action == "confirm":
        booking.status = Booking.BookingStatus.CONFIRMED
        bot.answer_callback_query(call.id, text="Бронирование подтверждено ✅")
        bot.send_message(call.message.chat.id, f'✅ Бронирование пользователя {booking.user.username} подтверждено.')
    elif action == "cancel":
        booking.status = Booking.BookingStatus.CANCELED
        bot.answer_callback_query(call.id, text="Бронирование отменено ❌")
        bot.send_message(call.message.chat.id, f'❌ Бронирование пользователя {booking.user.username} отменено.')

    booking.save()


def start_bot():
    bot.polling(non_stop=True, timeout=60)


class Command(BaseCommand):
    help = 'Запуск Telegram бота'

    def handle(self, *args, **kwargs):
        process = multiprocessing.Process(target=start_bot)
        process.start()
