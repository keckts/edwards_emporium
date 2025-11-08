import os
from pathlib import Path

from decouple import Csv, config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config(
    "SECRET_KEY",
    default="django-insecure-$$ia5f^+iukl3(4ol(sx23%f@l54@jh1az_!e&6pg!c(%!_0nx",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost,127.0.0.1", cast=Csv())


# Application definition

INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",  # Required for allauth
    # styling
    "tailwind",
    "apps.theme",
    "crispy_forms",
    "crispy_bootstrap5",
    "widget_tweaks",
    # apps
    "apps.core",
    "apps.users",
    "apps.antiques",
    "apps.blog",
    "apps.sellers.apps.SellersConfig",
    # third party
    "django_cotton",
    "django_viewcomponent",
    # allauth
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "phonenumber_field",
]

SITE_ID = 1

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",  # Required for allauth
]

ROOT_URLCONF = "apps.edwards_emporium.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],  # global templates
        "APP_DIRS": False,  # must be False if you define loaders
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",  # Required for allauth
                "apps.core.context_processors.global_context",
            ],
            "loaders": [
                (
                    "django.template.loaders.cached.Loader",
                    [
                        "django_cotton.cotton_loader.Loader",
                        "django.template.loaders.filesystem.Loader",
                        "django.template.loaders.app_directories.Loader",
                    ],
                )
            ],
            "builtins": ["django_cotton.templatetags.cotton"],
        },
    },
]

WSGI_APPLICATION = "apps.edwards_emporium.wsgi.application"


# ==============================================================================
# DATABASE CONFIGURATION
# ==============================================================================
# Supports both SQLite (default) and PostgreSQL
# Switch between databases by setting DATABASE_ENGINE in .env
#
# SQLite (default - no configuration needed):
#   - Perfect for development
#   - No additional setup required
#   - Database file: db.sqlite3
#
# PostgreSQL (production recommended):
#   - Set DATABASE_ENGINE=postgresql in .env
#   - Configure DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, etc.
#   - Requires psycopg2-binary: pip install psycopg2-binary
# ==============================================================================

# Get database engine from environment (defaults to sqlite3)
DATABASE_ENGINE = config("DATABASE_ENGINE", default="sqlite3")

if DATABASE_ENGINE == "postgresql":
    # PostgreSQL Configuration
    # Requires: pip install psycopg2-binary
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": config("DATABASE_NAME", default="edwards_emporium_db"),
            "USER": config("DATABASE_USER", default="postgres"),
            "PASSWORD": config("DATABASE_PASSWORD", default=""),
            "HOST": config("DATABASE_HOST", default="localhost"),
            "PORT": config("DATABASE_PORT", default="5432", cast=int),
            # Optional PostgreSQL-specific settings
            "OPTIONS": {
                # Connection timeout in seconds
                "connect_timeout": config(
                    "DATABASE_CONNECT_TIMEOUT", default=10, cast=int
                ),
                # Other options can be added here as needed
                # Example: "sslmode": "require" for SSL connections
            },
        }
    }
else:
    # SQLite Configuration (default)
    # No additional configuration needed
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# ==============================================================================
# PASSWORD VALIDATION
# ==============================================================================
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

PASSWORD_MIN_LENGTH = config("PASSWORD_MIN_LENGTH", default=8, cast=int)
PASSWORD_REQUIRE_NUMERIC = config("PASSWORD_REQUIRE_NUMERIC", default=True, cast=bool)

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": PASSWORD_MIN_LENGTH,
        },
    },
]

# Add numeric password validator if required
if PASSWORD_REQUIRE_NUMERIC:
    AUTH_PASSWORD_VALIDATORS.append(
        {
            "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
        }
    )


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Tailwind CSS Configuration
TAILWIND_APP_NAME = "apps.theme"

if DEBUG:
    # Add django_browser_reload only in DEBUG mode
    INSTALLED_APPS += ["django_browser_reload"]
    MIDDLEWARE += [
        "django_browser_reload.middleware.BrowserReloadMiddleware",
    ]

# ==============================================================================
# AUTHENTICATION SETTINGS
# ==============================================================================

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of allauth
    "django.contrib.auth.backends.ModelBackend",
    # allauth specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
]

# Django Allauth Settings (Updated for latest version)
ACCOUNT_AUTHENTICATION_METHOD = config("ACCOUNT_AUTHENTICATION_METHOD", default="email")
ACCOUNT_LOGIN_METHODS = {ACCOUNT_AUTHENTICATION_METHOD}
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"]
ACCOUNT_USERNAME_REQUIRED = config(
    "ACCOUNT_USERNAME_REQUIRED", default=False, cast=bool
)

# Email Verification Settings
ACCOUNT_EMAIL_VERIFICATION = config(
    "ACCOUNT_EMAIL_VERIFICATION", default="mandatory"
)  # Options: "none", "optional", "mandatory"
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = config(
    "ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION", default=True, cast=bool
)
ACCOUNT_UNIQUE_EMAIL = config("ACCOUNT_UNIQUE_EMAIL", default=True, cast=bool)
ACCOUNT_SESSION_REMEMBER = config("ACCOUNT_SESSION_REMEMBER", default=True, cast=bool)

# Email Verification Code Settings (Custom)
EMAIL_VERIFICATION_CODE_EXPIRY = config(
    "EMAIL_VERIFICATION_CODE_EXPIRY", default=10, cast=int
)  # in minutes
EMAIL_VERIFICATION_COOLDOWN = config(
    "EMAIL_VERIFICATION_COOLDOWN", default=60, cast=int
)  # in seconds

# Prevent login until email is verified
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = config(
    "ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL", default="/dashboard/"
)
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = config(
    "ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL", default="/auth/login/"
)

# Redirect URLs
LOGIN_URL = config("LOGIN_URL", default="/auth/login/")
LOGIN_REDIRECT_URL = config("LOGIN_REDIRECT_URL", default="/dashboard/")
LOGOUT_REDIRECT_URL = config("LOGOUT_REDIRECT_URL", default="/")
ACCOUNT_LOGOUT_REDIRECT_URL = config("ACCOUNT_LOGOUT_REDIRECT_URL", default="/")
ACCOUNT_SIGNUP_REDIRECT_URL = config(
    "ACCOUNT_SIGNUP_REDIRECT_URL", default="/dashboard/"
)

# Google OAuth Settings
GOOGLE_OAUTH_SCOPES = config("GOOGLE_OAUTH_SCOPES", default="profile,email", cast=Csv())
GOOGLE_OAUTH_ACCESS_TYPE = config("GOOGLE_OAUTH_ACCESS_TYPE", default="online")

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": GOOGLE_OAUTH_SCOPES,
        "AUTH_PARAMS": {
            "access_type": GOOGLE_OAUTH_ACCESS_TYPE,
        },
        "APP": {
            "client_id": config("GOOGLE_CLIENT_ID", default=""),
            "secret": config("GOOGLE_CLIENT_SECRET", default=""),
            "key": "",
        },
    }
}

# Social Account Settings
SOCIALACCOUNT_LOGIN_ON_GET = config(
    "SOCIALACCOUNT_LOGIN_ON_GET", default=True, cast=bool
)
SOCIALACCOUNT_AUTO_SIGNUP = config("SOCIALACCOUNT_AUTO_SIGNUP", default=True, cast=bool)
SOCIALACCOUNT_EMAIL_AUTHENTICATION = config(
    "SOCIALACCOUNT_EMAIL_AUTHENTICATION", default=True, cast=bool
)
SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = config(
    "SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT", default=True, cast=bool
)

# ==============================================================================
# EMAIL SETTINGS
# ==============================================================================

# Email backend configuration
# Development: Use console backend (prints emails to console)
# Production: Use SMTP backend with your email service
if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = config("EMAIL_HOST", default="smtp.gmail.com")
    EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
    EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
    EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
    EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
    DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="noreply@example.com")
    SERVER_EMAIL = config("SERVER_EMAIL", default="noreply@example.com")

# Default "from" email for development
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="noreply@localhost")

STATICFILES_DIRS = [
    BASE_DIR / "static",  # your project-level static folder
]

# ==============================================================================
# SESSION CONFIGURATION
# ==============================================================================

# Session cookie age in seconds (default: 1209600 = 2 weeks)
SESSION_COOKIE_AGE = config("SESSION_COOKIE_AGE", default=1209600, cast=int)

# Whether the session should expire when the user closes their browser
SESSION_EXPIRE_AT_BROWSER_CLOSE = config(
    "SESSION_EXPIRE_AT_BROWSER_CLOSE", default=False, cast=bool
)

# Make cookies only accessible via HTTP(S), not JavaScript (recommended)
SESSION_COOKIE_HTTPONLY = config("SESSION_COOKIE_HTTPONLY", default=True, cast=bool)

PROJECT_NAME = config(
    "PROJECT_NAME", default="edwards_emporium"
)  # change to whatever you want, this is mostly used for frontend

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
