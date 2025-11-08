# Configuration Guide

This document provides a quick reference for all configurable options in this Django boilerplate.

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Core Settings](#core-settings)
- [Database Options](#database-options)
- [Email Configuration](#email-configuration)
- [Authentication Settings](#authentication-settings)
- [Session Management](#session-management)
- [URL Configuration](#url-configuration)
- [Security Settings](#security-settings)
- [Third-Party Services](#third-party-services)

## Quick Start

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your preferred settings

3. Restart the development server to apply changes

## Core Settings

| Variable | Default | Description | Options |
|----------|---------|-------------|---------|
| `PROJECT_NAME` | `hcot` | Project name displayed throughout the app | Any string |
| `SECRET_KEY` | *(required)* | Django secret key for cryptographic signing | Generate with Django |
| `DEBUG` | `True` | Enable/disable debug mode | `True`, `False` |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Comma-separated list of allowed hosts | Domain names |

**Example:**
```env
PROJECT_NAME=MyAwesomeProject
SECRET_KEY=django-insecure-example-key-change-this
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,example.com
```

## Database Options

### SQLite (Default)

Perfect for development. No configuration needed!

```env
DATABASE_ENGINE=sqlite3
```

### PostgreSQL (Recommended for Production)

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_ENGINE` | `sqlite3` | Database engine to use |
| `DATABASE_NAME` | `hcot_db` | PostgreSQL database name |
| `DATABASE_USER` | `postgres` | PostgreSQL username |
| `DATABASE_PASSWORD` | *(required)* | PostgreSQL password |
| `DATABASE_HOST` | `localhost` | Database server host |
| `DATABASE_PORT` | `5432` | Database server port |
| `DATABASE_CONNECT_TIMEOUT` | `10` | Connection timeout (seconds) |

**Example:**
```env
DATABASE_ENGINE=postgresql
DATABASE_NAME=myproject_db
DATABASE_USER=myuser
DATABASE_PASSWORD=securepassword123
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

## Email Configuration

### SMTP Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `EMAIL_HOST` | `smtp.gmail.com` | SMTP server hostname |
| `EMAIL_PORT` | `587` | SMTP server port |
| `EMAIL_USE_TLS` | `True` | Use TLS encryption |
| `EMAIL_HOST_USER` | *(required for production)* | SMTP username/email |
| `EMAIL_HOST_PASSWORD` | *(required for production)* | SMTP password/app password |
| `DEFAULT_FROM_EMAIL` | `noreply@localhost` | Default "from" email address |
| `SERVER_EMAIL` | `noreply@localhost` | Server error email address |

**Note:** In `DEBUG=True` mode, emails are printed to the console—no SMTP configuration needed!

### Email Verification Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `EMAIL_VERIFICATION_CODE_EXPIRY` | `10` | How long codes are valid (minutes) |
| `EMAIL_VERIFICATION_COOLDOWN` | `60` | Time between code requests (seconds) |

**Example:**
```env
# Gmail Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=myapp@gmail.com
EMAIL_HOST_PASSWORD=app-specific-password-here
DEFAULT_FROM_EMAIL=noreply@myproject.com

# Verification Settings
EMAIL_VERIFICATION_CODE_EXPIRY=15
EMAIL_VERIFICATION_COOLDOWN=90
```

## Authentication Settings

| Variable | Default | Description | Options |
|----------|---------|-------------|---------|
| `ACCOUNT_AUTHENTICATION_METHOD` | `email` | How users log in | `email`, `username`, `username_email` |
| `ACCOUNT_USERNAME_REQUIRED` | `False` | Require username during signup | `True`, `False` |
| `ACCOUNT_EMAIL_VERIFICATION` | `mandatory` | Email verification requirement | `none`, `optional`, `mandatory` |
| `ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION` | `True` | Auto-login after verification | `True`, `False` |
| `ACCOUNT_UNIQUE_EMAIL` | `True` | Enforce unique emails | `True`, `False` |
| `ACCOUNT_SESSION_REMEMBER` | `True` | Remember user sessions | `True`, `False` |

**Examples:**

**Username-based authentication:**
```env
ACCOUNT_AUTHENTICATION_METHOD=username
ACCOUNT_USERNAME_REQUIRED=True
ACCOUNT_EMAIL_VERIFICATION=optional
```

**Email with optional verification:**
```env
ACCOUNT_AUTHENTICATION_METHOD=email
ACCOUNT_EMAIL_VERIFICATION=optional
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION=False
```

**Strict email verification:**
```env
ACCOUNT_AUTHENTICATION_METHOD=email
ACCOUNT_EMAIL_VERIFICATION=mandatory
ACCOUNT_UNIQUE_EMAIL=True
```

## Session Management

| Variable | Default | Description |
|----------|---------|-------------|
| `SESSION_COOKIE_AGE` | `1209600` | Session duration in seconds (2 weeks) |
| `SESSION_EXPIRE_AT_BROWSER_CLOSE` | `False` | Expire session when browser closes |
| `SESSION_COOKIE_HTTPONLY` | `True` | HTTP-only cookies (security) |

**Examples:**

**30-day sessions:**
```env
SESSION_COOKIE_AGE=2592000
SESSION_EXPIRE_AT_BROWSER_CLOSE=False
```

**Expire on browser close:**
```env
SESSION_EXPIRE_AT_BROWSER_CLOSE=True
```

## URL Configuration

Customize where users are redirected after authentication actions:

| Variable | Default | Description |
|----------|---------|-------------|
| `LOGIN_URL` | `/auth/login/` | Login page URL |
| `LOGIN_REDIRECT_URL` | `/dashboard/` | Where to go after login |
| `LOGOUT_REDIRECT_URL` | `/` | Where to go after logout |
| `ACCOUNT_SIGNUP_REDIRECT_URL` | `/dashboard/` | Where to go after signup |
| `ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL` | `/dashboard/` | Logged-in user email confirmation |
| `ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL` | `/auth/login/` | Anonymous user email confirmation |

**Example:**
```env
LOGIN_URL=/login/
LOGIN_REDIRECT_URL=/home/
LOGOUT_REDIRECT_URL=/goodbye/
ACCOUNT_SIGNUP_REDIRECT_URL=/welcome/
```

## Google OAuth (Optional)

| Variable | Default | Description |
|----------|---------|-------------|
| `GOOGLE_CLIENT_ID` | *(empty)* | Google OAuth client ID |
| `GOOGLE_CLIENT_SECRET` | *(empty)* | Google OAuth client secret |
| `GOOGLE_OAUTH_SCOPES` | `profile,email` | OAuth scopes (comma-separated) |
| `GOOGLE_OAUTH_ACCESS_TYPE` | `online` | Access type |

Get credentials at: [Google Cloud Console](https://console.cloud.google.com/apis/credentials)

**Example:**
```env
GOOGLE_CLIENT_ID=123456789-abcdefg.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-abcdefghijklmnop
GOOGLE_OAUTH_SCOPES=profile,email,openid
GOOGLE_OAUTH_ACCESS_TYPE=offline
```

## Security Settings

### Password Validation

| Variable | Default | Description |
|----------|---------|-------------|
| `PASSWORD_MIN_LENGTH` | `8` | Minimum password length |
| `PASSWORD_REQUIRE_NUMERIC` | `True` | Require numbers in password |

### Production Security (Uncomment for Production)

```env
# HTTPS Settings
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# Security Headers
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
SECURE_CONTENT_TYPE_NOSNIFF=True
SECURE_BROWSER_XSS_FILTER=True
X_FRAME_OPTIONS=DENY
```

## Third-Party Services

### Sentry (Error Tracking)

```env
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project-id
```

### AWS S3 (Static/Media Files)

```env
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=us-east-1
```

### Redis (Caching)

```env
REDIS_URL=redis://localhost:6379/0
```

## Common Configuration Scenarios

### Development Setup

```env
PROJECT_NAME=MyProject
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_ENGINE=sqlite3
ACCOUNT_EMAIL_VERIFICATION=optional
```

### Production Setup

```env
PROJECT_NAME=MyProject
DEBUG=False
ALLOWED_HOSTS=example.com,www.example.com
DATABASE_ENGINE=postgresql
DATABASE_NAME=production_db
DATABASE_USER=produser
DATABASE_PASSWORD=strongpassword
EMAIL_HOST=smtp.sendgrid.net
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-api-key
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### Testing Setup

```env
PROJECT_NAME=MyProject-Test
DEBUG=True
DATABASE_ENGINE=sqlite3
ACCOUNT_EMAIL_VERIFICATION=none
EMAIL_VERIFICATION_COOLDOWN=0
```

## Tips & Best Practices

1. **Keep Secrets Safe**: Never commit `.env` to version control
2. **Use Different Keys**: Generate unique `SECRET_KEY` for each environment
3. **Start Simple**: Use SQLite and console email backend for development
4. **Test Changes**: Restart the dev server after modifying `.env`
5. **Document Custom Settings**: Add comments for team members
6. **Backup Production**: Always backup `.env` before changes

## Troubleshooting

**Settings not updating?**
- Restart the Django development server
- Check for typos in variable names
- Verify `.env` is in the project root

**Database connection errors?**
- Verify database credentials
- Ensure PostgreSQL is running (if using PostgreSQL)
- Check `DATABASE_ENGINE` matches your setup

**Email not sending?**
- In development, check console output (DEBUG=True)
- For production, verify SMTP credentials
- Check firewall/security group settings

**Authentication issues?**
- Verify `ACCOUNT_EMAIL_VERIFICATION` setting
- Check redirect URLs are correct
- Ensure `ALLOWED_HOSTS` includes your domain

---

For more details, see:
- `.env.example` - Complete configuration template with inline documentation
- `README.md` - Full project documentation
- [Django Documentation](https://docs.djangoproject.com/)
