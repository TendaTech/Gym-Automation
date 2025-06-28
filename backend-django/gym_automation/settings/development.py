"""
Development settings for gym_automation project.
"""
from .base import *

# Debug toolbar
if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    
    INTERNAL_IPS = [
        '127.0.0.1',
        'localhost',
    ]

# Allow all hosts in development
ALLOWED_HOSTS = ['*']

# Email backend for development (console)
if not config('SENDGRID_API_KEY', default=''):
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Disable HTTPS redirect in development
SECURE_SSL_REDIRECT = False