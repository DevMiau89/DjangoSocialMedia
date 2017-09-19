from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)

from django.shortcuts import render

from .forms import RegistrationForm, LoginForm
from .models import SocialUser


# Create your views here.
def index(request):
    return render(request, 'index.html', {})


def index_nav(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST or None)

        login_form = LoginForm(request.POST or None)
        print form.errors
        if form.is_valid():
            form_name = form.cleaned_data["first_name"]
            form_surname = form.cleaned_data["last_name"]
            form_email = form.cleaned_data["email"]
            form_b_day = form.cleaned_data["b_day"]
            form_password = form.cleaned_data["password"]
            form_gender = form.cleaned_data["gender"]

            feedback = SocialUser(name=form_name, surname=form_surname, email=form_email,
                                  b_day=form_b_day, password=form_password, gender=form_gender
                                  )
            feedback.save()
            return render(request, "index_nav.html", {"formOne": form,
                                                      "name": form_name,
                                                      "surname": form_surname,
                                                      "email": form_email,
                                                      "b_day": form_b_day,
                                                      "password": form_password,
                                                      "gender": form_gender
                                                      })
        if login_form.is_valid():
            email = login_form.cleaned_data["email"]
            password = login_form.cleaned_data["password"]
            user = authenticate(email=email, password=password)
            login(request, user)
            print (request.user.is_authenticated())

            return render(request, 'index_nav.html', {"formTwo": login_form, "email": email, "password": password })
    else:
        form = RegistrationForm()
    return render(request, 'index_nav.html', {"form": form})


# def login_view(request):
#     if request.method == 'POST':
#         login_form = LoginForm(request.POST or None)
#         if login_form.is_valid():
#             email = login_form.cleaned_data["email"]
#             password = login_form.cleaned_data["password"]
#             user = authenticate(email=email, password=password)
#             login(request, user)
#             print (request.user.is_authenticated())
#
#             return render(request, 'index_nav.html', {"form": login_form, "email": email, "password": password })
#     return render(request, 'index_nav.html', {})
