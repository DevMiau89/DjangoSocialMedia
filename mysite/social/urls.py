from django.conf.urls import include, url
from django.contrib import admin

from django.views.generic import RedirectView

from . views import (
    index,
    index_nav,
    login_view,

)


urlpatterns = [
    url(r'^$', index),
    url(r'^index_nav/$', index_nav),
    url(r'^login_view$', login_view),
]
