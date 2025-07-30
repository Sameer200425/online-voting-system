@echo off
echo Starting Django Voting System in Production Mode...
echo ===================================================

cd /d "C:\Users\SAMEER KHAN\.vscode\online voting system"

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Collecting static files...
python manage.py collectstatic --noinput

echo Starting production server with Waitress...
echo Production server will be available at:
echo - Local: http://localhost:8080
echo - Network: http://192.168.1.5:8080
echo - Admin: http://192.168.1.5:8080/admin
echo.
echo Press Ctrl+C to stop the server
echo.

waitress-serve --host=0.0.0.0 --port=8080 online_voting_system.wsgi:application
