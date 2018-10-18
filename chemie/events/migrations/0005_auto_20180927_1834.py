# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-27 16:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('committees', '0003_auto_20180127_0949'),
        ('events', '0004_auto_20180208_1547'),
    ]

    operations = [
        migrations.AddField(
            model_name='social',
            name='committee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='committees.Committee'),
        ),
        migrations.AlterField(
            model_name='bedpres',
            name='sluts',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Antall plasser, sett til 0 for åpent arrangement'),
        ),
        migrations.AlterField(
            model_name='social',
            name='sluts',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Antall plasser, sett til 0 for åpent arrangement'),
        ),
    ]
