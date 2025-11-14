"""
Test mode settings for Gluide application.
Uses synthetic fixture data instead of connecting to real databases.
"""

from .settings import *

# Override to use test mode
USE_TEST_MODE = True
GENERATE_FIXTURES = True

# Use SQLite for test mode (in-memory or file-based)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'test_db.sqlite3',
    },
    'course_db': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'test_course_db.sqlite3',
    }
}

# Database router for test mode
DATABASE_ROUTERS = ['db_routers.TestDatabaseRouter']

# Disable external services in test mode
PINECONE_API_KEY = 'test-mode-disabled'
MEILISEARCH_HOST = 'test-mode-disabled'
OPENAI_API_KEY = 'test-mode-disabled'
USE_S3 = False

# Use local cache in test mode
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocalMemoryCache',
        'LOCATION': 'test-cache',
    }
}

# Optional: Use in-memory broker for Celery in test mode
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

print("🧪 Running in TEST MODE with synthetic data")
