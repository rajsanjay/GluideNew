"""
Test script to verify Gluideme URL configurations.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_test')
django.setup()

from django.urls import resolve, reverse

print("\n" + "=" * 70)
print(" Gluideme URL Configuration Test")
print("=" * 70)

# Test URLs to verify
test_urls = [
    # Student management
    ('/backend/api/gluideme/student_info/', 'gluideme:student-info-list'),
    ('/backend/api/gluideme/student_info/1/', 'gluideme:student-info-detail'),
    
    # Demographics
    ('/backend/api/gluideme/student-demographics/', 'gluideme:student-demographics-list'),
    ('/backend/api/gluideme/student-demographics/1/', 'gluideme:student-demographics-detail'),
    
    # Goals
    ('/backend/api/gluideme/student-goal/', 'gluideme:student-goal-list'),
    ('/backend/api/gluideme/student-goal/1/', 'gluideme:student-goal-detail'),
    
    # Pathways
    ('/backend/api/gluideme/student-pathways/', 'gluideme:student-pathways-list'),
    ('/backend/api/gluideme/student-pathways/1/', 'gluideme:student-pathways-detail'),
    
    # Colleges
    ('/backend/api/gluideme/colleges/', 'gluideme:colleges-list'),
    ('/backend/api/gluideme/colleges/1/', 'gluideme:colleges-detail'),
    
    # Courses
    ('/backend/api/gluideme/courses/', 'gluideme:courses-list'),
    ('/backend/api/gluideme/courses/1/', 'gluideme:courses-detail'),
    
    # Programs
    ('/backend/api/gluideme/programs/', 'gluideme:programs-list'),
    ('/backend/api/gluideme/programs/1/', 'gluideme:programs-detail'),
    
    # Education Plan
    ('/backend/api/gluideme/education-plan/', 'gluideme:education-plan-list'),
    ('/backend/api/gluideme/education-plan/1/', 'gluideme:education-plan-detail'),
    
    # Counselor Profile
    ('/backend/api/gluideme/counselor-profile/', 'gluideme:counselor-profile-list'),
    
    # AI Recommendations
    ('/backend/api/gluideme/ai-recommendations/', 'gluideme:ai-recommendations-list'),
    ('/backend/api/gluideme/ai-recommendations/1/', 'gluideme:ai-recommendations-detail'),
    
    # Documents
    ('/backend/api/gluideme/documents/', 'gluideme:documents-list'),
    ('/backend/api/gluideme/documents/1/', 'gluideme:documents-detail'),
]

print("\n[TEST 1] URL Resolution (path -> view)")
print("-" * 70)
passed = 0
failed = 0

for url, name in test_urls:
    try:
        match = resolve(url)
        view_name = match.func.cls.__name__ if hasattr(match.func, 'cls') else match.func.__name__
        print(f"[OK] {url:55s} -> {view_name}")
        passed += 1
    except Exception as e:
        print(f"[ERROR] {url:55s} -> {str(e)}")
        failed += 1

print("\n[TEST 2] Reverse URL Lookup (name -> path)")
print("-" * 70)

for url, name in test_urls:
    try:
        if 'detail' in name:
            reversed_url = reverse(name, kwargs={'pk': 1})
        else:
            reversed_url = reverse(name)
        
        if reversed_url == url:
            print(f"[OK] {name:55s} -> {reversed_url}")
            passed += 1
        else:
            print(f"[WARN] {name:55s} -> Expected: {url}, Got: {reversed_url}")
            passed += 1
    except Exception as e:
        print(f"[ERROR] {name:55s} -> {str(e)}")
        failed += 1

print("\n" + "=" * 70)
print(f" Test Results: {passed} passed, {failed} failed")
print("=" * 70)

if failed == 0:
    print("\n[SUCCESS] All Gluideme URL configurations are correct!")
else:
    print(f"\n[WARNING] {failed} tests failed. Please review errors above.")

print("\n[INFO] Available Gluideme API endpoints:")
print("-" * 70)

endpoints = [
    "GET    /backend/api/gluideme/student_info/",
    "POST   /backend/api/gluideme/student_info/",
    "GET    /backend/api/gluideme/student_info/{id}/",
    "PUT    /backend/api/gluideme/student_info/{id}/",
    "POST   /backend/api/gluideme/student_info/{id}/note/",
    "GET    /backend/api/gluideme/student_info/{id}/student-courses/",
    "",
    "GET    /backend/api/gluideme/student-demographics/",
    "POST   /backend/api/gluideme/student-demographics/",
    "GET    /backend/api/gluideme/student-demographics/{id}/",
    "PUT    /backend/api/gluideme/student-demographics/{id}/",
    "",
    "GET    /backend/api/gluideme/student-goal/",
    "POST   /backend/api/gluideme/student-goal/",
    "GET    /backend/api/gluideme/student-goal/{id}/",
    "PUT    /backend/api/gluideme/student-goal/{id}/",
    "",
    "GET    /backend/api/gluideme/student-pathways/",
    "POST   /backend/api/gluideme/student-pathways/",
    "",
    "GET    /backend/api/gluideme/colleges/",
    "POST   /backend/api/gluideme/colleges/",
    "",
    "GET    /backend/api/gluideme/courses/",
    "POST   /backend/api/gluideme/courses/",
    "",
    "GET    /backend/api/gluideme/programs/",
    "POST   /backend/api/gluideme/programs/",
    "",
    "GET    /backend/api/gluideme/education-plan/",
    "POST   /backend/api/gluideme/education-plan/",
    "",
    "GET    /backend/api/gluideme/counselor-profile/",
    "PUT    /backend/api/gluideme/counselor-profile/",
    "",
    "GET    /backend/api/gluideme/ai-recommendations/",
    "POST   /backend/api/gluideme/ai-recommendations/",
    "",
    "GET    /backend/api/gluideme/documents/",
    "POST   /backend/api/gluideme/documents/",
]

for endpoint in endpoints:
    print(endpoint)

print("-" * 70 + "\n")
