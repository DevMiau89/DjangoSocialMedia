from django.contrib.auth.models import User
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from django.forms.models import inlineformset_factory
from .forms import RegistrationForm, LoginForm, PostForm, UserForm, CommentForm
from .models import SocialUser, Post, Friend, UserProfile, Comment
from django.core.exceptions import PermissionDenied

User = get_user_model()


# Create your views here.
@login_required()
def index(request, id=None):
    my_current_user = SocialUser.objects.filter(email=request.user.email).first()
    name_of_logged_in_user = my_current_user.name
    posts = Post.objects.filter(author=request.user.id).all().order_by('-created_date')
    friend = Friend.objects.filter(current_user=request.user).first()
    users = User.objects.exclude(id=request.user.id)
    updated_user = User.objects.filter(email=request.user.email).first()
    updated_user2 = UserProfile.objects.filter(user_id=request.user.id).first()
    user_id = request.user.id
    comment_form = CommentForm()
    if request.method == 'POST':
        post_form = PostForm(request.POST or None)
        print post_form.errors
        if post_form.is_valid():
            form_title = post_form.cleaned_data['title']
            form_text = post_form.cleaned_data['text']

            feedback = Post(title=form_title, text=form_text, author=request.user)
            feedback.save()
            posts = Post.objects.filter(author=request.user.id).all().order_by('-created_date')

            if friend:
                users = User.objects.exclude(id=request.user.id)
                friends = friend.users.all()
            return render(request, "index.html", {"form": post_form,
                                                  "title": form_title,
                                                  "text": form_text,
                                                  "posts": posts,
                                                  "my_current_user": my_current_user,
                                                  "name_of_logged_in_user": name_of_logged_in_user,
                                                  "friends": friends,
                                                  "users": users,
                                                  "user_id": user_id,
                                                  "updated_user": updated_user,
                                                  "updated_user2": updated_user2,
                                                  "comment_form": comment_form
                                                  })

    if friend:
        users = User.objects.exclude(id=request.user.id)
        friends = friend.users.all()

        return render(request, 'index.html', {"posts": posts,
                                              "my_current_user": my_current_user,
                                              "name_of_logged_in_user": name_of_logged_in_user,
                                              "friends": friends,
                                              "users": users,
                                              "user_id": user_id,
                                              "updated_user": updated_user,
                                              "updated_user2": updated_user2,
                                              "comment_form": comment_form
                                              })

    return render(request, 'index.html', {"posts": posts,
                                          "my_current_user": my_current_user,
                                          "name_of_logged_in_user": name_of_logged_in_user,
                                          "users": users,
                                          "user_id": user_id,
                                          "updated_user": updated_user,
                                          "updated_user2": updated_user2,
                                          "comment_form": comment_form
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
            print user.is_active, "yolo"
            login(request, user)
            return redirect('/account/profile/%d' % request.user.id)
    else:
        form2 = RegistrationForm()
    return render(request, "login_view.html", {"form2": form2, "form": form1})


def logout_view(request):
    logout(request)
    print request.user.is_active
    return redirect('/')


def change_friends(request, operation, pk):
    friend = User.objects.get(pk=pk)
    if operation == "add":
        Friend.make_friend(request.user, friend)
    elif operation == "remove":
        Friend.lose_friend(request.user, friend)
    return redirect('/account/profile/%d' % request.user.id)


@login_required()
def edit_user(request, id):
    user = User.objects.get(id=id)
    my_current_user = SocialUser.objects.filter(email=request.user.email).first()
    updated_user2 = UserProfile.objects.filter(user_id=request.user.id).first()
    updated_user = User.objects.filter(email=request.user.email).first()
    user_form = UserForm(instance=user)

    ProfileInlineFormset = inlineformset_factory(User, UserProfile, fields=('photo', 'city', 'interests', 'job'))
    formset = ProfileInlineFormset(instance=user)

    if request.user.is_authenticated() and request.user.id == user.id:
        if request.method == 'POST':
            user_form = UserForm(request.POST, instance=user)
            formset = ProfileInlineFormset(request.POST, request.FILES, instance=user)
            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                formset = ProfileInlineFormset(request.POST, request.FILES, instance=created_user)
                if formset.is_valid():
                    print created_user
                    created_user.save()
                    formset.save()
                    return redirect('/account/profile/%d' % request.user.id)

            return render(request, 'edit_profile.html', {
                "noodle": id,
                "noodle_form": user_form,
                "formset": formset,
                "updated_user2": updated_user2,
                "my_current_user": my_current_user,
                "updated_user":updated_user
            })
            # else:
            #     raise PermissionDenied

    return render(request, "edit_profile.html", {
        "noodle": id,
        "noodle_form": user_form,
        "formset": formset,
        "updated_user2": updated_user2,
        "my_current_user": my_current_user,
        "updated_user": updated_user
    })


def create_comment(request):
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_body = comment_form.cleaned_data.get("body")
            post_title = comment_form.cleaned_data.get("post")
            post = Post.objects.filter(title=post_title).first()
            profile_id = UserProfile.objects.filter(user_id=request.user.id).first()
            comment_feedback = Comment(body=comment_body, post_id=post.id, user_id=request.user.id, profile_id=profile_id.id)
            comment_feedback.save()
            return redirect('/account/profile/%d' % request.user.id)
    return render(request, 'index.html', {"comment_form": comment_form})


def friend_profile(request, id):
    friend_id = id
    updated_user2 = UserProfile.objects.filter(user_id=friend_id).first()
    posts = Post.objects.filter(author=friend_id).all().order_by('-created_date')
    updated_user = User.objects.filter(id=friend_id).first()
    user_email = SocialUser.objects.filter(email=updated_user.email).first()
    current_user = UserProfile.objects.filter(user_id=request.user.id).first()
    friend = Friend.objects.filter(current_user=request.user).first()
    users = User.objects.exclude(id=friend_id)
    friends = friend.users.all()


    return render(request, 'friend_profile.html', {"updated_user2": updated_user2,
                                                   "posts": posts,
                                                   "updated_user": updated_user,
                                                   "user_email": user_email,
                                                   "friends": friends,
                                                   "users": users,
                                                   "current_user": current_user
                                                   })
