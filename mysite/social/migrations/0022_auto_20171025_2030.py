# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-25 18:30
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('social', '0021_userinterests'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinterests',
            name='user',
        ),
        migrations.RemoveField(
            model_name='interests',
            name='user_interests',
        ),
        migrations.AddField(
            model_name='interests',
            name='user_interests',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='UserInterests',
        ),
    ]
