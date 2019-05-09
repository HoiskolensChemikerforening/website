from django.db import models
from push_notifications.models import APNSDevice, GCMDevice
import datetime
from django.db.models.signals import pre_delete
from django.contrib.auth.models import User

HC_ICON = "https://chemie.no/static/favicons/android-chrome-192x192.png"

class CoffeeSubmission(models.Model):
    """ Submission that's created each time a notification is send """

    date = models.DateTimeField(default=datetime.datetime.now)

    @classmethod
    def check_last_submission(cls):
        """ Make sure that the send_notification is not activated too frequently """
        if cls.objects.count() == 0:
            return True

        # Checks if fifteen minutes have passed since last CoffeSubmission object was created
        fifteen_minutes = datetime.timedelta(0, 900)
        if CoffeeSubmission.objects.filter(
            date__gte=datetime.datetime.now() - fifteen_minutes
        ).exists():
            return False
        return True


class Device(models.Model):
    """ Overall model which saves gcm/apns device and the users subsciption settings """

    owner = models.ForeignKey(
        User, verbose_name="eier", on_delete=models.CASCADE
    )
    gcm_device = models.ForeignKey(
        GCMDevice,
        blank=True,
        null=True,
        related_name="Device",
        on_delete=models.DO_NOTHING,
        verbose_name="Tredje parts api for android telefoner",
    )
    """
    The commented lines below is the implementation for Safari browser
    Apples APNS certificat would be needed, cost ~1000 NOK/year
    The code has not been testet so no garanties it would work
    """
    # apns_device = models.ForeignKey(
    #   APNSDevice,
    #   blank=True,
    #   null=True,
    #   related_name="Device",
    #   on_delete=models.DO_NOTHING,
    #   verbose_name="Tredje parts api for android telefoner"
    # )
    coffee_subscription = models.BooleanField(
        default=True, verbose_name="Aboner på kaffe pushvsler"
    )

    """Hvis det er ønskelig kan feltet under brukes senere"""
    # news_subscription = models.BooleanField(default=True)

    date_created = models.DateTimeField(auto_now_add=True)

    def send_notification(self, title, message):
        """" Send notification to gcm_device """
        if self.gcm_device is not None:
            self.gcm_device.send_message(
                message, extra={"title": title, "icon": HC_ICON}
            )

        """
        The commented lines below is the implementation for Safari browser
        Apples APNS certificat would be needed, cost ~1000 NOK/year
        The code has not been testet so no garanties it would work
        """
        # if self.apns_device is not None:
        #     self.apns_device.send_message(
        #         message, extra={"title": title, "icon": HC_ICON}
        #     )

    @property
    def is_active(self):
        if self.gcm_device is not None:
            return self.gcm_device.active

        """
        The commented lines below is the implementation for Safari browser
        Apples APNS certificat would be needed, cost ~1000 NOK/year
        The code has not been testet so no garanties it would work
        """
        # if self.apns_device is not None:
        #     return self.apns_device.active


def delete_device_signal(sender, instance, **kwargs):
    """ Deletes gcm_device when deleting Device """
    if instance.gcm_device is not None:
        instance.gcm_device.delete()
    """
    The commented lines below is the implementation for Safari browser
    Apples APNS certificat would be needed, cost ~1000 NOK/year
    The code has not been testet so no garanties it would work
    """
    # if instance.apns_device is not None:
    #     instance.apns_device.delete()



# Connects delete_device_signal with the pre_delete signal reciever
pre_delete.connect(delete_device_signal, sender=Device)

