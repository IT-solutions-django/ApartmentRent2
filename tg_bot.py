import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'rent.settings'
django.setup()

import telebot
from apartment.models import Booking
from telebot import types

bot = telebot.TeleBot("7945761248:AAEtjVm4drm3nxgcEee-r3nu9gMLjPQk0_A")

BookingStatus = {
    'P': 'Ожидает',
    'C': 'Подтверждено',
    'X': 'Отменено',
    'D': 'Завершено'
}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,
                 "Бот для бронирования квартир!\n\n<b>Команды:</b>\n/active_bookings - Активные бронирования\n/notConfirmed_bookings - Не подтвержденные бронирования",
                 parse_mode="html")


@bot.message_handler(commands=['active_bookings'])
def list_bookings(message):
    bookings = Booking.objects.filter(status='C')
    if bookings:
        for booking in bookings:
            data_booking = booking.data_booking
            apart = booking.apartment
            status = BookingStatus[booking.status]
            messages = f'<b>Пользователь:</b> {booking.user.username}\n<b>Статус:</b> {status}\n\n<b>Данные бронирования:</b>\n- {apart.name}\n- до {apart.quantity_people} мест • {apart.square} м²\n- {apart.price}/сутки\n- Дата бронирования: с <b>{booking.start_date}</b> до <b>{booking.end_date}</b>\n\n<b>Контактная информация:</b>\nИмя - {data_booking.name}\nФамилия - {data_booking.surname}\nТелефон - {data_booking.phone}\nEmail - {data_booking.email}\nКомментарий - {data_booking.comment}'

            markup = types.InlineKeyboardMarkup()
            confirm_button = types.InlineKeyboardButton("✅ Подтвердить", callback_data=f'confirm_{booking.id}')
            cancel_button = types.InlineKeyboardButton("❌ Отменить", callback_data=f'cancel_{booking.id}')
            completed_button = types.InlineKeyboardButton("☑️ Завершить", callback_data=f'completed_{booking.id}')
            markup.add(confirm_button, cancel_button)
            markup.add(completed_button)

            bot.reply_to(message, messages, reply_markup=markup, parse_mode='HTML')
    else:
        bot.reply_to(message, 'Нет забронированных квартир.')


@bot.message_handler(commands=['notConfirmed_bookings'])
def list_bookings(message):
    bookings = Booking.objects.filter(status='P')
    if bookings:
        for booking in bookings:
            data_booking = booking.data_booking
            apart = booking.apartment
            status = BookingStatus[booking.status]
            messages = f'<b>Пользователь:</b> {booking.user.username}\n<b>Статус:</b> {status}\n\n<b>Данные бронирования:</b>\n- {apart.name}\n- до {apart.quantity_people} мест • {apart.square} м²\n- {apart.price}/сутки\n- Дата бронирования: с <b>{booking.start_date}</b> до <b>{booking.end_date}</b>\n\n<b>Контактная информация:</b>\nИмя - {data_booking.name}\nФамилия - {data_booking.surname}\nТелефон - {data_booking.phone}\nEmail - {data_booking.email}\nКомментарий - {data_booking.comment}'

            markup = types.InlineKeyboardMarkup()
            confirm_button = types.InlineKeyboardButton("✅ Подтвердить", callback_data=f'confirm_{booking.id}')
            cancel_button = types.InlineKeyboardButton("❌ Отменить", callback_data=f'cancel_{booking.id}')
            completed_button = types.InlineKeyboardButton("☑️ Завершить", callback_data=f'completed_{booking.id}')
            markup.add(confirm_button, cancel_button)
            markup.add(completed_button)

            bot.reply_to(message, messages, reply_markup=markup, parse_mode='HTML')
    else:
        bot.reply_to(message, 'Нет забронированных квартир.')


@bot.callback_query_handler(func=lambda call: call.data.startswith(('confirm_', 'cancel_', 'completed_')))
def handle_booking_action(call):
    action, booking_id = call.data.split('_')
    booking = Booking.objects.get(id=int(booking_id))

    if action == "confirm":
        booking.status = Booking.BookingStatus.CONFIRMED
        booking.save()
        bot.answer_callback_query(call.id, text="Бронирование подтверждено ✅")
        bot.reply_to(call.message, f'✅ Бронирование пользователя {booking.user.username} подтверждено.')
    elif action == "cancel":
        booking.delete()
        bot.answer_callback_query(call.id, text="Бронирование отменено ❌")
        bot.reply_to(call.message, f'❌ Бронирование пользователя {booking.user.username} отменено.')
    elif action == "completed":
        booking.delete()
        bot.answer_callback_query(call.id, text="Бронирование завершено ☑️")
        bot.reply_to(call.message, f'☑️ Бронирование пользователя {booking.user.username} завершено.')


def start_bot():
    bot.polling(non_stop=True)


if __name__ == '__main__':
    start_bot()
