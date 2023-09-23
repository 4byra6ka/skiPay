from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

NULLABLE = {'blank': True, 'null': True}
phone_validator = RegexValidator(
    r"^(\+?\d{0,4})?\s?-?\s?(\(?\d{3}\)?)\s?-?\s?(\(?\d{3}\)?)\s?-?\s?(\(?\d{4}\)?)?$",
    "Указанный номер не подходит по формату +7хххххххххх"
)


class User(AbstractUser):
    username = None
    email = None
    phone = models.CharField(max_length=16, validators=[phone_validator], unique=True)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['first_name', 'last_name']
