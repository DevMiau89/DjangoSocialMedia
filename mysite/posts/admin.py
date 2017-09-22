# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Post

# Register your models here.
class PostModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'published_date', 'created_date']
    list_display_links = ['published_date']
    list_filter = ['created_date', 'published_date']
    list_editable = ['title']
    search_fields = ['title', "text"]

    class Meta:
        model = Post


admin.site.register(Post, PostModelAdmin)
