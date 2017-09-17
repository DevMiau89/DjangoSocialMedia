from django import forms

from django.forms import extras
from .models import SocialUser

from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)

User = get_user_model()

class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    b_day = forms.DateField(widget=extras.SelectDateWidget)
    gender = forms.CharField(widget=forms.RadioSelect(
        choices=SocialUser.GENDER_CHOICES
    ))





