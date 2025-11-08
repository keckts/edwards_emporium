from django.contrib.auth.views import LogoutView
from django.urls import include, path

from .views import (DeleteAccountView, LoginView, ResendVerificationEmailView,
                    SettingsView, SignupView, VerifyEmailCodeView)

app_name = "users"

urlpatterns = [
    # Authentication
    path("login/", LoginView.as_view(), name="login"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("logout/", LogoutView.as_view(next_page="index"), name="logout"),
    # Profile Management
    path("settings/", SettingsView.as_view(), name="settings"),
    path("delete-account/", DeleteAccountView.as_view(), name="delete_account"),
    # Email Verification
    path(
        "resend-verification/",
        ResendVerificationEmailView.as_view(),
        name="resend_verification",
    ),
    path(
        "verify-email-code/",
        VerifyEmailCodeView.as_view(),
        name="verify_email_code",
    ),
    # Password Management (Django Allauth)
    # Note: Both "change password" and "reset password" use the same functionality
    # - "change password" = logged-in users changing their password
    # - "reset password" = forgot password flow via email
    path("password/", include("allauth.account.urls")),
]
