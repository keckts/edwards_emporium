import random
from datetime import timedelta

from allauth.account.models import EmailAddress, EmailConfirmationHMAC
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import FormView, UpdateView, View

from .forms import EmailLoginForm, EmailSignupForm, ProfileForm
from .models import Profile

User = get_user_model()


# ---------------------------
#   Shared Mixins
# ---------------------------


class RedirectAuthenticatedUserMixin:
    """Redirect authenticated users away from login/signup pages."""

    redirect_url = reverse_lazy("dashboard")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.redirect_url)
        return super().dispatch(request, *args, **kwargs)


# ---------------------------
#   Auth Views
# ---------------------------


class SignupView(RedirectAuthenticatedUserMixin, SuccessMessageMixin, FormView):
    """User signup view with email-based authentication."""

    template_name = "users/signup.html"
    form_class = EmailSignupForm
    success_url = reverse_lazy("dashboard")
    success_message = "Welcome! Your account has been created."

    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend="django.contrib.auth.backends.ModelBackend")
        return super().form_valid(form)


class LoginView(RedirectAuthenticatedUserMixin, FormView):
    """User login view with email-based authentication."""

    template_name = "users/login.html"
    form_class = EmailLoginForm
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(self.request, user)
            return super().form_valid(form)

        messages.error(self.request, "Invalid email or password.")
        return self.form_invalid(form)


class CustomLogoutView(SuccessMessageMixin, LogoutView):
    next_page = reverse_lazy("index")
    success_message = "You have been logged out successfully."


# ---------------------------
#   Profile / Settings
# ---------------------------


class SettingsView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """User settings and profile editing view."""

    model = Profile
    form_class = ProfileForm
    template_name = "users/settings.html"
    success_url = reverse_lazy("users:settings")
    success_message = "Your profile has been updated successfully!"

    def get_object(self, queryset=None):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile

    def dispatch(self, request, *args, **kwargs):
        # clear old messages (optional)
        list(messages.get_messages(request))
        return super().dispatch(request, *args, **kwargs)


# ---------------------------
#   Account Deletion
# ---------------------------


class DeleteAccountView(LoginRequiredMixin, View):
    """Account deletion view."""

    success_url = reverse_lazy("index")

    def post(self, request, *args, **kwargs):
        user = request.user
        email = user.email

        logout(request)
        user.delete()

        messages.success(request, f"Account '{email}' has been permanently deleted.")
        return redirect(self.success_url)


# ---------------------------
#   Email Verification
# ---------------------------


class ResendVerificationEmailView(LoginRequiredMixin, View):
    """
    Send 6-digit verification code via email with rate limiting.

    Security features:
    - Rate limiting: cooldown between requests (configurable via .env)
    - User authentication required
    - Only sends if email is unverified
    - 6-digit code stored in session with expiry (configurable via .env)
    - CSRF protection enabled
    """

    # Get settings from Django settings (which reads from .env)
    from django.conf import settings

    COOLDOWN_SECONDS = settings.EMAIL_VERIFICATION_COOLDOWN
    CODE_EXPIRY_MINUTES = settings.EMAIL_VERIFICATION_CODE_EXPIRY
    success_url = reverse_lazy("users:settings")

    def post(self, request, *args, **kwargs):
        """Handle POST request to send verification code."""
        user = request.user

        # Get or create user's primary email address
        try:
            email_address = EmailAddress.objects.get(user=user, primary=True)
        except EmailAddress.DoesNotExist:
            # Create EmailAddress record if it doesn't exist
            email_address = EmailAddress.objects.create(
                user=user,
                email=user.email,
                primary=True,
                verified=False
            )

        # Check if email is already verified
        if email_address.verified:
            return JsonResponse(
                {"success": False, "message": "Your email is already verified."},
                status=400,
            )

        # Rate limiting: Check cooldown period
        last_sent_key = f"email_verification_sent_{user.id}"
        last_sent = request.session.get(last_sent_key)

        if last_sent:
            last_sent_time = timezone.datetime.fromisoformat(last_sent)
            time_since_last = timezone.now() - last_sent_time
            cooldown_remaining = (
                timedelta(seconds=self.COOLDOWN_SECONDS) - time_since_last
            )

            if cooldown_remaining.total_seconds() > 0:
                seconds_remaining = int(cooldown_remaining.total_seconds())
                return JsonResponse(
                    {
                        "success": False,
                        "message": f"Please wait {seconds_remaining} seconds before requesting another code.",
                    },
                    status=429,
                )

        # Generate 6-digit verification code
        verification_code = str(random.randint(100000, 999999))

        # Store code in session with timestamp
        code_key = f"email_verification_code_{user.id}"
        code_timestamp_key = f"email_verification_code_timestamp_{user.id}"
        request.session[code_key] = verification_code
        request.session[code_timestamp_key] = timezone.now().isoformat()

        # Send verification email
        try:
            # Render HTML email template
            html_message = render_to_string(
                "users/email/verification_code_email.html",
                {
                    "user": user,
                    "verification_code": verification_code,
                    "expiry_minutes": self.CODE_EXPIRY_MINUTES,
                },
            )

            # Send email
            send_mail(
                subject="Email Verification Code",
                message=f"Your verification code is: {verification_code}",
                from_email=None,  # Uses DEFAULT_FROM_EMAIL
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=False,
            )

            # Store timestamp for rate limiting
            request.session[last_sent_key] = timezone.now().isoformat()

            return JsonResponse(
                {
                    "success": True,
                    "message": "Verification code has been sent to your email!",
                }
            )

        except Exception as e:
            # Log error in production (don't expose details to user)
            return JsonResponse(
                {
                    "success": False,
                    "message": "Failed to send verification email. Please try again later.",
                },
                status=500,
            )


class VerifyEmailCodeView(LoginRequiredMixin, View):
    """
    Verify the 6-digit email verification code.
    """

    # Get settings from Django settings (which reads from .env)
    from django.conf import settings

    CODE_EXPIRY_MINUTES = settings.EMAIL_VERIFICATION_CODE_EXPIRY

    def post(self, request, *args, **kwargs):
        """Handle POST request to verify code."""
        user = request.user
        submitted_code = request.POST.get("code", "").strip()

        # Get stored code from session
        code_key = f"email_verification_code_{user.id}"
        code_timestamp_key = f"email_verification_code_timestamp_{user.id}"

        stored_code = request.session.get(code_key)
        code_timestamp = request.session.get(code_timestamp_key)

        # Check if code exists
        if not stored_code or not code_timestamp:
            return JsonResponse(
                {
                    "success": False,
                    "message": "No verification code found. Please request a new one.",
                },
                status=400,
            )

        # Check if code has expired
        code_time = timezone.datetime.fromisoformat(code_timestamp)
        time_elapsed = timezone.now() - code_time
        if time_elapsed > timedelta(minutes=self.CODE_EXPIRY_MINUTES):
            # Clear expired code
            del request.session[code_key]
            del request.session[code_timestamp_key]
            return JsonResponse(
                {
                    "success": False,
                    "message": "Verification code has expired. Please request a new one.",
                },
                status=400,
            )

        # Verify code
        if submitted_code != stored_code:
            return JsonResponse(
                {"success": False, "message": "Invalid verification code. Please try again."},
                status=400,
            )

        # Code is valid - mark email as verified
        try:
            email_address = EmailAddress.objects.get(user=user, primary=True)
        except EmailAddress.DoesNotExist:
            # Create EmailAddress record if it doesn't exist
            email_address = EmailAddress.objects.create(
                user=user,
                email=user.email,
                primary=True,
                verified=False
            )

        email_address.verified = True
        email_address.save()

        # Clear verification code from session
        del request.session[code_key]
        del request.session[code_timestamp_key]
        if f"email_verification_sent_{user.id}" in request.session:
            del request.session[f"email_verification_sent_{user.id}"]

        return JsonResponse(
            {"success": True, "message": "Email verified successfully!"}
        )
