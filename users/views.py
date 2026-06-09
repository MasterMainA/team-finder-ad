from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, DetailView, UpdateView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from .forms import UserRegistrationForm, UserLoginForm, UserProfileChangeForm
from .models import CustomUser

class RegisterView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

class UserLoginView(FormView):
    form_class = UserLoginForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('projects:list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('projects:list')

class UserProfileView(DetailView):
    model = CustomUser
    template_name = 'users/user-details.html'
    context_object_name = 'profile_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = self.object.projects.all().order_by('-created_at')
        return context

class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UserProfileChangeForm
    template_name = 'users/edit_profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('users:profile', kwargs={'pk': self.request.user.pk})