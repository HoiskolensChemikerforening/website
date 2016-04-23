# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-09 13:47
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Locker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='LockerUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=40)),
                ('last_name', models.CharField(blank=True, max_length=40)),
                ('username', models.CharField(blank=True, max_length=10)),
                ('created', models.DateField(auto_now_add=True)),
                ('internal_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ownership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(auto_now_add=True)),
                ('edited', models.DateField(auto_now=True)),
                ('activation_code', models.UUIDField(default=uuid.uuid4)),
                ('active', models.BooleanField(default=False)),
                ('locker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lockers.Locker')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lockers.LockerUser')),
            ],
        ),
        migrations.AddField(
            model_name='lockeruser',
            name='ownerships',
            field=models.ManyToManyField(through='lockers.Ownership', to='lockers.Locker'),
        ),
    ]