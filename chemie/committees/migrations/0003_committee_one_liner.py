# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-10 23:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('committees', '0002_auto_20161201_2213'),
    ]

    operations = [
        migrations.AddField(
            model_name='committee',
            name='one_liner',
            field=models.CharField(default='lol', max_length=30, verbose_name='Lynbeskrivelse'),
            preserve_default=False,
        ),
    ]