from django.conf.urls import include, url
from django.contrib import admin

from django.views.generic import RedirectView

from . views import (
    index,
    index_nav,
    login_view,
    logout_view,
    post_detail

)


urlpatterns = [
    url(r'^account/$', index, name='account'),
    url(r'^$', index_nav, name='index_nav'),
    url(r'^account/(?P<id>\d+)/$', post_detail),
    url(r'^login_view$', login_view),
    url(r'^logout_view$', logout_view),
]
