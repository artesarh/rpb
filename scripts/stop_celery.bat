@echo off
REM Windows batch script to stop Celery services
REM This simply calls the Python script

echo Stopping Celery services on Windows...
python scripts\stop_celery.py %* 