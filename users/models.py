from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):

    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True,
        default='images/default-avatar.png',
        verbose_name='Аватар'
    )
    bio = models.TextField(
        verbose_name='О себе',
        blank=True
    )
    phone = models.CharField(
        max_length=20,
        verbose_name='Телефон',
        blank=True
    )
    github = models.URLField(
        verbose_name='GitHub',
        blank=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"