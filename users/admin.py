from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (
            "Дополнительная информация",
            {"fields": ("name", "surname", "avatar", "about", "phone", "github_url")},
        ),
    )

    list_display = ("username", "email", "name", "surname", "is_staff", "is_active")
    search_fields = ("username", "email", "name", "surname", "phone")
    list_filter = ("is_staff", "is_superuser", "is_active")
