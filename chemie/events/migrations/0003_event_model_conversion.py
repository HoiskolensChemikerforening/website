# -*- coding: utf-8 -*-
# Generated by Carl
from __future__ import unicode_literals

from django.db import migrations


def convert_old_event_to_social_event(app, schema_editor):
    try:
        OldEvent = app.get_model('events', 'Event')
        OldEventRegistration = app.get_model('events', 'EventRegistration')
        NewSocialEvent = app.get_model('events', 'Social')
        NewSocialEventRegistration = app.get_model('events', 'SocialEventRegistration')

    except LookupError:
        print("Old model is no longer installed")
        return

    previous_events = OldEvent.objects.all()

    new_events = []
    new_registrations = []
    for old_event in previous_events:
        new_events.append(
            NewSocialEvent(
                # From base class
                id=old_event.id,
                title=old_event.title,
                date=old_event.date,
                created=old_event.created,
                edited=old_event.edited,
                register_startdate=old_event.register_startdate,
                register_deadline=old_event.register_deadline,
                deregister_deadline=old_event.deregister_deadline,
                location=old_event.location,
                description=old_event.description,
                image=old_event.image,
                sluts=old_event.sluts,
                allowed_grades=[1, 2, 3, 4, 5, 6],

                # From Social event class
                author=old_event.author,
                payment_information=old_event.payment_information,
                price_member=old_event.price_member,
                price_not_member=old_event.price_not_member,
                price_companion=old_event.price_companion,
                companion=old_event.companion,
                sleepover=old_event.sleepover,
                night_snack=old_event.night_snack,
            )
        )

    NewSocialEvent.objects.bulk_create(new_events)

    for old_event in previous_events:
        old_attendees = OldEventRegistration.objects.filter(event=old_event)
        new_event = NewSocialEvent.objects.get(pk=old_event.pk)
        for old_attendee in old_attendees:
            new_registrations.append(
                NewSocialEventRegistration(event=new_event,
                                           user=old_attendee.user,
                                           created=old_attendee.created,
                                           edited=old_attendee.edited,
                                           status=old_attendee.status,
                                           arrival_status=1,
                                           payment_status=old_attendee.payment_status,
                                           sleepover=old_attendee.sleepover,
                                           night_snack=old_attendee.night_snack,
                                           companion=old_attendee.companion)
            )

    NewSocialEventRegistration.objects.bulk_create(new_registrations)


class Migration(migrations.Migration):
    operations = [
        migrations.RunPython(convert_old_event_to_social_event, migrations.RunPython.noop),
    ]
    dependencies = [
        ('events', '0002_auto_20180130_1645'),
    ]
