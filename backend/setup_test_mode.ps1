# PowerShell Setup Script for TEST MODE
# Run this script to automatically set up your local testing environment

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Gluide Monorepo - TEST MODE Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check Python version
Write-Host "[1/10] Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python not found. Please install Python 3.11+" -ForegroundColor Red
    exit 1
}
Write-Host "Found: $pythonVersion" -ForegroundColor Green

# Step 2: Create virtual environment
Write-Host "[2/10] Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "Virtual environment already exists. Skipping..." -ForegroundColor Yellow
} else {
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
    Write-Host "Virtual environment created successfully" -ForegroundColor Green
}

# Step 3: Activate virtual environment
Write-Host "[3/10] Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to activate virtual environment" -ForegroundColor Red
    Write-Host "You may need to run: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Yellow
    exit 1
}
Write-Host "Virtual environment activated" -ForegroundColor Green

# Step 4: Upgrade pip
Write-Host "[4/10] Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet
Write-Host "pip upgraded" -ForegroundColor Green

# Step 5: Install dependencies
Write-Host "[5/10] Installing dependencies..." -ForegroundColor Yellow
Write-Host "This may take a few minutes..." -ForegroundColor Yellow

if (Test-Path "pyproject.toml") {
    Write-Host "Found pyproject.toml, trying poetry install..." -ForegroundColor Yellow
    pip install poetry --quiet
    poetry install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Poetry install failed, falling back to pip..." -ForegroundColor Yellow
        pip install -r requirements.txt
    }
} elseif (Test-Path "requirements.txt") {
    pip install -r requirements.txt
} else {
    Write-Host "ERROR: No pyproject.toml or requirements.txt found" -ForegroundColor Red
    exit 1
}

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
    exit 1
}
Write-Host "Dependencies installed successfully" -ForegroundColor Green

# Step 6: Set environment variables
Write-Host "[6/10] Setting environment variables..." -ForegroundColor Yellow
$env:DJANGO_SETTINGS_MODULE = "config.settings_test"
$env:USE_TEST_MODE = "True"
$env:SECRET_KEY = "test-secret-key-for-local-development-$(Get-Random)"
Write-Host "Environment variables set" -ForegroundColor Green

# Step 7: Check Django configuration
Write-Host "[7/10] Checking Django configuration..." -ForegroundColor Yellow
python manage.py check --quiet
if ($LASTEXITCODE -ne 0) {
    Write-Host "WARNING: Django check found issues" -ForegroundColor Yellow
    Write-Host "Continuing anyway..." -ForegroundColor Yellow
} else {
    Write-Host "Django configuration OK" -ForegroundColor Green
}

# Step 8: Create migrations
Write-Host "[8/10] Creating migrations..." -ForegroundColor Yellow

Write-Host "  Creating api migrations..." -ForegroundColor Cyan
python manage.py makemigrations api
if ($LASTEXITCODE -ne 0) {
    Write-Host "WARNING: Failed to create api migrations" -ForegroundColor Yellow
}

Write-Host "  Creating gluideme migrations..." -ForegroundColor Cyan
python manage.py makemigrations gluideme
if ($LASTEXITCODE -ne 0) {
    Write-Host "WARNING: Failed to create gluideme migrations" -ForegroundColor Yellow
}

Write-Host "Migrations created" -ForegroundColor Green

# Step 9: Run migrations
Write-Host "[9/10] Running migrations..." -ForegroundColor Yellow
python manage.py migrate
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to run migrations" -ForegroundColor Red
    Write-Host "Check the error messages above" -ForegroundColor Yellow
    exit 1
}
Write-Host "Migrations completed successfully" -ForegroundColor Green

# Step 10: Load test fixtures
Write-Host "[10/10] Loading test fixtures..." -ForegroundColor Yellow
python manage.py generate_test_fixtures
if ($LASTEXITCODE -ne 0) {
    Write-Host "WARNING: Failed to load test fixtures" -ForegroundColor Yellow
    Write-Host "You can try running it manually later" -ForegroundColor Yellow
} else {
    Write-Host "Test fixtures loaded successfully" -ForegroundColor Green
}

# Success message
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Setup Complete! ✓" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Test the setup:" -ForegroundColor White
Write-Host "   python verify_models.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. Open Django shell:" -ForegroundColor White
Write-Host "   python manage.py shell" -ForegroundColor Cyan
Write-Host ""
Write-Host "3. Start development server:" -ForegroundColor White
Write-Host "   python manage.py runserver" -ForegroundColor Cyan
Write-Host ""
Write-Host "4. Access admin at:" -ForegroundColor White
Write-Host "   http://127.0.0.1:8000/admin" -ForegroundColor Cyan
Write-Host "   Username: admin" -ForegroundColor Cyan
Write-Host "   Password: admin123" -ForegroundColor Cyan
Write-Host ""
Write-Host "Happy coding! 🚀" -ForegroundColor Green
