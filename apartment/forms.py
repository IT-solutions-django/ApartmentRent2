from django import forms
from apartment.models import DataBooking, Feedback


class BookingForm(forms.ModelForm):
    class Meta:
        model = DataBooking
        fields = '__all__'

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}),
            'surname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}),
            'patronymic': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Отчество'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7', 'type': 'tel'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Комментарий'}),
        }


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = '__all__'

        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Имя', "style": "padding: 10px 20px;"}),
            'phone': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': '+7', "style": "padding: 10px 20px;", 'type': 'tel'}),
            'comment': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Сообщение', "style": "padding: 10px 20px;"}),
        }
