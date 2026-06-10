from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from team_finder.utils import generate_avatar_from_initials, validate_github_url

User = get_user_model()


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label="Пароль", widget=forms.PasswordInput(), validators=[validate_password]
    )

    class Meta:
        model = User
        fields = ["name", "surname", "email", "password"]
        labels = {
            "name": "Имя",
            "surname": "Фамилия",
            "email": "Email",
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()
            if not user.avatar:
                generate_avatar_from_initials(user)
        return user


class UserLoginForm(forms.Form):
    email = forms.EmailField(label="Электронная почта", widget=forms.EmailInput())
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            from django.contrib.auth import authenticate

            self._cached_user = authenticate(self.request, username=email, password=password)
            if self._cached_user is None:
                raise forms.ValidationError("Неверная почта или пароль")
        return cleaned_data

    def get_user(self):
        return self._cached_user


class UserProfileChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["name", "surname", "avatar", "about", "phone", "github_url"]
        widgets = {
            "avatar": forms.FileInput(),
        }

    def clean_github_url(self):
        github_url = self.cleaned_data.get("github_url")
        return validate_github_url(github_url)