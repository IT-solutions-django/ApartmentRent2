from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Apartment(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    quantity_people = models.IntegerField(verbose_name='Кол-во людей')
    square = models.IntegerField(verbose_name='Площадь', help_text='в м²')
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Цена', help_text='за сутку')
    available = models.BooleanField(verbose_name='Доступна', default=True)

    def __str__(self):
        return f'{self.name} | {self.price}'


class DataBooking(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя')
    surname = models.CharField(max_length=50, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=50, verbose_name='Отчество', null=True, blank=True)
    phone = models.CharField(max_length=50, verbose_name='Номер телефона')
    email = models.EmailField(verbose_name='Email')
    comment = models.TextField(verbose_name='Комментарий', null=True, blank=True)


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, verbose_name='Квартира')
    start_date = models.DateField(verbose_name='Дата въезда')
    end_date = models.DateField(verbose_name='Дата отъезда')
    data_booking = models.ForeignKey(DataBooking, on_delete=models.CASCADE, verbose_name='Данные бронирования')
    total_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Итоговая стоимость", default=0)

    def save(self, *args, **kwargs):
        if self.start_date and self.end_date and self.apartment:
            num_days = (self.end_date - self.start_date).days
            self.total_price = self.apartment.price * num_days if num_days > 0 else 0
        super().save(*args, **kwargs)

    def get_total_days(self):
        return (self.end_date - self.start_date).days

    class BookingStatus(models.TextChoices):
        PENDING = 'P', 'Ожидает'
        CONFIRMED = 'C', 'Подтверждено'
        CANCELED = 'X', 'Отменено'
        COMPLETED = 'D', 'Завершено'

    status = models.CharField(
        max_length=1,
        choices=BookingStatus.choices,
        default=BookingStatus.PENDING,
        verbose_name='Статус'
    )

    def __str__(self):
        return f'Пользователь: {self.user.username}. Дата бронирования: {self.start_date} - {self.end_date}. Статус: {self.status}'


class Feedback(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    phone = models.CharField(max_length=50, verbose_name='Телефон')
    comment = models.TextField(verbose_name='Сообщение')

    def __str__(self):
        return f'Вопрос от {self.name}. Вопрос: {self.comment}'
