from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    pass


class QuyChe(models.Model):
    ten = models.CharField(max_length=255, null=False)
    diemTong = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.ten