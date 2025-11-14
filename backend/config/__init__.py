"""
Django configuration package for the consolidated Gluide application.
"""
from .celery import app as celery_app

__all__ = ('celery_app',)
