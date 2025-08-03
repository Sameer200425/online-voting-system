#!/bin/bash
# Railway deployment script

echo "🚀 Starting Railway deployment..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Run migrations
echo "🗄️ Running database migrations..."
python manage.py migrate

# Start the application
echo "✅ Starting Django application..."
exec gunicorn online_voting_system.wsgi:application --bind 0.0.0.0:$PORT --workers 3
