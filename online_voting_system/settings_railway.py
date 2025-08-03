# Railway-specific Django settings
# This file extends settings_heroku.py for Railway deployment

from .settings_heroku import *
import os

# Railway-specific configurations
ALLOWED_HOSTS = [
    '.railway.app',
    '.railway.internal',
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
]

# Railway provides DATABASE_URL automatically when PostgreSQL is added
# No additional database configuration needed

# Static files configuration for Railway
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Railway-specific security settings
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'

# Logging configuration for Railway
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}
