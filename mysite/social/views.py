from django.contrib.auth.models import User
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)

from django.shortcuts import render, redirect

from .forms import RegistrationForm, LoginForm, PostForm
from .models import SocialUser, Post

user = get_user_model()

# Create your views here.
def index(request):

    if request.method == 'POST':
        post_form = PostForm(request.POST or None)
        print post_form.errors
        if post_form.is_valid():
            form_title = post_form.cleaned_data['title']
            form_text = post_form.cleaned_data['text']


            feedback = Post(title=form_title, text=form_text)
            feedback.save()
            return render(request, "index.html", {"form": post_form,
                                                  "title": form_title,
                                                  "text": form_text,
            })
    current_user = request.name
    print current_user
    posts = Post.objects.all()
    print posts
    return render(request, 'index.html', {"posts": posts, "user": current_user})


def index_nav(request):
    if request.method == 'POST':
        form1 = RegistrationForm(request.POST or None)

        print form1.errors
        if form1.is_valid():
            form_name = form1.cleaned_data["first_name"]
            form_surname = form1.cleaned_data["last_name"]
            form_email = form1.cleaned_data["email"]
            form_b_day = form1.cleaned_data["b_day"]
            form_password = form1.cleaned_data["password"]
            form_gender = form1.cleaned_data["gender"]

            feedback = SocialUser(name=form_name, surname=form_surname, email=form_email,
                                  b_day=form_b_day, password=form_password, gender=form_gender
                                  )

            user_admin = User.objects.create_user(username=form_email, email=form_email, password=form_password)
            user_admin.save()
            feedback.save()
            new_user = authenticate(username=feedback.email, password=feedback.password)
            login(request, new_user)
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
        form1 = RegistrationForm(request.POST or None)
        print form2.errors
        if form2.is_valid():
            email = request.POST.get("email")
            password = request.POST.get("password")
            user = authenticate(username=email, password=password)
            login(request, user)
            return redirect('/account')
    else:
        form2 = RegistrationForm()
    return render(request, "login_view.html", {'form2': form2, "form": form1})


def logout_view(request):
    logout(request)
    print request.user.is_active
    return redirect('/')
