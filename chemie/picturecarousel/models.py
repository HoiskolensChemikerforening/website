from django.contrib.auth.models import User
from django.db import models
from sorl.thumbnail import ImageField
from random import shuffle


class ContributionManager(models.Manager):
    def get_all_shuffled(self):
        result = list(self.filter(approved=True))
        shuffle(result)
        return result


class Contribution(models.Model):
    image = ImageField(upload_to='kontorbilder')
    approved = models.BooleanField(default=False)
    author = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)

    objects = ContributionManager()

    def approve(self):
        self.approved = True
        return True
