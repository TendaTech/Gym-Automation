"""
Production settings for gym_automation project.
"""
from .base import *

# Security settings
DEBUG = False
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# Static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Database must be configured via DATABASE_URL in production
if not config('DATABASE_URL', default=None):
    raise ValueError('DATABASE_URL environment variable is required in production')

# Logging
LOGGING['handlers']['file']['filename'] = '/var/log/gym_automation/django.log'