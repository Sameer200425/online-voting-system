<!-- cspell:ignore venv createsuperuser runserver yourdomain Gunicorn WSGI wsgi -->

# Online Voting System

A secure, modern web-based voting platform built with Django and Python that enables democratic elections with real-time results and comprehensive administration features.

## 🚀 Features

### Core Functionality

- **Secure User Registration & Authentication**
  - Age verification (18+ requirement)
  - Unique voter ID system
  - Email verification support
  - Password reset functionality

- **Election Management**
  - Create and manage multiple elections
  - Set election start/end times
  - Candidate management with photos and bios
  - Real-time election status tracking

- **Voting System**
  - One-vote-per-user enforcement
  - Secure vote casting with confirmation
  - Anonymous voting with audit trails
  - IP address logging for security

- **Results & Analytics**
  - Real-time vote counting
  - Percentage-based results visualization
  - Winner determination
  - Historical voting records

### Administrative Features

- **Admin Dashboard**
  - Comprehensive statistics overview
  - Recent activity monitoring
  - Quick action buttons
  - User management tools

- **Election Administration**
  - Create and edit elections
  - Manage candidates
  - Monitor voting progress
  - Export results

- **Security & Auditing**
  - Complete audit trail logging
  - IP address tracking
  - User activity monitoring
  - Data integrity checks

## 🛠 Technology Stack

- **Backend**: Django 5.2.4 (Python)
- **Database**: SQLite (Development) / PostgreSQL (Production)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Authentication**: Django's built-in auth system
- **Image Processing**: Pillow
- **Security**: CSRF protection, password hashing, SQL injection prevention

## 📦 Installation & Setup

### Prerequisites

- Python 3.8+
- pip package manager
- Virtual environment (recommended)

### Quick Start

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd online-voting-system
   ```

2. **Create and activate virtual environment**

   ```bash
   python -m venv .venv
   
   # On Windows
   .venv\Scripts\activate
   
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install Django Pillow
   ```

4. **Run database migrations**

   ```bash
   python manage.py migrate
   ```

5. **Create superuser account**

   ```bash
   python manage.py createsuperuser
   ```

6. **Start development server**

   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main site: <http://127.0.0.1:8000/>
   - Admin panel: <http://127.0.0.1:8000/admin/>

## 🎯 Usage Guide

### For Voters

1. **Registration**
   - Visit the registration page
   - Provide required information including voter ID
   - Verify age requirement (18+)
   - Create secure password

2. **Voting**
   - Log in to your account
   - Browse active elections
   - Select an election to participate
   - Choose your preferred candidate
   - Submit vote (one vote per election)

3. **View Results**
   - Check election results after completion
   - View your voting history in profile

### For Administrators

1. **Access Admin Dashboard**
   - Log in with admin credentials
   - Navigate to Admin Dashboard
   - Monitor system statistics

2. **Create Elections**
   - Use "Create Election" feature
   - Set title, description, and timeline
   - Add candidates with details and photos
   - Activate election when ready

3. **Manage Elections**
   - Monitor voting progress
   - Add/remove candidates
   - View real-time results
   - Close elections when finished

## 🔐 Security Features

- **Authentication Security**
  - Password hashing with Django's PBKDF2
  - Session management
  - CSRF protection on all forms
  - Login rate limiting

- **Voting Security**
  - One-vote-per-user enforcement
  - Vote anonymity preservation
  - Tamper-proof vote storage
  - IP address logging

- **Data Protection**
  - SQL injection prevention (Django ORM)
  - XSS protection
  - Secure file uploads
  - Input validation and sanitization

## 📊 Database Schema

### Core Models

- **User**: Extended Django user model
- **UserProfile**: Voter-specific information
- **Election**: Election details and timing
- **Candidate**: Candidate information and media
- **Vote**: Secure vote records
- **AuditLog**: System activity tracking

## 🚀 Deployment

### Production Deployment Steps

1. **Environment Configuration**

   ```python
   # settings.py
   DEBUG = False
   ALLOWED_HOSTS = ['yourdomain.com']
   
   # Use PostgreSQL for production
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'voting_system',
           'USER': 'your_user',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

2. **Web Server Setup**
   - Use Gunicorn/uWSGI for WSGI
   - Configure Nginx/Apache for static files
   - Set up SSL certificates (HTTPS required)

3. **Security Checklist**
   - Change SECRET_KEY
   - Enable HTTPS
   - Configure email backend
   - Set up regular backups
   - Monitor system logs

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:

- Create an issue on GitHub
- Check the documentation
- Contact: <sameerkhan28083@gmail.com>

## 🏗 Project Structure

```bash
online_voting_system/
├── manage.py
├── online_voting_system/          # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── voting_app/                    # Main application
│   ├── models.py                  # Database models
│   ├── views.py                   # View logic
│   ├── forms.py                   # Form definitions
│   ├── urls.py                    # URL patterns
│   ├── admin.py                   # Admin interface
│   ├── templates/                 # HTML templates
│   │   └── voting_app/
│   └── static/                    # CSS, JS, images
├── media/                         # Uploaded files
├── static/                        # Static files
└── requirements.txt               # Dependencies
```

## 🔄 Version History

- **v1.0.0** - Initial release with core voting functionality
- **v1.1.0** - Added admin dashboard and enhanced security
- **v1.2.0** - Improved UI/UX and added real-time features

---

Built with ❤️ for democratic participation
