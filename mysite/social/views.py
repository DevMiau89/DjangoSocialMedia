from django.contrib.auth.models import User
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)

from django.shortcuts import render, redirect, get_object_or_404

from .forms import RegistrationForm, LoginForm, PostForm
from .models import SocialUser, Post, Friend

User = get_user_model()

# Create your views here.
def index(request, id=None):
    # if id:
    #     user_id = request.user.id
    if request.method == 'POST':
        post_form = PostForm(request.POST or None)
        print post_form.errors
        if post_form.is_valid():
            form_title = post_form.cleaned_data['title']
            form_text = post_form.cleaned_data['text']


            feedback = Post(title=form_title, text=form_text)
            feedback.save()
            posts = Post.objects.all().order_by('-created_date')
            return render(request, "index.html", {"form": post_form,
                                                  "title": form_title,
                                                  "text": form_text,
                                                  "posts": posts
            })

    current_user = SocialUser.objects.filter(email=request.user.email).first()
    name_of_logged_in_user = current_user.name
    posts = Post.objects.all().order_by('-created_date')
    users = User.objects.exclude(id=request.user.id)

    return render(request, 'index.html', {"posts": posts,
                                          "name_of_logged_in_user": name_of_logged_in_user,
                                          "users": users,
                                          # "user_id": user_id,
                                          })


def post_detail(request, id=None):
    current_user = SocialUser.objects.filter(email=request.user.email).first()
    name_of_logged_in_user = current_user.name
    instance = get_object_or_404(Post, id=id)

    title_value = instance.title
    print instance.title
    text_value = instance.text
    print instance.text
    print request.POST
    if request.method == 'POST' and "text" not in request.POST:
        instance.delete()
        return redirect("/account")


    if request.method == 'POST' and request.POST['text']:
        edit_form = PostForm(request.POST or None)
        if edit_form.is_valid():
            edit_form_title = edit_form.cleaned_data['title']
            edit_form_text = edit_form.cleaned_data['text']

            Post.objects.select_for_update().filter(id=id).update(title=edit_form_title, text=edit_form_text)

            instance = get_object_or_404(Post, id=id)
            return render(request, "post_detail.html", {"instance": instance,
                                                        "edit_form": edit_form
                                                        })

    return render(request, "post_detail.html", {"instance": instance,
                                                "name_of_logged_in_user": name_of_logged_in_user,
                                                "title_value": title_value,
                                                "text_value": text_value
                                                })


def index_nav(request):
    if request.method == 'POST':
        form1 = RegistrationForm(request.POST or None)
        print form1.errors
        if form1.is_valid():
            form_name = form1.cleaned_data.get("first_name")
            form_surname = form1.cleaned_data.get("last_name")
            form_email = form1.cleaned_data.get("email")
            form_b_day = form1.cleaned_data.get("b_day")
            form_password = form1.cleaned_data.get("password")
            form_gender = form1.cleaned_data.get("gender")
            feedback = SocialUser(name=form_name, surname=form_surname, email=form_email,
                                  b_day=form_b_day, password=form_password, gender=form_gender
                                  )

            user_admin = User.objects.create_user(form_email, form_email, form_password)
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
            print user.is_active
            login(request, user)
            return redirect('/account/profile/%d' %request.user.id)
    else:
        form2 = RegistrationForm()
    return render(request, "login_view.html", {"form2": form2, "form": form1})


def logout_view(request):
    logout(request)
    print request.user.is_active
    return redirect('/')


def change_friends(request, operation, pk):
    new_friend = User.objects.get(pk=pk)
    if operation == "add":
        Friend.make_friend(request.user, new_friend)
    elif operation == "remove":
        Friend.lose_friend(request.user, new_friend)
    return redirect('templates:index')
