from django.conf.urls import include, url
from django.contrib import admin

from django.views.generic import RedirectView

from . views import (
    index,
    index_nav,
    login_view,
    logout_view,
    post_detail,
    change_friends,
    edit_user

)


urlpatterns = [
    url(r'^account/profile/(?P<id>\d+)$', index, name='account'),
    url(r'^$', index_nav, name='index_nav'),
    url(r'^account/article/(?P<id>\d+)/$', post_detail),
    url(r'^connect/(?P<operation>.+)/(?P<pk>\d+)/$', change_friends, name="change_friends"),
    url(r'^account/profile/update/(?P<id>\d+)/$', edit_user, name='account_update'),
    url(r'^login_view$', login_view),
    url(r'^logout_view$', logout_view),
]
