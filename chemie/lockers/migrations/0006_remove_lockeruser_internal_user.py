# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-31 20:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lockers', '0005_ownership_is_confirmed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lockeruser',
            name='internal_user',
        ),
    ]
