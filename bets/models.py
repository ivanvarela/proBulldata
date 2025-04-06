from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .constants import *

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    activo = models.BooleanField(default=True)
    alias = models.CharField(max_length=64, null=False, blank=False)
    first_name = models.CharField(max_length=64, null=True, blank=True)
    last_name = models.CharField(max_length=64, null=True, blank=True)
    celular = models.CharField(max_length=32, null=True, blank=True)
    imagen = models.ImageField(default='default.jpeg', null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)

    status = models.CharField(
        max_length=1,
        null=True,
        blank=True,
        default='B',
        choices=status_choices,
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'