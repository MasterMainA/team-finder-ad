from django import forms

from .models import Project
from team_finder import utils


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description", "github_url", "status"]

    def clean_github_url(self):
        github_url = self.cleaned_data.get("github_url")
        return utils.validate_github_url(github_url)