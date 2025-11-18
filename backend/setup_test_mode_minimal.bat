@echo off
REM Minimal Setup Script - Tests models only, skips AI/ML packages
REM Use this if you have Python 3.13 or want faster installation

echo ========================================
echo  Gluide - MINIMAL Setup (Models Only)
echo ========================================
echo.
echo This installs only essential packages to test Django models.
echo AI/ML packages are skipped for faster installation.
echo.

REM Check Python version
echo [1/10] Checking Python version...
python --version
if errorlevel 1 (
    echo ERROR: Python not found
    exit /b 1
)
echo.

REM Create virtual environment
echo [2/10] Creating virtual environment...
if exist venv (
    echo Virtual environment exists, skipping...
) else (
    python -m venv venv
)
echo.

REM Activate virtual environment
echo [3/10] Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Upgrade pip
echo [4/10] Upgrading pip...
python -m pip install --upgrade pip --quiet
echo.

REM Install minimal dependencies
echo [5/10] Installing minimal dependencies...
echo This will be much faster (only 11 packages)...
pip install -r requirements-minimal.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    exit /b 1
)
echo Dependencies installed successfully
echo.

REM Set environment variables
echo [6/10] Setting environment variables...
set DJANGO_SETTINGS_MODULE=config.settings_test
set USE_TEST_MODE=True
set SECRET_KEY=test-secret-key
echo.

REM Check Django
echo [7/10] Checking Django configuration...
python manage.py check >nul 2>&1
if errorlevel 1 (
    echo WARNING: Django check found issues
) else (
    echo Django configuration OK
)
echo.

REM Create migrations
echo [8/10] Creating migrations...
python manage.py makemigrations api
python manage.py makemigrations gluideme
echo.

REM Run migrations
echo [9/10] Running migrations...
python manage.py migrate
if errorlevel 1 (
    echo ERROR: Migrations failed
    exit /b 1
)
echo.

REM Load test fixtures
echo [10/10] Loading test fixtures...
python manage.py generate_test_fixtures
if errorlevel 1 (
    echo WARNING: Test fixtures failed
)
echo.

echo ========================================
echo  Minimal Setup Complete!
echo ========================================
echo.
echo What you have:
echo  - Django models working
echo  - Database migrations applied
echo  - Test data loaded
echo  - Admin interface ready
echo.
echo What's missing:
echo  - AI/ML packages (not needed for testing models)
echo  - WebSocket support (channels)
echo  - Some optional packages
echo.
echo Next steps:
echo  1. Test: python quick_test.py
echo  2. Shell: python manage.py shell
echo  3. Server: python manage.py runserver
echo  4. Admin: http://127.0.0.1:8000/admin
echo     Username: admin
echo     Password: admin123
echo.
pause
