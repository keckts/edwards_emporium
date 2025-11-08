from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Profile

# Common styling for all inputs

BASE_INPUT_STYLE = "input input-bordered border border-gray-300 w-full bg-white text-black placeholder-gray-500"


class EmailSignupForm(UserCreationForm):
    """Custom signup form using email instead of username."""

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": BASE_INPUT_STYLE,
                "placeholder": "Email address",
                "autofocus": True,
            }
        ),
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": BASE_INPUT_STYLE,
                "placeholder": "Password",
            }
        ),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "class": BASE_INPUT_STYLE,
                "placeholder": "Confirm password",
            }
        ),
    )

    class Meta:
        model = User
        fields = ["email", "password1", "password2"]

    def clean_email(self):
        """Validate that email is unique."""
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email

    def save(self, commit=True):
        """Save user with email as username."""
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.username = self.cleaned_data["email"]  # Use email as username
        if commit:
            user.save()
        return user


class EmailLoginForm(forms.Form):
    """Custom login form using email instead of username."""

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": BASE_INPUT_STYLE,
                "placeholder": "Email address",
                "autofocus": True,
            }
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": BASE_INPUT_STYLE,
                "placeholder": "Password",
            }
        ),
    )


class ProfileForm(forms.ModelForm):
    """Form for editing profile information."""

    first_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "input input-bordered w-full",
                "placeholder": "First name",
            }
        ),
    )
    last_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "input input-bordered w-full",
                "placeholder": "Last name",
            }
        ),
    )

    class Meta:
        model = Profile
        fields = ["bio", "location", "birth_date"]
        widgets = {
            "bio": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered w-full",
                    "placeholder": "Tell us about yourself...",
                    "rows": 4,
                }
            ),
            "location": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "City, Country",
                }
            ),
            "birth_date": forms.DateInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "type": "date",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields["first_name"].initial = self.instance.user.first_name
            self.fields["last_name"].initial = self.instance.user.last_name

    def save(self, commit=True):
        profile = super().save(commit=False)

        # Update user fields (but not email, which is read-only)
        profile.user.first_name = self.cleaned_data["first_name"]
        profile.user.last_name = self.cleaned_data["last_name"]

        if commit:
            profile.user.save()
            profile.save()

        return profile
