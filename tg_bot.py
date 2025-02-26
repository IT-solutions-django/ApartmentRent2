import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'rent.settings'
django.setup()

import telebot
from apartment.models import Booking, Feedback
from telebot import types
from rent.tasks import send_email_booking

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
                 "Бот для бронирования квартир!\n\n<b>Команды:</b>\n/active_bookings - Активные бронирования\n/not_bookings - Не подтвержденные бронирования",
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
            cancel_button = types.InlineKeyboardButton("❌ Отменить", callback_data=f'cancel_{booking.id}')
            completed_button = types.InlineKeyboardButton("☑️ Завершить", callback_data=f'completed_{booking.id}')
            markup.add(cancel_button)
            markup.add(completed_button)

            bot.reply_to(message, messages, reply_markup=markup, parse_mode='HTML')
    else:
        bot.reply_to(message, 'Нет забронированных квартир.')


@bot.message_handler(commands=['active_orders'])
def list_orders(message):
    orders = Feedback.objects.all()

    if orders:
        for order in orders:
            messages = f'<b>Имя</b>: {order.name}\n<b>Телефон</b>: {order.phone}\n<b>Сообщение</b>: {order.comment}'

            markup = types.InlineKeyboardMarkup()
            ready_button = types.InlineKeyboardButton("✅ Готово", callback_data=f'ready_{order.id}')

            markup.add(ready_button)
            bot.reply_to(message, messages, reply_markup=markup, parse_mode='HTML')
    else:
        bot.reply_to(message, 'Нет активных заявок.')


@bot.message_handler(commands=['not_bookings'])
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

        message_booking = f'Ваша заявка на бронирование квартиры подтверждена. Ссылка на квартиру: http://37.77.106.122/card/{booking.apartment.id}/'
        send_email_booking.delay(booking.data_booking.email, 'Статус бронирования', message_booking,
                                 '37.77.106.122')

        bot.answer_callback_query(call.id, text="Бронирование подтверждено ✅")
        bot.reply_to(call.message, f'✅ Бронирование пользователя {booking.user.username} подтверждено.')
    elif action == "cancel":
        message_booking = f'Ваша заявка на бронирование квартиры отменена. Ссылка на квартиру: http://37.77.106.122/card/{booking.apartment.id}/'
        send_email_booking.delay(booking.data_booking.email, 'Статус бронирования', message_booking,
                                 '37.77.106.122')

        bot.answer_callback_query(call.id, text="Бронирование отменено ❌")
        bot.reply_to(call.message, f'❌ Бронирование пользователя {booking.user.username} отменено.')

        booking.delete()
    elif action == "completed":
        message_booking = f'Ваше бронирование квартиры завершено. Ссылка на квартиру: http://37.77.106.122/card/{booking.apartment.id}/'
        send_email_booking.delay(booking.data_booking.email, 'Статус бронирования', message_booking,
                                 '37.77.106.122')

        bot.answer_callback_query(call.id, text="Бронирование завершено ☑️")
        bot.reply_to(call.message, f'☑️ Бронирование пользователя {booking.user.username} завершено.')

        booking.delete()


@bot.callback_query_handler(func=lambda call: call.data.startswith(('ready_',)))
def handle_booking_action(call):
    action, order_id = call.data.split('_')
    order = Feedback.objects.get(id=int(order_id))

    order.delete()
    bot.answer_callback_query(call.id, text="Заявка обработана ☑️")
    bot.reply_to(call.message, f'☑️ Заявка пользователя {order.name} обработана.')


def start_bot():
    bot.polling(non_stop=True)


if __name__ == '__main__':
    start_bot()
