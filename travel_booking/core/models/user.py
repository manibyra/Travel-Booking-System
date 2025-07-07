from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    aadhaar = models.CharField(max_length=12)
    address = models.TextField()

    def __str__(self):
        return self.username
