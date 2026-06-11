from django.contrib import admin

from projects.models import Project, Skill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("name", "description")
    filter_horizontal = ("skills", "participants", "favorites")
