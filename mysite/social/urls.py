from django.conf.urls import include, url
from django.contrib import admin


from . views import (
    index,
    index_nav,

)


urlpatterns = [
    url(r'^$', index),
    url(r'^index_nav/$', index_nav, name="nav"),

]
