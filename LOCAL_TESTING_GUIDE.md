# Local Testing Guide - Step by Step

Complete instructions to test all models on your Windows machine.

---

## Prerequisites

- Python 3.11+ installed
- Git installed
- Terminal (PowerShell or Command Prompt)

---

## PART 1: Pull Code from Git

### Step 1: Navigate to Your Project Directory

**PowerShell/Command Prompt:**
```powershell
cd C:\Path\To\Your\Projects
```

### Step 2: Clone or Pull Latest Changes

**If you haven't cloned yet:**
```powershell
git clone https://github.com/rajsanjay/GluideNew.git
cd GluideNew
```

**If you already have the repo:**
```powershell
cd GluideNew
git fetch origin
git checkout claude/init-monorepo-structure-01JEFX3RJS44XDhRepjQBwjU
git pull origin claude/init-monorepo-structure-01JEFX3RJS44XDhRepjQBwjU
```

### Step 3: Verify Files Are Present

```powershell
dir backend\api\models.py
dir backend\gluideme\models.py
dir backend\gluideai\models.py
dir backend\MIGRATION_GUIDE.md
```

You should see all these files listed.

---

## PART 2: Install Dependencies

### Step 4: Navigate to Backend Directory

```powershell
cd backend
```

### Step 5: Create Virtual Environment (Recommended)

**PowerShell:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**If you get ExecutionPolicy error:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

**Command Prompt:**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

You should see `(venv)` in your prompt.

### Step 6: Upgrade pip

```powershell
python -m pip install --upgrade pip
```

### Step 7: Install Dependencies

**Option A - Using Poetry (if pyproject.toml exists):**
```powershell
pip install poetry
poetry install
```

**Option B - If poetry install fails or you prefer pip:**

Create `requirements.txt` first:
```powershell
# Copy this content to backend/requirements.txt
```

I'll create a requirements.txt file for you in the next step.

---

## PART 3: Set Up Test Environment

### Step 8: Set Environment Variables

**PowerShell:**
```powershell
$env:DJANGO_SETTINGS_MODULE = "config.settings_test"
$env:USE_TEST_MODE = "True"
$env:SECRET_KEY = "test-secret-key-for-local-development"
```

**Command Prompt:**
```cmd
set DJANGO_SETTINGS_MODULE=config.settings_test
set USE_TEST_MODE=True
set SECRET_KEY=test-secret-key-for-local-development
```

**To make it permanent (optional):**
Create a `.env` file in backend directory:
```
DJANGO_SETTINGS_MODULE=config.settings_test
USE_TEST_MODE=True
SECRET_KEY=test-secret-key-for-local-development
```

### Step 9: Verify Django Installation

```powershell
python -c "import django; print(f'Django version: {django.get_version()}')"
```

Expected output: `Django version: 5.1.1`

### Step 10: Check Django Configuration

```powershell
python manage.py check
```

**Expected output:**
```
System check identified no issues (0 silenced).
```

**If you see errors:**
- Import errors → Dependencies not installed (go back to Step 7)
- Settings errors → Environment variables not set (go back to Step 8)
- Database errors → That's OK for now, we'll fix in next steps

---

## PART 4: Run Model Verification

### Step 11: Run the Verification Script

```powershell
python verify_models.py
```

**Expected output:**
```
======================================================================
 MODEL VERIFICATION SCRIPT - TEST MODE
======================================================================

======================================================================
 1. Checking Django Settings
======================================================================
✓ Settings module: config.settings_test
✓ Test mode: True
✓ Debug: True

Database Configuration:
  - default: django.db.backends.sqlite3
    Name: :memory:
  - course_db: django.db.backends.sqlite3
    Name: :memory:

...
```

**If errors occur:**
- `ModuleNotFoundError` → Missing dependencies, reinstall
- `ImportError` → Check file paths and imports
- `Settings error` → Check environment variables

### Step 12: Check What Migrations Are Needed

```powershell
python manage.py showmigrations
```

You should see that `api` and `gluideme` apps have no migrations yet.

---

## PART 5: Create and Run Migrations

### Step 13: Create Migrations for API App

```powershell
python manage.py makemigrations api
```

**Expected output:**
```
Migrations for 'api':
  api\migrations\0001_initial.py
    - Create model Session
    - Create model Message
    - Create model Question
    - Create model UserAnswer
    - Create model UserAttribute
    - Create model StudentCourse
    - Create model StudentTargetCollege
    - Create model StudentCommunityCollege
    - Create model CounselorDefaultCollege
    - Create model CounselorAssignedCollege
    - Create model ConnectionRequest
    - Create model File
    - Create model Room
    - Create model StudentDocument
    - Create model ChatMessage
    - Create model MeetingSchedule
    - Create model UserRequestResponse
    - Create model StudentCourseSchedule
```

**IMPORTANT:** You should see 18 models created.

### Step 14: Create Migrations for Gluideme App

```powershell
python manage.py makemigrations gluideme
```

**Expected output:**
```
Migrations for 'gluideme':
  gluideme\migrations\0001_initial.py
    - Create model College
    - Create model Course
    - Create model Department
    - Create model Program
    - Create model Students
    - Create model AIRecommendation
    - Create model CounselingSession
    - Create model StudentDemographics
    - Create model EducationPlan
    - Create model StudentGoal
    - Create model StudentPathways
    - Create model StudentTarget
    - Create model CounselorProfile
    - Create model Document
```

**IMPORTANT:** You should see 14 models created.

### Step 15: Verify No Migrations for Course DB Models

```powershell
python manage.py makemigrations
```

**Expected output:**
```
No changes detected
```

This is correct! The `models_course_db.py` models have `managed=False`, so no migrations should be created for them.

### Step 16: Review Migration Files (Optional)

**PowerShell:**
```powershell
type api\migrations\0001_initial.py | more
type gluideme\migrations\0001_initial.py | more
```

**Command Prompt:**
```cmd
more api\migrations\0001_initial.py
more gluideme\migrations\0001_initial.py
```

Verify the migrations look correct.

### Step 17: Run All Migrations

```powershell
python manage.py migrate
```

**Expected output:**
```
Operations to perform:
  Apply all migrations: admin, api, auth, contenttypes, gluideme, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying api.0001_initial... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying gluideme.0001_initial... OK
  Applying sessions.0001_initial... OK
```

**All should show "OK"!**

---

## PART 6: Load Test Data

### Step 18: Generate Test Fixtures

```powershell
python manage.py generate_test_fixtures
```

**Expected output:**
```
========================================
Starting Test Fixture Generation
========================================

✓ Superuser created: admin (password: admin123)
✓ Created 50 users
✓ Created 40 students
✓ Created 10 counselors
✓ Created 100 courses
✓ Created 200 parsed courses
...

========================================
✓ Test Fixture Generation Complete!
========================================

Summary:
  - Users: 51
  - Students: 40
  - Counselors: 10
  - Courses: 100
  - ...
```

**If errors occur:**
- Check migrations ran successfully
- Verify all models were created
- Check for unique constraint violations

---

## PART 7: Test the Models

### Step 19: Open Django Shell

```powershell
python manage.py shell
```

You should see:
```
Python 3.11.x (...)
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>>
```

### Step 20: Test Primary Database Models

**Copy and paste these commands one by one:**

```python
# Test User model
from django.contrib.auth.models import User
user_count = User.objects.count()
print(f"✓ Users in database: {user_count}")

# Test Session model
from api.models import Session
session_count = Session.objects.count()
print(f"✓ Sessions in database: {session_count}")

# Get a sample session
if session_count > 0:
    session = Session.objects.first()
    print(f"✓ Sample session: {session.session_name} - {session.user.username}")

# Test Message model
from api.models import Message
message_count = Message.objects.count()
print(f"✓ Messages in database: {message_count}")

# Test Question model
from api.models import Question
question_count = Question.objects.count()
print(f"✓ Questions in database: {question_count}")

# Test all primary models
from api.models import (
    UserAnswer, UserAttribute, StudentCourse,
    File, Room, ChatMessage, MeetingSchedule
)
print(f"✓ UserAnswers: {UserAnswer.objects.count()}")
print(f"✓ UserAttributes: {UserAttribute.objects.count()}")
print(f"✓ Files: {File.objects.count()}")
print(f"✓ Rooms: {Room.objects.count()}")
print(f"✓ ChatMessages: {ChatMessage.objects.count()}")
```

**Expected:** All counts should show numbers (from test fixtures).

### Step 21: Test Course Database Models

```python
# Test School model
from api.models_course_db import School
school_count = School.objects.using('course_db').count()
print(f"✓ Schools in course_db: {school_count}")

# Test Course model
from api.models_course_db import Course
course_count = Course.objects.using('course_db').count()
print(f"✓ Courses in course_db: {course_count}")

# Test Major model
from api.models_course_db import Major
major_count = Major.objects.using('course_db').count()
print(f"✓ Majors in course_db: {major_count}")

# Test Program model
from api.models_course_db import Program
program_count = Program.objects.using('course_db').count()
print(f"✓ Programs in course_db: {program_count}")
```

**Note:** In TEST mode, these might be 0 since course_db models are unmanaged. That's OK!

### Step 22: Test Gluideme Models

```python
# Test Students model
from gluideme.models import Students
students_count = Students.objects.count()
print(f"✓ Gluideme Students: {students_count}")

# Get a sample student
if students_count > 0:
    student = Students.objects.first()
    print(f"✓ Sample student: {student.first_name} {student.last_name}")
    print(f"  Email: {student.email}")
    print(f"  Student ID: {student.student_id}")

# Test College model
from gluideme.models import College
college_count = College.objects.count()
print(f"✓ Colleges: {college_count}")

# Test Course model (gluideme)
from gluideme.models import Course as GluidemeCourse
gluideme_course_count = GluidemeCourse.objects.count()
print(f"✓ Gluideme Courses: {gluideme_course_count}")

# Test Program model (gluideme)
from gluideme.models import Program as GluidemedProgram
gluideme_program_count = GluidemedProgram.objects.count()
print(f"✓ Gluideme Programs: {gluideme_program_count}")

# Test other gluideme models
from gluideme.models import (
    Department, StudentDemographics, StudentPathways,
    StudentGoal, CounselingSession, EducationPlan,
    CounselorProfile, AIRecommendation, Document
)
print(f"✓ Departments: {Department.objects.count()}")
print(f"✓ StudentDemographics: {StudentDemographics.objects.count()}")
print(f"✓ StudentPathways: {StudentPathways.objects.count()}")
print(f"✓ StudentGoals: {StudentGoal.objects.count()}")
print(f"✓ CounselingSessions: {CounselingSession.objects.count()}")
print(f"✓ EducationPlans: {EducationPlan.objects.count()}")
print(f"✓ CounselorProfiles: {CounselorProfile.objects.count()}")
print(f"✓ AIRecommendations: {AIRecommendation.objects.count()}")
print(f"✓ Documents: {Document.objects.count()}")
```

### Step 23: Test Pydantic Models

```python
# Test Course (Pydantic) model
from gluideai.models import Course as PydanticCourse, Transcript

# Create a sample course
course_data = {
    "college": "UC Berkeley",
    "major": "Computer Science",
    "semester": "Fall",
    "year": "2023",
    "course_code": "CS 61A",
    "course_title": "Structure and Interpretation of Computer Programs",
    "credit": "4.00",
    "grade": "A"
}

course = PydanticCourse(**course_data)
print(f"✓ Pydantic Course created: {course.course_code} - {course.course_title}")
print(f"  Grade: {course.grade}, Credits: {course.credit}")

# Create a sample transcript
transcript_data = {
    "courses": [course_data]
}

transcript = Transcript(**transcript_data)
print(f"✓ Pydantic Transcript created with {len(transcript.courses)} course(s)")

# Test validation - should fail with empty courses
try:
    invalid_transcript = Transcript(courses=[])
    print("✗ Validation failed to catch empty courses!")
except ValueError as e:
    print(f"✓ Validation working: {e}")
```

### Step 24: Test Foreign Key Relationships

```python
# Test Session -> User relationship
from api.models import Session
if Session.objects.exists():
    session = Session.objects.first()
    print(f"✓ Session has user: {session.user.username}")

# Test Message -> Session relationship
from api.models import Message
if Message.objects.exists():
    message = Message.objects.first()
    print(f"✓ Message has session: {message.session.session_name}")

# Test Room relationships
from api.models import Room
if Room.objects.exists():
    room = Room.objects.first()
    print(f"✓ Room: Student={room.student.username}, Counselor={room.counselor.username}")

# Test gluideme relationships
from gluideme.models import StudentTarget
if StudentTarget.objects.exists():
    target = StudentTarget.objects.first()
    print(f"✓ StudentTarget: {target.student.first_name} -> {target.target_college.name}")
```

### Step 25: Exit Django Shell

```python
exit()
```

---

## PART 8: Verify Database Router

### Step 26: Test Database Routing

```powershell
python manage.py shell
```

```python
from api.models import Session
from api.models_course_db import School
from db_routers import ModelDatabaseRouter

router = ModelDatabaseRouter()

# Test routing for managed models
print(f"Session routed to: {router.db_for_read(Session)}")  # Should be 'default'
print(f"Session write to: {router.db_for_write(Session)}")  # Should be 'default'

# Test routing for unmanaged models
print(f"School routed to: {router.db_for_read(School)}")  # Should be 'course_db'
print(f"School write to: {router.db_for_write(School)}")  # Should be 'course_db'

# Test migration blocking
print(f"Allow migrate on default: {router.allow_migrate('default', 'api')}")  # Should be True (TEST mode)
print(f"Allow migrate on course_db: {router.allow_migrate('course_db', 'api')}")  # Should be True (TEST mode)

exit()
```

---

## PART 9: Test Admin Interface (Optional)

### Step 27: Create Superuser (if not created by fixtures)

```powershell
python manage.py createsuperuser
```

Or use the one from fixtures:
- Username: `admin`
- Password: `admin123`

### Step 28: Run Development Server

```powershell
python manage.py runserver
```

**Expected output:**
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
November 17, 2025 - 12:00:00
Django version 5.1.1, using settings 'config.settings_test'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### Step 29: Access Admin Interface

Open browser and go to: `http://127.0.0.1:8000/admin`

Login with:
- Username: `admin`
- Password: `admin123`

**You should see:**
- API (Sessions, Messages, Questions, etc.)
- GLUIDEME (Students, Colleges, Programs, etc.)
- Authentication and Authorization

### Step 30: Browse Test Data

Click on different models to see the test data loaded.

**Stop the server:** Press `CTRL+C` in terminal

---

## PART 10: Verification Checklist

### ✓ Verification Checklist

- [ ] Code pulled from git successfully
- [ ] Virtual environment created and activated
- [ ] All dependencies installed
- [ ] Environment variables set correctly
- [ ] `python manage.py check` passes
- [ ] Migrations created for `api` app (18 models)
- [ ] Migrations created for `gluideme` app (14 models)
- [ ] NO migrations created for `models_course_db` (16 models)
- [ ] All migrations ran successfully
- [ ] Test fixtures loaded successfully
- [ ] Can query User model
- [ ] Can query api.models (Session, Message, etc.)
- [ ] Can query gluideme.models (Students, College, etc.)
- [ ] Can query course_db models (School, Course, etc.)
- [ ] Pydantic models work and validate
- [ ] Foreign key relationships work
- [ ] Database router works correctly
- [ ] Admin interface accessible
- [ ] Test data visible in admin

---

## Troubleshooting Common Issues

### Issue 1: "No module named 'django'"

**Solution:**
```powershell
# Make sure virtual environment is activated
# You should see (venv) in your prompt
.\venv\Scripts\Activate.ps1

# Reinstall Django
pip install django==5.1.1
```

### Issue 2: "ImportError: No module named 'rest_framework'"

**Solution:**
```powershell
pip install djangorestframework==3.15.2
```

### Issue 3: "ModuleNotFoundError: No module named 'pydantic'"

**Solution:**
```powershell
pip install pydantic==2.9.2
```

### Issue 4: Migration errors

**Solution:**
```powershell
# Delete all migrations and start fresh
Remove-Item -Recurse -Force api\migrations
Remove-Item -Recurse -Force gluideme\migrations

# Recreate migration folders
New-Item -ItemType Directory -Path api\migrations
New-Item -ItemType File -Path api\migrations\__init__.py
New-Item -ItemType Directory -Path gluideme\migrations
New-Item -ItemType File -Path gluideme\migrations\__init__.py

# Recreate migrations
python manage.py makemigrations api
python manage.py makemigrations gluideme
python manage.py migrate
```

### Issue 5: "execution of scripts is disabled"

**Solution (PowerShell):**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue 6: Test fixtures fail to load

**Solution:**
```powershell
# Check if migrations ran
python manage.py showmigrations

# Rerun migrations
python manage.py migrate

# Try fixtures again
python manage.py generate_test_fixtures
```

---

## Success Criteria

You have successfully tested everything when:

1. ✓ All 4 model files load without errors
2. ✓ Migrations created for 32 managed models (18 api + 14 gluideme)
3. ✓ No migrations for 16 unmanaged course_db models
4. ✓ Test data loaded successfully
5. ✓ Can query all models in Django shell
6. ✓ Foreign keys work correctly
7. ✓ Database router routes correctly
8. ✓ Admin interface shows all data

---

## Next Steps After Successful Testing

Once everything is verified:

1. Document any issues you encountered
2. Proceed to next prompt (API development, serializers, etc.)
3. Keep the virtual environment for continued development

---

## Need Help?

If you encounter issues not covered here:

1. Check `MIGRATION_GUIDE.md` for detailed troubleshooting
2. Run `python verify_models.py` for automated diagnostics
3. Check Django error messages carefully
4. Verify environment variables are set

---

**Good luck with testing! 🚀**
