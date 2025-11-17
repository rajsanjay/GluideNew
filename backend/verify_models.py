#!/usr/bin/env python
"""
Model verification script for TEST MODE.
Run this after installing dependencies and setting up TEST MODE.

Usage:
    export DJANGO_SETTINGS_MODULE=config.settings_test
    python verify_models.py
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_test')
django.setup()

from django.conf import settings
from django.db import connection
from django.core.management import call_command


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)


def check_settings():
    """Verify Django settings are correct."""
    print_section("1. Checking Django Settings")

    print(f"✓ Settings module: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
    print(f"✓ Test mode: {getattr(settings, 'USE_TEST_MODE', False)}")
    print(f"✓ Debug: {settings.DEBUG}")

    print("\nDatabase Configuration:")
    for db_name, db_config in settings.DATABASES.items():
        print(f"  - {db_name}: {db_config['ENGINE']}")
        if 'NAME' in db_config:
            print(f"    Name: {db_config['NAME']}")

    print("\nInstalled Apps:")
    for app in settings.INSTALLED_APPS:
        if not app.startswith('django.'):
            print(f"  - {app}")


def check_models():
    """Verify all models are importable."""
    print_section("2. Checking Model Imports")

    models_to_check = [
        ("Primary DB Models", [
            "api.models.Session",
            "api.models.Message",
            "api.models.Question",
            "api.models.UserAnswer",
            "api.models.UserAttribute",
            "api.models.StudentCourse",
            "api.models.File",
            "api.models.Room",
            "api.models.ChatMessage",
        ]),
        ("Course DB Models", [
            "api.models_course_db.School",
            "api.models_course_db.Course",
            "api.models_course_db.Major",
            "api.models_course_db.Program",
            "api.models_course_db.AcademicYear",
        ]),
        ("Gluideme Models", [
            "gluideme.models.College",
            "gluideme.models.Course",
            "gluideme.models.Program",
            "gluideme.models.Students",
            "gluideme.models.CounselorProfile",
        ]),
        ("Pydantic Models", [
            "gluideai.models.Course",
            "gluideai.models.Transcript",
        ]),
    ]

    all_success = True
    for category, model_paths in models_to_check:
        print(f"\n{category}:")
        for model_path in model_paths:
            try:
                module_path, model_name = model_path.rsplit('.', 1)
                module = __import__(module_path, fromlist=[model_name])
                model = getattr(module, model_name)
                print(f"  ✓ {model_name}")
            except Exception as e:
                print(f"  ✗ {model_name}: {str(e)}")
                all_success = False

    return all_success


def check_migrations():
    """Check migration status."""
    print_section("3. Checking Migrations")

    print("\nRunning 'showmigrations':")
    call_command('showmigrations')


def check_managed_flags():
    """Verify managed flags are set correctly."""
    print_section("4. Verifying Managed Flags")

    from api.models import Session
    from api.models_course_db import School
    from gluideme.models import Students

    print(f"\nPrimary DB Models (should be managed=True):")
    print(f"  Session._meta.managed: {Session._meta.managed}")

    print(f"\nCourse DB Models (should be managed=False):")
    print(f"  School._meta.managed: {School._meta.managed}")

    print(f"\nGluideme Models (should be managed=True):")
    print(f"  Students._meta.managed: {Students._meta.managed}")


def check_database_router():
    """Verify database router configuration."""
    print_section("5. Checking Database Router")

    from api.models import Session
    from api.models_course_db import School
    from db_routers import ModelDatabaseRouter

    router = ModelDatabaseRouter()

    print(f"\nSession model routing:")
    print(f"  - db_for_read: {router.db_for_read(Session)}")
    print(f"  - db_for_write: {router.db_for_write(Session)}")

    print(f"\nSchool model routing:")
    print(f"  - db_for_read: {router.db_for_read(School)}")
    print(f"  - db_for_write: {router.db_for_write(School)}")

    print(f"\nMigration allowed:")
    print(f"  - default db: {router.allow_migrate('default', 'api')}")
    print(f"  - course_db: {router.allow_migrate('course_db', 'api')}")


def check_model_counts():
    """Count models in each app."""
    print_section("6. Model Counts")

    from django.apps import apps

    for app_config in apps.get_app_configs():
        if app_config.name in ['api', 'gluideme', 'gluideai']:
            models = app_config.get_models()
            print(f"\n{app_config.name}:")
            print(f"  Total models: {len(models)}")
            for model in models:
                managed = model._meta.managed
                db_table = model._meta.db_table
                print(f"    - {model.__name__}: managed={managed}, table={db_table}")


def main():
    """Run all verification checks."""
    print("\n" + "=" * 70)
    print(" MODEL VERIFICATION SCRIPT - TEST MODE")
    print("=" * 70)

    try:
        # Run all checks
        check_settings()
        models_ok = check_models()
        check_managed_flags()
        check_database_router()
        check_model_counts()

        # Try to check migrations (may fail if not created yet)
        try:
            check_migrations()
        except Exception as e:
            print(f"\nNote: Migrations not created yet: {e}")
            print("Run: python manage.py makemigrations")

        # Summary
        print_section("Summary")
        if models_ok:
            print("\n✓ All model imports successful")
            print("\nNext steps:")
            print("1. Run: python manage.py makemigrations api")
            print("2. Run: python manage.py makemigrations gluideme")
            print("3. Run: python manage.py migrate")
            print("4. Run: python manage.py generate_test_fixtures")
        else:
            print("\n✗ Some model imports failed")
            print("Fix the errors above before proceeding.")

    except Exception as e:
        print(f"\n✗ Verification failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
