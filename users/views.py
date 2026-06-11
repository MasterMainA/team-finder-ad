from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import (CreateView, DetailView, FormView, ListView,
                                  UpdateView)

from team_finder.constants import USERS_LIST_PAGINATION
from users.forms import (UserLoginForm, UserProfileChangeForm,
                         UserRegistrationForm)

User = get_user_model()


class RegisterView(CreateView):
    form_class = UserRegistrationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")


class UserLoginView(FormView):
    form_class = UserLoginForm
    template_name = "users/login.html"
    success_url = reverse_lazy("projects:list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("projects:list")


class UserListView(ListView):
    model = User
    template_name = "users/participants.html"
    context_object_name = "users"
    paginate_by = USERS_LIST_PAGINATION

    def get_queryset(self):
        return User.objects.all().order_by("-date_joined")


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = "users/change_password.html"
    success_url = reverse_lazy("users:login")


class UserProfileView(DetailView):
    model = User
    template_name = "users/user-details.html"
    context_object_name = "profile_user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object

        context["user"] = user
        context["projects"] = user.owned_projects.all().order_by("-created_at")
        context["participating_projects"] = user.joined_projects.exclude(
            owner=user
        ).order_by("-created_at")
        context["favorite_projects"] = user.favorite_projects.all().order_by(
            "-created_at"
        )
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileChangeForm
    template_name = "users/edit_profile.html"

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse("users:profile", kwargs={"pk": self.request.user.pk})
