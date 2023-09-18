from django.contrib.auth.models import AbstractUser
from django.db import models


class Account(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        default='avatars/default_avatar.png'
    )

    SEX_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    date_of_birth = models.DateField(null=True, blank=True)
    sex = models.CharField(
        max_length=1, choices=SEX_CHOICES, blank=True, null=True)
