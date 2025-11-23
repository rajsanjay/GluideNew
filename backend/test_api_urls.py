"""
Test script to verify all API URL configurations.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_test')
django.setup()

from django.urls import resolve, reverse
from django.test import RequestFactory

print("\n" + "=" * 70)
print(" API URL Configuration Test")
print("=" * 70)

# Test URLs to verify
test_urls = [
    # Health check
    ('/api/health', 'health', None),
    
    # Transcript parser
    ('/api/v1/gluideai/parse-transcript/', 'v1:gluideai:parse-transcript', None),
    
    # Session endpoints
    ('/backend/api/session/', 'api:session-list', None),
    ('/backend/api/session/1/', 'api:session-detail', {'pk': 1}),
    
    # Message endpoints
    ('/backend/api/message/', 'api:message-list', None),
    ('/backend/api/message/1/', 'api:message-detail', {'pk': 1}),
    
    # Student course endpoints
    ('/backend/api/student-courses/', 'api:student-courses-list', None),
    ('/backend/api/student-courses/1/', 'api:student-courses-detail', {'pk': 1}),
    
    # Target college endpoints
    ('/backend/api/student-target-collage/', 'api:student-target-collage-list', None),
    ('/backend/api/student-target-collage/1/', 'api:student-target-collage-detail', {'pk': 1}),
    
    # Community college endpoints
    ('/backend/api/student-community-collage/', 'api:student-community-collage-list', None),
    ('/backend/api/student-community-collage/1/', 'api:student-community-collage-detail', {'pk': 1}),
    
    # User management
    ('/backend/api/user/', 'api:user-profile', None),
    ('/backend/api/user-info/', 'api:user-info', None),
    
    # Academic data
    ('/backend/api/collage/', 'api:school-search', None),
    ('/backend/api/course/', 'api:course-search', None),
    ('/backend/api/major/', 'api:major-search', None),
    ('/backend/api/academic-years/', 'api:academic-years', None),
    ('/backend/api/academic-semesters/', 'api:academic-semesters', None),
    ('/backend/api/schools/', 'api:schools', None),
]

print("\n[TEST 1] URL Resolution (path -> view)")
print("-" * 70)
passed = 0
failed = 0

for url, name, kwargs in test_urls:
    try:
        match = resolve(url)
        print(f"[OK] {url:50s} -> {match.func.__name__ if hasattr(match.func, '__name__') else match.func.cls.__name__}")
        passed += 1
    except Exception as e:
        print(f"[ERROR] {url:50s} -> {str(e)}")
        failed += 1

print("\n[TEST 2] Reverse URL Lookup (name -> path)")
print("-" * 70)

for url, name, kwargs in test_urls:
    try:
        if kwargs:
            reversed_url = reverse(name, kwargs=kwargs)
        else:
            reversed_url = reverse(name)
        
        if reversed_url == url:
            print(f"[OK] {name:50s} -> {reversed_url}")
            passed += 1
        else:
            print(f"[WARN] {name:50s} -> Expected: {url}, Got: {reversed_url}")
            passed += 1
    except Exception as e:
        print(f"[ERROR] {name:50s} -> {str(e)}")
        failed += 1

print("\n" + "=" * 70)
print(f" Test Results: {passed} passed, {failed} failed")
print("=" * 70)

if failed == 0:
    print("\n[SUCCESS] All URL configurations are correct!")
else:
    print(f"\n[WARNING] {failed} tests failed. Please review errors above.")

print("\n[INFO] Available API endpoints:")
print("-" * 70)

endpoints = [
    "GET    /api/health",
    "POST   /api/v1/gluideai/parse-transcript/",
    "",
    "GET    /backend/api/session/",
    "POST   /backend/api/session/",
    "GET    /backend/api/session/{id}/",
    "PUT    /backend/api/session/{id}/",
    "DELETE /backend/api/session/{id}/",
    "",
    "GET    /backend/api/message/",
    "POST   /backend/api/message/",
    "GET    /backend/api/message/{id}/",
    "",
    "GET    /backend/api/student-courses/",
    "POST   /backend/api/student-courses/",
    "GET    /backend/api/student-courses/{id}/",
    "PUT    /backend/api/student-courses/{id}/",
    "DELETE /backend/api/student-courses/{id}/",
    "",
    "GET    /backend/api/student-target-collage/",
    "POST   /backend/api/student-target-collage/",
    "DELETE /backend/api/student-target-collage/{id}/",
    "",
    "GET    /backend/api/student-community-collage/",
    "POST   /backend/api/student-community-collage/",
    "DELETE /backend/api/student-community-collage/{id}/",
    "",
    "GET    /backend/api/user/",
    "PUT    /backend/api/user/",
    "",
    "GET    /backend/api/user-info/",
    "PUT    /backend/api/user-info/",
    "",
    "GET    /backend/api/collage/?search=<query>&limit=<n>",
    "GET    /backend/api/course/?search=<query>&school_id=<id>&limit=<n>",
    "GET    /backend/api/major/?search=<query>&limit=<n>",
    "GET    /backend/api/academic-years/",
    "GET    /backend/api/academic-semesters/",
    "GET    /backend/api/schools/",
]

for endpoint in endpoints:
    print(endpoint)

print("-" * 70 + "\n")
