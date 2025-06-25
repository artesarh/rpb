# load backup script tasks here


from celery import shared_task
import subprocess
import os


@shared_task
def run_db_backup():
    """Run the database backup script."""
    script_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "scripts",
        "backup.py",
    )
    try:
        subprocess.run(["python", script_path], check=True)
        print("Backup script executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to run backup script: {e}")
    except FileNotFoundError:
        print(f"Backup script not found at: {script_path}")
