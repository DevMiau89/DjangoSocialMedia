# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
def post_list(request):
    return render(request, "post_form.html", {})


def post_create(request):
    return render(request, "post_form.html", {})


def post_detail(request):
    return render(request, "post_form.html", {})


def post_update(request):
    return render(request, "post_form.html", {})


def post_delete(request):
    return render(request, "post_form.html", {})

