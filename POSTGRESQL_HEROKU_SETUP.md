# PostgreSQL Database Setup for Heroku Deployment
<!-- cspell:ignore heroku psql -->

## 🚀 Complete Heroku Deployment with PostgreSQL

### Step 1: Login to Heroku

Open terminal and run:

```bash
cd "C:/Users/SAMEER KHAN/.vscode/online voting system"
& "C:\Program Files\heroku\bin\heroku.cmd" login
```

- This will open your browser for authentication
- Login with your Heroku account credentials

### Step 2: Create Heroku Application

```bash
# Create app with unique name
& "C:\Program Files\heroku\bin\heroku.cmd" create sameer-voting-system-2025

# Or let Heroku generate a unique name
& "C:\Program Files\heroku\bin\heroku.cmd" create
```

### Step 3: Add PostgreSQL Database

```bash
# Add PostgreSQL addon (Essential plan - free tier)
& "C:\Program Files\heroku\bin\heroku.cmd" addons:create heroku-postgresql:essential-0
```

**Available PostgreSQL Plans:**

- `essential-0` - Free tier (10,000 rows, 1GB storage)
- `essential-1` - $5/month (10M rows, 64GB storage)
- `standard-0` - $50/month (120M rows, 256GB storage)

### Step 4: Configure Environment Variables

```bash
# Set Django settings module for Heroku
& "C:\Program Files\heroku\bin\heroku.cmd" config:set DJANGO_SETTINGS_MODULE=online_voting_system.settings_heroku

# Disable debug mode
& "C:\Program Files\heroku\bin\heroku.cmd" config:set DEBUG=False

# Set a secure secret key (generate a new one for production)
& "C:\Program Files\heroku\bin\heroku.cmd" config:set SECRET_KEY=your-super-secret-key-here-change-this
```

### Step 5: Add Heroku Remote and Deploy

```bash
# If you haven't created the app yet, this will be done in step 2
# If you created the app, add the remote:
& "C:\Program Files\Git\bin\git.exe" remote add heroku https://git.heroku.com/your-app-name.git

# Deploy to Heroku
& "C:\Program Files\Git\bin\git.exe" push heroku main
```

### Step 6: Run Database Migrations

```bash
# Run migrations on Heroku
& "C:\Program Files\heroku\bin\heroku.cmd" run python manage.py migrate

# Create superuser account
& "C:\Program Files\heroku\bin\heroku.cmd" run python manage.py createsuperuser

# Load sample data (optional)
& "C:\Program Files\heroku\bin\heroku.cmd" run python create_sample_data.py
```

### Step 7: Open Your Live Application

```bash
# Open your app in browser
& "C:\Program Files\heroku\bin\heroku.cmd" open
```

## 🔍 Database Connection Information

### View Database URL

```bash
& "C:\Program Files\heroku\bin\heroku.cmd" config:get DATABASE_URL
```

### Connect to Database Directly

```bash
& "C:\Program Files\heroku\bin\heroku.cmd" pg:psql
```

### Database Information

```bash
& "C:\Program Files\heroku\bin\heroku.cmd" pg:info
```

## 📊 Monitoring Your Database

### Check Database Size

```bash
& "C:\Program Files\heroku\bin\heroku.cmd" pg:info
```

### View Database Connections

```bash
& "C:\Program Files\heroku\bin\heroku.cmd" pg:ps
```

### Create Database Backup

```bash
& "C:\Program Files\heroku\bin\heroku.cmd" pg:backups:capture
```

### Download Database Backup

```bash
& "C:\Program Files\heroku\bin\heroku.cmd" pg:backups:download
```

## 🔧 Troubleshooting

### Check Application Logs

```bash
& "C:\Program Files\heroku\bin\heroku.cmd" logs --tail
```

### Restart Application

```bash
& "C:\Program Files\heroku\bin\heroku.cmd" restart
```

### Check Configuration

```bash
& "C:\Program Files\heroku\bin\heroku.cmd" config
```

## 🚀 Expected Results After Deployment

Your live application will have:

- ✅ Public URL accessible worldwide
- ✅ PostgreSQL database (production-ready)
- ✅ SSL/HTTPS enabled automatically
- ✅ Static files served by WhiteNoise
- ✅ All your voting system features

### Your App URLs

- **Main App**: `https://your-app-name.herokuapp.com`
- **Admin Panel**: `https://your-app-name.herokuapp.com/admin`

## 📝 Important Notes

1. **Database URL**: Heroku automatically sets the `DATABASE_URL` environment variable
2. **Static Files**: Configured to use WhiteNoise for serving static files
3. **Migrations**: Must be run after each deployment with code changes
4. **Backups**: Free tier includes daily backups (retained for 2 days)

## 🔄 Future Updates

For any code changes:

```bash
# Commit changes
& "C:\Program Files\Git\bin\git.exe" add .
& "C:\Program Files\Git\bin\git.exe" commit -m "Description of changes"

# Deploy to Heroku
& "C:\Program Files\Git\bin\git.exe" push heroku main

# Run migrations if database changes
& "C:\Program Files\heroku\bin\heroku.cmd" run python manage.py migrate
```

## 🌟 Production Ready

Your Django Online Voting System will be:

- Accessible from anywhere in the world
- Running on professional cloud infrastructure
- Using production-grade PostgreSQL database
- Automatically backed up
- SSL secured

Ready to deploy! 🚀
