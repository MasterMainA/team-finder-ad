from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    name = models.CharField(max_length=150, blank=True, verbose_name="Имя")
    surname = models.CharField(max_length=150, blank=True, verbose_name="Фамилия")
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, default='images/default-avatar.png')
    about = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    github_url = models.URLField(blank=True)

    def save(self, *args, **kwargs):
        if self.email and not self.username:
            self.username = self.email
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} {self.surname} ({self.email})"