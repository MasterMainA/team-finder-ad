from django.contrib.auth import login, logout
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, DetailView, UpdateView, ListView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView, PasswordChangeView
from .forms import UserRegistrationForm, UserLoginForm, UserProfileChangeForm
from .models import CustomUser
from django.views import View

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

class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('projects:list')

class UserListView(ListView):
    model = CustomUser
    template_name = 'users/participants.html'
    context_object_name = 'users'
    paginate_by = 12

    def get_queryset(self):
        return CustomUser.objects.all().order_by('-date_joined')

class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_url = reverse_lazy('users:login')

class UserProfileView(DetailView):
    model = CustomUser
    template_name = 'users/user-details.html'
    context_object_name = 'profile_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        context['projects'] = user.projects.all().order_by('-created_at')
        context['participating_projects'] = user.joined_projects.exclude(author=user).order_by('-created_at')
        context['favorite_projects'] = user.favorite_projects.all().order_by('-created_at')
        return context

class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UserProfileChangeForm
    template_name = 'users/edit_profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('users:profile', kwargs={'pk': self.request.user.pk})