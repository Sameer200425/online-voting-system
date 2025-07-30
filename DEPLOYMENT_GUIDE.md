# Deployment Guide for Django Online Voting System
<!-- cspell:ignore venv psycopg gunicorn whitenoise decouple systemctl nginx certbot -->

## Overview

This guide covers the complete deployment process for your Django online voting system from development to production.

## Pre-Deployment Checklist

### ✅ Development Environment Ready

- Django project created and tested
- All dependencies listed in `requirements.txt`
- Sample data created and working
- Local server accessible at <http://192.168.1.5:8000>

### ✅ Production Files Created

- `settings_postgresql.py` - Production database settings
- `.env.example` - Environment variables template
- `POSTGRESQL_SETUP.md` - Database setup instructions
- All spelling/linting errors fixed

## Deployment Process

### 1. Choose Your Deployment Method

#### Option A: Local Network Deployment (Current Status)

Status: ✅ Complete and Working

- Your system is already accessible at <http://192.168.1.5:8000>
- Perfect for local testing and demonstrations
- Accessible to devices on your local network

#### Option B: Cloud Deployment (Recommended for Production)

Choose one platform:

- **Heroku** (Easiest for beginners)
- **DigitalOcean** (Good balance of ease and control)
- **AWS** (Most features, more complex)
- **Google Cloud Platform**
- **Azure**

### 2. Local Network Deployment Steps

**Already Completed - Your Current Setup:**

```bash
# 1. Virtual environment activated
.venv\Scripts\activate

# 2. Dependencies installed
pip install -r requirements.txt

# 3. Database migrated
python manage.py migrate

# 4. Sample data loaded
python create_sample_data.py

# 5. Server running on network
python manage.py runserver 0.0.0.0:8000
```

**Access URLs:**

- Local: <http://localhost:8000>
- Network: <http://192.168.1.5:8000>
- Admin: <http://192.168.1.5:8000/admin>

### 3. Production Cloud Deployment

#### Step 3.1: Server Setup

**For Ubuntu/Linux Server:**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv nginx postgresql postgresql-contrib -y

# Create project directory
sudo mkdir -p /var/www/voting_system
sudo chown $USER:$USER /var/www/voting_system
```

#### Step 3.2: Code Deployment

```bash
# Navigate to project directory
cd /var/www/voting_system

# Clone or upload your project
# Option 1: Git clone (if using version control)
git clone your-repository-url .

# Option 2: Upload files manually
# Upload your entire project folder to /var/www/voting_system

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Step 3.3: Database Setup (PostgreSQL)

**Follow the detailed guide in `POSTGRESQL_SETUP.md`:**

```bash
# Install PostgreSQL (if not already done)
sudo apt install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE DATABASE voting_system_db;
CREATE USER voting_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE voting_system_db TO voting_user;
\q

# Configure environment variables
cp .env.example .env
# Edit .env with your production values
```

#### Step 3.4: Django Production Setup

```bash
# Set production environment
export DJANGO_SETTINGS_MODULE=voting_system.settings_postgresql

# Run migrations
python manage.py migrate --settings=voting_system.settings_postgresql

# Create superuser
python manage.py createsuperuser --settings=voting_system.settings_postgresql

# Collect static files
python manage.py collectstatic --settings=voting_system.settings_postgresql

# Load sample data (optional)
python create_sample_data.py
```

#### Step 3.5: Gunicorn Setup

```bash
# Install Gunicorn (already in requirements.txt)
pip install gunicorn

# Test Gunicorn
gunicorn --bind 0.0.0.0:8000 --env DJANGO_SETTINGS_MODULE=voting_system.settings_postgresql voting_system.wsgi:application

# Create Gunicorn service file
sudo nano /etc/systemd/system/voting_system.service
```

**Service file content:**
```ini
[Unit]
Description=Gunicorn instance to serve voting_system
After=network.target

[Service]
User=your-username
Group=www-data
WorkingDirectory=/var/www/voting_system
Environment="PATH=/var/www/voting_system/.venv/bin"
EnvironmentFile=/var/www/voting_system/.env
ExecStart=/var/www/voting_system/.venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/var/www/voting_system/voting_system.sock voting_system.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl daemon-reload
sudo systemctl start voting_system
sudo systemctl enable voting_system
```

#### Step 3.6: Nginx Configuration

```bash
# Create Nginx configuration
sudo nano /etc/nginx/sites-available/voting_system
```

**Nginx configuration:**
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /var/www/voting_system;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/voting_system/voting_system.sock;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/voting_system /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

#### Step 3.7: SSL Certificate (HTTPS)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

### 4. Platform-Specific Deployment

#### 4.1: Heroku Deployment

```bash
# Install Heroku CLI
# Create Procfile
echo "web: gunicorn voting_system.wsgi:application" > Procfile

# Create runtime.txt
echo "python-3.11.0" > runtime.txt

# Heroku commands
heroku create your-app-name
heroku addons:create heroku-postgresql:mini
heroku config:set DJANGO_SETTINGS_MODULE=voting_system.settings_postgresql
heroku config:set SECRET_KEY=your-secret-key
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

#### 4.2: DigitalOcean App Platform

1. Connect your GitHub repository
2. Set environment variables in dashboard
3. Use `voting_system.settings_postgresql` as settings module
4. Deploy automatically from Git

### 5. Domain and DNS Setup

```bash
# Point your domain to your server IP
# A Record: @ -> your-server-ip
# A Record: www -> your-server-ip
# CNAME Record: www -> your-domain.com
```

### 6. Monitoring and Maintenance

#### 6.1: Log Monitoring

```bash
# Check application logs
sudo journalctl -u voting_system -f

# Check Nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

#### 6.2: Database Backup

```bash
# Create backup
pg_dump -U voting_user -h localhost voting_system_db > backup_$(date +%Y%m%d).sql

# Restore backup
psql -U voting_user -h localhost voting_system_db < backup_20250731.sql
```

#### 6.3: Security Updates

```bash
# Regular system updates
sudo apt update && sudo apt upgrade -y

# Django security updates
pip install --upgrade django
python manage.py migrate
```

## Current Project Status

### ✅ Completed

- Full Django voting system with authentication
- Sample elections and candidates data
- Admin interface configured
- Local network accessibility
- All code errors fixed
- PostgreSQL production settings ready
- Deployment documentation complete

### 🚀 Ready for Deployment

Your project is production-ready with:

- 5 sample elections with 16 candidates
- User authentication and voting system
- Admin panel for election management
- Audit logging for vote tracking
- Responsive Bootstrap UI
- PostgreSQL production configuration

### 🌐 Access Information

- **Local Development**: <http://localhost:8000>
- **Network Access**: <http://192.168.1.5:8000>
- **Admin Panel**: <http://192.168.1.5:8000/admin>
- **Sample Users**: Created via Django admin

## Next Steps

1. **For Local Demo**: Your system is ready! Access at <http://192.168.1.5:8000>
2. **For Production**: Follow cloud deployment steps above
3. **For Public Access**: Purchase domain and follow DNS setup
4. **For Scaling**: Implement load balancing and database optimization

Your Django online voting system is complete and ready for deployment! 🎉
