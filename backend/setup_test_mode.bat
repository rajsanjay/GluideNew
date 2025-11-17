@echo off
REM Batch Setup Script for TEST MODE (Command Prompt)
REM Run this script to automatically set up your local testing environment

echo ========================================
echo  Gluide Monorepo - TEST MODE Setup
echo ========================================
echo.

REM Step 1: Check Python version
echo [1/10] Checking Python version...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.11+
    exit /b 1
)
python --version
echo.

REM Step 2: Create virtual environment
echo [2/10] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists. Skipping...
) else (
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        exit /b 1
    )
    echo Virtual environment created successfully
)
echo.

REM Step 3: Activate virtual environment
echo [3/10] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    exit /b 1
)
echo Virtual environment activated
echo.

REM Step 4: Upgrade pip
echo [4/10] Upgrading pip...
python -m pip install --upgrade pip --quiet
echo pip upgraded
echo.

REM Step 5: Install dependencies
echo [5/10] Installing dependencies...
echo This may take a few minutes...
if exist requirements.txt (
    pip install -r requirements.txt
) else (
    echo ERROR: requirements.txt not found
    exit /b 1
)
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    exit /b 1
)
echo Dependencies installed successfully
echo.

REM Step 6: Set environment variables
echo [6/10] Setting environment variables...
set DJANGO_SETTINGS_MODULE=config.settings_test
set USE_TEST_MODE=True
set SECRET_KEY=test-secret-key-for-local-development
echo Environment variables set
echo.

REM Step 7: Check Django configuration
echo [7/10] Checking Django configuration...
python manage.py check >nul 2>&1
if errorlevel 1 (
    echo WARNING: Django check found issues
    echo Continuing anyway...
) else (
    echo Django configuration OK
)
echo.

REM Step 8: Create migrations
echo [8/10] Creating migrations...
echo   Creating api migrations...
python manage.py makemigrations api
echo   Creating gluideme migrations...
python manage.py makemigrations gluideme
echo Migrations created
echo.

REM Step 9: Run migrations
echo [9/10] Running migrations...
python manage.py migrate
if errorlevel 1 (
    echo ERROR: Failed to run migrations
    echo Check the error messages above
    exit /b 1
)
echo Migrations completed successfully
echo.

REM Step 10: Load test fixtures
echo [10/10] Loading test fixtures...
python manage.py generate_test_fixtures
if errorlevel 1 (
    echo WARNING: Failed to load test fixtures
    echo You can try running it manually later
) else (
    echo Test fixtures loaded successfully
)
echo.

REM Success message
echo ========================================
echo  Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Test the setup:
echo    python verify_models.py
echo.
echo 2. Open Django shell:
echo    python manage.py shell
echo.
echo 3. Start development server:
echo    python manage.py runserver
echo.
echo 4. Access admin at:
echo    http://127.0.0.1:8000/admin
echo    Username: admin
echo    Password: admin123
echo.
echo Happy coding!
pause
