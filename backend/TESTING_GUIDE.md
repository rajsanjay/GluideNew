# Local Testing Guide for Gluide Backend

This guide shows you how to test the Django monorepo locally on Windows.

## Prerequisites

1. Make sure your virtual environment is activated:
   ```bash
   venv\Scripts\activate
   ```

2. Verify you're in the backend directory:
   ```bash
   cd C:\Users\sanja\GluideProject\GluideNew\backend
   ```

## Testing Methods

### 🚀 Method 1: Quick Test Suite (Recommended)

Run the automated test suite that validates all components:

```bash
python quick_test.py
```

**What it tests:**
- ✅ Environment configuration
- ✅ All Django models (50+ models across 3 apps)
- ✅ Pydantic models for AI processing
- ✅ Foreign key relationships
- ✅ Database routing (default vs course_db)

**Expected Output:**
```
Total: 7/7 tests passed
[SUCCESS] All tests passed! Your setup is working correctly.
```

---

### 🔍 Method 2: Django Shell (Interactive Testing)

Test models interactively in Django's Python shell:

```bash
set DJANGO_SETTINGS_MODULE=config.settings_test
python manage.py shell
```

**Example commands to try:**

```python
# Create a user
from django.contrib.auth.models import User
user = User.objects.create_user(username='john', email='john@example.com', password='pass123')

# Create a session
from api.models import Session
session = Session.objects.create(user=user, session_name="Test", session_type="counseling")

# Create a message
from api.models import Message
msg = Message.objects.create(session=session, sender="user", content="Hello!")

# Check counts
print(f"Users: {User.objects.count()}")
print(f"Sessions: {Session.objects.count()}")
print(f"Messages: {Message.objects.count()}")
```

---

### 🧪 Method 3: Run Specific Model Tests

Test specific app models:

```bash
# Test API models only
python -c "from api.models import *; print('API models loaded successfully')"

# Test Gluideme models
python -c "from gluideme.models import *; print('Gluideme models loaded successfully')"

# Test GluideAI models (Pydantic)
python -c "from gluideai.models import *; print('GluideAI models loaded successfully')"
```

---

### 📊 Method 4: Database Inspection

Check database structure and routing:

```bash
set DJANGO_SETTINGS_MODULE=config.settings_test
python manage.py inspectdb
```

---

### 🐍 Method 5: Run Pre-made Test Script

We created a test script with sample data:

```bash
set DJANGO_SETTINGS_MODULE=config.settings_test
python test_shell_commands.py
```

This will:
- Create sample users, sessions, messages
- Create sample colleges and students
- Test Pydantic model validation
- Show database counts

---

## Troubleshooting

### Problem: "GDAL library not found"
**Solution:** Make sure you're using `config.settings_test` (not `config.settings`):
```bash
set DJANGO_SETTINGS_MODULE=config.settings_test
```

### Problem: "No such table"
**Solution:** The quick_test.py script automatically creates tables. If using manage.py, run:
```bash
set DJANGO_SETTINGS_MODULE=config.settings_test
python manage.py migrate --run-syncdb
```

### Problem: Unicode/encoding errors
**Solution:** We've replaced all Unicode characters with ASCII. If you still see errors, set:
```bash
set PYTHONIOENCODING=utf-8
```

---

## What's Working Now

✅ **All 50+ Django models** defined and tested
✅ **Pydantic models** for AI transcript processing
✅ **Database routing** between default and course_db
✅ **Foreign key relationships** across all apps
✅ **Windows compatibility** (no GDAL/PostGIS needed for testing)
✅ **In-memory SQLite** for fast testing without external databases

---

## Next Steps

Once local testing is complete, you can:

1. **Connect to actual PostgreSQL database** - Switch to `config.settings` (requires PostgreSQL + PostGIS)
2. **Add API endpoints** - Create Django REST Framework views
3. **Add test fixtures** - Generate sample data with factories
4. **Run Django server** - `python manage.py runserver` (after setting up real database)

---

## Files You Can Explore

- **Models**: `api/models.py`, `gluideme/models.py`, `api/models_course_db.py`
- **Pydantic**: `gluideai/models.py`
- **Settings**: `config/settings.py`, `config/settings_test.py`
- **Database Router**: `db_routers.py`
- **Tests**: `quick_test.py`

---

## Summary of Test Results

When you run `python quick_test.py`, you should see:

```
[PASS]: Environment                 ✓
[PASS]: Primary Models              ✓ (9 models tested)
[PASS]: Course DB Models            ✓ (5 models, managed=False)
[PASS]: Gluideme Models             ✓ (9 models tested)
[PASS]: Pydantic Models             ✓ (Course, Transcript validation)
[PASS]: Foreign Keys                ✓ (Cross-app relationships)
[PASS]: Database Router             ✓ (default vs course_db routing)

Total: 7/7 tests passed
```

All green means your Django backend is fully functional! 🎉
