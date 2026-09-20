@echo off
cd /d "%~dp0"
echo ========================================================
echo Starting Email Automation (AtMailWin)...
echo Server: http://127.0.0.1:8080/
echo Admin Login: admin@example.com / admin123
echo ========================================================
.\venv\Scripts\python.exe manage.py runserver 127.0.0.1:8080
pause
