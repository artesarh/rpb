# Celery Setup Guide

This document explains how to set up and run Celery workers for database backups and other background tasks.

## Overview

The project is configured with:
- **Celery Worker**: Executes background tasks
- **Celery Beat**: Scheduler for periodic tasks (cron-like functionality)
- **Database Backup Task**: Automatically backs up SQLite databases
- **Cross-platform scripts**: Work on Windows, Linux, and macOS

## Quick Start

### 1. Install Dependencies

Make sure you have all dependencies installed:
```bash
pip install -r requirements/base.txt
```

### 2. Run Database Migrations

Ensure django-celery-beat tables are created:
```bash
python manage.py migrate
```

### 3. Start Celery Services

**Cross-platform (Recommended):**
```bash
python scripts/start_celery.py
```

**Windows (Alternative):**
```cmd
scripts\start_celery.bat
```

**Linux/macOS (Alternative):**
```bash
# If you had the shell scripts (deleted), you would use:
# ./scripts/start_celery.sh
```

### 4. Stop Celery Services

**Cross-platform:**
```bash
python scripts/stop_celery.py
```

**Windows:**
```cmd
scripts\stop_celery.bat
```

## Configuration

### Scheduled Tasks

Current scheduled tasks are defined in `project/settings/base.py`:

```python
CELERY_BEAT_SCHEDULE = {
    'backup-databases-daily': {
        'task': 'project.tasks.run_db_backup',
        'schedule': 60.0 * 60.0 * 2,  # Every 2 hours (for testing)
        # For daily at 2 AM: 'schedule': crontab(hour=2, minute=0),
    },
    'test-celery-every-5-minutes': {
        'task': 'project.tasks.test_task',
        'schedule': 300.0,  # Every 5 minutes (for testing)
    },
}
```

### Database Backup Configuration

The backup task is configured to:
- Backup `db/app.sqlite` and `db/reporting.sqlite` 
- Store backups in `db/backups/` with timestamps
- Clean up backups older than 7 days
- Log to `logs/backup.log`

### Changing Schedule to Daily

To change the backup from every 2 hours to daily at 2 AM:

1. Edit `project/settings/base.py`
2. Replace:
   ```python
   'schedule': 60.0 * 60.0 * 2,  # Every 2 hours
   ```
   With:
   ```python
   'schedule': crontab(hour=2, minute=0),  # Daily at 2 AM
   ```

## File Structure

```
project/
├── scripts/
│   ├── start_celery.py      # Cross-platform start script
│   ├── stop_celery.py       # Cross-platform stop script
│   ├── start_celery.bat     # Windows batch file
│   ├── stop_celery.bat      # Windows batch file
│   └── backup.py            # Database backup script
├── project/
│   ├── celery.py            # Celery app configuration
│   ├── tasks.py             # Task definitions
│   └── settings/base.py     # Celery settings
├── celery/
│   ├── queue/               # Message queue storage
│   └── processed/           # Processed messages
├── logs/
│   ├── celery_worker.log    # Worker logs
│   ├── celery_beat.log      # Beat scheduler logs
│   └── backup.log           # Backup task logs
└── db/backups/              # Database backup files
```

## Manual Operations

### Run Backup Manually

**Direct script:**
```bash
python scripts/backup.py
```

**Through Django:**
```bash
python manage.py shell -c "from project.tasks import run_db_backup; run_db_backup()"
```

**Submit to Celery queue:**
```bash
python manage.py shell -c "from project.tasks import run_db_backup; result = run_db_backup.delay(); print(f'Task ID: {result.id}')"
```

### Monitor Tasks

**Check worker status:**
```bash
# View logs
tail -f logs/celery_worker.log
tail -f logs/celery_beat.log
```

**Django Admin:**
- Go to `/admin/`
- Look for "Periodic Tasks" section (django-celery-beat)
- View/edit scheduled tasks

## Troubleshooting

### Common Issues

**1. "No module named 'celery'"**
```bash
pip install celery django-celery-beat
```

**2. "Database not found" during backup**
- Ensure database files exist in `db/` directory
- Check paths in `scripts/backup.py`

**3. Celery won't start**
- Check Django settings with: `python manage.py check`
- Ensure migrations are applied: `python manage.py migrate`
- Check for port conflicts or existing processes

**4. Tasks not executing**
- Verify both worker AND beat are running
- Check logs for errors
- Ensure task is properly registered

### Platform-Specific Issues

**Windows:**
- Ensure Python is in PATH
- Some antivirus software may block subprocess calls
- Use Command Prompt or PowerShell as Administrator if needed

**Linux/macOS:**
- Ensure Python 3 is installed: `python3 --version`
- Check permissions on script files
- Verify shell has access to virtual environment

## Advanced Configuration

### Production Settings

For production, consider:

1. **Use Redis instead of filesystem broker:**
   ```python
   CELERY_BROKER_URL = 'redis://localhost:6379/0'
   CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
   ```

2. **Add proper logging:**
   ```python
   CELERY_WORKER_LOG_FORMAT = '[%(asctime)s: %(levelname)s/%(processName)s] %(message)s'
   CELERY_WORKER_TASK_LOG_FORMAT = '[%(asctime)s: %(levelname)s/%(processName)s][%(task_name)s(%(task_id)s)] %(message)s'
   ```

3. **Configure monitoring:**
   - Use Flower for web-based monitoring
   - Set up proper log rotation
   - Add health checks

4. **Security:**
   - Use proper authentication for broker
   - Restrict network access
   - Validate task inputs

### Adding New Tasks

1. Define task in `project/tasks.py`:
   ```python
   @shared_task(name='project.tasks.my_new_task')
   def my_new_task():
       # Task logic here
       return {'status': 'success'}
   ```

2. Add to schedule in `project/settings/base.py`:
   ```python
   CELERY_BEAT_SCHEDULE = {
       # ... existing tasks ...
       'my-new-task': {
           'task': 'project.tasks.my_new_task',
           'schedule': crontab(minute=0),  # Every hour
       },
   }
   ```

3. Restart Celery services to pick up changes.

## Support

For issues:
1. Check the logs in `logs/` directory
2. Verify configuration in settings
3. Test tasks manually before scheduling
4. Review Django and Celery documentation 