from django.db import models

from ckeditor.fields import RichTextField
from sorl.thumbnail import ImageField
from chemie.committees.models import Committee
from django.core.validators import MaxValueValidator, MinValueValidator


class Landlord(models.Model):  # Utleier aka promokom/ac
    committee = models.ForeignKey(Committee, on_delete=models.CASCADE)

    def __str__(self):
        return self.committee.title


class RentalObjectType(models.Model):
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.type


class Invoice(models.Model):
    # rentedObjects = models.ForeignKey(rentedObjects, on_delete=models.CASCADE)
    client = models.CharField(max_length=100, verbose_name="Kunde")
    client_mail = models.EmailField(max_length=254, verbose_name="E-post")
    client_nr = models.CharField(max_length=15, verbose_name="Telefon nr.")
    paid = models.BooleanField(default=False, verbose_name="Betalt?")
    event = models.CharField(max_length=100, verbose_name="Arrangement")


class RentalObject(models.Model):
    name = models.CharField(max_length=100)
    description = RichTextField(verbose_name="Beskrivelse", config_name="news")
    image = ImageField(upload_to="rentalservice", verbose_name="Bilde")
    owner = models.ForeignKey(
        Landlord, null=True, blank=True, on_delete=models.CASCADE
    )
    price = models.FloatField(
        validators=[MinValueValidator(0.0)],
        null=True,
        blank=True,
        verbose_name="Pris",
    )  # Trenger min og maks verdi
    type = models.ForeignKey(
        RentalObjectType, null=True, blank=True, on_delete=models.CASCADE
    )
    quantity = models.IntegerField(
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        verbose_name="Antall",
    )

    def __str__(self):
        return self.name + str(self.id)


class RentedObjects(models.Model):
    rentalObject = models.ForeignKey(
        RentalObject, null=True, blank=True, on_delete=models.CASCADE
    )
    quantity = models.IntegerField(
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        verbose_name="Antall",
    )
    rent_start = models.DateTimeField(verbose_name="Utleiestart")
    rent_end = models.DateTimeField(verbose_name="Utleieslutt")
    invoice = models.ForeignKey(
        Invoice,
        null=True,
        blank=True,
        verbose_name="Kontrakt",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.quantity) + "x " + self.rentalObject.name
