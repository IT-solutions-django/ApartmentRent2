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
    phone = models.CharField(max_length=11, verbose_name='Номер телефона')
    email = models.EmailField(verbose_name='Email')
    comment = models.TextField(verbose_name='Комментарий', null=True, blank=True)


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, verbose_name='Квартира')
    start_date = models.DateField(verbose_name='Дата въезда')
    end_date = models.DateField(verbose_name='Дата отъезда')
    data_booking = models.ForeignKey(DataBooking, on_delete=models.CASCADE, verbose_name='Данные бронирования')

    def __str__(self):
        return f'{self.user.username} - {self.apartment.name} ({self.start_date} to {self.end_date})'
