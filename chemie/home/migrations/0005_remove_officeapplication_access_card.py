# Generated by Django 2.1.3 on 2019-02-04 16:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_officeapplication_student_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='officeapplication',
            name='access_card',
        ),
    ]
