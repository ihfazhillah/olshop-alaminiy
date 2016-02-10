from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
from profil.models import Profil, Phone, Email
from profil.serializers import ProfilSerializer
from django.contrib.auth.models import User

