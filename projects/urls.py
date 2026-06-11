from django.urls import path
from django.views.generic import RedirectView

from projects import views

app_name = "projects"

urlpatterns = [
    path(
        "", RedirectView.as_view(url="/projects/list/", permanent=False), name="index"
    ),
    path("projects/list/", views.ProjectListView.as_view(), name="list"),
    path("projects/create-project/", views.ProjectCreateView.as_view(), name="create"),
    path("projects/<int:pk>/", views.ProjectDetailView.as_view(), name="detail"),
    path("projects/<int:pk>/edit/", views.ProjectUpdateView.as_view(), name="edit"),
    path(
        "projects/<int:pk>/complete/",
        views.ProjectCompleteView.as_view(),
        name="complete",
    ),
    path(
        "projects/<int:pk>/toggle-participate/",
        views.ProjectParticipateView.as_view(),
        name="participate",
    ),
    path(
        "projects/<int:pk>/favorite/",
        views.ProjectFavoriteView.as_view(),
        name="favorite",
    ),
    path("projects/skills/", views.skills_search, name="skills_search"),
    path("projects/<int:pk>/skills/add/", views.skill_add, name="skill_add"),
    path(
        "projects/<int:pk>/skills/<int:skill_id>/remove/",
        views.skill_remove,
        name="skill_remove",
    ),
]
