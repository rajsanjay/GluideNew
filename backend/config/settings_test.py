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

# Test mode flag
USE_TEST_MODE = True

print("🧪 Running in TEST MODE with in-memory SQLite databases")
