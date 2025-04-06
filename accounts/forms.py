from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


# from django_flatpickr.widgets import DatePickerInput
# from django_flatpickr.schemas import FlatpickrOptions

class EmailUsernameField(forms.EmailField):
    default_validators = [EmailValidator(message='Ingrese un correo electrónico válido')]


class PhoneNumberField(forms.CharField):
    default_validators = [
        RegexValidator(
            regex=r'^\+[1-9]\d{1,14}$',
            message='Ingrese un número de teléfono válido en formato internacional (con +)'
        )
    ]


class CustomUserCreationForm(UserCreationForm):
    username = EmailUsernameField()
    celular = PhoneNumberField(
        max_length=16,
        required=True,
        help_text='Formato Internacional ejemplo: +52 55 5555 5555 para uso con whatsapp'
    )
    alias = forms.CharField(max_length=64)

    class Meta:
        model = User
        fields = ['username',
                  'email',
                  'first_name',
                  'last_name',
                  'password1',
                  'password2']

    first_name = forms.CharField(max_length=64)
    last_name = forms.CharField(max_length=64)

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})

        self.fields['celular'].widget.attrs.update({
            'placeholder': '+52 XX XX XX XX XX',
            'pattern': '\\+[0-9]{1,3}\\s?[0-9]{2}\\s?[0-9]{2}\\s?[0-9]{2}\\s?[0-9]{2}\\s?[0-9]{2}',
            'title': 'Formato: +52 XX XX XX XX XX'
        })

