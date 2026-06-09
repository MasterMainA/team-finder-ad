from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from .forms import CustomUserCreationForm, CustomAuthenticationForm

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

class UserLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'users/login.html'

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('projects:list')