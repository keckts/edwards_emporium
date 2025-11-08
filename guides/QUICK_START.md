# Quick Start Guide

## 🚀 Get Started in 5 Minutes

This project is now fully configured with authentication! Follow these steps to get everything running.

## Prerequisites

- Python 3.13+
- Node.js and npm (for Tailwind CSS)

## Setup Steps

### 1. Configure Google OAuth (Optional but Recommended)

Add your Google OAuth credentials to `.env`:

```bash
# Open .env and add your credentials:
GOOGLE_CLIENT_ID=your-google-client-id-here.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret-here
```

**Don't have Google OAuth keys?** See [AUTHENTICATION_SETUP.md](AUTHENTICATION_SETUP.md) for detailed instructions.

**Or skip Google OAuth** - The email/password authentication will still work!

### 2. Configure Site Domain

Run this in the Django shell:

```bash
python manage.py shell
```

Then paste this:

```python
from django.contrib.sites.models import Site
site = Site.objects.get(id=1)
site.domain = 'localhost:8000'
site.name = 'HCOT'
site.save()
exit()
```

### 3. Start the Development Server

```bash
python manage.py runserver
```

### 4. In a New Terminal: Start Tailwind CSS Watcher

```bash
cd theme/static_src
npm run dev
```

## 🎉 You're All Set!

Visit http://localhost:8000

### What You Can Do Now:

- **Browse Components** - Visit `/` to see all Django Cotton components
- **Sign Up** - Click signup and create an account (email or Google)
- **Login** - Sign in with your credentials
- **View Dashboard** - Authenticated users see their personal dashboard

## URL Guide

| URL | What It Does |
|-----|--------------|
| `http://localhost:8000/` | Homepage with component demos |
| `http://localhost:8000/auth/login/` | Login page |
| `http://localhost:8000/auth/signup/` | Signup page |
| `http://localhost:8000/dashboard/` | User dashboard (auth required) |
| `http://localhost:8000/admin/` | Django admin |

## Authentication Flow

### For Non-Authenticated Users:
1. Visit `/` → See component showcase
2. Click any auth button → Redirected to login/signup
3. Sign up/login → Redirected to `/dashboard/`

### For Authenticated Users:
1. Visit `/` → Auto-redirected to `/dashboard/`
2. Browse dashboard with personalized content
3. Click logout → Redirected back to `/`

## Troubleshooting

### Styling Not Showing?
```bash
# Make sure Tailwind watcher is running:
cd theme/static_src
npm run dev
```

### Google OAuth Not Working?
- Check your credentials in `.env`
- Make sure you configured the Site domain (step 2)
- See [AUTHENTICATION_SETUP.md](AUTHENTICATION_SETUP.md) for detailed setup

### Other Issues?
```bash
# Check for errors:
python manage.py check

# View migrations:
python manage.py showmigrations

# Restart everything:
# 1. Kill both terminals (Ctrl+C)
# 2. Run migrations: python manage.py migrate
# 3. Start server: python manage.py runserver
# 4. Start Tailwind: cd theme/static_src && npm run dev
```

## What's Included?

✅ **Complete Authentication System**
- Email/Password signup & login
- Google OAuth integration
- Password reset functionality
- User dashboard

✅ **9 Beautiful Django Cotton Components**
- Card, Alert, Badge, Modal
- Navbar, Input, Accordion
- Gradient Button, Loading Button (HTMX)

✅ **Modern Tech Stack**
- Django 5.2.7
- django-allauth for authentication
- Tailwind CSS 4.x for styling
- Alpine.js for interactivity
- HTMX for dynamic content

✅ **Professional Code Structure**
- Clean separation of concerns
- Environment-based configuration
- Reusable component library
- Comprehensive documentation

## Next Steps

1. **Customize Components** - Edit files in `templates/cotton/`
2. **Style Your App** - Modify Tailwind classes
3. **Add Features** - Build on the authentication system
4. **Deploy** - Follow production checklist in [AUTHENTICATION_SETUP.md](AUTHENTICATION_SETUP.md)

## File Structure

```
hcot/
├── users/              # Authentication app
├── core/               # Main app with component demos
├── components/         # ViewComponent examples
├── templates/cotton/   # Reusable Cotton components
├── theme/              # Tailwind CSS configuration
├── .env                # Your environment variables
├── AUTHENTICATION_SETUP.md  # Detailed auth guide
└── QUICK_START.md      # This file
```

## Need Help?

- **Component Docs:** `templates/cotton/COMPONENTS.md`
- **Auth Setup:** `AUTHENTICATION_SETUP.md`
- **Django Allauth:** https://django-allauth.readthedocs.io/
- **Django Cotton:** https://django-cotton.com/

---

**Enjoy building! 🎨🚀**
