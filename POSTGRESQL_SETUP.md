# PostgreSQL Setup Instructions for Production
<!-- cspell:ignore psql postgresql gunicorn amazonaws subdomains createuser createdb yourdomain venv makemigrations createsuperuser runserver wsgi -->

## 1. Install PostgreSQL

### Windows

1. Download PostgreSQL from <https://www.postgresql.org/download/windows/>
2. Run the installer and follow the setup wizard
3. Set a password for the 'postgres' user (remember this!)
4. Default port is 5432 (keep this unless you have conflicts)

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo -u postgres createuser --interactive
sudo -u postgres createdb voting_system_db
```

### macOS

```bash
brew install postgresql
brew services start postgresql
createdb voting_system_db
```

## 2. Create Database and User

After installing PostgreSQL, connect to it:

```sql
-- Connect as postgres user
psql -U postgres

-- Create database
CREATE DATABASE voting_system_db;

-- Create user
CREATE USER voting_user WITH PASSWORD 'your_secure_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE voting_system_db TO voting_user;

-- Exit
\q
```

## 3. Configure Environment Variables

1. Copy `.env.example` to `.env`:

   ```bash
   cp .env.example .env
   ```

2. Edit `.env` file with your actual values:

   ```env
   SECRET_KEY=your-actual-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,your-server-ip
   DATABASE_URL=postgresql://voting_user:your_secure_password@localhost:5432/voting_system_db
   ```

## 4. Run Database Migrations

```bash
# Activate virtual environment
.venv\Scripts\activate

# Set environment to use PostgreSQL settings
set DJANGO_SETTINGS_MODULE=voting_system.settings_postgresql

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load sample data (optional)
python create_sample_data.py
```

## 5. Test the Configuration

```bash
# Run with PostgreSQL settings
python manage.py runserver --settings=voting_system.settings_postgresql
```

## 6. Production Deployment with PostgreSQL

### Using Gunicorn

```bash
# Install production dependencies
pip install gunicorn

# Run with Gunicorn
gunicorn --bind 0.0.0.0:8000 --env DJANGO_SETTINGS_MODULE=voting_system.settings_postgresql voting_system.wsgi:application
```

### Environment Variables for Production

- Set `DEBUG=False`
- Update `ALLOWED_HOSTS` with your domain
- Use strong `SECRET_KEY`
- Configure proper database credentials
- Set up SSL certificates for HTTPS

## 7. Cloud Database Options

### Heroku Postgres

```env
DATABASE_URL=postgres://user:password@host:port/database
```

### AWS RDS

```env
DATABASE_URL=postgresql://username:password@your-rds-endpoint.amazonaws.com:5432/voting_system_db
```

### Google Cloud SQL

```env
DATABASE_URL=postgresql://username:password@your-instance-connection-name/voting_system_db
```

## 8. Backup and Restore

### Create Backup

```bash
pg_dump -U voting_user -h localhost voting_system_db > backup.sql
```

### Restore Backup

```bash
psql -U voting_user -h localhost voting_system_db < backup.sql
```

## Common Issues and Solutions

1. **Connection Refused**: Check if PostgreSQL service is running
2. **Authentication Failed**: Verify username/password in DATABASE_URL
3. **Database Not Found**: Ensure database was created
4. **Permission Denied**: Grant proper privileges to user

## Performance Optimization

- Create database indexes for frequently queried fields
- Use connection pooling in production
- Configure PostgreSQL settings for your server specs
- Monitor query performance with Django Debug Toolbar
