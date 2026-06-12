from django.conf import settings
from django.db import models

from team_finder.constants import (
    MAX_PROJECT_DESCRIPTION_LENGTH,
    MAX_PROJECT_NAME_LENGTH,
    MAX_SKILL_NAME_LENGTH,
    PROJECT_STATUS_CHOICES,
    PROJECT_STATUS_OPEN,
)


class Skill(models.Model):
    name = models.CharField(
        max_length=MAX_SKILL_NAME_LENGTH, unique=True, verbose_name="Название навыка"
    )

    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(
        max_length=MAX_PROJECT_NAME_LENGTH, verbose_name="Название проекта"
    )
    description = models.TextField(
        max_length=MAX_PROJECT_DESCRIPTION_LENGTH,
        verbose_name="Описание проекта",
        blank=True,
    )
    github_url = models.URLField(blank=True, verbose_name="Ссылка на GitHub")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_projects",
        verbose_name="Автор проекта",
    )
    status = models.CharField(
        max_length=10,
        choices=PROJECT_STATUS_CHOICES,
        default=PROJECT_STATUS_OPEN,
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
        return self.name
