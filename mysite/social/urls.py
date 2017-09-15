from django.conf.urls import url
from django.contrib import admin


from . views import (
    index,
    index_nav,

)


urlpatterns = [
    url(r'^$', index),
    url(r'^nav/$', index_nav),
]
