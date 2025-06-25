import os
import shutil
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    filename="backups/backup.log",
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def backup_database():
    """Back up the SQLite database by copying the file."""
    try:
        db_path = os.path.join("db", "core.sqlite")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"db/backups/backup_{timestamp}.sqlite"

        os.makedirs("backups", exist_ok=True)

        if not os.path.exists(db_path):
            logger.error(f"Database file not found at: {db_path}")
            return False

        shutil.copy2(db_path, backup_file)
        logger.info(f"Backup successful: {backup_file}")
        return True
    except Exception as e:
        logger.error(f"Backup failed: {e}")
        return False


if __name__ == "__main__":
    backup_database()
