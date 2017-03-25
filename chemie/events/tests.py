import os

from django.contrib.auth.models import User
from django.core.files import File
from django.test import TestCase
from django.utils import timezone

from chemie import settings
from events.models import Event, EventRegistration


# Create your tests here.


class TestEventAndRegistration(TestCase):
    # Fetch all templates for sending mail
    fixtures = ['fixtures/email-templates.json']

    def setUp(self):
        user = User.objects.create(username='glenny')
        date = timezone.now() + timezone.timedelta(days=5)
        start_date = timezone.now()
        reg_deadline = timezone.now() + timezone.timedelta(days=1)
        dereg_deadline = timezone.now() + timezone.timedelta(days=2)
        image_path = os.path.join(settings.BASE_DIR, 'media/events/blank_person.png')
        image = File(image_path)
        Event.objects.create(title='Indok er helt ok',
                             author=user,
                             date=date,
                             register_startdate=start_date,
                             register_deadline=reg_deadline,
                             deregister_deadline=dereg_deadline,
                             location='Samfundet',
                             description='Litta fest',
                             image=image,
                             sluts=40,
                             payment_information='Alle maa benytte Vipps til aa betale',
                             )

    def test_event_registration_exceeding_max_slots(self):
        event = Event.objects.get(title='Indok er helt ok')
        for i in range(event.sluts + 5):
            user = User.objects.create(username=i,
                                       email='test@mail.com',
                                       )
            registration = EventRegistration(event=event,
                                             user=user,
                                             )
            registration.save()
            # Bumping all users on wait list by
            # calling overridden save function
            event.save()
        self.assertEqual(event.waiting_users(), 5)
        self.assertEqual(event.registered_users(), event.sluts)
