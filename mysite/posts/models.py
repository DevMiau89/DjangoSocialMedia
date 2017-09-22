# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=100)
    image = models.ImageField(null=True, blank=True)
    text = models.TextField()
    created_date = models.DateTimeField( auto_now=False, auto_now_add=True)
    published_date = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title
