<!-- cspell:ignore Gunicorn certbot journalctl yourdomain venv collectstatic noinput -->

# Deployment Guide for Online Voting System

## 🚀 Production Deployment Guide

### Prerequisites

- Ubuntu/Debian server (20.04+ recommended)
- Domain name (optional but recommended)
- SSH access to server

### Quick Deployment Steps

#### 1. Server Setup

```bash
# Make deploy script executable
chmod +x deploy.sh

# Run deployment script
./deploy.sh
```

#### 2. Manual Configuration Steps

##### A. Update Environment Variables

Edit `.env` file with your actual values:

```bash
nano /var/www/voting_system/.env
```

##### B. Configure Nginx

```bash
# Copy nginx configuration
sudo cp nginx.conf /etc/nginx/sites-available/voting-system
sudo ln -s /etc/nginx/sites-available/voting-system /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default

# Test configuration
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx
```

##### C. Set up Gunicorn Service

```bash
# Copy service file
sudo cp voting-system.service /etc/systemd/system/

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable voting-system
sudo systemctl start voting-system
```

##### D. SSL Certificate (Let's Encrypt)

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

#### 3. Security Checklist

- [ ] Change SECRET_KEY in production
- [ ] Set DEBUG=False
- [ ] Configure proper ALLOWED_HOSTS
- [ ] Set up SSL certificates
- [ ] Configure firewall (UFW)
- [ ] Set up regular backups
- [ ] Configure monitoring

#### 4. Post-Deployment

```bash
# Check service status
sudo systemctl status voting-system

# Check logs
sudo journalctl -u voting-system -f

# Check nginx logs
sudo tail -f /var/log/nginx/error.log
```

### Alternative Deployment Options

#### Option 1: Heroku Deployment

1. Install Heroku CLI
2. Create Heroku app: `heroku create your-app-name`
3. Add PostgreSQL addon: `heroku addons:create heroku-postgresql:hobby-dev`
4. Set environment variables: `heroku config:set DEBUG=False`
5. Deploy: `git push heroku main`

#### Option 2: DigitalOcean App Platform

1. Connect GitHub repository
2. Configure environment variables
3. Set build and run commands
4. Deploy automatically

#### Option 3: AWS EC2

1. Launch EC2 instance
2. Configure security groups
3. Use deploy.sh script
4. Set up load balancer (optional)

### Environment Variables

Required environment variables for production:

```env
DEBUG=False
SECRET_KEY=your-super-secret-key-change-this
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_ENGINE=django.db.backends.postgresql
DB_NAME=voting_system_db
DB_USER=voting_user
DB_PASSWORD=secure-password
DB_HOST=localhost
DB_PORT=5432
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Maintenance Commands

```bash
# Update application
cd /var/www/voting_system
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart voting-system

# Database backup
pg_dump voting_system_db > backup_$(date +%Y%m%d).sql

# View logs
sudo journalctl -u voting-system -n 50
```

### Troubleshooting

Common issues and solutions:

1. **Static files not loading**
   - Run `python manage.py collectstatic`
   - Check nginx configuration

2. **Database connection errors**
   - Verify PostgreSQL is running
   - Check database credentials

3. **Permission denied errors**
   - Check file permissions: `sudo chown -R www-data:www-data /var/www/voting_system/`

4. **Service won't start**
   - Check logs: `sudo journalctl -u voting-system -f`
   - Verify virtual environment path

### Performance Optimization

- Enable gzip compression
- Set up Redis for caching
- Configure CDN for static files
- Implement database connection pooling
- Set up monitoring with tools like New Relic or DataDog

Your voting system is now ready for production deployment! 🎉
