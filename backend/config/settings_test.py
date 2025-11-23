"""
Test mode settings for Gluide application.
Uses in-memory SQLite databases for fast testing.
"""

from .settings import *

# TEST MODE: Use in-memory SQLite databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
    'course_db': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Override GIS backend for testing (SQLite doesn't support PostGIS)
# Models with PostGIS fields will use regular fields in test mode
SPATIALITE_LIBRARY_PATH = 'mod_spatialite'

# Fast password hashing for tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Disable migrations in test mode
class DisableMigrations:
    def __contains__(self, item):
        return True
    def __getitem__(self, item):
        return None

MIGRATION_MODULES = DisableMigrations()

# Load fixtures automatically
FIXTURE_DIRS = [
    os.path.join(BASE_DIR, 'api', 'fixtures'),
    os.path.join(BASE_DIR, 'gluideme', 'fixtures'),
]

# Transcript parser settings (test values)
STATIC_TOKEN = 'test-token-123'
GLUIDE_ME_BACKEND_TOKEN = 'test-backend-token-123'

# Celery Configuration for TEST mode
# Use in-memory broker for testing
CELERY_TASK_ALWAYS_EAGER = True  # Execute tasks synchronously
CELERY_TASK_EAGER_PROPAGATES = True  # Propagate exceptions
CELERY_BROKER_URL = 'memory://'
CELERY_RESULT_BACKEND = 'cache+memory://'

# Test mode flag
USE_TEST_MODE = True

# Remove GIS app if it was added (we don't need GDAL for SQLite testing)
if 'django.contrib.gis' in INSTALLED_APPS:
    INSTALLED_APPS.remove('django.contrib.gis')

print("Running in TEST MODE with in-memory SQLite databases")
