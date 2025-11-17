# Quick Start Guide - Test Locally in 5 Minutes

This is the **fastest way** to get your Gluide monorepo running locally on Windows.

---

## 🚀 Super Quick Start (Automated)

**For PowerShell users:**

```powershell
# 1. Pull the code
git pull origin claude/init-monorepo-structure-01JEFX3RJS44XDhRepjQBwjU

# 2. Navigate to backend
cd backend

# 3. Run the automated setup script
.\setup_test_mode.ps1
```

**For Command Prompt users:**

```cmd
REM 1. Pull the code
git pull origin claude/init-monorepo-structure-01JEFX3RJS44XDhRepjQBwjU

REM 2. Navigate to backend
cd backend

REM 3. Run the automated setup script
setup_test_mode.bat
```

**That's it!** The script will:
- Create virtual environment
- Install all dependencies
- Set environment variables
- Create and run migrations
- Load test data
- Tell you what to do next

---

## ✅ Verify Everything Works

After the automated setup:

```powershell
# Run the quick test suite
python quick_test.py
```

You should see:
```
🎉 All tests passed! Your setup is working correctly.
```

---

## 🎯 Start Development

### Option 1: Django Shell (Test Models)
```powershell
python manage.py shell
```

Then try:
```python
from api.models import Session
print(f"Sessions: {Session.objects.count()}")

from gluideme.models import Students
print(f"Students: {Students.objects.count()}")
```

### Option 2: Admin Interface
```powershell
python manage.py runserver
```

Open browser: `http://127.0.0.1:8000/admin`
- Username: `admin`
- Password: `admin123`

### Option 3: API Development
Start building your REST API endpoints!

---

## 📚 Need More Details?

**For detailed step-by-step instructions:**
- Read `LOCAL_TESTING_GUIDE.md` (30 steps with explanations)

**For migration and database info:**
- Read `backend/MIGRATION_GUIDE.md`

**For verification:**
- Run `python verify_models.py`

---

## 🔧 Manual Setup (If Scripts Fail)

If the automated scripts don't work:

```powershell
# 1. Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set environment
$env:DJANGO_SETTINGS_MODULE = "config.settings_test"
$env:USE_TEST_MODE = "True"

# 4. Create migrations
python manage.py makemigrations api
python manage.py makemigrations gluideme

# 5. Run migrations
python manage.py migrate

# 6. Load test data
python manage.py generate_test_fixtures

# 7. Verify
python quick_test.py
```

---

## 📦 What You Get

After setup, you'll have:

✅ **50 Models** defined and working:
   - 18 Primary database models (api/models.py)
   - 16 Course database models (api/models_course_db.py)
   - 14 Gluideme app models (gluideme/models.py)
   - 2 Pydantic validation models (gluideai/models.py)

✅ **Test Data** loaded:
   - 51 users (including admin)
   - 40 students
   - 10 counselors
   - Courses, sessions, messages, etc.

✅ **Admin Interface** ready:
   - Browse and edit all data
   - Test relationships
   - Verify everything works

✅ **Database Routing** configured:
   - Primary database (SQLite in-memory)
   - Course database (SQLite in-memory)
   - Automatic routing based on model

---

## ❓ Common Issues

**Issue:** "execution of scripts is disabled"
**Fix:** Run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

**Issue:** "No module named 'django'"
**Fix:** Make sure virtual environment is activated (you should see `(venv)` in prompt)

**Issue:** Dependencies fail to install
**Fix:** Try installing one by one:
```powershell
pip install Django==5.1.1
pip install djangorestframework==3.15.2
pip install pydantic==2.9.2
# ... etc
```

**Issue:** Migrations fail
**Fix:** Delete migrations and recreate:
```powershell
Remove-Item -Recurse -Force api\migrations
Remove-Item -Recurse -Force gluideme\migrations
# Then run makemigrations again
```

---

## 🎉 Success Criteria

You're ready to develop when:

- ✅ `python quick_test.py` shows all tests passing
- ✅ `python manage.py runserver` starts without errors
- ✅ Admin interface shows test data at http://127.0.0.1:8000/admin
- ✅ Can query models in Django shell

---

## 🚀 Next Steps

1. **Explore the models** in Django shell
2. **Browse test data** in admin interface
3. **Start building API endpoints** (DRF serializers and views)
4. **Write unit tests** for your models
5. **Connect frontend** to backend APIs

---

## 📞 Need Help?

- Check `LOCAL_TESTING_GUIDE.md` for detailed instructions
- Check `backend/MIGRATION_GUIDE.md` for database info
- Check `backend/VERIFICATION_README.md` for quick reference

---

**Happy coding! 🎊**
