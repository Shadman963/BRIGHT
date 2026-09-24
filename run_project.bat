@echo off
title Bright Edu Consultancy - Django Server
echo ===================================================
echo     BRIGHT EDU CONSULTANCY - PORTAL LAUNCHER
echo ===================================================
echo.

echo 1. Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo Python is not installed or not added to PATH. Please install Python 3.10+.
    pause
    exit /b
)

echo.
echo 2. Installing project dependencies...
pip install -r requirements.txt

echo.
echo 3. Applying database migrations...
python manage.py makemigrations core universities portal
python manage.py migrate

echo.
echo 4. Populating seed data (Universities, Programs, Demo Accounts)...
python manage.py seed_data

echo.
echo ===================================================
echo   PORTAL DEMO ACCOUNTS CREATED:
echo   - Admin Superuser: username: admin / password: admin123
echo   - Counselor Staff: username: counselor / password: counselor123
echo   - Demo Student:    username: student@brightedu.com / password: student123
echo.
echo   Starting development server at http://127.0.0.1:8000
echo ===================================================
echo.
python manage.py runserver

pause
