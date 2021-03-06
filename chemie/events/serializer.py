from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Social,
    Bedpres,
    SocialEventRegistration,
    BedpresRegistration,
)

from chemie.customprofile.serializers import UserSerializer
from chemie.committees.serializers import CommitteeSerializer


class SocialSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    committee = CommitteeSerializer()
    attendees = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Social
        fields = "__all__"


class SocialEventRegistrationSerializer(serializers.ModelSerializer):
    event = SocialSerializer()
    user = UserSerializer()

    class Meta:
        model = SocialEventRegistration
        fields = "__all__"


class BedpresSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    attendees = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Bedpres
        fields = "__all__"


class BedpresRegistrationSerializer(serializers.ModelSerializer):
    event = BedpresSerializer()
    user = UserSerializer()

    class Meta:
        model = BedpresRegistration
        fields = "__all__"
