import os
import shutil
from datetime import datetime
import logging
from pathlib import Path

# Setup logging
BASE_DIR = Path(__file__).resolve().parent.parent
os.makedirs(BASE_DIR / "logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    filename=BASE_DIR / "logs" / "backup.log",
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def backup_database(db_name: str, db_path: str) -> bool:
    """Back up a specific SQLite database by copying the file."""
    try:
        full_db_path = BASE_DIR / db_path
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"backup_{db_name}_{timestamp}.sqlite"
        backup_path = BASE_DIR / "db" / "backups" / backup_filename

        # Ensure backup directory exists
        os.makedirs(backup_path.parent, exist_ok=True)

        if not full_db_path.exists():
            logger.error(f"Database file not found at: {full_db_path}")
            return False

        shutil.copy2(full_db_path, backup_path)
        logger.info(f"Backup successful: {backup_path}")
        print(f"✅ Backup successful: {backup_path}")
        return True
    except Exception as e:
        logger.error(f"Backup failed for {db_name}: {e}")
        print(f"❌ Backup failed for {db_name}: {e}")
        return False


def backup_all_databases() -> bool:
    """Back up all configured databases."""
    databases = {
        "app": "db/app.sqlite",
        "reporting": "db/reporting.sqlite",
    }
    
    all_successful = True
    backup_count = 0
    
    logger.info("Starting database backup process...")
    print("🔄 Starting database backup process...")
    
    for db_name, db_path in databases.items():
        if backup_database(db_name, db_path):
            backup_count += 1
        else:
            all_successful = False
    
    if all_successful:
        logger.info(f"All {backup_count} databases backed up successfully!")
        print(f"✅ All {backup_count} databases backed up successfully!")
    else:
        logger.warning(f"Some backups failed. {backup_count}/{len(databases)} successful.")
        print(f"⚠️ Some backups failed. {backup_count}/{len(databases)} successful.")
    
    return all_successful


def cleanup_old_backups(keep_days: int = 7) -> None:
    """Remove backup files older than specified days."""
    try:
        backup_dir = BASE_DIR / "db" / "backups"
        if not backup_dir.exists():
            return
        
        cutoff_time = datetime.now().timestamp() - (keep_days * 24 * 60 * 60)
        removed_count = 0
        
        for backup_file in backup_dir.glob("backup_*.sqlite"):
            if backup_file.stat().st_mtime < cutoff_time:
                backup_file.unlink()
                removed_count += 1
                logger.info(f"Removed old backup: {backup_file.name}")
        
        if removed_count > 0:
            logger.info(f"Cleaned up {removed_count} old backup files")
            print(f"🧹 Cleaned up {removed_count} old backup files")
    except Exception as e:
        logger.error(f"Cleanup failed: {e}")
        print(f"❌ Cleanup failed: {e}")


if __name__ == "__main__":
    success = backup_all_databases()
    cleanup_old_backups()
    exit(0 if success else 1)
