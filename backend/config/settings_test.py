"""
Test settings for OT Assessment Tracker
Uses in-memory SQLite database for testing
"""
from .settings import *

# Override database to use SQLite for testing
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Remove tenant-specific database router
DATABASE_ROUTERS = []

# Disable django-tenants for unit tests (we'll test tenant features separately)
# Remove from installed apps
if 'django_tenants' in SHARED_APPS:
    SHARED_APPS = [app for app in SHARED_APPS if app != 'django_tenants']
if 'django_tenants' in TENANT_APPS:
    TENANT_APPS = [app for app in TENANT_APPS if app != 'django_tenants']

# Rebuild INSTALLED_APPS without django-tenants
INSTALLED_APPS = SHARED_APPS + [app for app in TENANT_APPS if app not in SHARED_APPS]

# Remove django-tenants middleware
MIDDLEWARE = [mw for mw in MIDDLEWARE if 'django_tenants' not in mw]

# Speed up password hashing in tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Disable encryption for tests (we'll test encryption separately)
FIELD_ENCRYPTION_KEY = 'test-key-32-characters-long!!!'

# Disable debug toolbar in tests
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: False,
}
