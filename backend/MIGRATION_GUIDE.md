# Migration and Model Verification Guide

This guide explains how to verify models and handle migrations for both TEST and DATABASE modes.

## Prerequisites

Install dependencies first (on your local machine):
```bash
cd backend
poetry install
# OR if using pip:
pip install -r requirements.txt
```

---

## TEST MODE Verification

TEST MODE uses in-memory SQLite databases and requires migrations to create tables.

### 1. Set Environment
```bash
export DJANGO_SETTINGS_MODULE=config.settings_test
export USE_TEST_MODE=True
```

### 2. Check Configuration
```bash
python manage.py check
```
Expected output: `System check identified no issues (0 silenced).`

### 3. Create Migrations for Managed Models

Create migrations for `api` app (18 managed models):
```bash
python manage.py makemigrations api
```

Create migrations for `gluideme` app (14 models):
```bash
python manage.py makemigrations gluideme
```

**IMPORTANT:** Do NOT create migrations for `api.models_course_db` - those models have `managed=False`

### 4. Review Migration Files
```bash
ls -la api/migrations/
ls -la gluideme/migrations/
```

Check the migration files to ensure:
- All expected models are included
- Field types are correct
- Foreign keys are properly configured

### 5. Run Migrations
```bash
python manage.py migrate
```

This will create all tables in the in-memory SQLite databases.

### 6. Verify Tables Created
```bash
python manage.py dbshell --database=default
```
In SQLite shell:
```sql
.tables
.schema sessions
.schema gluideme_students
.quit
```

### 7. Load Test Fixtures
```bash
python manage.py generate_test_fixtures
```

Expected output:
- Creates admin user (admin/admin123)
- Creates ~50 users
- Creates ~40 students
- Creates ~10 counselors
- Creates ~100 courses
- And more test data...

### 8. Verify Test Data
```bash
python manage.py shell
```

In Django shell:
```python
from django.contrib.auth.models import User
from api.models import Session, Message, Question
from gluideme.models import Students, College, Program
from api.models_course_db import School, Course as CourseDB

# Check primary database tables
print(f"Users: {User.objects.count()}")
print(f"Sessions: {Session.objects.count()}")
print(f"Messages: {Message.objects.count()}")

# Check gluideme tables
print(f"Students: {Students.objects.count()}")
print(f"Colleges: {College.objects.count()}")

# Check course_db tables (should work in test mode too)
print(f"Schools: {School.objects.using('course_db').count()}")
print(f"Courses: {CourseDB.objects.using('course_db').count()}")
```

### TEST MODE Checklist
- [ ] `python manage.py check` passes with no errors
- [ ] Migrations created for `api` app
- [ ] Migrations created for `gluideme` app
- [ ] NO migrations created for `models_course_db`
- [ ] `python manage.py migrate` completes successfully
- [ ] All tables created in SQLite
- [ ] Test fixtures loaded successfully
- [ ] Can query test data without errors

---

## DATABASE MODE Verification

DATABASE MODE connects to existing PostgreSQL databases. Tables already exist, so DO NOT run migrations.

### 1. Set Environment
```bash
export DJANGO_SETTINGS_MODULE=config.settings_database
export USE_TEST_MODE=False

# Set database credentials
export POSTGRES_DB=gluide_me
export POSTGRES_USER=your_username
export POSTGRES_PASSWORD=your_password
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432

export DB_DATABASE=course_db
export DB_USER=your_username
export DB_PASSWORD=your_password
export DB_HOST=localhost
export DB_PORT=5432
```

### 2. Check Configuration
```bash
python manage.py check
```
Expected output: `System check identified no issues (0 silenced).`

### 3. Verify Database Connections

Test connection to primary database:
```bash
python manage.py dbshell --database=default
```

In PostgreSQL shell:
```sql
-- List all tables
\dt

-- Check specific tables exist
\d sessions
\d messages
\d questions

-- Exit
\q
```

Test connection to course_db:
```bash
python manage.py dbshell --database=course_db
```

In PostgreSQL shell:
```sql
-- List all tables
\dt

-- Check specific tables exist
\d school
\d courses
\d majors
\d program

-- Exit
\q
```

### 4. Inspect Existing Schema

Generate schema from existing database:
```bash
python manage.py inspectdb --database=default > existing_default_schema.txt
python manage.py inspectdb --database=course_db > existing_course_schema.txt
```

Compare with your model definitions:
- Check field names match exactly (case-sensitive)
- Check field types match (CharField, IntegerField, etc.)
- Check max_length values match
- Check null/blank settings match
- Check foreign keys point to correct tables

### 5. Verify Database Router

The `ModelDatabaseRouter` in `db_routers.py` should prevent migrations:
```bash
python manage.py showmigrations
```

Expected: Shows migrations but router prevents running them in DATABASE mode.

### 6. Test Queries

```bash
python manage.py shell
```

In Django shell:
```python
from django.contrib.auth.models import User
from api.models import Session, Message, Question, UserAttribute
from api.models_course_db import School, Course, Major, Program
from gluideme.models import Students, College

# Test querying primary database
print(f"Users in database: {User.objects.count()}")
print(f"Sessions in database: {Session.objects.count()}")

# Test querying with specific database
sessions = Session.objects.all()[:5]
for session in sessions:
    print(f"Session: {session.session_name} - {session.user.username}")

# Test querying course_db
print(f"Schools in course_db: {School.objects.using('course_db').count()}")
print(f"Courses in course_db: {Course.objects.using('course_db').count()}")
print(f"Majors in course_db: {Major.objects.using('course_db').count()}")

# Test foreign key relationships
schools = School.objects.using('course_db').all()[:5]
for school in schools:
    print(f"School: {school.name}")

# Test gluideme models
print(f"Gluideme students: {Students.objects.count()}")
print(f"Gluideme colleges: {College.objects.count()}")
```

### 7. Verify Database Router Behavior

```python
from api.models import Session
from api.models_course_db import School

# These should route to 'default' database
print(f"Session uses database: default")
print(f"Session.objects.db: {Session.objects.db}")

# These should route to 'course_db' database
print(f"School uses database: course_db")
school = School.objects.first()
print(f"School queried from: course_db")
```

### DATABASE MODE Checklist
- [ ] Can connect to `default` database
- [ ] Can connect to `course_db` database
- [ ] All expected tables exist in `default` database
- [ ] All expected tables exist in `course_db`
- [ ] Model fields match existing table columns
- [ ] Foreign keys match existing relationships
- [ ] Can query existing data without errors
- [ ] Database router routes queries correctly
- [ ] NO new tables were created
- [ ] NO migrations were run

---

## Common Issues and Troubleshooting

### Issue: Field name mismatch
**Problem:** Model field name doesn't match database column name
**Solution:** Add `db_column='actual_name'` to the field definition

### Issue: Table name mismatch
**Problem:** Model db_table doesn't match actual table name
**Solution:** Update `db_table` in model's Meta class

### Issue: Foreign key error
**Problem:** Foreign key references non-existent table
**Solution:**
- Check `db_column` is set correctly
- Verify referenced model exists
- Ensure `on_delete` behavior is appropriate

### Issue: Migration created for unmanaged model
**Problem:** Django tries to create migration for `managed=False` model
**Solution:**
- Ensure `managed = False` in Meta class
- Check model is in correct file (models_course_db.py)
- Delete unwanted migration files

### Issue: Database routing not working
**Problem:** Queries go to wrong database
**Solution:**
- Check `DATABASE_ROUTERS` in settings.py
- Verify `managed` flag is set correctly
- Use `.using('course_db')` explicitly if needed

### Issue: PostGIS field error in test mode
**Problem:** PointField fails in SQLite
**Solution:**
- Check `get_point_field()` helper is used
- Verify `USE_TEST_MODE` setting is correct
- Fallback to CharField in test mode

---

## Model Summary

### Primary Database (default) - Managed Models
**File:** `api/models.py`
- Session (18 models total)
- Message
- Question
- UserAnswer
- UserAttribute
- StudentCourse
- StudentTargetCollege
- StudentCommunityCollege
- CounselorDefaultCollege
- CounselorAssignedCollege
- ConnectionRequest
- File
- Room
- StudentDocument
- ChatMessage
- MeetingSchedule
- UserRequestResponse
- StudentCourseSchedule

### Course Database (course_db) - Unmanaged Models
**File:** `api/models_course_db.py`
- School (16 models total)
- SchoolAddress
- Major
- Course
- SchoolMajor
- SchoolCourse
- AcademicYear
- AcademicSemester
- CourseSchedule
- Program
- ProgramDetail
- Requirement
- RequirementSection
- RequirementCourse
- Equivalency
- AdmissionRates

### Gluideme App - Managed Models
**File:** `gluideme/models.py`
- College (14 models total)
- Course
- Program
- Department
- Students
- StudentDemographics
- StudentPathways
- StudentGoal
- CounselingSession
- EducationPlan
- StudentTarget
- CounselorProfile
- AIRecommendation
- Document

### Pydantic Models
**File:** `gluideai/models.py`
- Course (Pydantic)
- Transcript (Pydantic)

---

## Next Steps

After verifying models:

1. **TEST MODE:** Continue with test data generation and API development
2. **DATABASE MODE:** Verify data integrity and begin API endpoint development

For both modes:
- Create Django REST Framework serializers
- Implement API views and endpoints
- Write unit tests
- Create frontend components
