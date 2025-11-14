"""
Database mode settings for Gluide application.
Connects to existing PostgreSQL databases and external services.
"""

from .settings import *

# Override to use database mode
USE_TEST_MODE = False

# Connect to EXISTING PostgreSQL databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'gluide_me'),
        'USER': os.environ.get('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', ''),
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    },
    'course_db': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_DATABASE', 'course_db'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Database router for production mode
DATABASE_ROUTERS = ['db_routers.ProductionDatabaseRouter']

# Redis configuration (existing service)
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')
REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': REDIS_URL,
    }
}

CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL

# External services (existing)
PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY', '')
PINECONE_ENVIRONMENT = os.environ.get('PINECONE_ENVIRONMENT', '')
PINECONE_INDEX_NAME = os.environ.get('PINECONE_INDEX_NAME', '')

MEILISEARCH_HOST = os.environ.get('MEILISEARCH_HOST', '')
MEILISEARCH_API_KEY = os.environ.get('MEILISEARCH_API_KEY', '')

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')

# AWS S3 (existing bucket)
USE_S3 = os.environ.get('USE_S3', 'True') == 'True'
if USE_S3:
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'us-east-1')

print("🗄️  Running in DATABASE MODE with real PostgreSQL")
