from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            "Дополнительная информация",
            {"fields": ("name", "surname", "avatar", "about", "phone", "github_url")},
        ),
    )
