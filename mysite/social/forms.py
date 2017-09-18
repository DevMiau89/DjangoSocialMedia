from django import forms
from datetime import datetime
from django.forms import extras
from .models import SocialUser

# from django.contrib.auth import (
#     authenticate,
#     get_user_model,
#     login,
#     logout,
# )
#
# User = get_user_model()


class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    b_day = forms.DateField(widget=extras.SelectDateWidget(years=range(1939, datetime.now().year)), required=True)
    gender = forms.CharField(widget=forms.RadioSelect(
        choices=SocialUser.GENDER_CHOICES
    ), required=True)
    # class Meta:
    #     model = SocialUser
    #     fields = ('name',
    #               'surname',
    #               'email',
    #               'password',
    #               'b_day',
    #               'gender',
    #               )
