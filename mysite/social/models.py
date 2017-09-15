from __future__ import unicode_literals

from django.db import models

# Create your models here.

class SocialUser(models.Model):
    name = models.CharField(max_length=40)
    surname = models.CharField(max_length=40)
    email = models.EmailField(max_length=80)
    city = models.CharField(max_length=40)
    job = models.CharField(max_length=40)
    bday = models.DateField(auto_now=False, auto_now_add=False)
    password = models.CharField(max_length=80)
    gender = models.CharField(max_length=25)
    created_date = models.DateTimeField(auto_now=False, auto_now_add=True)


    def __unicode__(self):
        return self.name + " " + self.last_name

    def __str__(self):
        return self.name + " " + self.last_name
