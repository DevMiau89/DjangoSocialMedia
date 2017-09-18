from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)

from django.shortcuts import render

from .forms import RegistrationForm
from .models import SocialUser


# Create your views here.
def index(request):
    return render(request, 'index.html', {})


def index_nav(request):
    print 'dupa'
    if request.method == 'POST':
        form = RegistrationForm(request.POST or None)
        #form.b_day = request.body['birthday_month'] + "/" + request.body['birthday_day'] + "/" + request.body['birthday_year']
        print 'chuj'
        print form.errors
        if form.is_valid():
            print 'kurwa'
            form_name = form.cleaned_data["first_name"]
            form_surname = form.cleaned_data["last_name"]
            form_email = form.cleaned_data["email"]
            form_b_day = form.cleaned_data["b_day"]
            form_password = form.cleaned_data["password"]
            form_gender = form.cleaned_data["gender"]

            feedback = SocialUser(name=form_name, surname=form_surname, email=form_email,
                                  b_day=form_b_day, password=form_password, gender=form_gender
                                  )
            print 'cipa'
            feedback.save()
            return render(request, "index_nav.html", {"form": form,
                                                      "name": form_name,
                                                      "surname": form_surname,
                                                      "email": form_email,
                                                      "b_day": form_b_day,
                                                      "password": form_password,
                                                      "gender": form_gender
                                                      })
    else:
        print 'troll'
        form = RegistrationForm()
    return render(request, 'index_nav.html', {"form": form})
