@echo off
REM Windows batch script to start Celery services
REM This simply calls the Python script

echo Starting Celery services on Windows...
python scripts\start_celery.py %* 