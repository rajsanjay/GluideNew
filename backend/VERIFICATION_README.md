# Model Verification and Migration Quick Start

## Overview

This directory contains all Django models and migration tools for the Gluide monorepo:

- **Primary Database Models** (`api/models.py`): 18 managed models for main application data
- **Course Database Models** (`api/models_course_db.py`): 16 unmanaged models for existing course data
- **Gluideme Models** (`gluideme/models.py`): 14 managed models for counselor dashboard
- **Pydantic Models** (`gluideai/models.py`): 2 Pydantic v2 models for transcript parsing

## Quick Syntax Verification (Done in Sandbox)

✓ All model files have been verified for Python syntax correctness:

```bash
✓ api/models.py syntax is valid
✓ api/models_course_db.py syntax is valid
✓ gluideme/models.py syntax is valid
✓ gluideai/models.py syntax is valid
```

## Next Steps (Run on Local Machine)

### 1. Install Dependencies

```bash
cd backend
poetry install
# OR
pip install -r requirements.txt
```

### 2. Choose Your Mode

#### TEST MODE (Recommended for Development)

```bash
# Set environment
export DJANGO_SETTINGS_MODULE=config.settings_test
export USE_TEST_MODE=True

# Run verification script
python verify_models.py

# Create migrations
python manage.py makemigrations api
python manage.py makemigrations gluideme

# Run migrations
python manage.py migrate

# Load test data
python manage.py generate_test_fixtures
```

#### DATABASE MODE (For Production/Existing Database)

```bash
# Set environment
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

# Verify connection
python manage.py check

# DO NOT run migrations (tables already exist)
# Instead, verify schema matches
python manage.py inspectdb --database=default > existing_default_schema.txt
python manage.py inspectdb --database=course_db > existing_course_schema.txt
```

## Model Architecture Summary

### Database Routing

The `ModelDatabaseRouter` in `db_routers.py` automatically routes queries:
- **managed=True** models → `default` database (primary PostgreSQL)
- **managed=False** models → `course_db` database (course catalog PostgreSQL)

### Model Breakdown

**Primary Database (managed=True):**
- Session, Message, Question, UserAnswer
- UserAttribute, StudentCourse, StudentTargetCollege
- File, Room, ChatMessage, MeetingSchedule
- And more... (18 total)

**Course Database (managed=False):**
- School, Major, Course, Program
- AcademicYear, CourseSchedule, Requirement
- And more... (16 total)

**Gluideme App (managed=True):**
- College, Course, Program, Department
- Students, StudentDemographics, StudentPathways
- CounselingSession, EducationPlan
- And more... (14 total)

**Pydantic Models (for validation):**
- Course (Pydantic)
- Transcript (Pydantic)

## Files Reference

- **MIGRATION_GUIDE.md**: Comprehensive guide for both TEST and DATABASE modes
- **verify_models.py**: Automated verification script for TEST mode
- **db_routers.py**: Database routing configuration

## Support

If you encounter issues:

1. Check `MIGRATION_GUIDE.md` for detailed troubleshooting
2. Verify environment variables are set correctly
3. Ensure database connections are working
4. Check that model `managed` flags are correct

## Important Notes

⚠️ **DATABASE MODE:**
- Tables already exist in production databases
- DO NOT run migrations
- DO NOT create new migrations
- Only verify schema matches

✓ **TEST MODE:**
- Safe to run migrations
- Creates tables in SQLite
- Can regenerate test data anytime
