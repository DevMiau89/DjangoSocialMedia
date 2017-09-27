from __future__ import unicode_literals

from django.db import models

# Create your models here.

class SocialUser(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    city = models.CharField(max_length=255, null=True)
    job = models.CharField(max_length=255, null=True)
    b_day = models.DateField(auto_now=False, auto_now_add=False)
    password = models.CharField(max_length=255)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    created_date = models.DateTimeField(auto_now=False, auto_now_add=True)


    def __unicode__(self):
        return self.name + " " + self.last_name

    def __str__(self):
        return self.name + " " + self.last_name


class Post(models.Model):
    author = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    image = models.ImageField(null=True, blank=True)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now=False, auto_now_add=True)


    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title
