from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class ApartmentPhoto(models.Model):
    image = models.ImageField(upload_to='apartments/', verbose_name='Фото')

    class Meta:
        verbose_name = "Фотография"
        verbose_name_plural = "Фотографии"

    def __str__(self):
        return self.image.name


class Apartment(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    quantity_people = models.IntegerField(verbose_name='Кол-во людей')
    square = models.IntegerField(verbose_name='Площадь', help_text='в м²')
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Цена', help_text='за сутки')
    available = models.BooleanField(verbose_name='Доступна', default=True)
    photos = models.ManyToManyField('ApartmentPhoto', related_name='apartments', blank=True, verbose_name='Фотографии',
                                    null=True)
    street = models.TextField(verbose_name='Улица', null=True, blank=True)

    class Meta:
        verbose_name = "Квартира"
        verbose_name_plural = "Квартиры"

    def __str__(self):
        return f'{self.name} | {self.price}'


class DataBooking(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя')
    surname = models.CharField(max_length=50, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=50, verbose_name='Отчество', null=True, blank=True)
    phone = models.CharField(max_length=50, verbose_name='Номер телефона')
    email = models.EmailField(verbose_name='Email')
    comment = models.TextField(verbose_name='Комментарий', null=True, blank=True)

    class Meta:
        verbose_name = "Данные бронирования"
        verbose_name_plural = "Данные бронирования"

    def __str__(self):
        return f'ФИ: {self.surname} {self.name}. Почта: {self.email}. Комментарий: {self.comment}'


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, verbose_name='Квартира')
    start_date = models.DateField(verbose_name='Дата въезда')
    end_date = models.DateField(verbose_name='Дата отъезда')
    data_booking = models.ForeignKey(DataBooking, on_delete=models.CASCADE, verbose_name='Данные бронирования')
    total_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Итоговая стоимость", default=0)

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"

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

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    def __str__(self):
        return f'Заявка от {self.name}. Вопрос: {self.comment}'
