from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    phone_regex = RegexValidator(regex=r'\d{9,10}$',message='Phone number in format 9999999999. Upto 10 digits')

    is_customer = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    phone = models.CharField(validators=[phone_regex],max_length=10,null = False,unique=True)
