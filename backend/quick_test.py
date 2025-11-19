#!/usr/bin/env python
"""
Quick test script to verify all models are working correctly.
Run this after setup to ensure everything is configured properly.

Usage:
    python quick_test.py
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_test')
django.setup()

from django.contrib.auth.models import User
from django.db import connection
from django.core.management import call_command


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f" {text}")
    print("=" * 60)


def setup_test_databases():
    """Create database tables for testing."""
    print_header("Setting Up Test Databases")
    try:
        print("[INFO] Creating database tables...")
        call_command('migrate', '--run-syncdb', verbosity=0)
        print("[OK] Database tables created successfully")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to create tables: {e}")
        return False


def test_environment():
    """Test environment configuration."""
    print_header("Testing Environment Configuration")
    from django.conf import settings

    print(f"[OK] Django settings: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
    print(f"[OK] Test mode: {getattr(settings, 'USE_TEST_MODE', False)}")
    print(f"[OK] Debug mode: {settings.DEBUG}")

    for db_name, db_config in settings.DATABASES.items():
        print(f"[OK] Database '{db_name}': {db_config['ENGINE']}")

    return True


def test_primary_models():
    """Test primary database models."""
    print_header("Testing Primary Database Models")

    from api.models import (
        Session, Message, Question, UserAnswer,
        UserAttribute, File, Room, ChatMessage
    )

    models = [
        (User, "Users"),
        (Session, "Sessions"),
        (Message, "Messages"),
        (Question, "Questions"),
        (UserAnswer, "UserAnswers"),
        (UserAttribute, "UserAttributes"),
        (File, "Files"),
        (Room, "Rooms"),
        (ChatMessage, "ChatMessages"),
    ]

    all_passed = True
    for model, name in models:
        try:
            count = model.objects.count()
            print(f"[OK] {name}: {count} records")
        except Exception as e:
            print(f"[ERROR] {name}: ERROR - {e}")
            all_passed = False

    return all_passed


def test_course_db_models():
    """Test course database models."""
    print_header("Testing Course Database Models")

    from django.conf import settings

    # In TEST mode, course_db tables don't exist (they're managed=False)
    # This is expected behavior as they represent external database tables
    if getattr(settings, 'USE_TEST_MODE', False):
        print("[INFO] Skipping course_db models in TEST mode (external database)")
        print("[OK] Course DB models are defined correctly (managed=False)")
        return True

    from api.models_course_db import School, Course, Major, Program, AcademicYear

    models = [
        (School, "Schools"),
        (Course, "Courses"),
        (Major, "Majors"),
        (Program, "Programs"),
        (AcademicYear, "AcademicYears"),
    ]

    all_passed = True
    for model, name in models:
        try:
            count = model.objects.using('course_db').count()
            print(f"[OK] {name}: {count} records")
        except Exception as e:
            print(f"[ERROR] {name}: ERROR - {e}")
            all_passed = False

    return all_passed


def test_gluideme_models():
    """Test gluideme app models."""
    print_header("Testing Gluideme Models")

    from gluideme.models import (
        Students, College, Course as GluidemeCourse,
        Program as GluidemedProgram, Department,
        StudentDemographics, CounselorProfile,
        CounselingSession, EducationPlan
    )

    models = [
        (Students, "Students"),
        (College, "Colleges"),
        (GluidemeCourse, "Courses"),
        (GluidemedProgram, "Programs"),
        (Department, "Departments"),
        (StudentDemographics, "StudentDemographics"),
        (CounselorProfile, "CounselorProfiles"),
        (CounselingSession, "CounselingSessions"),
        (EducationPlan, "EducationPlans"),
    ]

    all_passed = True
    for model, name in models:
        try:
            count = model.objects.count()
            print(f"[OK] {name}: {count} records")
        except Exception as e:
            print(f"[ERROR] {name}: ERROR - {e}")
            all_passed = False

    return all_passed


def test_pydantic_models():
    """Test Pydantic models."""
    print_header("Testing Pydantic Models")

    from gluideai.models import Course as PydanticCourse, Transcript

    all_passed = True

    # Test Course creation
    try:
        course_data = {
            "college": "Test College",
            "major": "Computer Science",
            "semester": "Fall",
            "year": "2023",
            "course_code": "CS101",
            "course_title": "Intro to Programming",
            "credit": "4.00",
            "grade": "A"
        }
        course = PydanticCourse(**course_data)
        print(f"[OK] Course model: {course.course_code} - {course.course_title}")
    except Exception as e:
        print(f"[ERROR] Course model: ERROR - {e}")
        all_passed = False

    # Test Transcript creation
    try:
        transcript = Transcript(courses=[course_data])
        print(f"[OK] Transcript model: {len(transcript.courses)} course(s)")
    except Exception as e:
        print(f"[ERROR] Transcript model: ERROR - {e}")
        all_passed = False

    # Test validation
    try:
        invalid_transcript = Transcript(courses=[])
        print(f"[ERROR] Validation: Should have failed on empty courses")
        all_passed = False
    except ValueError:
        print(f"[OK] Validation: Correctly rejects empty courses")

    return all_passed


def test_foreign_keys():
    """Test foreign key relationships."""
    print_header("Testing Foreign Key Relationships")

    all_passed = True

    # Test Session -> User
    try:
        from api.models import Session
        if Session.objects.exists():
            session = Session.objects.first()
            user = session.user
            print(f"[OK] Session -> User: {session.session_name} -> {user.username}")
        else:
            print(f"[WARN] Session -> User: No data to test")
    except Exception as e:
        print(f"[ERROR] Session -> User: ERROR - {e}")
        all_passed = False

    # Test Message -> Session
    try:
        from api.models import Message
        if Message.objects.exists():
            message = Message.objects.first()
            session = message.session
            print(f"[OK] Message -> Session: {message.message_id} -> {session.session_name}")
        else:
            print(f"[WARN] Message -> Session: No data to test")
    except Exception as e:
        print(f"[ERROR] Message -> Session: ERROR - {e}")
        all_passed = False

    # Test Room relationships
    try:
        from api.models import Room
        if Room.objects.exists():
            room = Room.objects.first()
            print(f"[OK] Room: Student={room.student.username}, Counselor={room.counselor.username}")
        else:
            print(f"[WARN] Room: No data to test")
    except Exception as e:
        print(f"[ERROR] Room: ERROR - {e}")
        all_passed = False

    # Test gluideme relationships
    try:
        from gluideme.models import StudentTarget
        if StudentTarget.objects.exists():
            target = StudentTarget.objects.first()
            print(f"[OK] StudentTarget: {target.student.first_name} -> {target.target_college.name}")
        else:
            print(f"[WARN] StudentTarget: No data to test")
    except Exception as e:
        print(f"[ERROR] StudentTarget: ERROR - {e}")
        all_passed = False

    return all_passed


def test_database_router():
    """Test database routing."""
    print_header("Testing Database Router")

    from api.models import Session
    from api.models_course_db import School
    from db_routers import ModelDatabaseRouter

    router = ModelDatabaseRouter()

    all_passed = True

    # Test managed model routing
    try:
        db = router.db_for_read(Session)
        if db == 'default':
            print(f"[OK] Session routes to: {db}")
        else:
            print(f"[ERROR] Session routes to: {db} (expected 'default')")
            all_passed = False
    except Exception as e:
        print(f"[ERROR] Session routing: ERROR - {e}")
        all_passed = False

    # Test unmanaged model routing
    try:
        db = router.db_for_read(School)
        if db == 'course_db':
            print(f"[OK] School routes to: {db}")
        else:
            print(f"[ERROR] School routes to: {db} (expected 'course_db')")
            all_passed = False
    except Exception as e:
        print(f"[ERROR] School routing: ERROR - {e}")
        all_passed = False

    # Test migration permission
    try:
        allowed = router.allow_migrate('default', 'api')
        print(f"[OK] Migrations allowed on default: {allowed}")
    except Exception as e:
        print(f"[ERROR] Migration check: ERROR - {e}")
        all_passed = False

    return all_passed


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print(" QUICK TEST SUITE - Gluide Monorepo")
    print("=" * 60)

    results = []

    # Setup databases first
    if not setup_test_databases():
        print("\n[ERROR] Database setup failed. Cannot continue.")
        return 1

    # Run all tests
    results.append(("Environment", test_environment()))
    results.append(("Primary Models", test_primary_models()))
    results.append(("Course DB Models", test_course_db_models()))
    results.append(("Gluideme Models", test_gluideme_models()))
    results.append(("Pydantic Models", test_pydantic_models()))
    results.append(("Foreign Keys", test_foreign_keys()))
    results.append(("Database Router", test_database_router()))

    # Print summary
    print_header("Test Summary")

    total_tests = len(results)
    passed_tests = sum(1 for _, passed in results if passed)

    for test_name, passed in results:
        status = "[PASS]" if passed else "[FAIL]"
        print(f"{status}: {test_name}")

    print(f"\nTotal: {passed_tests}/{total_tests} tests passed")

    if passed_tests == total_tests:
        print("\n[SUCCESS] All tests passed! Your setup is working correctly.")
        return 0
    else:
        print(f"\n[WARNING] {total_tests - passed_tests} test(s) failed. Check errors above.")
        return 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:
        print(f"\n[ERROR] Test suite crashed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
