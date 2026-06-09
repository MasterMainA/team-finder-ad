from django.conf import settings
from django.db import models


class Skill(models.Model):

    name = models.CharField(max_length=50, unique=True, verbose_name="Название навыка")

    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Project(models.Model):

    STATUS_CHOICES = [
        ("open", "Открыт"),
        ("closed", "Закрыт"),
    ]

    title = models.CharField(max_length=255, verbose_name="Название проекта")
    description = models.TextField(verbose_name="Описание проекта", blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="projects",
        verbose_name="Автор проекта",
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="open",
        verbose_name="Текущий статус",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")

    skills = models.ManyToManyField(
        Skill, blank=True, related_name="projects", verbose_name="Необходимые навыки"
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="joined_projects",
        verbose_name="Участники проекта",
    )
    favorites = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="favorite_projects",
        verbose_name="Добавили в избранное",
    )

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title