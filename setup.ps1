# Bright Edu Consultancy PowerShell Launcher
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "     BRIGHT EDU CONSULTANCY - PORTAL LAUNCHER" -ForegroundColor Yellow
Write-Host "===================================================" -ForegroundColor Cyan

Write-Host "1. Installing requirements..." -ForegroundColor Green
pip install -r requirements.txt

Write-Host "2. Running migrations..." -ForegroundColor Green
python manage.py makemigrations core universities portal
python manage.py migrate

Write-Host "3. Seeding database with initial universities and users..." -ForegroundColor Green
python manage.py seed_data

Write-Host "4. Collecting static files..." -ForegroundColor Green
python manage.py collectstatic --noinput

Write-Host ""
Write-Host "DEMO ACCOUNTS READY:" -ForegroundColor Yellow
Write-Host "  * Superuser / Admin: admin / admin123" -ForegroundColor White
Write-Host "  * Staff Counselor:   counselor / counselor123" -ForegroundColor White
Write-Host "  * Demo Student:      student@brightedu.com / student123" -ForegroundColor White
Write-Host ""
Write-Host "Starting Django server on http://127.0.0.1:8000..." -ForegroundColor Cyan
python manage.py runserver
