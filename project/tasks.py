# Celery tasks for the project

from celery import shared_task
from django.conf import settings
import subprocess
import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, name='project.tasks.run_db_backup')
def run_db_backup(self):
    """
    Run the database backup script.
    
    This task backs up all configured SQLite databases and cleans up old backups.
    """
    try:
        # Get the project root directory
        base_dir = Path(settings.BASE_DIR)
        script_path = base_dir / "scripts" / "backup.py"
        
        if not script_path.exists():
            error_msg = f"Backup script not found at: {script_path}"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)
        
        # Run the backup script
        result = subprocess.run(
            ["python", str(script_path)], 
            capture_output=True, 
            text=True,
            cwd=str(base_dir),
            check=True
        )
        
        success_msg = f"Database backup completed successfully. Output: {result.stdout}"
        logger.info(success_msg)
        
        return {
            'status': 'success',
            'message': success_msg,
            'stdout': result.stdout,
            'task_id': self.request.id
        }
        
    except subprocess.CalledProcessError as e:
        error_msg = f"Backup script failed with exit code {e.returncode}. Error: {e.stderr}"
        logger.error(error_msg)
        self.retry(countdown=300, max_retries=3)  # Retry after 5 minutes, max 3 times
        return {
            'status': 'error',
            'message': error_msg,
            'stderr': e.stderr,
            'task_id': self.request.id
        }
        
    except FileNotFoundError as e:
        error_msg = f"Backup script not found: {e}"
        logger.error(error_msg)
        raise  # Don't retry for missing script
        
    except Exception as e:
        error_msg = f"Unexpected error during backup: {e}"
        logger.error(error_msg)
        self.retry(countdown=600, max_retries=2)  # Retry after 10 minutes, max 2 times
        return {
            'status': 'error',
            'message': error_msg,
            'task_id': self.request.id
        }


@shared_task(name='project.tasks.test_task')
def test_task():
    """Simple test task to verify Celery is working."""
    logger.info("Test task executed successfully!")
    return {
        'status': 'success',
        'message': 'Test task completed',
        'result': 'Celery is working properly!'
    }
