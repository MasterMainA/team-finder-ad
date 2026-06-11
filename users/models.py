from django.contrib.auth.models import AbstractUser
from django.db import models

from team_finder.constants import (MAX_USER_ABOUT_LENGTH, MAX_USER_NAME_LENGTH,
                                   MAX_USER_PHONE_LENGTH,
                                   MAX_USER_SURNAME_LENGTH)


class User(AbstractUser):
    name = models.CharField(
        max_length=MAX_USER_NAME_LENGTH, blank=True, verbose_name="Имя"
    )
    surname = models.CharField(
        max_length=MAX_USER_SURNAME_LENGTH, blank=True, verbose_name="Фамилия"
    )
    avatar = models.ImageField(
        upload_to="avatars/", null=True, blank=True, verbose_name="Аватар"
    )
    about = models.TextField(
        max_length=MAX_USER_ABOUT_LENGTH, blank=True, verbose_name="О себе"
    )
    phone = models.CharField(
        max_length=MAX_USER_PHONE_LENGTH, blank=True, verbose_name="Телефон"
    )
    github_url = models.URLField(blank=True, verbose_name="Ссылка на GitHub")

    def save(self, *args, **kwargs):
        if self.email and not self.username:
            self.username = self.email
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} {self.surname} ({self.email})"
