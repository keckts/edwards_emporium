# Database Configuration Guide

This project supports both **SQLite** and **PostgreSQL** databases. You can switch between them by editing your `.env` file—no code changes required!

## Quick Reference

### SQLite (Default)
```env
DATABASE_ENGINE=sqlite3
```
That's it! No other configuration needed.

### PostgreSQL
```env
DATABASE_ENGINE=postgresql
DATABASE_NAME=hcot_db
DATABASE_USER=hcot_user
DATABASE_PASSWORD=your_secure_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

---

## Detailed Setup Instructions

### Option 1: SQLite (Development)

**When to use:**
- Local development
- Testing
- Small projects
- Quick prototyping

**Advantages:**
- ✅ Zero configuration
- ✅ No installation needed
- ✅ File-based (portable)
- ✅ Perfect for development

**Setup:**
1. Make sure `DATABASE_ENGINE=sqlite3` in your `.env` (or just leave it out—it's the default)
2. Run migrations: `python manage.py migrate`
3. Done! Database created as `db.sqlite3`

---

### Option 2: PostgreSQL (Production)

**When to use:**
- Production environments
- Staging servers
- Team collaboration
- Large-scale applications

**Advantages:**
- ✅ Better performance
- ✅ Advanced features
- ✅ Better concurrency
- ✅ Production-ready

**Prerequisites:**
1. PostgreSQL installed: https://www.postgresql.org/download/
2. Python driver installed: `pip install psycopg2-binary`

**Step-by-Step Setup:**

#### 1. Install PostgreSQL

**macOS:**
```bash
# Using Homebrew
brew install postgresql
brew services start postgresql
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

**Windows:**
Download and install from https://www.postgresql.org/download/windows/

#### 2. Create Database and User

Open PostgreSQL shell:
```bash
# macOS/Linux
psql -U postgres

# Windows (run from psql in Start Menu or pgAdmin)
```

Run these SQL commands:
```sql
-- Create database
CREATE DATABASE hcot_db;

-- Create user with password
CREATE USER hcot_user WITH PASSWORD 'your_secure_password_here';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE hcot_db TO hcot_user;

-- Set owner
ALTER DATABASE hcot_db OWNER TO hcot_user;

-- Exit
\q
```

#### 3. Install Python PostgreSQL Driver

```bash
# Activate your virtual environment first!
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Install the driver
pip install psycopg2-binary
```

#### 4. Configure Environment Variables

Edit your `.env` file:

```env
# Database Configuration
DATABASE_ENGINE=postgresql

# PostgreSQL Connection Settings
DATABASE_NAME=hcot_db
DATABASE_USER=hcot_user
DATABASE_PASSWORD=your_secure_password_here
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_CONNECT_TIMEOUT=10
```

#### 5. Run Migrations

```bash
python manage.py migrate
```

#### 6. Create Superuser

```bash
python manage.py createsuperuser
```

---

## Configuration Options

### Required Settings (PostgreSQL)

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `DATABASE_ENGINE` | Database type | `sqlite3` | `postgresql` |
| `DATABASE_NAME` | Database name | `hcot_db` | `myapp_db` |
| `DATABASE_USER` | Database username | `postgres` | `myapp_user` |
| `DATABASE_PASSWORD` | User password | *(none)* | `SecurePass123!` |
| `DATABASE_HOST` | Server address | `localhost` | `db.example.com` |
| `DATABASE_PORT` | PostgreSQL port | `5432` | `5432` |

### Optional Settings

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_CONNECT_TIMEOUT` | Connection timeout (seconds) | `10` |

---

## Switching Between Databases

### From SQLite to PostgreSQL

1. **Backup your data (optional)**
   ```bash
   python manage.py dumpdata > backup.json
   ```

2. **Update `.env`**
   ```env
   DATABASE_ENGINE=postgresql
   DATABASE_NAME=hcot_db
   DATABASE_USER=hcot_user
   DATABASE_PASSWORD=your_password
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

4. **Load data (optional)**
   ```bash
   python manage.py loaddata backup.json
   ```

### From PostgreSQL to SQLite

1. **Backup your data (optional)**
   ```bash
   python manage.py dumpdata > backup.json
   ```

2. **Update `.env`**
   ```env
   DATABASE_ENGINE=sqlite3
   ```

3. **Delete old SQLite database (if exists)**
   ```bash
   rm db.sqlite3
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Load data (optional)**
   ```bash
   python manage.py loaddata backup.json
   ```

---

## Troubleshooting

### PostgreSQL Connection Issues

**Error: `could not connect to server`**
- Check PostgreSQL is running: `pg_isready`
- Start PostgreSQL: `brew services start postgresql` (macOS)
- Or: `sudo systemctl start postgresql` (Linux)

**Error: `password authentication failed`**
- Verify credentials in `.env` match PostgreSQL user
- Try connecting manually: `psql -U hcot_user -d hcot_db -h localhost`

**Error: `database "hcot_db" does not exist`**
- Create the database: `psql -U postgres -c "CREATE DATABASE hcot_db;"`

**Error: `psycopg2 not installed`**
- Install the driver: `pip install psycopg2-binary`

### SQLite Issues

**Error: `database is locked`**
- Close all database connections
- Restart development server
- Check no other process is using the database

**Error: `no such table`**
- Run migrations: `python manage.py migrate`

### General Database Commands

```bash
# Check database connection
python manage.py dbshell

# Show all migrations
python manage.py showmigrations

# Create migrations for model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Verify configuration
python manage.py check
```

---

## Best Practices

### Development
- ✅ Use SQLite for local development
- ✅ Keep `db.sqlite3` in `.gitignore`
- ✅ Use fixtures for test data
- ✅ Run migrations regularly

### Production
- ✅ Use PostgreSQL for production
- ✅ Use strong passwords
- ✅ Enable connection pooling
- ✅ Regular backups
- ✅ Monitor performance
- ✅ Use environment variables (never hardcode credentials)

### Security
- 🔒 Never commit `.env` file
- 🔒 Use strong passwords (12+ characters)
- 🔒 Restrict database user permissions
- 🔒 Use SSL/TLS for remote connections
- 🔒 Regular security updates

---

## Additional Resources

- [Django Database Documentation](https://docs.djangoproject.com/en/stable/ref/databases/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [psycopg2 Documentation](https://www.psycopg.org/docs/)

---

## Need Help?

If you encounter issues not covered here:
1. Check the main `README.md` file
2. Review Django's official database documentation
3. Check PostgreSQL logs: `/var/log/postgresql/` (Linux) or Console.app (macOS)
4. Verify your `.env` file matches `.env.example` format
