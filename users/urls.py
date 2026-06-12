from django.urls import path

from users.views import (
    ProfileEditView,
    RegisterView,
    UserListView,
    UserLoginView,
    UserLogoutView,
    UserPasswordChangeView,
    UserProfileView,
)

app_name = "users"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("list/", UserListView.as_view(), name="participants"),
    path("change-password/", UserPasswordChangeView.as_view(), name="change_password"),
    path("edit-profile/", ProfileEditView.as_view(), name="edit_profile"),
    path("<int:pk>/", UserProfileView.as_view(), name="profile"),
]
