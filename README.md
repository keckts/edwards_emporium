# Edwards Emporium


Extra guides can be found in the guides directory if needed.

## ✨ Features

- 🔐 **Email-Based Authentication** - Modern signup/login with email instead of username
- ✉️ **Email Verification System** - 6-digit code verification with beautiful modal interface
- 👤 **User Profile Management** - Complete profile editing with bio, location, and birth date
- 🎨 **Beautiful UI** - TailwindCSS + DaisyUI for stunning, responsive design
- ⚡ **HTMX Integration** - Dynamic, modern interactions without writing JavaScript
- 🎭 **Django Cotton** - Component-based templating for cleaner code
- 🌓 **Dark Mode** - Built-in dark mode toggle that persists across sessions
- 🔒 **Security First** - CSRF protection, secure password handling, rate limiting
- 📱 **Fully Responsive** - Works beautifully on all devices
- 🗑️ **Account Management** - Delete account functionality with confirmation modals
- ⚙️ **Settings Page** - Comprehensive user settings with profile editing
- 📊 **Dashboard** - Beautiful user dashboard with stats and quick actions
- 🎯 **Highly Configurable** - Extensive .env customization without code changes
- 🗄️ **Dual Database Support** - Easy switch between SQLite and PostgreSQL

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Node.js and npm (for TailwindCSS) - Download from [https://nodejs.org/](https://nodejs.org/)
- Git (optional, for cloning)

### Installation

1. **Clone or download the repository**

```bash
git clone https://github.com/keckts/hcot
cd hcot
```

2. **Create and activate a virtual environment**

```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Rename the project (IMPORTANT)**

Run the included rename script to customize the project name:

```bash
python rename_project.py yourprojectname
```

This will automatically:
- Rename the project directory
- Update all file references
- Update HTML templates
- Update configuration files

5. **Set up the database**

```bash
python manage.py migrate
```

6. **Create a superuser**

```bash
python manage.py createsuperuser
```

7. **Install Node.js dependencies and build TailwindCSS**

**Prerequisites:** Make sure you have Node.js and npm installed. Download from [https://nodejs.org/](https://nodejs.org/) if needed.

```bash
# Navigate to theme static source directory
cd theme/static_src

# Install npm dependencies (TailwindCSS v4, DaisyUI, PostCSS)
npm install

# Build CSS for production (one-time build)
npm run build

# OR run in development mode with watch (recommended during development)
# This will automatically rebuild CSS when you change templates or styles
npm run dev
```

**Note:** If you run `npm run dev`, keep this terminal running. It will watch for changes and rebuild your CSS automatically.

8. **Run the development server**

```bash
# Open a new terminal and navigate back to project root
cd ../..

# Run the Django development server
python manage.py runserver
```

**Tip:** During development, keep both terminals running:
- Terminal 1: `npm run dev` (in `theme/static_src/` directory)
- Terminal 2: `python manage.py runserver` (in project root)

9. **Open your browser**

Navigate to `http://127.0.0.1:8000/` and start building!

## 📁 Project Structure

```
yourprojectname/
├── core/                   # Core app (homepage, dashboard)
├── users/                  # User authentication & profiles
│   ├── templates/
│   │   └── users/
│   │       ├── login.html
│   │       ├── signup.html
│   │       └── settings.html
│   ├── forms.py           # Email-based auth forms
│   ├── models.py          # User Profile model
│   └── views.py           # Authentication views
├── theme/                  # Theme and base templates
│   ├── static/css/dist/   # Compiled CSS output
│   ├── static_src/        # TailwindCSS source files
│   │   ├── src/styles.css # Main Tailwind/DaisyUI config
│   │   └── package.json   # npm dependencies
│   └── templates/
│       └── theme/
│           └── base.html  # Base template with sidebar
├── yourprojectname/       # Project settings
│   ├── settings.py
│   └── urls.py
├── manage.py
├── rename_project.py      # Project renaming script
└── requirements.txt
```

## 🎨 Customization

### Changing the Project Name

Use the included rename script:

```bash
python rename_project.py mynewproject
```

### Customizing Styles

1. Edit `theme/static_src/src/styles.css` for global styles and Tailwind configuration
2. Configure DaisyUI themes and plugins directly in `styles.css` using `@config` directive
3. Use TailwindCSS utility classes directly in templates
4. After making changes, CSS will rebuild automatically if `npm run dev` is running
5. For production, run `npm run build` from the `theme/static_src/` directory

### Adding New Features

1. Create new Django apps: `python manage.py startapp myapp`
2. Add app to `INSTALLED_APPS` in settings
3. Create models, views, and templates
4. Add URL patterns

## 🔧 Configuration

### Environment Variables

This boilerplate is **highly customizable** through environment variables. All configuration is done via the `.env` file, making it easy to adapt the project to your needs without touching the code.

#### Quick Setup

1. **Copy the example file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` and customize your settings:**
   ```bash
   nano .env  # or use your favorite editor (i use neovim btw)
   ```

3. **Key settings to update:**
   - `PROJECT_NAME` - Your project name (appears in templates, emails)
   - `SECRET_KEY` - Generate with: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
   - `DEBUG` - Set to `False` for production
   - `ALLOWED_HOSTS` - Your domain names (comma-separated)

#### Complete Configuration Reference

The `.env.example` file includes comprehensive documentation for all available settings. Here's an overview:

##### 🏗️ Core Settings
```env
PROJECT_NAME=myproject               # Project name used throughout the app
SECRET_KEY=your-secret-key          # Django secret key (keep secure!)
DEBUG=True                          # Debug mode (False for production)
ALLOWED_HOSTS=localhost,127.0.0.1  # Allowed hosts (comma-separated)
```

##### 🗄️ Database Configuration
```env
DATABASE_ENGINE=sqlite3             # sqlite3 or postgresql
# PostgreSQL settings (when DATABASE_ENGINE=postgresql)
DATABASE_NAME=myproject_db
DATABASE_USER=myuser
DATABASE_PASSWORD=mypassword
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

##### 📧 Email Configuration
```env
# SMTP Settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# Email Verification Settings
EMAIL_VERIFICATION_CODE_EXPIRY=10   # Code expiry in minutes
EMAIL_VERIFICATION_COOLDOWN=60      # Cooldown between requests in seconds
```

##### 🔐 Authentication Settings
```env
ACCOUNT_AUTHENTICATION_METHOD=email  # email, username, or username_email
ACCOUNT_USERNAME_REQUIRED=False      # Require username during signup
ACCOUNT_EMAIL_VERIFICATION=mandatory # none, optional, or mandatory
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION=True
ACCOUNT_UNIQUE_EMAIL=True
ACCOUNT_SESSION_REMEMBER=True
```

##### 🔒 Session Configuration
```env
SESSION_COOKIE_AGE=1209600           # 2 weeks in seconds
SESSION_EXPIRE_AT_BROWSER_CLOSE=False
SESSION_COOKIE_HTTPONLY=True
```

##### 🌐 Google OAuth (Optional)
```env
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_OAUTH_SCOPES=profile,email
GOOGLE_OAUTH_ACCESS_TYPE=online
```

##### 🔗 URL Configuration
```env
LOGIN_URL=/auth/login/
LOGIN_REDIRECT_URL=/dashboard/
LOGOUT_REDIRECT_URL=/
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL=/dashboard/
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL=/auth/login/
ACCOUNT_SIGNUP_REDIRECT_URL=/dashboard/
```

##### 🔑 Password Validation
```env
PASSWORD_MIN_LENGTH=8                # Minimum password length
PASSWORD_REQUIRE_NUMERIC=True        # Require numeric characters
```

##### 🎨 Styling Configuration
```env
TAILWIND_APP_NAME=theme              # Tailwind CSS app name
```

##### 🛡️ Security Settings (Production)
```env
# Uncomment these for production:
# SECURE_SSL_REDIRECT=True
# SESSION_COOKIE_SECURE=True
# CSRF_COOKIE_SECURE=True
# SECURE_HSTS_SECONDS=31536000
```

##### 📊 Third-Party Integrations (Optional)
```env
# Sentry Error Tracking
# SENTRY_DSN=your-sentry-dsn

# AWS S3 Storage
# AWS_ACCESS_KEY_ID=your-access-key
# AWS_SECRET_ACCESS_KEY=your-secret-key
# AWS_STORAGE_BUCKET_NAME=your-bucket

# Redis Cache
# REDIS_URL=redis://localhost:6379/0
```

#### Environment-Specific Configurations

**Development (.env):**
```env
PROJECT_NAME=myproject
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_ENGINE=sqlite3
EMAIL_VERIFICATION_CODE_EXPIRY=10
```

**Production (.env):**
```env
PROJECT_NAME=MyProject
DEBUG=False
ALLOWED_HOSTS=example.com,www.example.com
DATABASE_ENGINE=postgresql
DATABASE_NAME=production_db
# ... other production settings
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
```

#### 📝 Important Notes

- ⚠️ **Never commit your `.env` file** to version control
- ✅ `.env.example` is safe to commit (contains no secrets)
- 🔒 Keep `SECRET_KEY` secure and unique per environment
- 📧 In DEBUG mode, emails print to console (no SMTP needed)
- 🔄 After changing settings, restart the development server
- 💾 Changes to some settings may require migrations

#### 🎯 Customization Examples

**Change project name everywhere:**
```env
PROJECT_NAME=MyAwesomeProject
```
This updates the name in templates, emails, and the UI.

**Adjust email verification timing:**
```env
EMAIL_VERIFICATION_CODE_EXPIRY=5    # Codes expire in 5 minutes
EMAIL_VERIFICATION_COOLDOWN=30      # Can resend after 30 seconds
```

**Switch authentication methods:**
```env
ACCOUNT_AUTHENTICATION_METHOD=username_email  # Allow both
ACCOUNT_USERNAME_REQUIRED=True
```

**Disable email verification:**
```env
ACCOUNT_EMAIL_VERIFICATION=none
```

### Database Configuration

The project supports both **SQLite** (default) and **PostgreSQL** databases. You can switch between them without changing any Python code—just edit your `.env` file!

#### Option 1: SQLite (Default - Development)

SQLite is perfect for development and comes pre-configured. No additional setup needed!

**Advantages:**
- ✅ Zero configuration
- ✅ No installation required
- ✅ Perfect for development and testing
- ✅ Database stored as a single file (`db.sqlite3`)

**Usage:**
```env
# In your .env file (or leave it out entirely - it's the default)
DATABASE_ENGINE=sqlite3
```

#### Option 2: PostgreSQL (Recommended for Production)

PostgreSQL is a powerful, production-ready database with better performance and features for production environments.

**Prerequisites:**
1. Install PostgreSQL: [https://www.postgresql.org/download/](https://www.postgresql.org/download/)
2. Install the Python PostgreSQL driver:
   ```bash
   pip install psycopg2-binary
   ```

**Setup Steps:**

1. **Create the PostgreSQL database and user**

   Open PostgreSQL terminal (psql):
   ```bash
   # macOS/Linux
   psql -U postgres

   # Windows
   # Use pgAdmin or psql from the Start Menu
   ```

   Run these SQL commands:
   ```sql
   CREATE DATABASE hcot_db;
   CREATE USER hcot_user WITH PASSWORD 'your_secure_password';
   GRANT ALL PRIVILEGES ON DATABASE hcot_db TO hcot_user;
   ALTER DATABASE hcot_db OWNER TO hcot_user;
   \q
   ```

2. **Configure your `.env` file**

   Update your `.env` file with your PostgreSQL credentials:
   ```env
   # Database Configuration
   DATABASE_ENGINE=postgresql

   # PostgreSQL Settings
   DATABASE_NAME=hcot_db
   DATABASE_USER=hcot_user
   DATABASE_PASSWORD=your_secure_password
   DATABASE_HOST=localhost
   DATABASE_PORT=5432
   DATABASE_CONNECT_TIMEOUT=10
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

**Connection Options:**

The configuration includes several PostgreSQL-specific options:

- `DATABASE_NAME`: Name of your database (default: `hcot_db`)
- `DATABASE_USER`: PostgreSQL username (default: `postgres`)
- `DATABASE_PASSWORD`: User password (required for PostgreSQL)
- `DATABASE_HOST`: Database server address (default: `localhost`)
- `DATABASE_PORT`: PostgreSQL port (default: `5432`)
- `DATABASE_CONNECT_TIMEOUT`: Connection timeout in seconds (default: `10`)

**Switching Between Databases:**

You can easily switch between SQLite and PostgreSQL by changing one line in your `.env` file:

```env
# Use SQLite (development)
DATABASE_ENGINE=sqlite3

# Use PostgreSQL (production)
DATABASE_ENGINE=postgresql
```

**Important Notes:**
- ⚠️ Switching databases requires running migrations again
- ⚠️ Data is NOT automatically transferred between databases
- ⚠️ Make sure to backup your database before switching
- 💡 Use SQLite for development, PostgreSQL for production

### Email Backend (Optional)

Configure email settings in `settings.py` for:
- Password reset
- Email notifications
- User verification

### Social Authentication (Optional)

The boilerplate includes Google OAuth setup. Configure in `settings.py`:

1. Get OAuth credentials from Google Cloud Console
2. Add to `SOCIALACCOUNT_PROVIDERS` in settings
3. Update templates as needed

## 📝 Key Features Explained

### Email-Based Authentication

Users sign up and log in with email addresses instead of usernames. The system automatically uses email as the username internally for Django compatibility.

### Profile Management

Each user has an associated Profile model with:
- Bio
- Location
- Birth date
- Automatically created on user signup

### Dark Mode

Dark mode preference is stored in localStorage and persists across sessions. Toggle available in settings page.

### Settings Page

Comprehensive settings interface with:
- Profile editing
- Account information display
- Dark mode toggle
- Logout functionality
- Account deletion (with confirmation)

## 🛠️ Development

### Running Tests

```bash
python manage.py test
```

### Creating Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Collecting Static Files (Production)

```bash
python manage.py collectstatic
```

## 📦 Dependencies

Key packages included:
- **Django 5.1.3** - Web framework
- **django-tailwind** - TailwindCSS integration
- **django-cotton** - Component-based templates
- **django-allauth** - Authentication & social auth
- **python-dotenv** - Environment variable management

See `requirements.txt` for complete list.

## 🤝 Contributing

Feel free to fork this project and customize it for your needs. If you make improvements, consider sharing them back!

## 📄 License

This project is provided as-is for use as a boilerplate template.

## 👨‍💻 Author

Created by **Henry Sheffield**

## 🙏 Acknowledgments

- Django community
- TailwindCSS team
- DaisyUI creators
- HTMX developers
- Django Cotton project

## 💡 Tips

1. **Always use the virtual environment** - Activate it before running any Python commands
2. **Keep TailwindCSS watch running** - Run `npm run dev` in `theme/static_src/` during development for instant CSS updates
3. **Customize early** - Run the rename script before making changes
4. **Check migrations** - Run `makemigrations` and `migrate` after model changes
5. **Use the admin panel** - Access at `/admin` for easy data management
6. **Two terminals for development** - One for `npm run dev`, another for `python manage.py runserver`

## 🆘 Troubleshooting

### TailwindCSS not loading or updating
- Make sure you've run `npm install` in the `theme/static_src/` directory
- Run `npm run build` to generate the CSS file
- During development, run `npm run dev` to watch for changes
- Check that you're editing `theme/static_src/src/styles.css`, not the compiled output
- Verify the compiled CSS exists at `theme/static/css/dist/styles.css`
- Check browser console for 404 errors on CSS file

### Database errors
- **SQLite**: Delete `db.sqlite3` and run migrations again
- **PostgreSQL**: Check credentials in `.env` file
- **PostgreSQL**: Verify database exists: `psql -U postgres -l`
- **PostgreSQL**: Ensure `psycopg2-binary` is installed: `pip install psycopg2-binary`
- Check that all migrations are applied: `python manage.py showmigrations`
- Test database connection: `python manage.py dbshell`

### Import errors
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

### Static files not loading
- Run `python manage.py collectstatic`
- Check `STATIC_URL` and `STATIC_ROOT` in settings

---

**Happy coding!** 🚀
