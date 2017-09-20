from django.contrib.auth.models import User
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)

from django.shortcuts import render, redirect

from .forms import RegistrationForm, LoginForm
from .models import SocialUser

user = get_user_model()

# Create your views here.
def index(request):
    return render(request, 'index.html', {})


def index_nav(request):
    if request.method == 'POST':
        form1 = RegistrationForm(request.POST or None)

        print form1.errors
        print "cipa"
        if form1.is_valid() and "btnform1" in request.POST:
            form_name = form1.cleaned_data["first_name"]
            form_surname = form1.cleaned_data["last_name"]
            form_email = form1.cleaned_data["email"]
            form_b_day = form1.cleaned_data["b_day"]
            form_password = form1.cleaned_data["password"]
            form_gender = form1.cleaned_data["gender"]

            feedback = SocialUser(name=form_name, surname=form_surname, email=form_email,
                                  b_day=form_b_day, password=form_password, gender=form_gender
                                  )

            user_admin = User.objects.create_user(form_email, form_email, form_password)
            user_admin.save()
            feedback.save()
            return render(request, "index_nav.html", {"form": form1,
                                                      "name": form_name,
                                                      "surname": form_surname,
                                                      "email": form_email,
                                                      "b_day": form_b_day,
                                                      "password": form_password,
                                                      "gender": form_gender,
                                                      })
    else:
        form1 = RegistrationForm()
    return render(request, 'index_nav.html', {"form": form1})


def login_view(request):
    if request.method == 'POST':
        form2 = LoginForm(request.POST or None)
        print form2.errors
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(username=email, password=password)
        if user:
            login(request, user)
            return redirect('/')
    return render(request, 'login_view.html', {})
