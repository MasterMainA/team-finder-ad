from django.urls import path
from .views import ProjectListView, ProjectDetailView, ProjectCreateView, ProjectUpdateView

app_name = 'projects'

urlpatterns = [
    path('', ProjectListView.as_view(), name='list'),
    path('projects/create-project/', ProjectCreateView.as_view(), name='create'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='detail'),
    path('projects/<int:pk>/edit/', ProjectUpdateView.as_view(), name='edit'),
]