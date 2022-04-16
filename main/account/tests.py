from django.test import TestCase
from .models import CustomUser

class UserTestCase(TestCase):
    def setUp(self):
        CustomUser.objects.create(
            username="Client1",password
        )