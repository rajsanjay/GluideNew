"""
Django Shell Test Commands
Run: python manage.py shell < test_shell_commands.py

Or copy these commands into: python manage.py shell
"""

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_test')

import django
django.setup()

print("\n=== Testing Django Models ===\n")

# Test User creation
from django.contrib.auth.models import User
user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass123')
print(f"✓ Created user: {user.username}")

# Test Session creation
from api.models import Session
session = Session.objects.create(
    user=user,
    session_name="Test Session",
    session_type="counseling"
)
print(f"✓ Created session: {session.session_name}")

# Test Message creation
from api.models import Message
message = Message.objects.create(
    session=session,
    sender="user",
    content="Hello, this is a test message"
)
print(f"✓ Created message in session: {message.content[:30]}...")

# Test Gluideme models
from gluideme.models import Students, College
college = College.objects.create(
    name="Test University",
    college_type="4-year",
    state="CA"
)
print(f"✓ Created college: {college.name}")

student = Students.objects.create(
    user=user,
    first_name="John",
    last_name="Doe",
    student_id="STU001"
)
print(f"✓ Created student: {student.first_name} {student.last_name}")

# Test Pydantic models
from gluideai.models import Course as PydanticCourse, Transcript

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
print(f"✓ Created Pydantic course: {course.course_code}")

transcript = Transcript(courses=[course_data])
print(f"✓ Created transcript with {len(transcript.courses)} course(s)")

print("\n=== All manual tests passed! ===\n")

# Show counts
print(f"Total Users: {User.objects.count()}")
print(f"Total Sessions: {Session.objects.count()}")
print(f"Total Messages: {Message.objects.count()}")
print(f"Total Colleges: {College.objects.count()}")
print(f"Total Students: {Students.objects.count()}")
