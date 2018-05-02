# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-01-27 08:49
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fundsapplication',
            name='bank_account_id',
            field=models.BigIntegerField(validators=[django.core.validators.RegexValidator(code='nomatch', message='Kun tall, 11 siffer', regex='^(\\d{10}|\\d{11})$')], verbose_name='Kontonummer'),
        ),
    ]
