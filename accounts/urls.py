from django.urls import path
from django.contrib.auth.views import LoginView
from .views import profile, edit_profile, signup, custom_logout

app_name = "accounts"

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("profile/", profile, name="profile"),
    path("profile/edit/", edit_profile, name="edit-profile"),

    # Secure POST logout
    path("logout/", custom_logout, name="logout"),

    # Login page
    path("login/", LoginView.as_view(
        template_name="accounts/login.html",
        redirect_authenticated_user=True
    ), name="login"),
]
