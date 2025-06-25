import os
import subprocess
from datetime import datetime


def backup_database():
    try:
        db_user = os.getenv("DB_USER", "username")
        db_name = os.getenv("DB_NAME", "database_name")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"backups/backup_{timestamp}.sql"
        os.makedirs("backups", exist_ok=True)

        with open(backup_file, "w") as f:
            subprocess.run(["pg_dump", f"-U {db_user}", db_name], stdout=f, check=True)
        print(f"Backup successful: {backup_file}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Backup failed: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False
