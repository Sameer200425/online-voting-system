#!/bin/bash
# cspell:ignore venv psql CREATEDB createsuperuser collectstatic noinput Gunicorn

echo "🚀 Starting deployment of Online Voting System..."

# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip python3-venv postgresql postgresql-contrib nginx -y

# Create project directory
sudo mkdir -p /var/www/voting_system
cd /var/www/voting_system

# Clone or copy your project files here
echo "📁 Copy your project files to /var/www/voting_system/"

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create PostgreSQL database
sudo -u postgres psql << EOF
CREATE DATABASE voting_system_db;
CREATE USER voting_user WITH ENCRYPTED PASSWORD 'your-secure-password';
GRANT ALL PRIVILEGES ON DATABASE voting_system_db TO voting_user;
ALTER USER voting_user CREATEDB;
\q
EOF

# Set up environment variables
cp .env.production .env

# Run migrations
python manage.py migrate

# Create superuser (you'll be prompted)
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Set proper permissions
sudo chown -R www-data:www-data /var/www/voting_system/
sudo chmod -R 755 /var/www/voting_system/

echo "✅ Basic setup complete!"
echo "📝 Next steps:"
echo "1. Configure Nginx (see nginx.conf)"
echo "2. Set up SSL certificates"
echo "3. Configure Gunicorn service"
echo "4. Update .env with your actual values"
