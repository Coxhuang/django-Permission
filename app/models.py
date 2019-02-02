from django.db import models
from django.contrib.auth.models import AbstractUser



class UserProfile(AbstractUser):
    Role = models.CharField(max_length=16, default="00001")


