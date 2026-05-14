@echo off
cd /d %~dp0

echo Activating virtual environment...
call venv\Scripts\activate

echo Starting Django server...
start http://127.0.0.1:8000

python manage.py runserver