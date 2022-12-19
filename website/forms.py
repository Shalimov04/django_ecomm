from django.core.mail import send_mail
from django import forms
from django.core import validators

class CheckOutForm(forms.Form):
    name = forms.CharField(label='Ваше имя:', max_length=100, min_length=5)
    email = forms.EmailField(label='Ваш Email:', validators=[validators.EmailValidator])

