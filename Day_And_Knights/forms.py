from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Player

class PlayerRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=200, required=True)
    last_name = forms.CharField(max_length=200, required=True)
    phone_number = forms.CharField(max_length=200, required=True)
    email = forms.EmailField(max_length=200, required=True)
    ecf_code = forms.CharField(max_length=200, required=True)
